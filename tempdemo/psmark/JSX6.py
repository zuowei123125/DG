dxf6_jscode = """


function 前景色修改()	//取消选择
    {
  
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("color"), stringIDToTypeID("foregroundColor"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        d1.putDouble(stringIDToTypeID("cyan"), 20);
        d1.putDouble(stringIDToTypeID("magenta"), 0);
        d1.putDouble(stringIDToTypeID("yellowColor"), 0);
        d1.putDouble(stringIDToTypeID("black"), 0);
        d.putObject(stringIDToTypeID("to"), stringIDToTypeID("CMYKColorClass"), d1);
        d.putString(stringIDToTypeID("source"), "photoshopPicker");
        executeAction(stringIDToTypeID("set"), d, DialogModes.NO);
  
    }



function 图像切割2() {
    
    app.activeDocument.suspendHistory("图像切割", "图像切割()");
}


function 图像切割() {
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
  添加图层蒙版()
  当前图层=app.activeDocument.activeLayer 
  当前图层.name=layerName
       }
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










































    function 右下对齐2() {
        
    app.activeDocument.suspendHistory("右下对齐", "右下对齐()");
}
 
 
 function 右下对齐() {
  var groupName = 获取当前图层组名称();
  if (groupName !== null) {
    app.preferences.rulerUnits = Units.PIXELS;
    var splitGroupName = groupName.split("-");
    var firstPart = splitGroupName[0];
  } else {
    // 如果未获取到当前图层组名称，退出程序
  //  alert("未获取到当前图层组名称！");
    return;
  }

  try {
    当前花样图层 = app.activeDocument.layers.getByName(firstPart);
  } catch (e) {
    // 处理异常情况
    alert("没有找到对应的花样裁片: ");
    return; // 中断函数执行
  }

  app.activeDocument.activeLayer = 当前花样图层;

  切换mask();
   载入选区蒙版()
 // 应用图层蒙版();
 // 载入选区();

  var 边距 = 获取当前选区四边距();
  var 获取左右的中心坐标 = (边距.right - 边距.left) / 2 + 边距.left;
  var 获取右上的坐标 = 边距.right
  $.writeln("中心坐标=：" + 获取左右的中心坐标);

  var currentDocument = app.activeDocument;
  var height = currentDocument.height.value;

  var 上边距新 = 0;
  var 左边距新 = 获取右上的坐标-1 ;
  var 下边距新 = height;
  var 右边距新 = 获取右上的坐标 + 1;

  var 边距 = 获取当前选区四边距();
  $.writeln("上边距：" + 边距.top);
  $.writeln("左边距：" + 边距.left);
  $.writeln("下边距：" + 边距.bottom);
  $.writeln("右边距：" + 边距.right);

  //历史记录回退领口函数();
  新建选区(上边距新, 左边距新, 下边距新, 右边距新);
  app.activeDocument.activeLayer = 当前花样图层;
  切换mask();
  选区减去();

获取右上的坐标 = 获取当前选区四边距();
获取右上的坐标y坐标信息 = 获取右上的坐标.bottom;  //////////////////////以上的是获取花样的的中心坐标信息
  
获取右上的坐标x坐标信息 = 获取右上的坐标.left;
 // $.writeln("居中领口y坐标信息" + 获取到花样图层当前居中领口y坐标信息);
  //$.writeln("居中领口x坐标信息" + 获取到花样图层当前居中领口x坐标信息);
  
  //////////////////////以上的是获取花样的的中心坐标信息
  
  
  var currentDocument = app.activeDocument;
  var targetLayerSet = currentDocument.layerSets.getByName(groupName);

  if (targetLayerSet) {
    var layers = targetLayerSet.layers;

    if (layers.length > 0) {
      for (var i = 0; i < layers.length; i++) {
        var layer = layers[i];
        var 裁片图层 = layer.name;
        $.writeln("裁片图层坐标信息=" + 裁片图层);

        try {
          var 当前裁片图层 = app.activeDocument.layerSets.getByName(groupName).layers.getByName(裁片图层);
        } catch (e) {
          // 处理异常情况
          alert("没有找到对应的花样裁片 " );
          return; // 中断函数执行
        }

  


 app.activeDocument.activeLayer = 当前裁片图层;
  载入选区11()
  //var selectedLayer =  app.activeDocument.activeLayer;
//  var bounds = selectedLayer.bounds;
/*
  图层上边距新 = 0;
图层左边距新 = 右right ;
图层下边距新 = height;
图层右边距新 = 右right +1;
  
  
左left = bounds[0].value;
上top = bounds[1].value;
右right = bounds[2].value;
下bottom = bounds[3].value;
中心坐标centerX = (bounds[2].value - bounds[0].value) / 2 + bounds[0].value;

中心坐标centerY = (bounds[3].value - bounds[1].value) / 2 + bounds[1].value;
*/
//  $.writeln("中心坐标centerX" + 中心坐标centerX); 
//  $.writeln("中心坐标centerY" +中心坐标cent*erY);

   获取花样右上的坐标裁片位置坐标 = 获取当前选区四边距();

 图层上边距新 = 0;
图层左边距新 =  获取花样右上的坐标裁片位置坐标.right-1 ;
图层下边距新 = height;
图层右边距新 =  获取花样右上的坐标裁片位置坐标.right +1;

  
    新建选区(图层上边距新, 图层左边距新, 图层下边距新, 图层右边距新);
    app.activeDocument.activeLayer = 当前裁片图层;
   载入选区交叉图层()
 获取右上的坐标裁片位置坐标 = 获取当前选区四边距();
 获取右上的坐标裁片位置坐标x=获取右上的坐标裁片位置坐标.left
获取右上的坐标裁片位置坐标y=获取右上的坐标裁片位置坐标.bottom

位移距离PXy = 获取右上的坐标y坐标信息 - 获取右上的坐标裁片位置坐标y;
位移距离PXx = 获取右上的坐标x坐标信息 -  获取右上的坐标裁片位置坐标x;
  $.writeln(位移距离PXy); 
    $.writeln(位移距离PXx);
    取消选择()
 自由变换2(位移距离PXy,位移距离PXx)
 //alert("移动")
  }
  }
}

取消选择();
}

  function 获取当前图层组名称() {
  var currentDocument = app.activeDocument;
  var currentLayer = currentDocument.activeLayer;

  if (currentLayer.typename === "LayerSet") {
    var groupName = currentLayer.name;
    return groupName;
  } else {
   alert("当前图层不是图层组。");
    return null;
  }
}





function 载入选区交叉图层()	//载入选区
    {
    
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("channel"), stringIDToTypeID("channel"), stringIDToTypeID("transparencyEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        var r1 = new ActionReference();
        r1.putProperty(stringIDToTypeID("channel"), stringIDToTypeID("selection"));
        d.putReference(stringIDToTypeID("with"), r1);
        executeAction(charIDToTypeID("Intr"), d, DialogModes.NO);
        }
 
  
function 载入选区蒙版()	//载入选区
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
  

  
  function 遍历图层组内的图层(图层组名称) {
  var currentDocument = app.activeDocument;
  var targetLayerSet = currentDocument.layerSets.getByName(图层组名称);

  if (targetLayerSet) {
    var layers = targetLayerSet.layers;

    if (layers.length > 0) {
      for (var i = 0; i < layers.length; i++) {
        var layer = layers[i];
        // 在这里对每个图层进行进一步的操作
        $.writeln("图层名称：" + layer.name);
      }
    } else {
      $.writeln("图层组中没有任何图层。");
    }
  } else {
    $.writeln("找不到指定名称的图层组。");
  }
}

  
  
  
function 新建选区(上边距, 左边距, 下边距, 右边距) {
  var currentDocument = app.activeDocument;
  var top = 上边距;
  var left = 左边距;
  var bottom = 下边距;
  var right = 右边距;

  var selectionRegion = Array(Array(left, top), Array(right, top), Array(right, bottom), Array(left, bottom));
  currentDocument.selection.select(selectionRegion);
}



function 选区减去()	//载入选区
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("channel"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        var r1 = new ActionReference();
        r1.putProperty(stringIDToTypeID("channel"), stringIDToTypeID("selection"));
        d.putReference(stringIDToTypeID("with"), r1);
        executeAction(charIDToTypeID("Intr"), d, DialogModes.NO);
  
    }
  
  
  
// 将像素转换为毫米
function pixelsToMillimeters(pixels) {
  // 获取当前文档
  var doc = app.activeDocument;

  // 获取图像的分辨率（像素/英寸）
  var resolution = doc.resolution;

  // 计算像素转换为毫米
  var inches = pixels / resolution;
  var millimeters = inches * 25.4;

  return millimeters.toFixed(2); // 保留两位小数
}

  
  
  
function 切换mask()	//
    {
    
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("channel"), stringIDToTypeID("channel"), stringIDToTypeID("mask"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putBoolean(stringIDToTypeID("makeVisible"), false);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
     
  
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


function 获取当前文档四边距() {
  var currentDocument = app.activeDocument;
  var documentBounds = currentDocument.bounds;

  var top = documentBounds[1].value;
  var left = documentBounds[0].value;
  var bottom = documentBounds[3].value;
  var right = documentBounds[2].value;

  return {
    top: top,
    left: left,
    bottom: bottom,
    right: right
  };
}


function 选区减去2()	//
    {
  
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("channel"), stringIDToTypeID("channel"), stringIDToTypeID("transparencyEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        var r1 = new ActionReference();
        r1.putProperty(stringIDToTypeID("channel"), stringIDToTypeID("selection"));
        d.putReference(stringIDToTypeID("with"), r1);
        executeAction(charIDToTypeID("Intr"), d, DialogModes.NO);
   
    }

function 遍历图层组内的图层(图层组名称) {
  var currentDocument = app.activeDocument;
  var targetLayerSet = currentDocument.layerSets.getByName(图层组名称);

  if (targetLayerSet) {
    var layers = targetLayerSet.layers;

    if (layers.length > 0) {
      for (var i = 0; i < layers.length; i++) {
        var layer = layers[i];
        // 在这里对每个图层进行进一步的操作
        $.writeln("图层名称：" + layer.name);
      }
    } else {
      $.writeln("图层组中没有任何图层。");
    }
  } else {
    $.writeln("找不到指定名称的图层组。");
  }
}


function 自由变换2(位移距离PXy,位移距离PXx)	//自由变换
    {
  
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putEnumerated(stringIDToTypeID("freeTransformCenterState"), stringIDToTypeID("quadCenterState"), stringIDToTypeID("QCSAverage"));
        var d1 = new ActionDescriptor();
        d1.putUnitDouble(stringIDToTypeID("horizontal"), stringIDToTypeID("pixelsUnit"), 位移距离PXx);
        d1.putUnitDouble(stringIDToTypeID("vertical"), stringIDToTypeID("pixelsUnit"), 位移距离PXy);
        d.putObject(stringIDToTypeID("offset"), stringIDToTypeID("offset"), d1);
        d.putBoolean(stringIDToTypeID("linked"), true);
        d.putEnumerated(charIDToTypeID("Intr"), stringIDToTypeID("interpolationType"), stringIDToTypeID("nearestNeighbor"));
        executeAction(stringIDToTypeID("transform"), d, DialogModes.NO);

  
    }

function 历史记录回退领口函数()	//
    {
 
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putOffset(stringIDToTypeID("historyState"), -2    );
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
   
    }
function 取消选择()	//取消选择
    {
    
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("channel"), stringIDToTypeID("selection"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putEnumerated(stringIDToTypeID("to"), stringIDToTypeID("ordinal"), stringIDToTypeID("none"));
        executeAction(stringIDToTypeID("set"), d, DialogModes.NO);
    
    }


function 历史记录回退1领口函数()	//
    {
 
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putOffset(stringIDToTypeID("historyState"), -1   );
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
   
  
    }

function 载入选区11()	//载入选区
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
    
function 取消选择()	//取消选择
    {
    
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("channel"), stringIDToTypeID("selection"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putEnumerated(stringIDToTypeID("to"), stringIDToTypeID("ordinal"), stringIDToTypeID("none"));
        executeAction(stringIDToTypeID("set"), d, DialogModes.NO);
    
    }













"""








