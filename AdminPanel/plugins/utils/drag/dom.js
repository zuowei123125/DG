/**
 * 在指定节点前插入节点
 * @param {*} newElement 
 * @param {*} targentElement 
 */
export function insertBefore(newElement, targentElement) {
    targentElement.parentNode.insertBefore(newElement, targentElement)
}

/**
 * 在指定节点后插入节点
 * @param {*} newNode 
 * @param {*} referenceNode 
 */
export function insertAfter(newNode, referenceNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}


/**
 * 获取元素上坐标
 * @param {*} e 
 * @returns 
 */
export function getTop(e) {
    var result = e.offsetTop;
    if (e.offsetParent != null)
        result += getTop(e.offsetParent);
    return result;
}

/**
 * 获取元素左坐标
 * @param {*} e 
 * @returns 
 */
export function getLeft(e) {
    var result = e.offsetLeft;
    if (e.offsetParent != null)
        result += getLeft(e.offsetParent);
    return result;
}

/**
 * 获取dom元素位置
 * @param {*} e 
 * @returns 
 */
export function getPosition(e) {
    var evt = e || event;
    return { x: evt.clientX, y: evt.clientY }
}

/**
 * 设置dom元素的位置 left top
 * @param {*} dom 
 * @param {*} x 
 * @param {*} y 
 * @param {*} unit 后缀单位，默认px
 */
export function setPosition(dom, left, top, unit = 'px') {
    dom.style.left = left + unit;
    dom.style.top = top + unit;
}