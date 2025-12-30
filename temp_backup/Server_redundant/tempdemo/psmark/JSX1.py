# -*- coding: utf-8 -*-

dxf_jscode = """




/////////////////////////////////////#############主函数设置花样组

function 设置花样组2() {
	
app.activeDocument.suspendHistory("设置花样组", "设置花样组()");

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
    alert("当前文档没有匹配的花样图层，请进行图层更名操作", "来自左威的提醒");
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
    alert("当前文档已设置花样组，请勿重复设置", "来自左威的提醒");
    return;
  }

  // 创建相应数量的图层组
  for (var i = 0; i < matchCount; i++) {
    var newLayerSet = currentDocument.layerSets.add();
    newLayerSet.name = "P" + (i + 1) + "-大货裁片";
  }

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

}
/////////////////////////////////////#############主函数设置花样组




 /////////////////////////////////////#############主函数裁片吸取 

function 裁片吸取2() {
	
	app.activeDocument.suspendHistory("裁片吸取", "裁片吸取()")
}

function 裁片吸取() {



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
  // 在这里继续执行下面的代码
  // ...



var 主文档 = app.activeDocument;
var 主文档名称 = 主文档.name;

// 遍历当前打开的文档
for (var i = 0; i < app.documents.length; i++) {
  var document = app.documents[i];
  var documentName = document.name;

  // 判断文档名称是否与主文档名称不相同
  if (documentName !== 主文档名称) {
    app.activeDocument = document;
    遍历图层();
  }
}

function 遍历图层() {
  var layerNames = []; // 用于存储图层名称的数组
  var currentDocument = app.activeDocument;

  for (var j = 0; j < currentDocument.layers.length; j++) {
    var layer = currentDocument.layers[j];
    var layerName = layer.name;
    
    // 检查图层名称前缀是否已存在于数组中，如果是，则跳过当前图层
    if (startsWithDuplicatePrefix(layerNames, layerName)) {
      continue;
    }
    
    layerNames.push(layerName);
  }

  // 逐个处理图层
  for (var k = 0; k < layerNames.length; k++) {
    var 当前图层名称 = layerNames[k];
   $.writeln("图层名称：" + 当前图层名称);
    
    var 裁片 = currentDocument.layers.getByName(当前图层名称);
    currentDocument.activeLayer = 裁片;
    裁片.copy();
    app.activeDocument = 主文档
    var 主文档裁片名称 = 当前图层名称.split("-")[0];
 try {
  var 主文档裁片 = 主文档.layers.getByName(主文档裁片名称);
} catch (e) {
  // 处理异常情况
  //alert("无法找到指定的主文档裁片：" + 主文档裁片名称);
  return; // 或者执行其他适当的操作
}

    
     var targetLayerSet = getExistingLayerSet(主文档, 主文档裁片名称 + "大货裁片");

    // 如果图层组不存在，则创建新的图层组
   
     //targetLayerSet = 主文档.layerSets.add();
     组名= 主文档裁片名称 + "-大货裁片";
    //  targetLayerSet.name = 组名
     app.activeDocument.activeLayer = 主文档裁片;
     // 载入蒙版选区()
  //这个代码用上就会影响速度
   //activeDocument.selection.load (activeDocument.channels.getByName(主文档裁片名称))  
   // 载入选区();
    粘贴图层();
    
    var 裁片名称 = 当前图层名称.split("_");
    if (裁片名称.length > 1) {
      var 角度信息 = 裁片名称[1];
      
 if (角度信息 === "180" || 角度信息 === "-180") {
        自由变换()
        } else if (角度信息 === "-90") {
            逆时针90旋转()
           
        } else if (角度信息 === "90") {
          
             顺时针90旋转()
        } else {
            // 如果以上条件都不满足，则执行默认的代码
        }

var 当前图层 = app.activeDocument.activeLayer;

初始化模板裁片名称 = 当前图层名称.split("-");
初始化码数裁片名称 = 当前图层名称.split("_");
实际模板裁片名称 = 初始化模板裁片名称[0]+"-"+初始化码数裁片名称[2]
修改图层名称(当前图层,  实际模板裁片名称); 
        // 在这里添加处理图层的代码
        
try {
  var doc = app.activeDocument;
  var targetLayerSet = doc.layerSets.getByName(组名); // 指定的图层组名称
  
  // 在这里处理图层组存在的情况
  
} catch (e) {
  // 处理异常情况
  alert("找不到指定的大货裁片组: " );
  
  if (shouldAbortOnError) {
    return; // 根据条件判断中断代码执行
  }
}

// 继续执行其他操作
// ...


// 将当前图层移动到目标组中
var currentLayer = doc.activeLayer;
currentLayer.move(targetLayerSet, ElementPlacement.INSIDE);
 

    }
    
    app.activeDocument = currentDocument; // 将 app.activeDocument 重置为 currentDocument
    
  }
}

app.activeDocument = 主文档
//alert("裁片吸取成功", "来自左威的提醒");

} else {
  // 如果没有找到匹配的图层组，退出程序
 // alert("当前文档没有匹配的大货裁片组，请先设置大货裁片组！！！")
}
}



function getExistingLayerSet(document, layerSetName) {
  var existingLayerSet = null;
  var layerSets = document.layerSets;
  
  for (var i = 0; i < layerSets.length; i++) {
    var layerSet = layerSets[i];
    
    if (layerSet.name === layerSetName) {
      existingLayerSet = layerSet;
      break;
    }
  }
  
  return existingLayerSet;
}


// 检查数组中是否存在以指定前缀开头的字符串
function startsWithDuplicatePrefix(array, str) {
  var prefix = str.split("-")[0]; // 获取以"-"分隔的前缀部分
  for (var i = 0; i < array.length; i++) {
    if (array[i].indexOf(prefix) === 0) {
      return true;
    }
  }
  return false;
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

function 粘贴图层()	//粘贴图层
    {
  
        var d = new ActionDescriptor();
        executeAction(stringIDToTypeID("paste"), d, DialogModes.NO);
    
    }




function 旋转()	//自由变换
    {
  
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putEnumerated(stringIDToTypeID("freeTransformCenterState"), stringIDToTypeID("quadCenterState"), stringIDToTypeID("QCSAverage"));
        var d1 = new ActionDescriptor();
        d1.putUnitDouble(stringIDToTypeID("horizontal"), stringIDToTypeID("distanceUnit"), 0);
        d1.putUnitDouble(stringIDToTypeID("vertical"), stringIDToTypeID("distanceUnit"), 0);
        d.putObject(stringIDToTypeID("offset"), stringIDToTypeID("offset"), d1);
        d.putUnitDouble(stringIDToTypeID("width"), stringIDToTypeID("percentUnit"), -100);
        d.putUnitDouble(stringIDToTypeID("height"), stringIDToTypeID("percentUnit"), -100);
        d.putBoolean(stringIDToTypeID("linked"), true);
        d.putEnumerated(charIDToTypeID("Intr"), stringIDToTypeID("interpolationType"), stringIDToTypeID("nearestNeighbor"));
        executeAction(stringIDToTypeID("transform"), d, DialogModes.NO);
    
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





// 修改图层名称
function 修改图层名称(layer, newName) {
  if (layer && layer.name !== newName) {
    layer.name = newName;
  }
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


function select_21902465820313()	//
    {
  
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putOffset(stringIDToTypeID("historyState"), -3);
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
    
  
    }
    
 /////////////////////////////////////#############主函数裁片吸取 
    
    
    
 /////////////////////////////////////#############主函数裁片放置
 
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
        应用图层蒙版();
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
        历史记录回退();
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
    alert("当前文档未设置大货裁片组！！！");
  }
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
  var currentLayer = currentDocument.activeLayer;

  if (currentLayer) {
    var bounds = currentLayer.bounds;
    var centerX = bounds[0] + (bounds[2] - bounds[0]) / 2;
    var centerY = bounds[1] + (bounds[3] - bounds[1]) / 2;

    return {
      layerName: currentLayer.name,
      centerX: centerX,
      centerY: centerY
    };
  } else {
    $.writeln("没有当前图层。");
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








 /////////////////////////////////////#############主函数裁片放置



////////////////通码延伸 
    



function 裁片射出() {
 主文档 = app.activeDocument;
var 主文档名称 = 主文档.name;

// 遍历当前打开的文档
for (var i = 0; i < app.documents.length; i++) {
  var document = app.documents[i];
  var documentName = document.name;

  // 判断文档名称是否与主文档名称不相同
  if (documentName !== 主文档名称) {
    app.activeDocument = document;
    遍历图层();
  }
}

function 遍历图层() {
  var layerNames = []; // 用于存储图层名称的数组
  var currentDocument = app.activeDocument;

  for (var j = 0; j < currentDocument.layers.length; j++) {
    var layer = currentDocument.layers[j];
    var layerName = layer.name;
    layerNames.push(layerName);
  }

  // 逐个处理图层
  for (var k = 0; k < layerNames.length; k++) {
    var 当前图层名称 = layerNames[k];
  //   $.writeln("图层名称：" + 当前图层名称);
   // alert(当前图层名称);

    var parts = 当前图层名称.split("-");
    if (parts.length > 0) {
      var 裁片名称 = parts[0];
      app.activeDocument = 主文档;
      $.writeln(裁片名称);
初始化模板裁片名称 = 当前图层名称.split("-");
初始化码数裁片名称 = 当前图层名称.split("_");
大货组名称 =初始化模板裁片名称[0]+("-大货裁片")
实际裁片名称 = 初始化模板裁片名称[0]+"-"+初始化码数裁片名称[2]
 $.writeln(大货组名称);
 $.writeln(实际裁片名称);
var 空白裁片模板 = app.activeDocument.layerSets.getByName(大货组名称).layers.getByName(实际裁片名称 );
   app.activeDocument.activeLayer = 空白裁片模板;

      载入选区();
      var 裁片 = app.activeDocument.layers.getByName(裁片名称);
      app.activeDocument.activeLayer = 裁片;
      添加图层蒙版()
      应用图层蒙版()
      裁片.copy();
      历史记录回退()
      app.activeDocument = currentDocument;
      图层选择(当前图层名称);
      载入选区();
      粘贴图层();
      
      取消选择();
     // app.refresh();


var 裁片名称 = 当前图层名称.split("_");
if (裁片名称.length > 1) {
  var 角度信息 = 裁片名称[1];
  
 if (角度信息 === "180" || 角度信息 === "-180") {
        旋转();
        } else if (角度信息 === "-90") {
            逆时针90旋转()
           
        } else if (角度信息 === "90") {
          
             顺时针90旋转()
        } else {
            // 如果以上条件都不满足，则执行默认的代码
        }





}

    }
  }

烧花线添加()//alert("当前码拍好")///////////////////////////////////这里可以填写添加烧花线函数

}
//alert("排版完成，请检查文件！！！")
app.activeDocument = 主文档;


function 粘贴图层()	//粘贴图层
    {
   
        var d = new ActionDescriptor();
        executeAction(stringIDToTypeID("paste"), d, DialogModes.NO);
  
  
    }



function 复制图层()	//复制图层
    {
  
        var d = new ActionDescriptor();
        executeAction(stringIDToTypeID("copyEvent"), d, DialogModes.NO);
   
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


function 取消选择()	//取消选择
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("channel"), stringIDToTypeID("selection"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putEnumerated(stringIDToTypeID("to"), stringIDToTypeID("ordinal"), stringIDToTypeID("none"));
        executeAction(stringIDToTypeID("set"), d, DialogModes.NO);
   
    }

function 图层选择(当前图层名称)	//
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putName(stringIDToTypeID("layer"), 当前图层名称);
        d.putReference(stringIDToTypeID("null"), r);
        d.putBoolean(stringIDToTypeID("makeVisible"), false);
        var list = new ActionList();
        list.putInteger(6);
        d.putList(stringIDToTypeID("layerID"), list);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
     
    }



function 自由变换()	//自由变换
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putEnumerated(stringIDToTypeID("freeTransformCenterState"), stringIDToTypeID("quadCenterState"), stringIDToTypeID("QCSAverage"));
        var d1 = new ActionDescriptor();
        d1.putUnitDouble(stringIDToTypeID("horizontal"), stringIDToTypeID("distanceUnit"), 0);
        d1.putUnitDouble(stringIDToTypeID("vertical"), stringIDToTypeID("distanceUnit"), 0);
        d.putObject(stringIDToTypeID("offset"), stringIDToTypeID("offset"), d1);
        d.putUnitDouble(stringIDToTypeID("width"), stringIDToTypeID("percentUnit"), -100);
        d.putUnitDouble(stringIDToTypeID("height"), stringIDToTypeID("percentUnit"), -100);
        d.putBoolean(stringIDToTypeID("linked"), true);
        d.putEnumerated(charIDToTypeID("Intr"), stringIDToTypeID("interpolationType"), stringIDToTypeID("nearestNeighbor"));
        executeAction(stringIDToTypeID("transform"), d, DialogModes.NO);
   
    }




function 选择上一图层()	//
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("forwardEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putBoolean(stringIDToTypeID("makeVisible"), false);
        var list = new ActionList();
        list.putInteger(8);
        d.putList(stringIDToTypeID("layerID"), list);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
      
   
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


function 应用图层蒙版()	//应用图层蒙版
    {
    
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("channel"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putBoolean(stringIDToTypeID("apply"), true);
        executeAction(stringIDToTypeID("delete"), d, DialogModes.NO);
    
    }


function 拼合所有蒙版()	//拼合所有蒙版
    {
    
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("document"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("e805a6ee-6d75-4b62-b6fe-f5873b5fdf20"), d, DialogModes.NO);
     
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



function 历史记录回退()	//
    {
  
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putOffset(stringIDToTypeID("historyState"), -5);
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);

    }






function 烧花线添加() {
	
app.activeDocument.suspendHistory("烧花线添加", "烧花线()");


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
 画布大小(); 
 var layer = app.activeDocument.activeLayer;
layer.name = "底图";
恢复默认颜色()
矩形选框像素点()
//色彩范围()
填充();
 魔棒烧花线()
新建图层()
var layer2 = app.activeDocument.activeLayer;
layer2.name = "剪口";
扩展2();
恢复止口线默认颜色()
填充();
矩形选框准备删除()
清除();
魔棒();
扩展();
选择反向();
清除();
 var 底图 =  app.activeDocument.layers.getByName( "底图");
 app.activeDocument.activeLayer=底图;
矩形选框准备删除()
清除();
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

function 恢复止口线默认颜色()	//取消选择
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




function 合并图层()	//合并图层
    {
  
        var d = new ActionDescriptor();
        executeAction(stringIDToTypeID("mergeLayersNew"), d, DialogModes.NO);
    
    }



function 恢复默认颜色()	//
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("color"), stringIDToTypeID("colors"));
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("reset"), d, DialogModes.NO);
  
  
    }


function 魔棒烧花线()	//魔棒
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("channel"), stringIDToTypeID("selection"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        d1.putUnitDouble(stringIDToTypeID("horizontal"), stringIDToTypeID("distanceUnit"), 0);
        d1.putUnitDouble(stringIDToTypeID("vertical"), stringIDToTypeID("distanceUnit"), 0);
        d.putObject(stringIDToTypeID("to"), stringIDToTypeID("point"), d1);
        d.putInteger(stringIDToTypeID("tolerance"), 6);
        d.putBoolean(stringIDToTypeID("contiguous"), false);
        executeAction(stringIDToTypeID("set"), d, DialogModes.NO);
    
    }
function 矩形选框像素点()	//矩形选框
    {
    
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("channel"), stringIDToTypeID("selection"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        d1.putUnitDouble(stringIDToTypeID("top"), stringIDToTypeID("distanceUnit"), 0);
        d1.putUnitDouble(stringIDToTypeID("left"), stringIDToTypeID("distanceUnit"), 0);
        d1.putUnitDouble(stringIDToTypeID("bottom"), stringIDToTypeID("distanceUnit"), 0.48);
        d1.putUnitDouble(stringIDToTypeID("right"), stringIDToTypeID("distanceUnit"), 0.48);
        d.putObject(stringIDToTypeID("to"), stringIDToTypeID("rectangle"), d1);
        executeAction(stringIDToTypeID("set"), d, DialogModes.NO);
    
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
        d.putUnitDouble(stringIDToTypeID("width"), stringIDToTypeID("distanceUnit"), 40);
        d.putUnitDouble(stringIDToTypeID("height"), stringIDToTypeID("distanceUnit"), 40);
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
        d1.putUnitDouble(stringIDToTypeID("horizontal"), stringIDToTypeID("pixelsUnit"), 3);
        d1.putUnitDouble(stringIDToTypeID("vertical"), stringIDToTypeID("pixelsUnit"), 3);
        d.putObject(stringIDToTypeID("to"), stringIDToTypeID("point"), d1);
        d.putInteger(stringIDToTypeID("tolerance"), 6);
        executeAction(stringIDToTypeID("set"), d, DialogModes.NO);
     
    }

function 矩形选框准备删除()	//矩形选框
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("channel"), stringIDToTypeID("selection"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        d1.putUnitDouble(stringIDToTypeID("top"), stringIDToTypeID("distanceUnit"), 0);
        d1.putUnitDouble(stringIDToTypeID("left"), stringIDToTypeID("distanceUnit"), 0);
        d1.putUnitDouble(stringIDToTypeID("bottom"), stringIDToTypeID("distanceUnit"), 0.96);
        d1.putUnitDouble(stringIDToTypeID("right"), stringIDToTypeID("distanceUnit"), 0.96);
        d.putObject(stringIDToTypeID("to"), stringIDToTypeID("rectangle"), d1);
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
         app.activeDocument.selection.clear();

   
    }


function 图层样式()	//图层样式
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("property"), stringIDToTypeID("layerEffects"));
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        d1.putUnitDouble(stringIDToTypeID("scale"), stringIDToTypeID("percentUnit"), 12);
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
}

}    
    
 ///////////////////////////////////////   删除指定名称蒙版主函数体
    
function 删除指定名称蒙版() {
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
       选择蒙版();
       删除图层蒙版()
  }
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



function 删除图层蒙版()	//删除图层蒙版
    {
  
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("channel"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("delete"), d, DialogModes.NO);
   
    }    
    
    
     ///////////////////////////////////////   删除指定名称蒙版主函数体
     
     
     ///////////////////////////////////////   信息写入主函数体
       
function 信息写入() {
    app.activeDocument.suspendHistory("信息写入", "信息写入2()");
}

function 信息写入2() {
    // 修改后的遍历图层代码
    app.preferences.rulerUnits = Units.MM; // 修改指定单位为毫米
    var currentDocument = app.activeDocument;
    var layerNames = []; // 保存匹配到的图层名称的数组

    // 遍历图层
    for (var j = 0; j < currentDocument.layers.length; j++) {
        var layer = currentDocument.layers[j];
        var layerName = layer.name;

        // 检查图层名称是否以P开头并且后面跟着数字
        if (/^P\d+$/.test(layerName)) {
            layerNames.push(layerName); // 将匹配到的图层名称添加到数组中
        }
    }

    // 创建一个新的图层组来保存信息
    var infoGroup = currentDocument.layerSets.add();
    infoGroup.name = "图层基础信息";

    // 遍历匹配到的图层，输出宽度和高度，并创建图层保存信息
    for (var i = 0; i < layerNames.length; i++) {
        var 当前裁片名称 = layerNames[i];
        var 裁片 = app.activeDocument.layers.getByName(当前裁片名称);
        app.activeDocument.activeLayer = 裁片;
        载入蒙版选区();
        var 选区尺寸 = 获取当前选区宽高();

        // 检查是否有有效选区，并输出宽度和高度
        if (选区尺寸.宽度 !== undefined && 选区尺寸.高度 !== undefined) {
            // 输出宽度和高度
            $.writeln("选区宽度：" + 选区尺寸.宽度 + " 毫米");
            $.writeln("选区高度：" + 选区尺寸.高度 + " 毫米");

            // 创建文本图层，并将宽度和高度信息写入图层
            var textLayer = infoGroup.artLayers.add();
            var 当前图层=app.activeDocument.activeLayer 
            当前图层.name=当前裁片名称 + "_" + 选区尺寸.宽度 + "_" + 选区尺寸.高度 ;
        } else {
            $.writeln("当前没有有效选区。");
        }
    }
}


function 载入蒙版选区()	//载入选区
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("channel"), stringIDToTypeID("selection"));
        d.putReference(stringIDToTypeID("null"), r);
        var r1 = new ActionReference();
        r1.putEnumerated(stringIDToTypeID("channel"), stringIDToTypeID("channel"), stringIDToTypeID("mask"));
        d.putReference(stringIDToTypeID("to"), r1);
        executeAction(stringIDToTypeID("set"), d, DialogModes.NO);
      
    }

function 获取当前选区宽高() {
  app.preferences.rulerUnits = Units.MM; // 修改指定单位为毫米

  // 获取当前的活动文档
  var currentDocument = app.activeDocument;

  // 获取当前的选区
  var currentSelection = currentDocument.selection;

  // 检查是否有有效选区
  if (currentSelection !== null && !currentSelection.bounds.isNull) {
    // 获取选区的边界坐标
    var bounds = currentSelection.bounds;

    // 计算选区的宽度和高度并保留两位小数
    var selectionWidth = parseFloat(bounds[2] - bounds[0]).toFixed(2);
    var selectionHeight = parseFloat(bounds[3] - bounds[1]).toFixed(2);

    // 返回选区的宽度和高度
    return { 宽度: selectionWidth, 高度: selectionHeight };
  } else {
    // 返回空对象表示当前没有有效选区
    return {};
  }
}
    
      ///////////////////////////////////////   信息写入主函数体
      
      
       ///////////////////////////////////////   裁片射出缩放主函数体
      
      
      



function 裁片射出缩放() {
app.preferences.rulerUnits = Units.PIXELS
var 主文档 = app.activeDocument;
var 主文档名称 = 主文档.name;

// 遍历当前打开的文档
for (var i = 0; i < app.documents.length; i++) {
  var document = app.documents[i];
  var documentName = document.name;

  // 判断文档名称是否与主文档名称不相同
  if (documentName !== 主文档名称) {
    app.activeDocument = document;
    遍历图层();
  }
}

function 遍历图层() {
  var layerNames = []; // 用于存储图层名称的数组
  var currentDocument = app.activeDocument;

  for (var j = 0; j < currentDocument.layers.length; j++) {
    var layer = currentDocument.layers[j];
    var layerName = layer.name;
    layerNames.push(layerName);
  }

  // 逐个处理图层
  for (var k = 0; k < layerNames.length; k++) {
    var 当前图层名称 = layerNames[k];
  //   $.writeln("图层名称：" + 当前图层名称);
   // alert(当前图层名称);

    var parts = 当前图层名称.split("-");
    if (parts.length > 0) {
      var 裁片名称 = parts[0];
      app.activeDocument = 主文档;
      $.writeln(裁片名称);
初始化模板裁片名称 = 当前图层名称.split("-");
初始化码数裁片名称 = 当前图层名称.split("_");
大货组名称 =初始化模板裁片名称[0]+("-大货裁片")
实际裁片名称 = 初始化模板裁片名称[0]+"-"+初始化码数裁片名称[2]
 $.writeln(大货组名称);
 $.writeln(实际裁片名称);
var 空白裁片模板 = app.activeDocument.layerSets.getByName(大货组名称).layers.getByName(实际裁片名称 );
   app.activeDocument.activeLayer = 空白裁片模板;
  载入选区()

      var 边距 = 获取当前选区四边距();
      var 当前选区高度=边距.bottom-边距.top
      var 当前选区宽度=边距.right-边距.left
      var 高度转毫米 = pixelsToMillimeters(当前选区高度);
      var 宽度转毫米 = pixelsToMillimeters(当前选区宽度);
      
      
      选择反向()
      
      var 裁片缩放定位点 = app.activeDocument.layers.getByName("缩放定位点");
        app.activeDocument.activeLayer = 裁片缩放定位点;
        
      
      清除()
      
      

 var 搜索词 = 裁片名称;
var 匹配图层数组 = 匹配图层名(搜索词);

// 显示匹配的图层列表
if (匹配图层数组.length > 0) {
  var 图层列表文本 = "匹配的图层列表：";
  for (var i = 0; i < 匹配图层数组.length; i++) {
    if (i !== 0) {
      图层列表文本 += " ";
    }
    图层列表文本 += 匹配图层数组[i].name;
  }
         var  数据解析分割=图层列表文本.split("_");
     //var 实际套花名称=名称部分[0]
       var 基码图层宽度 = parseFloat(数据解析分割[1]);
        var 基码图层高度 = parseFloat(数据解析分割[2]);
        var 缩放比例=高度转毫米/基码图层高度*100

 //    alert(基码图层宽度);
    } else {
      alert("没有找到匹配的图层。");
    }




      /*
       $.writeln("上边距：" + 边距.top);
      $.writeln("左边距：" + 边距.left);
      $.writeln("下边距：" + 边距.bottom);
      $.writeln("右边距：" + 边距.right);
      */8
    // 示例用法：
var 毫米 = 300;
var 每英寸像素数 = app.activeDocument.resolution; // 获取当前文档的分辨率（每英寸像素数）
var 扩展像素 = 毫米转像素(毫米, 每英寸像素数);     

var   裁切上边距= 边距.top-扩展像素
var   裁切左边距= 边距.left-扩展像素
var   裁切下边距=  边距.bottom+扩展像素
var   裁切右边距=  边距.right+扩展像素
     $.writeln(裁切上边距);
     $.writeln(裁切左边距);
   $.writeln(裁切下边距);
    $.writeln(裁切右边距);
裁切图层(裁切上边距,裁切左边距,裁切下边距,裁切右边距)

var 裁片缩放定位点 = app.activeDocument.layers.getByName("缩放定位点");
        app.activeDocument.activeLayer = 裁片缩放定位点;
        载入选区()
var 缩放定位点的中心坐标=获取当前缩放定位点选区四边距()
var 缩放定位点的Y轴坐标=缩放定位点的中心坐标.top2
var 缩放定位点的X轴坐标=缩放定位点的中心坐标.left2
    $.writeln("Y轴中心坐标"+缩放定位点的Y轴坐标);
$.writeln("X轴中心坐标"+缩放定位点的X轴坐标);

  var 裁片 = app.activeDocument.layers.getByName(裁片名称);
      app.activeDocument.activeLayer = 裁片
//var 空白裁片模板 = app.activeDocument.layerSets.getByName(大货组名称).layers.getByName(实际裁片名称 );
   //app.activeDocument.activeLayer = 空白裁片模板;
   取消选择()
      图层按照缩放定位点进行缩放(缩放定位点的X轴坐标,缩放定位点的Y轴坐标,缩放比例)

    //  var 裁片 = app.activeDocument.layers.getByName(裁片名称);
     // app.activeDocument.activeLayer = 裁片;

     var 空白裁片模板 = app.activeDocument.layerSets.getByName(大货组名称).layers.getByName(实际裁片名称 );
  app.activeDocument.activeLayer = 空白裁片模板;
      载入选区()
var 裁片 = app.activeDocument.layers.getByName(裁片名称);
      app.activeDocument.activeLayer = 裁片
      添加图层蒙版()
      应用图层蒙版()
      裁片.copy();
      历史记录回退()
      app.activeDocument = currentDocument;
      图层选择(当前图层名称);
      载入选区();
      粘贴图层();

      取消选择();
     // app.refresh();


var 裁片名称 = 当前图层名称.split("_");
if (裁片名称.length > 1) {
  var 角度信息 = 裁片名称[1];

 if (角度信息 === "180" || 角度信息 === "-180") {
        自由变换()
        } else if (角度信息 === "-90") {
            逆时针90旋转()
           
        } else if (角度信息 === "90") {
          
             顺时针90旋转()
        } else {
            // 如果以上条件都不满足，则执行默认的代码
        }


//历史记录回退缩放函数()
}
   app.activeDocument = 主文档;
历史记录回退缩放函数()
    }


  }
 app.activeDocument = currentDocument;
烧花线添加()//alert("当前码拍好")///////////////////////////////////这里可以填写添加烧花线函数

}
//alert("排版完成，请检查文件！！！")
app.activeDocument = 主文档;
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




// 搜索并处理图层名的函数
function 匹配图层名(搜索词) {
  // 获取指定图层组中的所有图层
  function 获取组中所有图层(组) {
    var 图层数组 = [];
    var 图层组中图层 = 组.layers;

    for (var i = 0; i < 图层组中图层.length; i++) {
      var 图层 = 图层组中图层[i];
      图层数组.push(图层);
      if (图层.typename === "LayerSet") {
        var 子图层 = 获取组中所有图层(图层);
        图层数组 = 图层数组.concat(子图层);
      }
    }

    return 图层数组;
  }

  // 获取指定名称的图层组
  function 根据名称获取图层组(文档, 组名称) {
    var 组 = null;
    var 所有图层 = 文档.layers;

    for (var i = 0; i < 所有图层.length; i++) {
      var 图层 = 所有图层[i];
      if (图层.typename === "LayerSet" && 图层.name === 组名称) {
        组 = 图层;
        break;
      }
    }

    return 组;
  }

  var 文档 = app.activeDocument;
  var 组名称 = "图层基础信息"; // 指定要匹配的图层组名称
  var 组 = 根据名称获取图层组(文档, 组名称);

  if (组) {
    var 图层数组 = 获取组中所有图层(组);
    var 模糊匹配图层数组 = [];

    // 首先进行模糊匹配
    for (var i = 0; i < 图层数组.length; i++) {
      var 图层 = 图层数组[i];
      if (图层.name.indexOf(搜索词) !== -1) {
        模糊匹配图层数组.push(图层);
      }
    }

    // 在模糊匹配结果中进行图层基础信息数组分割过滤
    var 精确匹配图层数组 = [];
    for (var j = 0; j < 模糊匹配图层数组.length; j++) {
      var 模糊匹配图层 = 模糊匹配图层数组[j];
      // 进行图层基础信息数组分割过滤
      var 图层基础信息数组 = 模糊匹配图层.name.split("_"); // 假设分割符是 "_"
      if (图层基础信息数组[0] === 搜索词) {
        精确匹配图层数组.push(模糊匹配图层);
      }
    }

    // 返回匹配的图层数组
    return 精确匹配图层数组;
  } else {
    alert('未找到名为"' + 组名称 + '"的图层组。');
    return [];
  }
}




function 毫米转像素(毫米, 每英寸像素数) {
  var 每英寸毫米数 = 25.4;
  var 英寸 = 毫米 / 每英寸毫米数;
  return Math.round(英寸 * 每英寸像素数);
}

function 图层按照缩放定位点进行缩放(缩放定位点的X轴坐标,缩放定位点的Y轴坐标,缩放比例)	//自由变换
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putEnumerated(stringIDToTypeID("freeTransformCenterState"), stringIDToTypeID("quadCenterState"), stringIDToTypeID("QCSIndependent"));
        var d1 = new ActionDescriptor();  
        d1.putUnitDouble(stringIDToTypeID("horizontal"), stringIDToTypeID("pixelsUnit"), 缩放定位点的X轴坐标);
        d1.putUnitDouble(stringIDToTypeID("vertical"), stringIDToTypeID("pixelsUnit"), 缩放定位点的Y轴坐标);
        d.putObject(stringIDToTypeID("position"), stringIDToTypeID("point"), d1);
        var d2 = new ActionDescriptor();
        d2.putUnitDouble(stringIDToTypeID("horizontal"), stringIDToTypeID("pixelsUnit"), 0);
        d2.putUnitDouble(stringIDToTypeID("horizontal"), stringIDToTypeID("pixelsUnit"), 0);
        d2.putUnitDouble(stringIDToTypeID("vertical"), stringIDToTypeID("pixelsUnit"), 0);
        d.putObject(stringIDToTypeID("offset"), stringIDToTypeID("offset"), d2);
        d.putUnitDouble(stringIDToTypeID("width"), stringIDToTypeID("percentUnit"), 缩放比例);
        d.putUnitDouble(stringIDToTypeID("height"), stringIDToTypeID("percentUnit"), 缩放比例);
        d.putBoolean(stringIDToTypeID("linked"), true);
        d.putEnumerated(charIDToTypeID("Intr"), stringIDToTypeID("interpolationType"), stringIDToTypeID("nearestNeighbor"));
        executeAction(stringIDToTypeID("transform"), d, DialogModes.NO);
        }


function 裁切图层(裁切上边距,裁切左边距,裁切下边距,裁切右边距)	//
    {

        var d = new ActionDescriptor();
        var d1 = new ActionDescriptor();
        d1.putUnitDouble(stringIDToTypeID("top"), stringIDToTypeID("pixelsUnit"), 裁切上边距);
        d1.putUnitDouble(stringIDToTypeID("left"), stringIDToTypeID("pixelsUnit"), 裁切左边距);
        d1.putUnitDouble(stringIDToTypeID("bottom"), stringIDToTypeID("pixelsUnit"),裁切下边距);
        d1.putUnitDouble(stringIDToTypeID("right"), stringIDToTypeID("pixelsUnit"), 裁切右边距);
        d.putObject(stringIDToTypeID("to"), stringIDToTypeID("rectangle"), d1);
        d.putUnitDouble(stringIDToTypeID("angle"), stringIDToTypeID("angleUnit"), 0);
        d.putBoolean(stringIDToTypeID("delete"), true);
        d.putEnumerated(stringIDToTypeID("cropAspectRatioModeKey"), stringIDToTypeID("cropAspectRatioModeClass"), stringIDToTypeID("pureAspectRatio"));
        d.putBoolean(stringIDToTypeID("constrainProportions"), false);
        executeAction(stringIDToTypeID("crop"), d, DialogModes.NO);

    }





   function 获取当前缩放定位点选区四边距() {
  var currentDocument = app.activeDocument;
        var selectionBounds = currentDocument.selection.bounds;

  var top2 = selectionBounds[1].value;
  var left2 = selectionBounds[0].value;
  var bottom2 = selectionBounds[3].value;
  var right2 = selectionBounds[2].value;

  return {
    top2: top2,
    left2: left2,
    bottom2: bottom2,
    right2: right2
  };
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

function 历史记录回退缩放函数()	//
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putOffset(stringIDToTypeID("historyState"), -7   );
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);

    }



function 粘贴图层()	//粘贴图层
    {

        var d = new ActionDescriptor();
        executeAction(stringIDToTypeID("paste"), d, DialogModes.NO);


    }



function 复制图层()	//复制图层
    {

        var d = new ActionDescriptor();
        executeAction(stringIDToTypeID("copyEvent"), d, DialogModes.NO);

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


function 取消选择()	//取消选择
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("channel"), stringIDToTypeID("selection"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putEnumerated(stringIDToTypeID("to"), stringIDToTypeID("ordinal"), stringIDToTypeID("none"));
        executeAction(stringIDToTypeID("set"), d, DialogModes.NO);

    }

function 图层选择(当前图层名称)	//
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putName(stringIDToTypeID("layer"), 当前图层名称);
        d.putReference(stringIDToTypeID("null"), r);
        d.putBoolean(stringIDToTypeID("makeVisible"), false);
        var list = new ActionList();
        list.putInteger(6);
        d.putList(stringIDToTypeID("layerID"), list);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);

    }



function 自由变换()	//自由变换
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putEnumerated(stringIDToTypeID("freeTransformCenterState"), stringIDToTypeID("quadCenterState"), stringIDToTypeID("QCSAverage"));
        var d1 = new ActionDescriptor();
        d1.putUnitDouble(stringIDToTypeID("horizontal"), stringIDToTypeID("distanceUnit"), 0);
        d1.putUnitDouble(stringIDToTypeID("vertical"), stringIDToTypeID("distanceUnit"), 0);
        d.putObject(stringIDToTypeID("offset"), stringIDToTypeID("offset"), d1);
        d.putUnitDouble(stringIDToTypeID("width"), stringIDToTypeID("percentUnit"), -100);
        d.putUnitDouble(stringIDToTypeID("height"), stringIDToTypeID("percentUnit"), -100);
        d.putBoolean(stringIDToTypeID("linked"), true);
        d.putEnumerated(charIDToTypeID("Intr"), stringIDToTypeID("interpolationType"), stringIDToTypeID("nearestNeighbor"));
        executeAction(stringIDToTypeID("transform"), d, DialogModes.NO);

    }










function 选择上一图层()	//
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("forwardEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putBoolean(stringIDToTypeID("makeVisible"), false);
        var list = new ActionList();
        list.putInteger(8);
        d.putList(stringIDToTypeID("layerID"), list);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);


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






function 选择反向()	//选择反向
    {

        var d = new ActionDescriptor();
        executeAction(stringIDToTypeID("inverse"), d, DialogModes.NO);

    }


function 清除()	//清除
    {

       app.activeDocument.selection.clear();
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


function 拼合所有蒙版()	//拼合所有蒙版
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("document"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("e805a6ee-6d75-4b62-b6fe-f5873b5fdf20"), d, DialogModes.NO);

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



function 历史记录回退()	//
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putOffset(stringIDToTypeID("historyState"), -5);
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);

    }






function 烧花线添加() {
	
app.activeDocument.suspendHistory("烧花线添加", "烧花线()");


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
 画布大小(); 
 var layer = app.activeDocument.activeLayer;
layer.name = "底图";
恢复默认颜色()
矩形选框像素点()
//色彩范围()
填充();
 魔棒烧花线()
新建图层()
var layer2 = app.activeDocument.activeLayer;
layer2.name = "剪口";
扩展2();
恢复止口线默认颜色()
填充();
矩形选框准备删除()
清除();
魔棒();
扩展();
选择反向();
清除();
 var 底图 =  app.activeDocument.layers.getByName( "底图");
 app.activeDocument.activeLayer=底图;
矩形选框准备删除()
清除();
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

function 恢复止口线默认颜色()	//取消选择
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




function 合并图层()	//合并图层
    {
  
        var d = new ActionDescriptor();
        executeAction(stringIDToTypeID("mergeLayersNew"), d, DialogModes.NO);
    
    }



function 恢复默认颜色()	//
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("color"), stringIDToTypeID("colors"));
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("reset"), d, DialogModes.NO);
  
  
    }


function 魔棒烧花线()	//魔棒
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("channel"), stringIDToTypeID("selection"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        d1.putUnitDouble(stringIDToTypeID("horizontal"), stringIDToTypeID("distanceUnit"), 0);
        d1.putUnitDouble(stringIDToTypeID("vertical"), stringIDToTypeID("distanceUnit"), 0);
        d.putObject(stringIDToTypeID("to"), stringIDToTypeID("point"), d1);
        d.putInteger(stringIDToTypeID("tolerance"), 6);
        d.putBoolean(stringIDToTypeID("contiguous"), false);
        executeAction(stringIDToTypeID("set"), d, DialogModes.NO);
    
    }
function 矩形选框像素点()	//矩形选框
    {
    
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("channel"), stringIDToTypeID("selection"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        d1.putUnitDouble(stringIDToTypeID("top"), stringIDToTypeID("distanceUnit"), 0);
        d1.putUnitDouble(stringIDToTypeID("left"), stringIDToTypeID("distanceUnit"), 0);
        d1.putUnitDouble(stringIDToTypeID("bottom"), stringIDToTypeID("distanceUnit"), 0.48);
        d1.putUnitDouble(stringIDToTypeID("right"), stringIDToTypeID("distanceUnit"), 0.48);
        d.putObject(stringIDToTypeID("to"), stringIDToTypeID("rectangle"), d1);
        executeAction(stringIDToTypeID("set"), d, DialogModes.NO);
    
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
        d.putUnitDouble(stringIDToTypeID("by"), stringIDToTypeID("pixelsUnit"), 2);
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
        d.putUnitDouble(stringIDToTypeID("width"), stringIDToTypeID("distanceUnit"), 40);
        d.putUnitDouble(stringIDToTypeID("height"), stringIDToTypeID("distanceUnit"), 40);
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
        d1.putUnitDouble(stringIDToTypeID("horizontal"), stringIDToTypeID("pixelsUnit"), 3);
        d1.putUnitDouble(stringIDToTypeID("vertical"), stringIDToTypeID("pixelsUnit"), 3);
        d.putObject(stringIDToTypeID("to"), stringIDToTypeID("point"), d1);
        d.putInteger(stringIDToTypeID("tolerance"), 6);
        executeAction(stringIDToTypeID("set"), d, DialogModes.NO);
     
    }

function 矩形选框准备删除()	//矩形选框
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("channel"), stringIDToTypeID("selection"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        d1.putUnitDouble(stringIDToTypeID("top"), stringIDToTypeID("distanceUnit"), 0);
        d1.putUnitDouble(stringIDToTypeID("left"), stringIDToTypeID("distanceUnit"), 0);
        d1.putUnitDouble(stringIDToTypeID("bottom"), stringIDToTypeID("distanceUnit"), 0.96);
        d1.putUnitDouble(stringIDToTypeID("right"), stringIDToTypeID("distanceUnit"), 0.96);
        d.putObject(stringIDToTypeID("to"), stringIDToTypeID("rectangle"), d1);
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
         app.activeDocument.selection.clear();

   
    }


function 图层样式()	//图层样式
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("property"), stringIDToTypeID("layerEffects"));
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        d1.putUnitDouble(stringIDToTypeID("scale"), stringIDToTypeID("percentUnit"), 12);
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
}

      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
 ///////////////////////////////////////   裁片射出缩放主函数体
      
      
      
      
       ///////////////////////////////////////   加缩放定位点主函数体
      
      
      
    
function 添加缩放定位点(){
addMarkerLayer()
select_41598510742188()
select_197021484375()
applyLocking_97616577148438()
set_90863037109375()


}


function addMarkerLayer() {
    var doc = app.activeDocument;
    var markerLayerName = "缩放定位点";
    var markerLayer = null;

    // 检查是否存在名为"定位点"的图层
    for (var i = 0; i < doc.artLayers.length; i++) {
        if (doc.artLayers[i].name === markerLayerName) {
            markerLayer = doc.artLayers[i];
            break;
        }
    }

    // 如果不存在，添加"定位点"图层
    if (markerLayer === null) {
        markerLayer = doc.artLayers.add();
        markerLayer.name = markerLayerName;    
        alert("已添加定位点标记图层，请将画笔大小调整为一个像素点进行标记");
    } else {
        alert("定位点标记图层已存在，请将画笔大小调整为一个像素点进行标记");
    }

    // 显示特征码信息
   // alert("定位点标记特征码是一个小方块");
}


function select_41598510742188()	//
    {
    
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putClass(stringIDToTypeID("pencilTool"));
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
     
    }



function select_197021484375()	//移动
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putName(stringIDToTypeID("brush"), "硬边圆");
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
        }
   





function applyLocking_97616577148438()	//锁定图层
    {
  
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        d1.putBoolean(stringIDToTypeID("protectPosition"), true);
        d.putObject(stringIDToTypeID("layerLocking"), stringIDToTypeID("layerLocking"), d1);
        executeAction(stringIDToTypeID("applyLocking"), d, DialogModes.NO);
      
    
    }
   
   
   function set_90863037109375()	//
    {
  
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("color"), stringIDToTypeID("foregroundColor"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        d1.putUnitDouble(stringIDToTypeID("hue"), stringIDToTypeID("angleUnit"), 0);
        d1.putDouble(stringIDToTypeID("saturation"), 100);
        d1.putDouble(stringIDToTypeID("brightness"), 100);
        d.putObject(stringIDToTypeID("to"), stringIDToTypeID("HSBColorClass"), d1);
        d.putString(stringIDToTypeID("source"), "photoshopPicker");
        executeAction(stringIDToTypeID("set"), d, DialogModes.NO);
        }  
      
       function 名称赋予(new_value)	//
    {
      
        var doc = app.activeDocument;
        var selectedLayer = doc.activeLayer;
        selectedLayer.name = "P"+new_value
      
        }   
      
 
      
      
      
   
"""
