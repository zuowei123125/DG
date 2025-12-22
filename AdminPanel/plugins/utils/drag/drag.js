//引入操作dom元素的
import { insertBefore, insertAfter, getTop, getLeft, getPosition, setPosition } from './dom.js'

class Drap {
    static status = {
        downIndex: null,
        upIndex: null,
        node: null,
        transparentNode: null,
        time: null,
        callback: null,
        styleWidth: null,
        styleHeight: null,
    }

    /**
     * 鼠标松开
     * @returns 
     */
    static onMouseUp() {
        Drap.status.time && clearTimeout(Drap.status.time);

        let obj = Object.assign({}, Drap.status); //浅复制一份
        Drap.resetStatus(); //重置

        if (obj.downIndex != null && obj.upIndex != null && obj.downIndex != obj.upIndex) {
            Drap.status.callback && Drap.status.callback(obj);
            Drap.status.callback = null;
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
        let res = getPosition(e);
        setPosition(Drap.status.node, res.x, res.y);
    }

    /**
     * 重置状态
     * @returns 
     */
    static resetStatus() {
        if (Drap.status.downIndex == null)
            return;
        Drap.status.downIndex = null;
        Drap.status.upIndex = null;
        Drap.status.upIndex = null;
        Drap.status.time = null;

        if (Drap.status.node != null) {
            Drap.status.node.style.width = Drap.status.styleWidth;
            Drap.status.node.style.height = Drap.status.styleHeight;
            Drap.status.node.style.position = "static";
        }


        Drap.status.transparentNode && Drap.status.transparentNode.remove();
        Drap.status.transparentNode = null;
    }

    constructor(el, option = {}) {
        let config = {
            direction: 'x', //默认配置 左右方向
            callback: null,
        }
        Object.assign(config, option);
        this.option = config;

        this.el = el;
        this.downTime = 300;
        this.init();
    }

    /**
     * 初始化
     */
    init() {
        // console.log(this.option);
        this.el.onmousedown = (e) => {
            this.onMouseDown(e)
            return false
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
        document.addEventListener('mouseup', Drap.onMouseUp);

        Drap.status.time = setTimeout(() => {
            Drap.status.downIndex = this.option.index;
            Drap.status.node = this.el;
            Drap.status.transparentNode = this.el.cloneNode(true); //克隆节点
            Drap.status.callback = this.option.callback;

            console.log(this.el.offsetWidth);

            Drap.status.styleWidth = Drap.status.node.style.width;
            Drap.status.styleHeight = Drap.status.node.style.height;
            Drap.status.node.style.width = this.el.offsetWidth + "px";
            Drap.status.node.style.height = this.el.offsetHeight + "px"
                //处理节点显示
            Drap.status.node.style.position = "fixed";



            Drap.status.transparentNode.style.cssText += ";opacity: 0;"
            insertBefore(Drap.status.transparentNode, this.el);

            document.addEventListener('mousemove', Drap.onMouseMove);
        }, this.downTime);
    }


    /**
     * 鼠标移动事件
     * @param {*} e 
     * @returns 
     */
    onMouseMove(e) {
        if (Drap.status.downIndex == null)
            return false;

        let left = getLeft(this.el) + this.el.offsetWidth / 2;
        let top = getTop(this.el) + this.el.offsetHeight / 2;

        let obj = getPosition(e);
        let min = Drap.status.downIndex < this.option.index;

        //左右方向进行拖拽
        Drap.status.upIndex = this.option.index;
        if (this.option.direction == 'x') {
            if (obj.x < left) {
                // console.log('左边');
                insertBefore(Drap.status.transparentNode, this.el)
            } else {
                // console.log('右边');
                insertAfter(Drap.status.transparentNode, this.el)
                Drap.status.upIndex += min ? 0 : 1; //按下大于松开的下标+1
            }
            return;
        }

        //上下方向拖拽
        if (obj.y < top) {
            // console.log('上边');
            insertBefore(Drap.status.transparentNode, this.el);
        } else {
            // console.log('下边');
            insertAfter(Drap.status.transparentNode, this.el);
            Drap.status.upIndex += min ? 0 : 1; //按下大于松开的下标+1
        }
    }
}

//导出vue指令用到的对象
export const drag = {
    mounted(el, binding) {
        new Drap(el, binding.value || {})
    }
}