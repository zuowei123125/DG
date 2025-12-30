dxf2_jscode = """




  function 设置花样组顺序居中() {
  var doc = app.activeDocument;
  var targetLayerSet = null;

  // 遍历所有图层组
  for (var i = 0; i < doc.layerSets.length; i++) {
    var layerSet = doc.layerSets[i];

    // 判断图层组名称是否包含"大货裁片"
    if (layerSet.name.indexOf("大货裁片") !== -1) {
      targetLayerSet = layerSet; // 找到匹配的图层组
      break; // 中断循环，不再继续遍历其他图层组
    }
  }

  // 判断是否找到匹配的图层组
  if (targetLayerSet) {
    // 判断图层组中是否存在图层
    if (targetLayerSet.layers.length > 0) {
      // 在这里执行处理图层的操作
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
          layerNames.push(layerName); // 将匹配到的图层名称添加到数组中
        }
      }

      // 输出匹配到的数值个数
      // $.writeln("匹配到的数值个数：" + matchCount);

      // 遍历保存的图层名称数组
      for (var i = 0; i < layerNames.length; i++) {
        var name = layerNames[i];
        var 当前花样图层 = app.activeDocument.layers.getByName(name);
        app.activeDocument.activeLayer = 当前花样图层;
        选择蒙版();
        载入选区蒙版()
        //应用图层蒙版();
        var layerCenterInfo = 获取当前图层中心坐标();
        if (layerCenterInfo !== null) {
          var layerName = layerCenterInfo.layerName;
          var 花样图层X = layerCenterInfo.centerX;
          var 花样图层Y = layerCenterInfo.centerY;

          // $.writeln("图层名称：" + layerName);
          //$.writeln("中心坐标：(" + centerX + ", " + centerY + ")");
        } else {
          $.writeln("无法获取当前图层中心坐标。");
        }
        //历史记录回退();
        var 裁片组名称 = name + "-大货裁片";
        var 裁片组 = app.activeDocument.layerSets.getByName(裁片组名称);
        app.activeDocument.activeLayer = 裁片组;
        对裁片进行大小排序();
        app.activeDocument.activeLayer = 裁片组;
        var centerCoordinates = 获取图层组中心坐标();
        if (centerCoordinates !== null) {
          var 空白裁片组X = centerCoordinates[0];
          var 空白裁片组Y = centerCoordinates[1];

          app.activeDocument.activeLayer.translate(
            花样图层X - Number(空白裁片组X),
            花样图层Y - Number(空白裁片组Y)
          ); //全局单位设置为mm即可

          //$.writeln("图层组中心坐标：(" + centerX + ", " + centerY + ")");
        } else {
          $.writeln("无法获取图层组中心坐标。");
        }
      }
    } else {
      // 如果图层组中不存在图层，执行其他操作或退出程序
      alert("当前大货裁片内未抓取裁片！！！");
    }
  } else {
    // 如果没有找到匹配的图层组，退出程序
    //alert("当前文档未设置大货裁片组！！！");
  }
}



function 顺时针90旋转()	//自由变换
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putEnumerated(stringIDToTypeID("freeTransformCenterState"), stringIDToTypeID("quadCenterState"), stringIDToTypeID("QCSAverage"));
        var d1 = new ActionDescriptor();
        d1.putUnitDouble(stringIDToTypeID("horizontal"), stringIDToTypeID("pixelsUnit"), 0);
        d1.putUnitDouble(stringIDToTypeID("vertical"), stringIDToTypeID("pixelsUnit"), 0);
        d.putObject(stringIDToTypeID("offset"), stringIDToTypeID("offset"), d1);
        d.putUnitDouble(stringIDToTypeID("angle"), stringIDToTypeID("angleUnit"), 90);
        d.putBoolean(stringIDToTypeID("linked"), true);
        d.putEnumerated(charIDToTypeID("Intr"), stringIDToTypeID("interpolationType"), stringIDToTypeID("nearestNeighbor"));
        executeAction(stringIDToTypeID("transform"), d, DialogModes.NO);
   
    }



function 逆时针90旋转()	//自由变换
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putEnumerated(stringIDToTypeID("freeTransformCenterState"), stringIDToTypeID("quadCenterState"), stringIDToTypeID("QCSAverage"));
        var d1 = new ActionDescriptor();
        d1.putUnitDouble(stringIDToTypeID("horizontal"), stringIDToTypeID("pixelsUnit"), 0);
        d1.putUnitDouble(stringIDToTypeID("vertical"), stringIDToTypeID("pixelsUnit"), 0);
        d.putObject(stringIDToTypeID("offset"), stringIDToTypeID("offset"), d1);
        d.putUnitDouble(stringIDToTypeID("angle"), stringIDToTypeID("angleUnit"), -90);
        d.putBoolean(stringIDToTypeID("linked"), true);
        d.putEnumerated(charIDToTypeID("Intr"), stringIDToTypeID("interpolationType"), stringIDToTypeID("nearestNeighbor"));
        executeAction(stringIDToTypeID("transform"), d, DialogModes.NO);
   
    }


function 选择蒙版()	//选择蒙版
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("channel"), stringIDToTypeID("channel"), stringIDToTypeID("mask"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putBoolean(stringIDToTypeID("makeVisible"), false);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);

    }


function 应用图层蒙版()	//应用图层蒙版
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("channel"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putBoolean(stringIDToTypeID("apply"), true);
        executeAction(stringIDToTypeID("delete"), d, DialogModes.NO);

    }


function 获取当前图层中心坐标() {
  var currentDocument = app.activeDocument;
  var selectionBounds = currentDocument.selection.bounds;
  var currentLayer = currentDocument.activeLayer;
  if (selectionBounds) {
    var centerX = selectionBounds[0] + (selectionBounds[2] - selectionBounds[0]) / 2;
    var centerY = selectionBounds[1] + (selectionBounds[3] - selectionBounds[1]) / 2;

    return {
      layerName: currentLayer.name,
      centerX: centerX,
      centerY: centerY
    };
  } else {
    $.writeln("没有当前选区。");
    return null;
  }
}



function 历史记录回退()	//
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putOffset(stringIDToTypeID("historyState"), -1);
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);

    }


function 获取图层组中心坐标() {
  var currentDocument = app.activeDocument;
  var currentLayer = currentDocument.activeLayer;

  if (currentLayer.typename === "LayerSet") {
    var layers = currentLayer.layers;

    if (layers.length > 0) {
      var firstLayer = layers[0];
      var bounds = firstLayer.bounds;

      var centerX = bounds[0] + (bounds[2] - bounds[0]) / 2;
      var centerY = bounds[1] + (bounds[3] - bounds[1]) / 2;

      return [centerX, centerY];
    } else {
      $.writeln("图层组没有任何图层。");
    }
  } else {
    $.writeln("当前图层不是图层组。");
  }

  // 如果无法获取图层组的中心坐标，则返回 null
  return null;
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
  



function 对裁片进行大小排序() {
  var currentDocument = app.activeDocument;
  var currentLayer = currentDocument.activeLayer;

  if (currentLayer.typename === "LayerSet") {
    var layers = currentLayer.layers;

    if (layers.length > 0) {
      var layerArray = [];

      // 遍历图层组的每个图层，将图层和它们的宽度、高度存储到数组中
      for (var i = 0; i < layers.length; i++) {
        var layer = layers[i];
        if (layer.kind === LayerKind.NORMAL && layer.bounds) {
          var width = layer.bounds[2] - layer.bounds[0];
          var height = layer.bounds[3] - layer.bounds[1];
          layerArray.push({
            layer: layer,
            width: width,
            height: height
          });
        }
      }

      // 按照宽度和高度从大到小排序图层数组
      layerArray.sort(function(a, b) {
        if (a.width === b.width) {
          return b.height - a.height;
        }
        return b.width - a.width;
      });

      // 创建一个临时图层组，用于存放排序后的裁片
      var tempGroup = currentLayer.parent.layerSets.add();

      // 将排序后的裁片依次移动到临时图层组中
      for (var i = 0; i < layerArray.length; i++) {
        var layerInfo = layerArray[i];
        var layer = layerInfo.layer;
        layer.move(tempGroup, ElementPlacement.INSIDE);
      }

      // 将临时图层组的裁片移动回原始图层组中
      for (var i = tempGroup.layers.length - 1; i >= 0; i--) {
        var layer = tempGroup.layers[i];
        layer.move(currentLayer, ElementPlacement.PLACEATBEGINNING);
      }

      // 删除临时图层组
      tempGroup.remove();

      $.writeln("已对裁片进行大小排序。");
    } else {
      $.writeln("图层组没有任何图层。");
    }
  } else {
    $.writeln("当前图层不是图层组。");
  }
}
////////////////主函数体领口对齐
 

 function 领口对齐() {
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
  应用图层蒙版();
  载入选区();

  var 边距 = 获取当前选区四边距();
  var 获取左右的中心坐标 = (边距.right - 边距.left) / 2 + 边距.left;
  $.writeln("中心坐标=：" + 获取左右的中心坐标);

  var currentDocument = app.activeDocument;
  var height = currentDocument.height.value;

  var 上边距新 = 0;
  var 左边距新 = 获取左右的中心坐标 - 1;
  var 下边距新 = height;
  var 右边距新 = 获取左右的中心坐标 + 1;

  var 边距 = 获取当前选区四边距();
  $.writeln("上边距：" + 边距.top);
  $.writeln("左边距：" + 边距.left);
  $.writeln("下边距：" + 边距.bottom);
  $.writeln("右边距：" + 边距.right);

  历史记录回退领口函数();
  新建选区(上边距新, 左边距新, 下边距新, 右边距新);
  app.activeDocument.activeLayer = 当前花样图层;
  切换mask();
  选区减去();

  var 领窝边距 = 获取当前选区四边距();
  var 获取到花样图层当前居中领口坐标信息 = 领窝边距.top;
  $.writeln("居中领口坐标信息" + 获取到花样图层当前居中领口坐标信息);

  历史记录回退1领口函数();

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

        选区减去2();
        var 领窝边距A = 获取当前选区四边距();
        var 获取到当前裁片图层当前居中领口坐标信息 = 领窝边距A.top;
        $.writeln("裁片领口" + 获取到当前裁片图层当前居中领口坐标信息);

        历史记录回退1领口函数();
        取消选择();

      var 当前裁片图层 = app.activeDocument.layerSets.getByName(groupName).layers.getByName(裁片图层);
      app.activeDocument.activeLayer = 当前裁片图层;

      var 位移距离PX = 获取到花样图层当前居中领口坐标信息 - 获取到当前裁片图层当前居中领口坐标信息;
      自由变换(位移距离PX);

      新建选区(上边距新, 左边距新, 下边距新, 右边距新);
      $.writeln("分割后的第一个部分：" + firstPart);
    }
  }
}

取消选择();
}

////////////////主函数体


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





function 切换mask()	//
    {
    
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("channel"), stringIDToTypeID("channel"), stringIDToTypeID("mask"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putBoolean(stringIDToTypeID("makeVisible"), false);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
     
  
    }




function 应用图层蒙版()	//应用图层蒙版
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("channel"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putBoolean(stringIDToTypeID("apply"), true);
        executeAction(stringIDToTypeID("delete"), d, DialogModes.NO);
     
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



function 新建选区(上边距, 左边距, 下边距, 右边距) {
  var currentDocument = app.activeDocument;
  var top = 上边距;
  var left = 左边距;
  var bottom = 下边距;
  var right = 右边距;

  var selectionRegion = Array(Array(left, top), Array(right, top), Array(right, bottom), Array(left, bottom));
  currentDocument.selection.select(selectionRegion);
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




function 历史记录回退领口函数()	//
    {
 
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putOffset(stringIDToTypeID("historyState"), -2    );
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
   
    }


function 历史记录回退1领口函数()	//
    {
 
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putOffset(stringIDToTypeID("historyState"), -1   );
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
   
  
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



function 自由变换(位移距离PX)	//自由变换
    {
  
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putEnumerated(stringIDToTypeID("freeTransformCenterState"), stringIDToTypeID("quadCenterState"), stringIDToTypeID("QCSAverage"));
        var d1 = new ActionDescriptor();
        d1.putUnitDouble(stringIDToTypeID("horizontal"), stringIDToTypeID("pixelsUnit"), 0);
        d1.putUnitDouble(stringIDToTypeID("vertical"), stringIDToTypeID("pixelsUnit"), 位移距离PX);
        d.putObject(stringIDToTypeID("offset"), stringIDToTypeID("offset"), d1);
        d.putBoolean(stringIDToTypeID("linked"), true);
        d.putEnumerated(charIDToTypeID("Intr"), stringIDToTypeID("interpolationType"), stringIDToTypeID("nearestNeighbor"));
        executeAction(stringIDToTypeID("transform"), d, DialogModes.NO);

  
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



////////////////主函数体领口对齐


function 烧花线添加() {

app.activeDocument.suspendHistory("烧花线添加", "烧花线()");
}

function 烧花线() {








// 遍历当前文档图层

var doc = app.activeDocument;
var layers = doc.layers;
var filteredLayers = [];

// 遍历图层，筛选以P开头的图层
for (var i = 0; i < layers.length; i++) {
  var layer = layers[i];
  if (layer.name.charAt(0) === 'P') {
    filteredLayers.push(layer);
  }
}

空置图层()
// 输出图层名称
for (var j = 0; j <  filteredLayers.length; j++) {
  var filteredLayer = filteredLayers[j];

  var 裁片底图名称=filteredLayer.name;

  多选图层(裁片底图名称);

 // alert(filteredLayer.name);

}
  合并图层();
  置为顶层();
var layer = app.activeDocument.activeLayer;
layer.name = "底图";
色彩范围()
新建图层()
var layer2 = app.activeDocument.activeLayer;
layer2.name = "剪口";
扩展2();
填充();
画布大小();
魔棒();
扩展();
选择反向();
清除();
 var 底图 =  app.activeDocument.layers.getByName( "底图");
 app.activeDocument.activeLayer=底图;

置为底层()
图层样式()
取消选择()
function 多选图层(裁片底图名称)	//
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putName(stringIDToTypeID("layer"), 裁片底图名称);
        d.putReference(stringIDToTypeID("null"), r);
        d.putEnumerated(stringIDToTypeID("selectionModifier"), stringIDToTypeID("selectionModifierType"), stringIDToTypeID("addToSelection"));
        d.putBoolean(stringIDToTypeID("makeVisible"), false);
        var list = new ActionList();
        list.putInteger(4);

        d.putList(stringIDToTypeID("layerID"), list);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);

    }



function 空置图层()	//
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("selectNoLayers"), d, DialogModes.NO);

    }

function 合并图层()	//合并图层
    {

        var d = new ActionDescriptor();
        executeAction(stringIDToTypeID("mergeLayersNew"), d, DialogModes.NO);

    }


function 置为底层()	//置为底层
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        var r1 = new ActionReference();
        r1.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("back"));
        d.putReference(stringIDToTypeID("to"), r1);
        executeAction(stringIDToTypeID("move"), d, DialogModes.NO);

    }


function 置为顶层()	//置为顶层
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        var r1 = new ActionReference();
        r1.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("front"));
        d.putReference(stringIDToTypeID("to"), r1);
        executeAction(stringIDToTypeID("move"), d, DialogModes.NO);

    }




function 色彩范围()	//色彩范围
    {

        var d = new ActionDescriptor();
        d.putInteger(stringIDToTypeID("fuzziness"), 40);
        var d1 = new ActionDescriptor();
        d1.putDouble(stringIDToTypeID("luminance"), 0);
        d1.putDouble(stringIDToTypeID("a"), 0);
        d1.putDouble(stringIDToTypeID("b"), 0);
        d.putObject(stringIDToTypeID("minimum"), stringIDToTypeID("labColor"), d1);
        var d2 = new ActionDescriptor();
        d2.putDouble(stringIDToTypeID("luminance"), 0);
        d2.putDouble(stringIDToTypeID("a"), 0);
        d2.putDouble(stringIDToTypeID("b"), 0);
        d.putObject(stringIDToTypeID("maximum"), stringIDToTypeID("labColor"), d2);
        d.putInteger(stringIDToTypeID("colorModel"), 0);
        executeAction(stringIDToTypeID("colorRange"), d, DialogModes.NO);

    }

function 新建图层()	//新建图层
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putClass(stringIDToTypeID("layer"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putInteger(stringIDToTypeID("layerID"), 33);
        executeAction(stringIDToTypeID("make"), d, DialogModes.NO);

    }


function 扩展2()	//扩展
    {

        var d = new ActionDescriptor();
        d.putUnitDouble(stringIDToTypeID("by"), stringIDToTypeID("pixelsUnit"), 1);
        d.putBoolean(stringIDToTypeID("selectionModifyEffectAtCanvasBounds"), false);
        executeAction(stringIDToTypeID("expand"), d, DialogModes.NO);

    }



function 填充()	//填充
    {

        var d = new ActionDescriptor();
        d.putEnumerated(stringIDToTypeID("using"), stringIDToTypeID("fillContents"), stringIDToTypeID("foregroundColor"));
        d.putUnitDouble(stringIDToTypeID("opacity"), stringIDToTypeID("percentUnit"), 100);
        d.putEnumerated(stringIDToTypeID("mode"), stringIDToTypeID("blendMode"), stringIDToTypeID("normal"));
        executeAction(stringIDToTypeID("fill"), d, DialogModes.NO);

    }



function 画布大小()	//画布大小
    {

        var d = new ActionDescriptor();
        d.putBoolean(stringIDToTypeID("relative"), true);
        d.putUnitDouble(stringIDToTypeID("width"), stringIDToTypeID("distanceUnit"), 28.3200028808597);
        d.putUnitDouble(stringIDToTypeID("height"), stringIDToTypeID("distanceUnit"), 28.3200028808597);
        d.putEnumerated(stringIDToTypeID("horizontal"), stringIDToTypeID("horizontalLocation"), stringIDToTypeID("center"));
        d.putEnumerated(stringIDToTypeID("vertical"), stringIDToTypeID("verticalLocation"), stringIDToTypeID("center"));
        executeAction(stringIDToTypeID("canvasSize"), d, DialogModes.NO);

    }


function 魔棒()	//魔棒
   {
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("channel"), stringIDToTypeID("selection"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        d1.putUnitDouble(stringIDToTypeID("horizontal"), stringIDToTypeID("pixelsUnit"), 1);
        d1.putUnitDouble(stringIDToTypeID("vertical"), stringIDToTypeID("pixelsUnit"), 1);
        d.putObject(stringIDToTypeID("to"), stringIDToTypeID("point"), d1);
        d.putInteger(stringIDToTypeID("tolerance"), 6);
        executeAction(stringIDToTypeID("set"), d, DialogModes.NO);

    }



function 扩展()	//扩展
    {

        var d = new ActionDescriptor();
        d.putUnitDouble(stringIDToTypeID("by"), stringIDToTypeID("pixelsUnit"), 25);
        d.putBoolean(stringIDToTypeID("selectionModifyEffectAtCanvasBounds"), false);
        executeAction(stringIDToTypeID("expand"), d, DialogModes.NO);

    }


function 选择反向()	//选择反向
    {

        var d = new ActionDescriptor();
        executeAction(stringIDToTypeID("inverse"), d, DialogModes.NO);

    }


function 清除()	//清除
    {

        var d = new ActionDescriptor();
        executeAction(stringIDToTypeID("delete"), d, DialogModes.NO);

    }


function 图层样式()	//图层样式
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("property"), stringIDToTypeID("layerEffects"));
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        d1.putUnitDouble(stringIDToTypeID("scale"), stringIDToTypeID("percentUnit"), 208.333312140571);
        var d2 = new ActionDescriptor();
        d2.putBoolean(stringIDToTypeID("enabled"), true);
        d2.putBoolean(stringIDToTypeID("present"), true);
        d2.putBoolean(stringIDToTypeID("showInDialog"), true);
        d2.putEnumerated(stringIDToTypeID("style"), stringIDToTypeID("frameStyle"), stringIDToTypeID("outsetFrame"));
        d2.putEnumerated(stringIDToTypeID("paintType"), stringIDToTypeID("frameFill"), stringIDToTypeID("solidColor"));
        d2.putEnumerated(stringIDToTypeID("mode"), stringIDToTypeID("blendMode"), stringIDToTypeID("normal"));
        d2.putUnitDouble(stringIDToTypeID("opacity"), stringIDToTypeID("percentUnit"), 100);
        d2.putUnitDouble(stringIDToTypeID("size"), stringIDToTypeID("pixelsUnit"), 16);
        var d3 = new ActionDescriptor();
        d3.putDouble(stringIDToTypeID("red"), 255);
        d3.putDouble(stringIDToTypeID("green"), 0);
        d3.putDouble(stringIDToTypeID("blue"), 0);
        d2.putObject(stringIDToTypeID("color"), stringIDToTypeID("RGBColor"), d3);
        d2.putBoolean(stringIDToTypeID("overprint"), false);
        d1.putObject(stringIDToTypeID("frameFX"), stringIDToTypeID("frameFX"), d2);
        d.putObject(stringIDToTypeID("to"), stringIDToTypeID("layerEffects"), d1);
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
 }










//////////////////////////////标记函数


function 信息标记2() {
    RUN1()
    RUN2()
    }
    
function RUN1(){
    
app.preferences.rulerUnits = Units.CM;

// 获取当前选区
var currentSelection = app.activeDocument.selection;

// 确保当前选区不为空且为矩形选区
if (currentSelection != null && currentSelection.hasOwnProperty('bounds')) {
  // 获取当前选区的坐标
 var bounds = currentSelection.bounds;

  // 获取当前选区的宽度和高度（以 cm 为单位）
  var resolution = app.activeDocument.resolution;
  var widthInCM = (bounds[2].as("cm") - bounds[0].as("cm"));
  var heightInCM = (bounds[3].as("cm") - bounds[1].as("cm"));

  // 将宽度和高度输出到调试台
  $.writeln("宽度：" + widthInCM.toFixed(2) + "cm");
  $.writeln("高度：" + heightInCM.toFixed(2) + "cm");

  // 创建一个文本图层
  var textLayer = app.activeDocument.artLayers.add();
  textLayer.kind = LayerKind.TEXT;

  // 设置文本图层的文本内容
  textLayer.textItem.contents = "宽度：" + widthInCM.toFixed(2) + "cm，高度：" + heightInCM.toFixed(2) + "cm";
  textLayer.textItem.size = 40
  // 将文本图层移动到选区的最上方
    textLayer.textItem.position = [app.activeDocument.width / 2, app.activeDocument.height / 2-2];
   
}
}
function RUN2()
{

// 获取当前活动文档
var currentDocument = app.activeDocument;

// 获取当前文档的文件名
var fileName = currentDocument.name;

// 去掉文件名的后缀名
var fileNameWithoutExtension = fileName.split('.').slice(0, -1).join('.');

// 用分割符 "-" 分割文件名
var fileNameParts = fileNameWithoutExtension.split('-');

// 获取最后两个数组
var lastTwoParts = fileNameParts.slice(-2);

// 创建一个新的文本图层
var textLayer = currentDocument.artLayers.add();
textLayer.kind = LayerKind.TEXT;

// 设置文本图层的文本内容
textLayer.textItem.contents = fileNameWithoutExtension;
textLayer.textItem.size = 50
// 可选：将文本图层移动到文档的中心
textLayer.textItem.position = [currentDocument.width / 2, currentDocument.height / 2];


}

//////////////////////////////标记函数

//////////////////////////////标记函数



function 批量缩水值修改(宽度值,高度值) {
  app.preferences.rulerUnits = Units.CM;
  var 主文档 = app.activeDocument;
  var 主文档名称 = 主文档.name;

  // 遍历当前打开的文档
  for (var i = 0; i < app.documents.length; i++) {
    var document = app.documents[i];
    var documentName = document.name;

    // 判断文档名称是否与主文档名称不相同
    if (documentName !== 主文档名称) {
      // 设置当前文档为活动文档
      app.activeDocument = document;

      var 匹配图层数组 = 遍历图层查找P1();

      // 遍历匹配图层数组
      for (var j = 0; j < 匹配图层数组.length; j++) {
        var 当前匹配图层 = 匹配图层数组[j];
}
        // 选中当前匹配图层
       

        // 获取当前选区
        var currentSelection = app.activeDocument.selection;

        // 确保当前选区不为空且为矩形选区
        if (currentSelection != null && currentSelection.hasOwnProperty('bounds')) {
          // 进行缩放操作
        
            app.activeDocument.activeLayer = 当前匹配图层;

        // 载入选区
            载入选区();
          // 获取当前选区的坐标
          var bounds = currentSelection.bounds;

          // 获取当前选区的宽度和高度（以 cm 为单位）
          var resolution = app.activeDocument.resolution;
          var widthInCM = (bounds[2].as("cm") - bounds[0].as("cm"));
          var heightInCM = (bounds[3].as("cm") - bounds[1].as("cm"));
          var 当前P1图层宽高信息 = "宽度：" + widthInCM.toFixed(2) + "cm，高度：" + heightInCM.toFixed(2) + "cm";

          // 获取当前裁片套数
          var 搜索关键词 = "P1";
          var 匹配的图层数量 = 获取匹配图层数量(搜索关键词);
          var 当前裁片套数 = "一段" + 匹配的图层数量 + "件";

          // 创建新图层并设置名称
        ///  var 新图层 = 主文档.artLayers.add();
        var  新图层 = "当前文档宽度缩水" + 宽度值 + "高度缩水" + 高度值;

          // 移动选区到新图层
        //  currentSelection.cut();
        //  app.activeDocument.paste();

          // 文件简介写入
         // 文件简介写入(当前裁片套数, 当前P1图层宽高信息 + "-" + 新图层);
         //这里删除了文件简介的写入将缩水值修改按钮
            调整图像尺寸(宽度值, 高度值);
            ////这里取消了保存功能 为了防止运行的时候变卡
            //activeDocument.save();
        } else {
          alert("没有找到匹配的图层。");
        }
      
    }
  }
  app.activeDocument=主文档 
  alert("写入信息成功","来自左威的提醒");
}

function 文件简介写入(当前裁片套数, 当前P1图层宽高信息) {
  var d = new ActionDescriptor();
  var r = new ActionReference();
  r.putProperty(stringIDToTypeID("property"), stringIDToTypeID("fileInfo"));
  r.putEnumerated(stringIDToTypeID("document"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
  d.putReference(stringIDToTypeID("null"), r);
  var d1 = new ActionDescriptor();
  d1.putString(stringIDToTypeID("caption"), 当前裁片套数);
  d1.putString(stringIDToTypeID("keywords"), 当前P1图层宽高信息);
  d.putObject(stringIDToTypeID("to"), stringIDToTypeID("fileInfo"), d1);
  executeAction(stringIDToTypeID("set"), d, DialogModes.NO);
}




function 调整图像尺寸(宽度值, 高度值) {
  var 动作描述 = new ActionDescriptor();
  动作描述.putUnitDouble(stringIDToTypeID("width"), stringIDToTypeID("percentUnit"), 100 + 宽度值);
  动作描述.putUnitDouble(stringIDToTypeID("height"), stringIDToTypeID("percentUnit"), 100 + 高度值);
  动作描述.putEnumerated(charIDToTypeID("Intr"), stringIDToTypeID("interpolationType"), stringIDToTypeID("nearestNeighbor"));
  executeAction(stringIDToTypeID("imageSize"), 动作描述, DialogModes.NO);
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




function 遍历图层查找P1() {
  var 匹配图层数组 = [];
  var 文档 = app.activeDocument;

  // 遍历所有图层
  function 遍历所有图层(图层) {
    if (图层.typename === "LayerSet") {
      for (var i = 0; i < 图层.layers.length; i++) {
        遍历所有图层(图层.layers[i]);
      }
    } else {
      var 图层名分割数组 = 图层.name.split("-");  // 假设分割符是 "_"
      if (图层名分割数组[0] === "P1") {  // 精确匹配
        匹配图层数组.push(图层);
      }
    }
  }

  // 开始遍历
  for (var j = 0; j < 文档.layers.length; j++) {
    遍历所有图层(文档.layers[j]);
  }

  return 匹配图层数组;
}


function 获取匹配图层数量(搜索关键词) {
  var 匹配图层数量 = 0;

  // 递归遍历图层及其子图层
  function 遍历图层(图层) {
    if (图层.typename === "LayerSet") {
      for (var i = 0; i < 图层.layers.length; i++) {
        遍历图层(图层.layers[i]);
      }
    } else {
      // 进行模糊匹配和精确分割匹配
      if (图层.name.indexOf(搜索关键词) !== -1 && 精确分割匹配图层(图层.name, 搜索关键词)) {
        匹配图层数量++;
      }
    }
  }

  // 精确分割匹配图层名
  function 精确分割匹配图层(图层名, 搜索词) {
    var 图层名分割数组 = 图层名.split("-");  // 假设分割符是 "_"
    return 图层名分割数组[0] === 搜索词;
  }

  var 当前文档 = app.activeDocument;
  var 所有图层 = 当前文档.layers;

  for (var i = 0; i < 所有图层.length; i++) {
    遍历图层(所有图层[i]);
  }

  return 匹配图层数量;
}








//////////////////////////////标记函数
//////////////////////////////信息激活函数











 function 信息激活2() {
        
    app.activeDocument.suspendHistory("宽高码数信息激活", "信息激活()");
    }

function 信息激活() {


var 主文档 = app.activeDocument;
var 主文档名称 = 主文档.name;

// 遍历当前打开的文档
for (var i = 0; i < app.documents.length; i++) {
    var document = app.documents[i];
    var documentName = document.name;

    // 判断文档名称是否与主文档名称不相同
    if (documentName !== 主文档名称) {
        // 设置当前文档为活动文档
        app.activeDocument = document;

        var 文件信息 = 获取文件简介信息();
        if (typeof 文件信息 === 'object') {
            var 版权 = 文件信息.版权;
            var 关键字 = 文件信息.关键字;
            var 描述 = 文件信息.描述;

            var 当前套数 = 描述; // 这一行可能需要根据描述的实际数据进行修改
            var 宽高信息跟缩水信息 = 关键字.join(", ");
            var 分割信息 = 宽高信息跟缩水信息.split("-");
            var 宽高信息 = 分割信息[0];
            var 缩水信息 = 分割信息[1];
           var currentDocument = app.activeDocument;
            var fileName = currentDocument.name;
            var fileNameWithoutExtension = fileName.split('.').slice(0, -1).join('.');



// 去掉文件名的后缀名

            
            // 创建宽高信息的文本图层
            var textLayer = app.activeDocument.artLayers.add();
            textLayer.kind = LayerKind.TEXT;
            textLayer.textItem.contents = 宽高信息;
            textLayer.textItem.size = 10;
            textLayer.textItem.position = [currentDocument.width / 2, currentDocument.height / 2];

            // 修改文本颜色为M90
            var textColor = new SolidColor();
            textColor.rgb.red = 230;
            textColor.rgb.green = 46;
            textColor.rgb.blue = 139;
            textLayer.textItem.color = textColor;
            // 创建文件名处理的文本图层
             栅格化文字()
            var textLayer2 = app.activeDocument.artLayers.add();
            textLayer2.kind = LayerKind.TEXT;
            textLayer2.textItem.contents = fileNameWithoutExtension;
            textLayer2.textItem.size = 60;
         
            var textColor2 = new SolidColor();
            textColor2.rgb.red = 230;
                 textColor2.rgb.green = 46;
                    textColor2.rgb.blue = 139;
                    textLayer2.textItem.color = textColor2;  
            
             textLayer2.textItem.position = [currentDocument.width / 2, currentDocument.height / 2];
                     栅格化文字()
                  自由变换向下1cm()                     
                    向下合并()
                    图层关闭()
        } else {
            // 处理没有文件信息的情况
            alert(文件信息);
        }
    }
}
app.activeDocument = 主文档;
alert("排版完成，请检查文件！！！")
   }

function 获取文件简介信息() {
    try {
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("property"), stringIDToTypeID("fileInfo"));
        r.putEnumerated(stringIDToTypeID("document"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));

        var fileInfoDescriptor = executeActionGet(r);
        if (fileInfoDescriptor.hasKey(stringIDToTypeID("fileInfo"))) {
            var fileInfoObject = fileInfoDescriptor.getObjectValue(stringIDToTypeID("fileInfo"));
         //   var 版权 = fileInfoObject.getString(stringIDToTypeID("copyrightNotice"));
            var 关键字列表 = fileInfoObject.getList(stringIDToTypeID("keywords"));
            var 关键字 = [];
            for (var i = 0; i < 关键字列表.count; i++) {
                关键字.push(关键字列表.getString(i));
            }
            var 描述 = fileInfoObject.getString(stringIDToTypeID("caption"));

            return {
                //版权: 版权,
                关键字: 关键字,
                描述: 描述
            };
        } else {
            return "没有文件简介信息";
        }
    } catch (e) {
        return "发生错误：" + e;
    }
}




function 栅格化文字()	//栅格化文字
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putEnumerated(stringIDToTypeID("what"), stringIDToTypeID("rasterizeItem"), stringIDToTypeID("type"));
        executeAction(stringIDToTypeID("rasterizeLayer"), d, DialogModes.NO);
    }



function 自由变换向下1cm()	//自由变换
    {
  
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putEnumerated(stringIDToTypeID("freeTransformCenterState"), stringIDToTypeID("quadCenterState"), stringIDToTypeID("QCSAverage"));
        var d1 = new ActionDescriptor();
        d1.putUnitDouble(stringIDToTypeID("horizontal"), stringIDToTypeID("distanceUnit"), 0);
        d1.putUnitDouble(stringIDToTypeID("vertical"), stringIDToTypeID("distanceUnit"), 60);
        d.putObject(stringIDToTypeID("offset"), stringIDToTypeID("offset"), d1);
        d.putEnumerated(charIDToTypeID("Intr"), stringIDToTypeID("interpolationType"), stringIDToTypeID("nearestNeighbor"));
        executeAction(stringIDToTypeID("transform"), d, DialogModes.NO);
 
    }

function 向下合并()	//向下合并
    {
   
        var d = new ActionDescriptor();
        executeAction(stringIDToTypeID("mergeLayersNew"), d, DialogModes.NO);
    
    }


function 图层关闭()	//
    {
   
        var d = new ActionDescriptor();
        var list = new ActionList();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        list.putReference(r);
        d.putList(stringIDToTypeID("null"), list);
        executeAction(stringIDToTypeID("hide"), d, DialogModes.NO);
      
 
    }




///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////




function 文档保存最新(前缀) {
    app.preferences.rulerUnits = Units.CM;

        var 主文档 = app.activeDocument;
        var 主文档路径 = 主文档.path;
        var 输出路径 = new Folder(主文档路径 + "/大货裁片");
    
        if (!输出路径.exists) {
            输出路径.create();
        }

    var 主文档名称 = 主文档.name;

    // 遍历当前打开的文档
    for (var i = 0; i < app.documents.length; i++) {
        try {
            var document = app.documents[i];
            var documentName = document.name;

            // 判断文档名称是否与主文档名称不相同
            // if (documentName !== 主文档名称) {
            // 设置当前文档为活动文档
            app.activeDocument = document;

            var 文件信息 = 获取文件简介信息();
            if (typeof 文件信息 === 'object') {
                var 关键字 = 文件信息.关键字;
                var 描述 = 文件信息.描述;

                if (描述) {
                    var 当前套数 = 描述; // 根据描述的实际数据进行修改
                    var 当前文档 = app.activeDocument;
                    var 文件名 = 当前文档.name;
                    var 去除扩展名的文件名 = 文件名.split('.').slice(0, -1).join('.');
                    var 文档高度厘米 = 当前文档.height.as("cm");
                    保存为带高度的TIF文件(当前文档, 文档高度厘米, 前缀, 输出路径, 当前套数);
                } else {
                    // 如果描述信息不存在，继续下一次循环
                    continue;
                }
            }
        } catch (error) {
            // 处理异常，可以在此处添加适当的错误处理逻辑
            // 并继续下一次循环
            continue;
        }
    }

    alert("所有文档已保存为 TIF 格式，并存储在裁片处理文件夹中。");
}

function 保存为带高度的TIF文件(文档, 高度厘米, 前缀, 输出路径,当前套数) {
    // 生成保存路径和文件名
    var 文件名 = 文档.name;
    var 去除扩展名的文件名 = 文件名.split('.').slice(0, -1).join('.');
    var tif文件名 = 前缀 +"-"+去除扩展名的文件名 +"-"+当前套数+ "_文档高度" + 高度厘米.toFixed(2) + "cm.tif";
    var tif文件路径 = 输出路径 + "/" + tif文件名;

    // 保存当前文档为 TIF 格式
    var tif选项 = new TiffSaveOptions();
    文档.saveAs(new File(tif文件路径), tif选项);
}


function 获取文件简介信息() {
  
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("property"), stringIDToTypeID("fileInfo"));
        r.putEnumerated(stringIDToTypeID("document"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));

        var fileInfoDescriptor = executeActionGet(r);
        if (fileInfoDescriptor.hasKey(stringIDToTypeID("fileInfo"))) {
            var fileInfoObject = fileInfoDescriptor.getObjectValue(stringIDToTypeID("fileInfo"));
         //   var 版权 = fileInfoObject.getString(stringIDToTypeID("copyrightNotice"));
            var 关键字列表 = fileInfoObject.getList(stringIDToTypeID("keywords"));
            var 关键字 = [];
            for (var i = 0; i < 关键字列表.count; i++) {
                关键字.push(关键字列表.getString(i));
            }
            var 描述 = fileInfoObject.getString(stringIDToTypeID("caption"));

            return {
                //版权: 版权,
                关键字: 关键字,
                描述: 描述
            };
        } else {
           return "没有文件简介信息";
        }
   
}







///////////////////////////////////////////////////////////////////////////////////////////////////






/////////////////////////////////////#############主函数设置花样组

 
function 设置花样组删除图层设置名称() {
	
app.activeDocument.suspendHistory("缩水修改", "设置花样组2()");

function 设置花样组2() {
   currentDocument = app.activeDocument;
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
      layerNames.push(layerName); // 将匹配到的图层名称添加到数组中
    }
  }

  // 输出匹配到的数值个数
  $.writeln("匹配到的数值个数：" + matchCount);

  // 如果没有匹配到图层，则显示提示框并中断执行
  if (matchCount === 0) {
   // alert("当前文档没有匹配的花样图层，请进行图层更名操作", "来自左威的提醒");
    return;
  }

  // 检查是否已存在含有"-大货裁片"的图层组
  var layerSets = currentDocument.layerSets;
  for (var k = 0; k < layerSets.length; k++) {
    var layerSet = layerSets[k];
   // if (layerSet.name.indexOf("-大货裁片") !== -1) {
     // existingPatternSet = true;
      break;
    }
  }

  // 如果已存在含有"-大货裁片"的图层组，则显示提示框并中断执行

  // 创建相应数量的图层组


  // 遍历当前打开的文档，除了主文档外
  for (var i = 0; i < app.documents.length; i++) {
    var document = app.documents[i];
    var documentName = document.name.replace(/\.[^.]+$/, ""); // Remove extension

    // 判断文档名称是否与主文档名称不相同
    if (documentName !== currentDocument.name.replace(/\.[^.]+$/, "")) {
      app.activeDocument = document;
      删除背景()
      修改图层名称(document, documentName);
    }
  }

  // 恢复主文档为活动文档
  app.activeDocument = currentDocument;
 // alert("花样设置成功!", "来自左威的提醒");
}

function 修改图层名称(document, documentName) {
  var currentDocument = document;

  for (var j = 0; j < currentDocument.layers.length; j++) {
    var layer = currentDocument.layers[j];
    var layerName = layer.name;
    var splitArray = layerName.split("_");
    var olddocumentName = documentName.split(".");
    var newlayerName =splitArray[2]
    var newdocumentName =olddocumentName [0]
  //    alert(splitArray)
    // 检查正则分割后的第二个数组是否为空
   if (newlayerName ===newdocumentName) {
      return; // 如果相同，则跳过当前图层，不执行操作
    }

    var newLayerName = layerName + "_" + documentName;
    layer.name = newLayerName;
   
  }
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




function 载入蒙版选区()	//载入选区
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

function 存储选区(name)	//存储选区
    {
 
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("channel"), stringIDToTypeID("selection"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putString(stringIDToTypeID("name"), name);
        executeAction(stringIDToTypeID("duplicate"), d, DialogModes.NO);
   
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

function 删除背景() {
    try {
        找到背景图层();
        删除图层()
    } catch (error) {
     //   alert("删除背景时出现错误：" + error);
    }
}





function 找到背景图层() {
    try {
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putName(stringIDToTypeID("layer"), "背景");
        d.putReference(stringIDToTypeID("null"), r);
        d.putBoolean(stringIDToTypeID("makeVisible"), false);
        var list = new ActionList();
        list.putInteger(2);
        d.putList(stringIDToTypeID("layerID"), list);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
    } catch (error) {
        throw "找到背景图层时出现错误：" + error;
    }
}

function 删除图层() {
    try {
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        var list = new ActionList();
        list.putInteger(2);
        d.putList(stringIDToTypeID("layerID"), list);
        executeAction(stringIDToTypeID("delete"), d, DialogModes.NO);
    } catch (error) {
        throw "删除图层时出现错误：" + error;
    }
}


/////////////////////////////////////#############主函数设置花样组




//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////




function 设置花样组2() {
	
app.activeDocument.suspendHistory("设置花样组", "设置花样组()");

}
function 设置花样组() {
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
      layerNames.push(layerName); // 将匹配到的图层名称添加到数组中
    }
  }

  // 输出匹配到的数值个数
  $.writeln("匹配到的数值个数：" + matchCount);

  // 如果没有匹配到图层，则显示提示框并中断执行
  if (matchCount === 0) {
   // alert("当前文档没有匹配的花样图层，请进行图层更名操作", "来自左威的提醒");
    return;
  }

  // 检查是否已存在含有"-大货裁片"的图层组
  var layerSets = currentDocument.layerSets;
  for (var k = 0; k < layerSets.length; k++) {
    var layerSet = layerSets[k];
    if (layerSet.name.indexOf("-大货裁片") !== -1) {
      existingPatternSet = true;
      break;
    }
  }

  // 如果已存在含有"-大货裁片"的图层组，则显示提示框并中断执行
  if (existingPatternSet) {
   // alert("当前文档已设置花样组，请勿重复设置", "来自左威的提醒");
    return;
  }

  // 创建相应数量的图层组
  for (var i = 0; i < matchCount; i++) {
    var newLayerSet = currentDocument.layerSets.add();
    newLayerSet.name = "P" + (i + 1) + "-大货裁片";
  }

//alert("大货裁片组创建成功")
}









    function 右上对齐2() {
        
    app.activeDocument.suspendHistory("右上对齐", "右上对齐()");
}
 
 
 function 右上对齐() {
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
获取右上的坐标y坐标信息 = 获取右上的坐标.top;
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
获取右上的坐标裁片位置坐标y=获取右上的坐标裁片位置坐标.top

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