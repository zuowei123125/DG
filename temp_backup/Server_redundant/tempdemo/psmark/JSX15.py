dxf15_jscode = """



function 图层自动编组2() {

    app.activeDocument.suspendHistory("图层自动编组", "图层自动编组()");
}


 function 图层自动编组(){
 var currentDocument = app.activeDocument;
  var matchCount = 0; // 匹配到的数值计数
  var existingPatternSet = false;
  var layerNames = []; // 保存匹配到的图层名称的数组

  // 遍历图层
  for (var j = 0; j < currentDocument.layers.length; j++) {
    var layer = currentDocument.layers[j];
    var layerName = layer.name;

    // 检查图层名称是否以P开头并且后面跟着数字
    if (/^P\d+$/.test(layerName)) {
      matchCount++;
      layerNames.push(layer); // 将匹配到的图层添加到数组中
    }
  }

  // 输出匹配到的数值个数
  $.writeln("匹配到的数值个数：" + matchCount);

  // 遍历匹配到的图层名称
  for (var i = 0; i < layerNames.length; i++) {
    var layerName = layerNames[i].name;
   // $.writeln("匹配到的图层名称：" + layerName);
     var 当前花样图层 = app.activeDocument.layers.getByName(layerName);
     app.activeDocument.activeLayer = 当前花样图层;
      图层编组main()
       app.activeDocument.activeLayer.name=layerName
  }
}




function 图层编组main()	//图层编组
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putClass(stringIDToTypeID("layerSection"));
        d.putReference(stringIDToTypeID("null"), r);
        var r1 = new ActionReference();
        r1.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("from"), r1);
        d.putInteger(stringIDToTypeID("layerSectionStart"), 43);
        d.putInteger(stringIDToTypeID("layerSectionEnd"), 44);
        d.putString(stringIDToTypeID("name"), "main");
        executeAction(stringIDToTypeID("make"), d, DialogModes.NO);

    }


function 快速超级链接2() {

    app.activeDocument.suspendHistory("快速超链接", "快速超级链接()");
}


function 快速超级链接() {
   var 导出目录 = Folder.selectDialog("选择超链接素材目录");
    if (!导出目录) {
        alert("未选择导出目录。操作已取消。");
        return;
    }


   画布大小()
   app.preferences.rulerUnits = Units.PIXELS
  var currentDocument = app.activeDocument;
  var matchCount = 0; // 匹配到的数值计数
  var existingPatternSet = false;
  var layerNames = []; // 保存匹配到的图层名称的数组

  // 遍历图层
  for (var j = 0; j < currentDocument.layers.length; j++) {
    var layer = currentDocument.layers[j];
    var layerName = layer.name;

    // 检查图层名称是否以P开头并且后面跟着数字
    if (/^P\d+$/.test(layerName)) {
      matchCount++;
      layerNames.push(layer); // 将匹配到的图层添加到数组中
    }
  }

  // 输出匹配到的数值个数
 // $.writeln("匹配到的数值个数：" + matchCount);

  // 遍历匹配到的图层名称
  for (var i = 0; i < layerNames.length; i++) {
    var layerName = layerNames[i].name;
   $.writeln("匹配到的图层名称：" + layerName);
   var 当前花样图层 = app.activeDocument.layers.getByName(layerName);
        app.activeDocument.activeLayer = 当前花样图层;
        切换mask()
        载入选区()
      var 边距 = 获取当前选区四边距();
      var 毫米 = 130;
       var 每英寸像素数 = app.activeDocument.resolution; // 获取当前文档的分辨率（每英寸像素数）
       var 扩展像素 = 毫米转像素(毫米, 每英寸像素数);     

        var   裁切上边距= 边距.top-扩展像素
        var   裁切左边距= 边距.left-扩展像素
        var   裁切下边距=  边距.bottom+扩展像素
        var   裁切右边距=  边距.right+扩展像素

           var selRegion = [
            [裁切左边距,裁切上边距],
            [裁切右边距,裁切上边距],
            [裁切右边距,裁切下边距],
            [裁切左边距,裁切下边距]
        ];

app.activeDocument.selection.select(selRegion, SelectionType.REPLACE);
 新建图层()      
 app.activeDocument.selection.select(selRegion, SelectionType.REPLACE);

var c = new SolidColor();
c.rgb.hexValue = "FFFFFF";
app.activeDocument.selection.fill(c); 
后移一层()
 app.activeDocument.activeLayer = 当前花样图层;
  切换mask()
  载入选区()
  删除图层蒙版()
  创建剪贴蒙版()
  向下合并()
  新建文档()
 当前花样图层 = app.activeDocument.activeLayer 
 app.activeDocument.crop( 当前花样图层.bounds, 0);
 var 文件路径 = 导出目录 + "/" + layerName + ".tif";
   tiffOptions = new TiffSaveOptions();
   app.activeDocument.saveAs(new File(文件路径), tiffOptions);
   app.activeDocument.close(SaveOptions.DONOTSAVECHANGES);
  app.activeDocument=currentDocument
  转换为智能对象()
  重新链接到文件(文件路径)
  添加图层蒙版()
  //当前图层=app.activeDocument.activeLayer 
  //当前图层.name=layerName
       }
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


function 转换为智能对象()	//转换为智能对象
    {

        var d = new ActionDescriptor();
        executeAction(stringIDToTypeID("newPlacedLayer"), d, DialogModes.NO);

    }

function 重新链接到文件(文件路径)	//重新链接到文件
    {

        var d = new ActionDescriptor();
        d.putPath(stringIDToTypeID("null"), new File(文件路径));
        d.putInteger(stringIDToTypeID("layerID"), 94);
        executeAction(stringIDToTypeID("placedLayerRelinkToFile"), d, DialogModes.NO);

    }

function 切换mask()	//取消选择
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("channel"), stringIDToTypeID("channel"), stringIDToTypeID("mask"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putBoolean(stringIDToTypeID("makeVisible"), false);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);

    }


function 毫米转像素(毫米, 每英寸像素数) {
  var 每英寸毫米数 = 25.4;
  var 英寸 = 毫米 / 每英寸毫米数;
  return Math.round(英寸 * 每英寸像素数);
}



function 画布大小()	//画布大小
    {

        var d = new ActionDescriptor();
        d.putBoolean(stringIDToTypeID("relative"), true);
        d.putUnitDouble(stringIDToTypeID("width"), stringIDToTypeID("distanceUnit"), 850.56);
        d.putUnitDouble(stringIDToTypeID("height"), stringIDToTypeID("distanceUnit"), 850.56);
        d.putEnumerated(stringIDToTypeID("horizontal"), stringIDToTypeID("horizontalLocation"), stringIDToTypeID("center"));
        d.putEnumerated(stringIDToTypeID("vertical"), stringIDToTypeID("verticalLocation"), stringIDToTypeID("center"));
        executeAction(stringIDToTypeID("canvasSize"), d, DialogModes.NO);

    }






function 载入选区()	//载入选区
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("channel"), stringIDToTypeID("selection"));
        d.putReference(stringIDToTypeID("null"), r);
        var r1 = new ActionReference();
        r1.putEnumerated(stringIDToTypeID("channel"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("to"), r1);
        executeAction(stringIDToTypeID("set"), d, DialogModes.NO);

    }



   function 获取当前选区四边距() {
  var currentDocument = app.activeDocument;
  var selectionBounds = currentDocument.selection.bounds;

  var top = selectionBounds[1].value;
  var left = selectionBounds[0].value;
  var bottom = selectionBounds[3].value;
  var right = selectionBounds[2].value;

  return {
    top: top,
    left: left,
    bottom: bottom,
    right: right
  };
}



function 新建图层()	//新建图层
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putClass(stringIDToTypeID("layer"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putInteger(stringIDToTypeID("layerID"), 135);
        executeAction(stringIDToTypeID("make"), d, DialogModes.NO);


    }


function 后移一层()	//后移一层
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        var r1 = new ActionReference();
        r1.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("previous"));
        d.putReference(stringIDToTypeID("to"), r1);
        executeAction(stringIDToTypeID("move"), d, DialogModes.NO);


    }







function 删除图层蒙版()	//删除图层蒙版
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("channel"), stringIDToTypeID("channel"), stringIDToTypeID("mask"));
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("delete"), d, DialogModes.NO);

    }





function 载入选区()	//载入选区
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("channel"), stringIDToTypeID("selection"));
        d.putReference(stringIDToTypeID("null"), r);
        var r1 = new ActionReference();
        r1.putEnumerated(stringIDToTypeID("channel"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("to"), r1);
        executeAction(stringIDToTypeID("set"), d, DialogModes.NO);

    }


function 删除图层蒙版()	//删除图层蒙版
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("channel"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("delete"), d, DialogModes.NO);


    }



function 向下合并()	//向下合并
    {

        var d = new ActionDescriptor();
        executeAction(stringIDToTypeID("mergeLayersNew"), d, DialogModes.NO);


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


function 创建剪贴蒙版()	//创建剪贴蒙版
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("groupEvent"), d, DialogModes.NO);


    }






"""