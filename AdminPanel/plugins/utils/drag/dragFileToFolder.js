/**
 * 实现拖拽文件到文件夹
 */
import { getPosition, setPosition } from './dom.js'
import { ipcSend } from "@/api/electronApi/ipc.js"

let g_time = null;
let g_div = null;
let g_foldersElement = [];//所有文件夹的dom元素
let g_selectId = 'g_selectId';
let g_moveCssTest = '';//css样式
let g_callback = null;
/**
 * 开启拖拽
 * @param {Array} folderIds 所有文件夹的id数组，需要通过获取文件夹单个的id开启拖移入移出事件
 * @param {String} imgPath 预览图片的路径地址
 * @param {Int} number 拖动的数量
 * @param {Function} endCallback 回调函数，返回null || id
 */
export function startDragFileToFolder(e, folderIds, imgPath, number, endCallback, readyCallback) {

    const downTime = 200;
    // document.addEventListener('mouseup', mouseUp, true);//绑定鼠标松开事件

    g_time = setTimeout(() => {
        // console.log('dragFileToFolder=>绑定事件');
        // readyCallback && readyCallback();//准备
        // createPreviewElement(imgPath, number);

        // mouseMove(e)
        ipcSend('ondragstart', imgPath)

        // addFolderEvent(folderIds);
        // g_callback = endCallback;
        // document.addEventListener('mousemove', mouseMove, true);//绑定鼠标松开事件
    }, downTime);
}
// export function startDragFileToFolder(e, folderIds, imgPath, number, endCallback, readyCallback) {

//     const downTime = 200;
//     document.addEventListener('mouseup', mouseUp, true);//绑定鼠标松开事件

//     g_time = setTimeout(() => {
//         console.log('dragFileToFolder=>绑定事件');
//         readyCallback && readyCallback();//准备
//         createPreviewElement(imgPath, number);

//         // mouseMove(e)
//         ipcSend('ondragstart',imgPath)

//         addFolderEvent(folderIds);
//         g_callback = endCallback;
//         document.addEventListener('mousemove', mouseMove, true);//绑定鼠标松开事件
//     }, downTime);
// }

/**
 * 鼠标拖动的处理事件
 * @param {*} params 
 */
function mouseMove(e) {
    console.log('dragFileToFolder=>拖动');
    let res = getPosition(e);
    setPosition(g_div, res.x + 4, res.y + 4);
}

/**
 * 松开鼠标的处理事件
 */
function mouseUp() {
    if (g_time)
        clearTimeout(g_time);

    clearPreviewElement();//清除节点
    removeFolderEvent();//清除所有文件夹元素的事件
    document.removeEventListener('mouseup', mouseUp, true);
    document.removeEventListener('mousemove', mouseMove, true);
    console.log('dragFileToFolder=>取消绑定');

    if (g_selectId) {
        console.log('最终id:', g_selectId);
        if (g_selectId.style)
            g_selectId.style.cssText = g_moveCssTest;

        const idText = '#leftFolderItem';
        if (g_selectId.id)
            g_callback && g_callback(g_selectId.id.replace(idText, ''))
        g_selectId = null;
    }
    g_callback = null;
}


/**
 * 创建预览元素
 */
function createPreviewElement(imgPath, number) {
    if (g_div != null)
        return;
    g_div = document.createElement('div');
    let img = document.createElement('img');
    img.src = imgPath;

    g_div.appendChild(img);
    Object.assign(img.style, {
        maxWidth: '100px',
        maxHeight: '100px',
        border: '2px solid #2a98ff',
        borderRadius: '4px'
    })

    Object.assign(g_div.style, {
        position: 'fixed',
        zIndex: 10011,
        left: '-1000px',
    })

    g_div.appendChild(createTextElement(number));
    document.body.appendChild(g_div);
}

/**
 * 创建文件数量的样式
 * @param {*} number 
 * @returns 
 */
function createTextElement(number) {
    let dom = document.createElement('div');
    dom.innerHTML = number;
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
    Object.assign(dom.style, style);
    return dom;
}

/**
 * 清除创建的元素
 */
function clearPreviewElement() {
    if (g_div) {
        g_div.remove();
        g_div = null;
    }
}


function mouseover(e) {
    console.log('移入', e);
    let el = e.target;
    if (el.id == '')
        el = el.parentNode;
    g_selectId = el;
    g_moveCssTest = el.style.cssText
    el.style.border = '1px solid #2a98ff';
    el.style.background = 'rgba(42,152,255,0.2)';
}

function mouseout(e) {
    let el = e.target;
    if (el.id == '') {
        el = el.parentNode;
    }
    console.log('移出', el);
    g_selectId = null;
    // let el = e.target;
    el.style.cssText = g_moveCssTest;
}

/**
 * 给文件夹id添加关联事件
 * @param {Array} ids 所有文件夹id
 */
function addFolderEvent(ids) {
    const idText = '#leftFolderItem';

    g_foldersElement = ids.map(id => document.getElementById(idText + id)).filter(el => el)
    g_foldersElement.forEach(el => {
        el.addEventListener('mouseover', mouseover);//鼠标移入
        el.addEventListener('mouseout', mouseout);//鼠标移出事件
    })
}

function removeFolderEvent(params) {
    if (g_foldersElement.length > 0) {
        g_foldersElement.forEach(el => {
            el.removeEventListener('mouseover', mouseover);//鼠标移入
            el.removeEventListener('mouseout', mouseout);//鼠标移出事件
        })
        g_foldersElement.splice(0, g_foldersElement.length);
    }
}