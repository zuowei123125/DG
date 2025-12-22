

//引入操作dom元素的
import { insertBefore, getTop, getPosition, setPosition } from './dom.js'

interface IOption {
    index?:string,
    callback?:Function,
    downCallback?: Function,
}

export class DragTag {
    public el: HTMLElement
    public option: IOption
    public downTime: number

    static status = {
        node: null,
        transparentNode: null,
        moveNode: null,
        moveCssTest: null,
        time: null,
        callback: null,
        cssText: null,
        position: null,
        multipleChoice: null,//多选样式节点
        option: null
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
     * 鼠标松开
     * @returns 
     */
    static onMouseUp() {
        DragTag.status.time && clearTimeout(DragTag.status.time);

        if (DragTag.status.moveNode != null) {
            DragTag.status.moveNode.style.cssText = DragTag.status.moveCssTest;
            DragTag.status.moveNode = null;
        }


        DragTag.resetStatus(); //重置

        console.log('拖拽松开');
        DragTag.status.callback && DragTag.status.callback();

        document.removeEventListener('mouseup', DragTag.onMouseUp);
        document.removeEventListener('mousemove', DragTag.onMouseMove);
        return false;
    }

    /**
     * 鼠标移动
     * @param {*} e 
     */
    static onMouseMove(e) {
        console.log('移动');
        let res = getPosition(e);
        setPosition(DragTag.status.node, res.x + 4, res.y + 4);
    }

    /**
     * 重置状态
     * @returns 
     */
    static resetStatus() {

        DragTag.status.time = null;

        if (DragTag.status.node != null) {
            DragTag.status.node.style.cssText = DragTag.status.cssText;
            DragTag.status.node.style.position = "static";

        }

        if (DragTag.status.transparentNode != null) {
            DragTag.status.transparentNode.remove();
            DragTag.status.transparentNode = null;
        }
        if (DragTag.status.multipleChoice != null) {
            DragTag.status.multipleChoice.remove();
            DragTag.status.multipleChoice = null;
        }
    }



    /**
     * 初始化
     */
    init() {
        // console.log('初始化',this.el)
        this.el.onmousedown = (e) => {
            this.onMouseDown(e)
        }
        this.el.onmousemove = (e) => {
            this.onMouseMove(e);
        }

    }

    /**
     * 鼠标按下事件
     * @param {*} e 
     */
    onMouseDown(e) {
        e.preventDefault();
        e.stopPropagation();
        if (e.button != 0) return
        console.log('按下', e.button)
        document.addEventListener('mouseup', DragTag.onMouseUp);
        DragTag.status.time = setTimeout(() => {
            DragTag.status.callback = this.option.callback;
            if (this.option.downCallback) {
                // debugger
                let temp = this.option.downCallback(this.option.index);
                let select = temp.indexOf(this.option.index) > -1 ? temp : [this.option.index];
                console.log(this.option.index, select)
                //创建数量的提醒
                if (select.length > 1) {
                    DragTag.status.multipleChoice = document.createElement('div');
                    DragTag.status.multipleChoice.innerHTML = select.length;
                    let style = {
                        width: '14px',
                        height: '14px',
                        lineHeight: '14px',
                        borderRadius: '100%',
                        background: "#6450FF",
                        color: '#fff',
                        fontSize: '10px',
                        position: "absolute",
                        top: '-10px',
                        right: '0px',
                        boxShadow: '0px 0px 10px rgba(0, 0, 0, 0.3)',
                        textAlign: 'center'
                    }
                    Object.assign(DragTag.status.multipleChoice.style, style)
                }
                // console.error('按下回调',select);
            }

            DragTag.status.node = this.el;
            DragTag.status.transparentNode = this.el.cloneNode(true); //克隆节点
            // DragTag.status.node = this.el.cloneNode(true); //克隆节点



            DragTag.status.cssText = DragTag.status.node.style.cssText;
            DragTag.status.node.style.width = this.el.offsetWidth + 4 + "px";
            DragTag.status.node.style.height = this.el.offsetHeight + 4 + "px"

            //处理节点显示
            DragTag.status.node.style.position = "fixed";
            DragTag.status.node.style.background = "#8070FF";
            DragTag.status.node.style.zIndex = "101";

            let res = getPosition(e);
            setPosition(DragTag.status.node, res.x + 4, res.y + 4);

            DragTag.status.multipleChoice && DragTag.status.node.appendChild(DragTag.status.multipleChoice)
            insertBefore(DragTag.status.transparentNode, this.el);
            document.addEventListener('mousemove', DragTag.onMouseMove);
        }, this.downTime);
    }

    /**
     * 鼠标移动事件
     * @param {*} e 
     * @returns 
     */
    onMouseMove(e) {

    }
}
export default DragTag;