//引入操作dom元素的
import { insertBefore, getTop, getPosition, setPosition } from './dom.js'

export class DragFolder {
    static status = {
        downIndex: null,
        upIndex: null,
        node: null,
        transparentNode: null,
        moveNode: null,
        moveCssTest: null,
        time: null,
        callback: null,
        cssText: null,
        position: null,
        multipleChoice: null,//多选样式节点
    }

    /**
     * 鼠标松开
     * @returns 
     */
    static onMouseUp() {
        DragFolder.status.time && clearTimeout(DragFolder.status.time);

        if (DragFolder.status.moveNode != null) {
            DragFolder.status.moveNode.style.cssText = DragFolder.status.moveCssTest;
            DragFolder.status.moveNode = null;
        }

        // let obj = Object.assign({}, DragFolder.status); //浅复制一份
        let downIndex = DragFolder.status.downIndex;
        let upIndex = DragFolder.status.upIndex;
        let position = DragFolder.status.position;
        DragFolder.resetStatus(); //重置

        console.log('拖拽松开');
        if (downIndex != null && upIndex != null && downIndex != upIndex) {
            DragFolder.status.callback && DragFolder.status.callback({ downIndex, upIndex, position });
            DragFolder.status.callback = null;
        }

        document.removeEventListener('mouseup', DragFolder.onMouseUp);
        document.removeEventListener('mousemove', DragFolder.onMouseMove);
        return false;
    }

    /**
     * 鼠标移动
     * @param {*} e 
     */
    static onMouseMove(e) {
        console.log('移动');
        let res = getPosition(e);
        setPosition(DragFolder.status.node, res.x + 4, res.y + 4);
    }

    /**
     * 重置状态
     * @returns 
     */
    static resetStatus() {
        if (DragFolder.status.downIndex == null)
            return;
        DragFolder.status.downIndex = null;
        DragFolder.status.upIndex = null;
        DragFolder.status.upIndex = null;
        DragFolder.status.time = null;

        if (DragFolder.status.node != null) {
            DragFolder.status.node.style.cssText = DragFolder.status.cssText;
            DragFolder.status.node.style.position = "static";

        }

        if (DragFolder.status.transparentNode != null) {
            DragFolder.status.transparentNode.remove();
            DragFolder.status.transparentNode = null;
        }
        if (DragFolder.status.multipleChoice != null) {
            DragFolder.status.multipleChoice.remove();
            DragFolder.status.multipleChoice = null;
        }



    }

    constructor(el, option = {}) {
        let config = {
            direction: 'x', //默认配置 左右方向
            callback: null,
        }
        Object.assign(config, option);
        this.option = config;

        this.el = typeof el == 'string' ? document.getElementById(el) : el;

        // console.log(this.el);
        this.downTime = 300;
        this.init();
    }

    /**
     * 初始化
     */
    init() {
        // console.log(this.option);

        // debugger
        this.el.onmousedown = (e) => {
            // debugger
            this.onMouseDown(e)
            // return false
        }

        this.el.onmousemove = (e) => {
            this.onMouseMove(e);
        }
        // console.log('folder初始化', this.el,this.el.onmousedown);
    }

    /**
     * 鼠标按下事件
     * @param {*} e 
     */
    onMouseDown(e) {
        document.addEventListener('mouseup', DragFolder.onMouseUp, true);

        DragFolder.status.time = setTimeout(() => {
            DragFolder.status.downIndex = this.option.index;
            DragFolder.status.callback = this.option.callback;
            
            if (this.option.downCallback) {
                // debugger
                let temp = this.option.downCallback();
              
                let select = temp.indexOf(this.option.index) > -1 ? temp : [this.option.index];
                console.log(this.option.index,temp,select)
                //创建数量的提醒
                if (select.length > 1) {
                    DragFolder.status.multipleChoice = document.createElement('div');
                    DragFolder.status.multipleChoice.innerHTML = select.length;
                    let style = {
                        width: '24px',
                        height: '24px',
                        lineHeight: '24px',
                        borderRadius: '100%',
                        background: "#D84A4A",
                        color: '#fff',
                        fontSize: '12px',
                        position: "absolute",
                        top: '-12px',
                        right: '-12px',
                        boxShadow: '0px 0px 10px rgba(0, 0, 0, 0.3)',
                        textAlign: 'center'
                    }
                    Object.assign(DragFolder.status.multipleChoice.style, style)
                }
                console.error('按下回调', select);
            }

            DragFolder.status.node = this.el;
            DragFolder.status.transparentNode = this.el.cloneNode(true); //克隆节点
            // DragFolder.status.node = this.el.cloneNode(true); //克隆节点

            console.log(this.el.offsetWidth);

            DragFolder.status.cssText = DragFolder.status.node.style.cssText;
            DragFolder.status.node.style.width = this.el.offsetWidth + 4 + "px";
            DragFolder.status.node.style.height = this.el.offsetHeight + 4 + "px"

            //处理节点显示
            DragFolder.status.node.style.position = "fixed";
            DragFolder.status.node.style.background = "#2a98ff";
            DragFolder.status.node.style.zIndex = "101";

            DragFolder.status.transparentNode.style.cssText += ";border: 1px solid #797979"

            DragFolder.status.multipleChoice && DragFolder.status.node.appendChild(DragFolder.status.multipleChoice)
            insertBefore(DragFolder.status.transparentNode, this.el);

            document.addEventListener('mousemove', DragFolder.onMouseMove);
        }, this.downTime);
    }


    /**
     * 鼠标移动事件
     * @param {*} e 
     * @returns 
     */
    onMouseMove(e) {
        if (DragFolder.status.downIndex == null)
            return false;
        if (DragFolder.status.moveNode != null) {
            DragFolder.status.moveNode.style.cssText = DragFolder.status.moveCssTest;
            DragFolder.status.moveNode = null;
        }

        DragFolder.status.moveNode = this.el;
        DragFolder.status.moveCssTest = this.el.style.cssText;

        // let elTop = getTop(this.el)
        let elTop = this.el.getBoundingClientRect().top
        let top = elTop + this.el.offsetHeight / 10 * 3;
        let bottom = elTop + this.el.offsetHeight / 10 * 7;

        let obj = getPosition(e);

        //左右方向进行拖拽
        DragFolder.status.upIndex = this.option.index;

        //上下方向拖拽
        if (obj.y < top) {
            this.el.style.borderTop = '1px solid #2a98ff';
            DragFolder.status.position = 'top'
        } else if (obj.y > bottom) {
            this.el.style.borderBottom = '1px solid #2a98ff'
            DragFolder.status.position = 'bottom'

        } else {
            DragFolder.status.position = 'center'
            this.el.style.border = '1px solid #2a98ff';
            this.el.style.background = 'rgba(42,152,255,0.2)';
        }
    }
}

export default DragFolder;