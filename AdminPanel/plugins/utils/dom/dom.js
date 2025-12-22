/**
 * 简单版对dom的封装
 * 初始化一个myDom对象
 * 通过类、id、以及dom元素创建
 * 可以获取所有子节点、父节点、第一个子节点、最后一个子节点、上一个兄弟节点、下一个兄弟节点
 * 判断元素类型
 * 获取文本
 * 获取元素的坐标、宽高
 * 设置元素的坐标、宽高
 * 设置样式
 * 复制元素
 * 返回真正的dom元素
 * 获取所有父亲节点
 * 获取指定类型的父节点
 * 获取所有子节点
 * 获取自定类型的子节点
 */

/**
 * 获取dom元素
 * @param {*} 参数 ,可以接受dom元素或者id(id必须带#号)
 */
export function $(el) {
    //id选择器
    if (typeof el == 'object') {
        return new Dom(el);
    } else if (typeof el == 'string') {
        let dom = document.getElementById(el);
        return dom ? new Dom(dom) : null;
    } else {
        console.warn(`Dom：传入的字符串不符合要求${el}`);
    }

    return null;
}

export class Dom {
    constructor(el) {
        this._el = el;
    }
    /**
     * 获取元素内的所有文本内容
     */
    getTexts() {
        let result = [];
        const callback = (el) => {
            let arr = [...el.childNodes];
            arr.filter(item => item.nodeType == 3).forEach(item => result.push(item.nodeValue))
            arr.filter(item => item.nodeType == 1).forEach(item => callback(item));//遍历所有元素的子节点
        }
        callback(this._el);
        return result;
    }

    /**
     * 获取标签内第一个文本，没有返回空
     * @returns 
     */
    getText() {
        let texts = this.getTexts();
        return texts.length > 0 ? texts[0] : ''
    }

    /**
     * 获取元素的高
     */
    getHeight() {
        return this._el.offsetHeight;
    }

    /**
     * 获取元素的宽
     */
    getWidth() {
        return this._el.offsetWidth;
    }

    get left() {
        return this.getLeft();
    }

    get top() {
        return this.getTop();
    }

    get width() {
        return this._el.offsetWidth;
    }

    get height() {
        return this._el.offsetHeight;
    }

    get bottom() {
        return this.top + this.height;
    }

    get right() {
        return this.left + this.width;
    }

    /**
     * 获取元素的left坐标
     */
    getLeft() {
        const callback = (e) => {
            return e.offsetParent != null ? e.offsetLeft + callback(e.offsetParent) : e.offsetLeft
        }
        return callback(this._el)
    }

    /**
     * 获取元素的顶点坐标
     */
    getTop() {
        const callback = (e) => {
            return e.offsetParent != null ? e.offsetTop + callback(e.offsetParent) : e.offsetTop
        }
        return callback(this._el)
    }

    /**
     * 获取坐标，包含4个点以及宽高
     * @returns 
     */
    getPosition() {
        return {
            left: this.getLeft(),
            top: this.getTop(),
        }
    }

    /**
     * 设置样式，直接合并css的样式对象
     * @param {*} option 
     */
    setStyle(option) {
        Object.assign(this._el.style, option);
    }

    addUnit(val, unit = 'px') {
        // return unit ? val + unit : val;
        return val + unit;
    }

    /**
     * 设置坐标
     * @param {*} val 左坐标位置
     * @param {*} unit 默认单位为px，如果不用则，需要传递null
     */
    setLeft(val, unit = 'px') {
        this.setStyle({ left: this.addUnit(val, unit) })
    }

    /**
     * 设置顶坐标
     * @param {*} val 
     * @param {*} unit 
     */
    setTop(val, unit = 'px') {
        this.setStyle({ top: this.addUnit(val, unit) })
    }

    /**
     * 设置宽度
     * @param {*} val 
     * @param {*} unit 
     */
    setWidth(val, unit = 'px') {
        this.setStyle({ width: this.addUnit(val, unit) })
    }

    setHeight(val, unit = 'px') {
        this.setStyle({ height: this.addUnit(val, unit) })
    }

    setSize(width, height, unit = 'px') {
        this.setStyle({
            width: this.addUnit(width, unit),
            height: this.addUnit(height, unit),
        })
    }

    /**
     * 设置元素位置
     * @param {*} left 
     * @param {*} top 
     * @param {*} unit 单位，默认为px
     */
    setPosition(left, top, unit = 'px') {
        this.setStyle({
            left: this.addUnit(left, unit),
            top: this.addUnit(top, unit)
        })
    }

    /**
     * 克隆元素
     * @param {*} deep 
     * @returns 
     */
    clone(deep = true) {
        let el = this._el.cloneNode(deep);//克隆元素
        return new Dom(el);
    }

    /**
     * 移除元素
     */
    remove() {
        this._el.remove();
    }

    /**
     * 返回原本的dom元素
     * @returns 
     */
    getElement() {
        return this._el;
    }

    /**
     * 获取封装一层的子元素
     */
    childNodes() {
        return [...this._el.childNodes].map(item => new Dom(item))
    }

    parentNode() {
        return new Dom(this._el.parentNode)
    }

    firstChild() {
        return new Dom(this._el.firstChild);
    }

    lastChild() {
        return new Dom(this._el.lastChild)
    }

    nextSibling() {
        return new Dom(this._el.nextSibling)
    }

    previousSibling() {
        return new Dom(this._el.previousSibling)
    }

    /**
     * 是否是标签元素
     * @returns 
     */
    isElement() {
        return this._el.nodeType == 1;
    }

    /**
     * 获取第一个指定标签的元素
     * @param {*} name 标签名字
     */
    firstParentByName(name) {
        name = name.toUpperCase();//转大写
        const callback = (el) => {
            let parent = el.parentNode;
            if (parent.nodeName == 'BODY')
                return null;

            if (parent.nodeName == name)
                return new Dom(parent)
            return callback(parent);
        }

        return callback(this._el);
    }

    firstChildByName(name) {
        name = name.toUpperCase();//转大写
        const callback = (el) => {
            let childs = el.childNodes;
            if (childs.length == 0)
                return null;

            for (let i = 0; i < childs.length; i++) {
                const item = childs[i];
                if (item.nodeName == name)
                    return new Dom(item)
            }

            for (let i = 0; i < childs.length; i++) {
                const item = childs[i];
                if (item.childNodes.length > 0)
                    return callback(item)
            }
            return null;
        }

        return callback(this._el);
    }

    getNodeName() {
        return this._el.nodeName;
    }

    /**
     * 全选
     */
    select() {

        // console.log(this._el);
        this._el.focus();
        this._el.select();
    }
}