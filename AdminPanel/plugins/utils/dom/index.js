/**
 * 获取元素坐标
 * @param {*} params 
 */
export function getRefPosition(e) {
    return { left: getLeft(e), top: getTop(e) };
}

export function getTop(e) {
    var offset = e.offsetTop;
    if (e.offsetParent != null) offset += getTop(e.offsetParent);
    return offset;
}

export function getLeft(e) {
    var offset = e.offsetLeft;
    if (e.offsetParent != null) offset += getLeft(e.offsetParent);
    return offset;
}

export function getHeight(id) {
    let dom = document.getElementById(id);
    return dom.offsetHeight;
}

export function getWidth(id) {
    let dom = document.getElementById(id);
    return dom.offsetWidth;
}
export function getClientHeight(id) {
    let dom = document.getElementById(id);
    return dom.clientHeight;
}

export function getClientWidth(id) {
    let dom = document.getElementById(id);
    return dom.clientWidth;
}

export function getWindowsHeight(param) {
    return document.body.clientHeight
}

export function getWindowsWidth(param) {
    return document.body.clientWidth
}

/**
 * 教程菜单位置，保证菜单出现的位置不超出不可见区域
 * @param {*} e 
 * @param {*} menuId 
 * @returns 
 */
export function correctMenuPosition(e, menuId) {
    let winHeight = getWindowsHeight();
    let height = getHeight(menuId);

    let winWidth = getWindowsWidth();
    let windth = getWidth(menuId);

    let top = (height + e.clientY) > winHeight ? winHeight - height : e.clientY;

    let left = (windth + e.clientX) > winWidth ? winWidth - windth : e.clientX;
    return { top, left: left + 5 }
}

/**
 * 设置id的元素选择
 * @param {*} id 
 */
export function setInputSelect(id, time = 0) {
    let count = 0;
    const callbcak = () => {
        let dom = document.getElementById(id);
        if (!dom) {
            count += 1;
            if (count > 50) return
            return setTimeout(callbcak, 50);
        }
        dom.select();
        dom.focus()
    }
    time == 0 ? callbcak() : setTimeout(callbcak, 50);
}

export function setFoucs(id, time = 0) {
    setTimeout(() => {
        let dom = document.getElementById(id);
        dom.focus()
    }, time);
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
 * 根据id获取元素的位置
 * @param {*} elementId 
 * @returns 
 */
export function getPostionById(elementId) {
    var el = document.getElementById(elementId);
    return getRefPosition(el);
}