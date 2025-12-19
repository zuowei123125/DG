dxf21_jscode = """

function 创建裁片排版文档(画布宽,画布高,分辨率,文档名称)
{
    app.preferences.rulerUnits = Units.MM; //修改指定单位为毫米
    app.documents.add(画布宽, 画布高,分辨率, 文档名称, NewDocumentMode.CMYK);
}




function 置入链接的智能对象(dir, DXFname) {
    图片路径 = dir + "/" + DXFname + ".tif"
    var d = new ActionDescriptor();
    d.putInteger(stringIDToTypeID("ID"), 16);
    d.putPath(stringIDToTypeID("null"), new File(图片路径));
    d.putBoolean(stringIDToTypeID("linked"), true);
    d.putEnumerated(stringIDToTypeID("freeTransformCenterState"), stringIDToTypeID("quadCenterState"), stringIDToTypeID("QCSAverage"));
    var d1 = new ActionDescriptor();
    executeAction(stringIDToTypeID("placeEvent"), d, DialogModes.NO);
}

function 裁片排版_lay(中心x_mm, 中心y_mm) {
    ps中心x_mm = 中心x_mm;
    ps中心y_mm = 中心y_mm;

    alb = app.activeDocument.activeLayer.bounds;
    当前x = (alb[0] + alb[2]) / 2; //mm数
    当前y = (alb[1] + alb[3]) / 2; //mm数

    app.activeDocument.activeLayer.translate(ps中心x_mm - Number(当前x), ps中心y_mm - Number(当前y)); //全局单位设置为mm即可
}

function 裁片角度(角度) {
    app.activeDocument.activeLayer.rotate(角度);
    //app.refresh()
}

"""
