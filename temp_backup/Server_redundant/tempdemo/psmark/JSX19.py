dxf19_jscode = """

// 文件夹路径

function 裁片抓取新的() {
    app.activeDocument.suspendHistory("裁片抓取", "置入对象()");
}

function 置入对象() {
    var folderPath = "D:/MarkTemp/Pdfmarktemp";


    var folder = new Folder(folderPath);

    // 获取文件夹中的文件
    var files = folder.getFiles();

    // 新建一个数组来存储文件名称
    var fileNamesArray = [];

    for (var i = 0; i < files.length; i++) {
        if (files[i] instanceof File) {
            var doc = app.activeDocument;
            var fileName = files[i].name;
            var newDocumentName = fileName.replace(/\.pdf$/, '');
            var modifiedString = newDocumentName.replace(/-\d+_\d+/, '');
            var newmodifiedString = modifiedString.split("-");

            // 检查是否存在相同的文件名
            var duplicate = false;
            for (var j = 0; j < fileNamesArray.length; j++) {
                if (fileNamesArray[j] === modifiedString) {
                    duplicate = true;
                    break;
                }
            }

            if (duplicate) {
                $.writeln("文件名重复，跳过: " + fileName);
                continue;
            }

            // 将新的文档名添加到文件名数组中
            fileNamesArray.push(modifiedString);
            $.writeln("文档名称: " + fileName);

            var 文件路径 = folderPath + "/" + fileName;

            // 调用你的函数
            var match = newDocumentName.match(/_(\d+)/);
            var 角度信息 = match ? match[1] : "";

            if (角度信息 === "180" || 角度信息 === "-180") {
                置入对象180度(文件路径);
            } else {
                // 如果角度信息不是 "180" 或 "-180"，执行默认逻辑
                置入对象0度(文件路径);
            }

            var extractedPart = newmodifiedString[0];
            var 大货裁片组名 = extractedPart + "-大货裁片";

          //  var 当前花样图层 = app.activeDocument.layers.getByName(newDocumentName);
          //  app.activeDocument.activeLayer = 当前花样图层;

            var 大货裁片组;
            try {
                大货裁片组 = app.activeDocument.layerSets.getByName(大货裁片组名);
            } catch (e) {
                大货裁片组 = app.activeDocument.layerSets.add();
                大货裁片组.name = 大货裁片组名;
            }

            // 将当前图层移动到大货裁片图层组内
            app.activeDocument.activeLayer.move(大货裁片组, ElementPlacement.INSIDE);
            栅格化图层智能对象();
         //   modifiedString = fileName.replace(/-\d+_\d+/, '');
            app.activeDocument.activeLayer.name = modifiedString;
        }
    }
}

function 栅格化图层智能对象() {
    var d = new ActionDescriptor();
    var r = new ActionReference();
    r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
    d.putReference(stringIDToTypeID("null"), r);
    executeAction(stringIDToTypeID("rasterizeLayer"), d, DialogModes.NO);
}




function 栅格化图层智能对象()	//栅格化图层
    {
 
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("rasterizeLayer"), d, DialogModes.NO);
       
    }

function 置入对象0度(文件路径)	
    {
    
        var d = new ActionDescriptor();
        var d1 = new ActionDescriptor();
        d1.putEnumerated(stringIDToTypeID("selection"), stringIDToTypeID("pdfSelection"), stringIDToTypeID("page"));
        d1.putInteger(stringIDToTypeID("pageNumber"), 1);
        d1.putEnumerated(stringIDToTypeID("crop"), stringIDToTypeID("cropTo"), stringIDToTypeID("boundingBox"));
        d1.putBoolean(stringIDToTypeID("suppressWarnings"), false);
        d1.putBoolean(stringIDToTypeID("antiAlias"), true);
        d1.putBoolean(stringIDToTypeID("clippingPath"), true);
        d.putObject(stringIDToTypeID("as"), stringIDToTypeID("PDFGenericFormat"), d1);
        d.putInteger(stringIDToTypeID("ID"), 4);
        d.putPath(stringIDToTypeID("null"), new File(文件路径));
        d.putEnumerated(stringIDToTypeID("freeTransformCenterState"), stringIDToTypeID("quadCenterState"), stringIDToTypeID("QCSAverage"));
        var d2 = new ActionDescriptor();
        d2.putUnitDouble(stringIDToTypeID("horizontal"), stringIDToTypeID("distanceUnit"), 0);
        d2.putUnitDouble(stringIDToTypeID("vertical"), stringIDToTypeID("distanceUnit"), 0);
        d.putObject(stringIDToTypeID("offset"), stringIDToTypeID("offset"), d2);
        //d.putUnitDouble(stringIDToTypeID("width"), stringIDToTypeID("percentUnit"), -100);
       // d.putUnitDouble(stringIDToTypeID("height"), stringIDToTypeID("percentUnit"), -100);
        d.putBoolean(stringIDToTypeID("antiAlias"), false);
        executeAction(stringIDToTypeID("placeEvent"), d, DialogModes.NO);
    
    }



function 置入对象180度(文件路径)	
    {
    
        var d = new ActionDescriptor();
        var d1 = new ActionDescriptor();
        d1.putEnumerated(stringIDToTypeID("selection"), stringIDToTypeID("pdfSelection"), stringIDToTypeID("page"));
        d1.putInteger(stringIDToTypeID("pageNumber"), 1);
        d1.putEnumerated(stringIDToTypeID("crop"), stringIDToTypeID("cropTo"), stringIDToTypeID("boundingBox"));
        d1.putBoolean(stringIDToTypeID("suppressWarnings"), false);
        d1.putBoolean(stringIDToTypeID("antiAlias"), true);
        d1.putBoolean(stringIDToTypeID("clippingPath"), true);
        d.putObject(stringIDToTypeID("as"), stringIDToTypeID("PDFGenericFormat"), d1);
        d.putInteger(stringIDToTypeID("ID"), 4);
        d.putPath(stringIDToTypeID("null"), new File(文件路径));
        d.putEnumerated(stringIDToTypeID("freeTransformCenterState"), stringIDToTypeID("quadCenterState"), stringIDToTypeID("QCSAverage"));
        var d2 = new ActionDescriptor();
        d2.putUnitDouble(stringIDToTypeID("horizontal"), stringIDToTypeID("distanceUnit"), 0);
        d2.putUnitDouble(stringIDToTypeID("vertical"), stringIDToTypeID("distanceUnit"), 0);
        d.putObject(stringIDToTypeID("offset"), stringIDToTypeID("offset"), d2);
        d.putUnitDouble(stringIDToTypeID("width"), stringIDToTypeID("percentUnit"), -100);
        d.putUnitDouble(stringIDToTypeID("height"), stringIDToTypeID("percentUnit"), -100);
        d.putBoolean(stringIDToTypeID("antiAlias"), false);
        executeAction(stringIDToTypeID("placeEvent"), d, DialogModes.NO);
    
    }








"""
