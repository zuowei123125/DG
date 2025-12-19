dxf20_jscode = """





function 混排通码延申导出() {
var 主文档 = app.activeDocument;
var 主文档路径 = 主文档.path;
var 新文件夹 = (主文档路径 + "/小片裁片"); // 在桌面上创建一个名为"导出目录"的文件夹
var 导出目录 = Folder(新文件夹);
if (!导出目录.exists) {
    导出目录.create();
}

var doc = app.activeDocument;

// 获取所有图层
var layers = doc.layers;

// 存储符合条件的图层组
var matchingLayerSets = [];

// 遍历每个图层
for (var i = 0; i < layers.length; i++) {
    var layer = layers[i];

    // 如果是图层组，检查名称是否包含 "大货裁片"
    if (layer.typename == "LayerSet" && layer.name.indexOf("大货裁片") !== -1) {
        matchingLayerSets.push(layer);

        // 输出图层组名称
        $.writeln("图层组名称：" + layer.name);
          图层组名称=layer.name
        // 输出图层组内子图层的名称
        for (var j = 0; j < layer.layers.length; j++) {
            var subLayer = layer.layers[j];
            $.writeln("  子图层名称：" + subLayer.name);
            子图层名称=subLayer.name
            子图层名称分割=子图层名称.split("-")
            素材图名称=子图层名称分割[0]
          空白裁片模板 = app.activeDocument.layerSets.getByName(图层组名称).layers.getByName(子图层名称);
          app.activeDocument.activeLayer = 空白裁片模板;
          载入选区()
          素材名称 = app.activeDocument.layers.getByName(素材图名称);
           app.activeDocument.activeLayer = 素材名称;
           添加图层蒙版()
           新建文档()
           当前花样图层 = app.activeDocument.activeLayer 
            app.activeDocument.crop( 当前花样图层.bounds, 0);
             var 文件路径 = 导出目录 + "/" + 子图层名称 + ".tif";
               tiffOptions = new TiffSaveOptions();
               app.activeDocument.saveAs(new File(文件路径), tiffOptions);
               app.activeDocument.close(SaveOptions.DONOTSAVECHANGES);
              app.activeDocument=doc
                        
            历史记录回退3()
            
            
        }
    }
}

// 输出符合条件的图层组数量
//$.writeln("符合条件的图层组数量：" + matchingLayerSets.length);

    }

function 载入选区()	//载入选区
    {
  
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("channel"), stringIDToTypeID("selection"));
        d.putReference(stringIDToTypeID("null"), r);
        var r1 = new ActionReference();
        r1.putEnumerated(stringIDToTypeID("channel"), stringIDToTypeID("channel"), stringIDToTypeID("transparencyEnum"));
        d.putReference(stringIDToTypeID("to"), r1);
        executeAction(stringIDToTypeID("set"), d, DialogModes.NO);
    
    }


function 添加图层蒙版()	//添加图层蒙版
    {
    
        var d = new ActionDescriptor();
        d.putClass(stringIDToTypeID("new"), stringIDToTypeID("channel"));
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("channel"), stringIDToTypeID("channel"), stringIDToTypeID("mask"));
        d.putReference(stringIDToTypeID("at"), r);
        d.putEnumerated(stringIDToTypeID("using"), stringIDToTypeID("userMaskEnabled"), stringIDToTypeID("revealSelection"));
        executeAction(stringIDToTypeID("make"), d, DialogModes.NO);
       
    }



function 新建文档()	//复制图层
    {
    
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putClass(stringIDToTypeID("document"));
        d.putReference(stringIDToTypeID("null"), r);
        var r1 = new ActionReference();
        r1.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("using"), r1);
        d.putInteger(stringIDToTypeID("version"), 5);
        executeAction(stringIDToTypeID("make"), d, DialogModes.NO);
        }


function 历史记录回退3()	//
    {
 
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putOffset(stringIDToTypeID("historyState"), -2);
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
        }













"""