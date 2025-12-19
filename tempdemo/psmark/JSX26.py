dxf26_jscode = """
// 弹出文件夹选择框

function 模特换图(){
建立快照()
var folder = Folder.selectDialog("请选择一个文件夹");
var 模特文档 = app.activeDocument;

if (folder) {
    // 在选择的文件夹中创建一个新的子文件夹
    var targetFolder = new Folder(folder.fullName + "/模特图生成");
    if (!targetFolder.exists) {
        targetFolder.create();
    }

    var files = folder.getFiles();

    // 获取“贴图位置”图层组中的所有图层名称
    var layerSet = 模特文档.layerSets.getByName("贴图位置");
    var layerNames = [];
    for (var j = 0; j < layerSet.artLayers.length; j++) {
        layerNames.push(layerSet.artLayers[j].name);
    }

    // 遍历并尝试打开每个文件
    for (var i = 0; i < files.length; i++) {
        var file = files[i];
        if (file instanceof File) {
            try {
                app.open(file);        
                app.activeDocument.flatten()
                var 当前文档 = app.activeDocument;
                var 当前文档名称 = 当前文档.name;
                图像大小();
                预设图案(当前文档名称);
                app.activeDocument.close(SaveOptions.DONOTSAVECHANGES);
                app.activeDocument = 模特文档;
                var 水平增量 = 200;
                var 垂直增量 = 300;
                var 水平基数 = 200;
                var 垂直基数 = 300;
                // 遍历“贴图位置”图层组中的每个图层
                for (var k = 0; k < layerNames.length; k++) {
                    var layname = layerNames[k];
                    var 贴图位置 = app.activeDocument.layerSets.getByName("贴图位置").layers.getByName(layname);
                    app.activeDocument.activeLayer = 贴图位置;
                    载入选区();
                    填充图案(当前文档名称);
                    栅格化图层()
                    取消链接蒙版()
                    var 水平 = 水平基数 + 水平增量 * k;
                    var 垂直 = 垂直基数 + 垂直增量 * k;
                    位移(水平, 垂直);
                }

                    var saveFile = new File(targetFolder.fullName + "/" + file.name.replace(/\.[^\.]+$/, "") + ".tif");
                    var tiffSaveOptions = new TiffSaveOptions();
                    tiffSaveOptions.imageCompression = TIFFEncoding.NONE; // 或者根据需要设置其他压缩选项
                    tiffSaveOptions.alphaChannels = true;
                    tiffSaveOptions.layers = true;
                    app.activeDocument.saveAs(saveFile, tiffSaveOptions, true, Extension.LOWERCASE);

                // 关闭当前文档
                历史记录回退到快照1()
            } catch (e) {
                 alert("无法打开文件: " );
            }
    
        }
    }
    alert("换图完成")
} else {
    alert("没有选择文件夹");
}

// 其他函数保持不变


function generateRandomNumber(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}



function 图像大小()		//图像大小
    {
 
        var d = new ActionDescriptor();
        d.putUnitDouble(stringIDToTypeID("resolution"), stringIDToTypeID("densityUnit"), 150);
        d.putBoolean(stringIDToTypeID("scaleStyles"), true);
        d.putBoolean(stringIDToTypeID("constrainProportions"), true);
        d.putEnumerated(charIDToTypeID("Intr"), stringIDToTypeID("interpolationType"), stringIDToTypeID("nearestNeighbor"));
        executeAction(stringIDToTypeID("imageSize"), d, DialogModes.NO);
        }





function 取消链接蒙版()	//取消链接蒙版
    {
    
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        d1.putBoolean(stringIDToTypeID("userMaskLinked"), false);
        d.putObject(stringIDToTypeID("to"), stringIDToTypeID("layer"), d1);
        executeAction(stringIDToTypeID("set"), d, DialogModes.NO);
     
    }



function 栅格化图层()	//栅格化图层
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("rasterizeLayer"), d, DialogModes.NO);

    }





function 预设图案(当前文档名称)	//
    {
    
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putClass(stringIDToTypeID("pattern"));
        d.putReference(stringIDToTypeID("null"), r);
        var r1 = new ActionReference();
        r1.putProperty(stringIDToTypeID("property"), stringIDToTypeID("selection"));
        r1.putEnumerated(stringIDToTypeID("document"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("using"), r1);
        d.putString(stringIDToTypeID("name"), 当前文档名称);
        executeAction(stringIDToTypeID("make"), d, DialogModes.NO);
    
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


function 填充图案(当前文档名称)	//
    {
    
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putClass(stringIDToTypeID("contentLayer"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        var d2 = new ActionDescriptor();
        var d3 = new ActionDescriptor();
        d3.putString(stringIDToTypeID("name"), 当前文档名称);
      
        d2.putObject(stringIDToTypeID("pattern"), stringIDToTypeID("pattern"), d3);
        d1.putObject(stringIDToTypeID("type"), stringIDToTypeID("patternLayer"), d2);
        d.putObject(stringIDToTypeID("using"), stringIDToTypeID("contentLayer"), d1);
        executeAction(stringIDToTypeID("make"), d, DialogModes.NO);
       
    }


function 位移(水平,垂直)	//位移
    {
   
        var d = new ActionDescriptor();
        d.putInteger(stringIDToTypeID("horizontal"), 水平);
        d.putInteger(stringIDToTypeID("vertical"), 垂直);
        d.putEnumerated(stringIDToTypeID("fill"), stringIDToTypeID("fillMode"), stringIDToTypeID("wrap"));
        executeAction(stringIDToTypeID("offset"), d, DialogModes.NO);
      
    }


function 历史记录回退到快照1()	//
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putName(stringIDToTypeID("snapshotClass"), "快照 1");
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
    
    }

function 建立快照()	//打开
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putClass(stringIDToTypeID("snapshotClass"));
        d.putReference(stringIDToTypeID("null"), r);
        var r1 = new ActionReference();
        r1.putProperty(stringIDToTypeID("historyState"), stringIDToTypeID("currentHistoryState"));
        d.putReference(stringIDToTypeID("from"), r1);
        executeAction(stringIDToTypeID("make"), d, DialogModes.NO);
      
    }
}
"""