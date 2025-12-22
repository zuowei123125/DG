/**

 * 获取当前光标位置 返回表示位置的索引（number）以0开头

 * @param ctrl

 * @returns {number}

 */

export function getCursorPosition(element) {

    var CaretPos = 0;

    if (document.selection) {//支持IE

        element.focus();

        var Sel = document.selection.createRange();

        Sel.moveStart('character', -element.value.length);

        CaretPos = Sel.text.length;

    }

    else if (element.selectionStart || element.selectionStart == '0')//支持firefox

        CaretPos = element.selectionStart;

    return (CaretPos);

}

export function insertAtCursor(myField, myValue) {

    //IE 浏览器 
    if (document.selection) {
        myField.focus();
        sel = document.selection.createRange();
        sel.text = myValue;
        sel.select();
    }

    //FireFox、Chrome等 
    else if (myField.selectionStart || myField.selectionStart == '0') {
        var startPos = myField.selectionStart;
        var endPos = myField.selectionEnd;

        // 保存滚动条 
        var restoreTop = myField.scrollTop;
        myField.value = myField.value.substring(0, startPos) + myValue + myField.value.substring(endPos, myField.value.length);

        if (restoreTop > 0) {
            myField.scrollTop = restoreTop;
        }

        myField.focus();
        myField.selectionStart = startPos + myValue.length;
        myField.selectionEnd = startPos + myValue.length;
    } else {
        myField.value += myValue;
        myField.focus();
    }
}