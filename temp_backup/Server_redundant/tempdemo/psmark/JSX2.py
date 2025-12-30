# -*- coding: utf-8 -*-
dxf3_jscode = """

function 裁片射出宽高缩放() {
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
        var 缩放比例高度=高度转毫米/基码图层高度*100
        var 缩放比例宽度=宽度转毫米/基码图层宽度*100
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

     var 空白裁片模板 = app.activeDocument.layerSets.getByName(大货组名称).layers.getByName(实际裁片名称 );
  app.activeDocument.activeLayer = 空白裁片模板;
        载入选区()
var 缩放定位点的中心坐标=获取当前缩放定位点选区四边距()
var 缩放定位点的Y轴坐标=缩放定位点的中心坐标.top2+(缩放定位点的中心坐标.bottom2-缩放定位点的中心坐标.top2)/2    
var 缩放定位点的X轴坐标=缩放定位点的中心坐标.left2+(缩放定位点的中心坐标.right2-缩放定位点的中心坐标.left2)/2    
    $.writeln("Y轴中心坐标"+缩放定位点的Y轴坐标);
$.writeln("X轴中心坐标"+缩放定位点的X轴坐标);

  var 裁片 = app.activeDocument.layers.getByName(裁片名称);
      app.activeDocument.activeLayer = 裁片
//var 空白裁片模板 = app.activeDocument.layerSets.getByName(大货组名称).layers.getByName(实际裁片名称 );
   //app.activeDocument.activeLayer = 空白裁片模板;
   取消选择()
   
      //图层按照缩放定位点进行宽高缩放(缩放定位点的X轴坐标,缩放定位点的Y轴坐标, 缩放比例高度,缩放比例宽度)

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
       自由变换();
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

function 图层按照缩放定位点进行宽高缩放(缩放定位点的X轴坐标,缩放定位点的Y轴坐标,缩放比例高度,缩放比例宽度)	//自由变换
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
        d.putUnitDouble(stringIDToTypeID("width"), stringIDToTypeID("percentUnit"), 缩放比例宽度);
        d.putUnitDouble(stringIDToTypeID("height"), stringIDToTypeID("percentUnit"), 缩放比例高度);
  
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
        r.putOffset(stringIDToTypeID("historyState"), -4);
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
}  
    
    
    
     //  //  //  //  //  //  //  //  //  //   //  //  //  //  //  //  //  //  //  //
      

function 角度旋转() {



var 主文档 = app.activeDocument;
var 主文档名称 = 主文档.name;

// 遍历当前打开的文档
for (var i = 0; i < app.documents.length; i++) {
  var document = app.documents[i];
  var documentName = document.name;

  // 判断文档名称是否与主文档名称不相同
  if (documentName !== 主文档名称) {
    app.activeDocument = document;
  替换图层名称()
  }
}
app.activeDocument = 主文档
alert("角度校准成功")
}


function 替换图层名称() {
    var activeDocument = app.activeDocument;
    var layers = activeDocument.layers;

    for (var i = 0; i < layers.length; i++) {
        var layer = layers[i];
        var 当前图层名称 = layer.name;
          if (当前图层名称 === "背景") {
            continue;
        }
        var parts = 当前图层名称.split("_");
        var 特定部分 = parts[1]; // 假设特定部分在下划线后面的第二个位置
   // alert(特定部分)
        // 检查特定部分是否包含 "180" 或 "-180"
        if (特定部分.indexOf("180") !== -1 || 特定部分.indexOf("-180") !== -1) {
            // 替换 "180" 或 "-180" 为 "0"
            var new特定部分 = 特定部分.replace("180", "0").replace("-180", "0");
            parts[1] = new特定部分;
            var newLayerName = parts.join("_");
            layer.name = newLayerName;
        }
        // 检查特定部分是否为 "0"
        else if (特定部分 === "0") {
            // 替换 "0" 为 "180"
            var new特定部分 = "180";
            parts[1] = new特定部分;
            var newLayerName = parts.join("_");
            layer.name = newLayerName;
        }
    }
}
      
      
  

    function 裁片视图检查2() {
        
    app.activeDocument.suspendHistory("裁片视图检查", "裁片视图检查()");
}
function 裁片视图检查() {

var 描边函数列表 = [描边1, 描边2, 描边3, 描边4, 描边5, 描边6];
// 获取当前文档
var doc = app.activeDocument;

// 遍历所有图层组
var groupsContainingKeyword = [];
for (var i = 0; i < doc.layerSets.length; i++) {
    var group = doc.layerSets[i];
    // 检查组的名称是否含有 "大货裁片"
    if (group.name.indexOf("大货裁片") !== -1) {
        groupsContainingKeyword.push(group);
    }
}

// 遍历找到的组及其子图层
for (var j = 0; j < groupsContainingKeyword.length; j++) {
    var foundGroup = groupsContainingKeyword[j];
    // alert("找到的组名：" + foundGroup.name);
    var foundGroupName = foundGroup.name;
    var caipianGroup = app.activeDocument.layerSets.getByName(foundGroupName);
    app.activeDocument.activeLayer = caipianGroup;
    透明化处理();
    
    // 遍历组内的所有图层
    for (var k = 0; k < foundGroup.artLayers.length; k++) {
        var specificLayerName = foundGroup.artLayers[k].name;  // 获取图层的名称
        var specificLayer  = app.activeDocument.layerSets.getByName(foundGroupName).layers.getByName(specificLayerName );
        app.activeDocument.activeLayer = specificLayer;
         var 描边函数索引 = k % 描边函数列表.length;
        var 当前描边函数 = 描边函数列表[描边函数索引];
        当前描边函数();
        // 在这里可以执行你的操作，例如对子图层进行处理
    }
}






function 透明化处理()	//图层样式
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        var list = new ActionList();
        var d2 = new ActionDescriptor();
        var r1 = new ActionReference();
        r1.putEnumerated(stringIDToTypeID("channel"), stringIDToTypeID("channel"), stringIDToTypeID("gray"));
        d2.putReference(stringIDToTypeID("channel"), r1);
        d2.putInteger(stringIDToTypeID("srcBlackMin"), 0);
        d2.putInteger(stringIDToTypeID("srcBlackMax"), 0);
        d2.putInteger(stringIDToTypeID("srcWhiteMin"), 251);
        d2.putInteger(stringIDToTypeID("srcWhiteMax"), 251);
        d2.putInteger(stringIDToTypeID("destBlackMin"), 0);
        d2.putInteger(stringIDToTypeID("destBlackMax"), 0);
        d2.putInteger(stringIDToTypeID("destWhiteMin"), 255);
        d2.putInteger(stringIDToTypeID("desaturate"), 255);
        list.putObject(stringIDToTypeID("blendRange"), d2);
        d1.putList(stringIDToTypeID("blendRange"), list);
        var d3 = new ActionDescriptor();
        d3.putUnitDouble(stringIDToTypeID("scale"), stringIDToTypeID("percentUnit"), 208.333333333333);
        d1.putObject(stringIDToTypeID("layerEffects"), stringIDToTypeID("layerEffects"), d3);
        d.putObject(stringIDToTypeID("to"), stringIDToTypeID("layer"), d1);
        executeAction(stringIDToTypeID("set"), d, DialogModes.NO);
        }
    
    
    
 function  描边1()	//描边
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("property"), stringIDToTypeID("layerEffects"));
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        d1.putUnitDouble(stringIDToTypeID("scale"), stringIDToTypeID("percentUnit"), 208.333333333333);
        var d2 = new ActionDescriptor();
        d2.putBoolean(stringIDToTypeID("enabled"), true);
        d2.putBoolean(stringIDToTypeID("present"), true);
        d2.putBoolean(stringIDToTypeID("showInDialog"), true);
        d2.putEnumerated(stringIDToTypeID("style"), stringIDToTypeID("frameStyle"), stringIDToTypeID("outsetFrame"));
        d2.putEnumerated(stringIDToTypeID("paintType"), stringIDToTypeID("frameFill"), stringIDToTypeID("solidColor"));
        d2.putEnumerated(stringIDToTypeID("mode"), stringIDToTypeID("blendMode"), stringIDToTypeID("normal"));
        d2.putUnitDouble(stringIDToTypeID("opacity"), stringIDToTypeID("percentUnit"), 100);
        d2.putUnitDouble(stringIDToTypeID("size"), stringIDToTypeID("pixelsUnit"), 6);
        var d3 = new ActionDescriptor();
        d3.putDouble(stringIDToTypeID("cyan"), 60);
        d3.putDouble(stringIDToTypeID("magenta"), 0);
        d3.putDouble(stringIDToTypeID("yellowColor"), 0);
        d3.putDouble(stringIDToTypeID("black"), 0);
        d2.putObject(stringIDToTypeID("color"), stringIDToTypeID("CMYKColorClass"), d3);
        d2.putBoolean(stringIDToTypeID("overprint"), false);
        d1.putObject(stringIDToTypeID("frameFX"), stringIDToTypeID("frameFX"), d2);
        d.putObject(stringIDToTypeID("to"), stringIDToTypeID("layerEffects"), d1);
        executeAction(stringIDToTypeID("set"), d, DialogModes.NO);
  
    }
    
    
    
     function  描边2()	//描边
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("property"), stringIDToTypeID("layerEffects"));
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        d1.putUnitDouble(stringIDToTypeID("scale"), stringIDToTypeID("percentUnit"), 208.333333333333);
        var d2 = new ActionDescriptor();
        d2.putBoolean(stringIDToTypeID("enabled"), true);
        d2.putBoolean(stringIDToTypeID("present"), true);
        d2.putBoolean(stringIDToTypeID("showInDialog"), true);
        d2.putEnumerated(stringIDToTypeID("style"), stringIDToTypeID("frameStyle"), stringIDToTypeID("outsetFrame"));
        d2.putEnumerated(stringIDToTypeID("paintType"), stringIDToTypeID("frameFill"), stringIDToTypeID("solidColor"));
        d2.putEnumerated(stringIDToTypeID("mode"), stringIDToTypeID("blendMode"), stringIDToTypeID("normal"));
        d2.putUnitDouble(stringIDToTypeID("opacity"), stringIDToTypeID("percentUnit"), 100);
        d2.putUnitDouble(stringIDToTypeID("size"), stringIDToTypeID("pixelsUnit"), 6);
        var d3 = new ActionDescriptor();
        d3.putDouble(stringIDToTypeID("cyan"), 0);
        d3.putDouble(stringIDToTypeID("magenta"), 60);
        d3.putDouble(stringIDToTypeID("yellowColor"), 0);
        d3.putDouble(stringIDToTypeID("black"), 0);
        d2.putObject(stringIDToTypeID("color"), stringIDToTypeID("CMYKColorClass"), d3);
        d2.putBoolean(stringIDToTypeID("overprint"), false);
        d1.putObject(stringIDToTypeID("frameFX"), stringIDToTypeID("frameFX"), d2);
        d.putObject(stringIDToTypeID("to"), stringIDToTypeID("layerEffects"), d1);
        executeAction(stringIDToTypeID("set"), d, DialogModes.NO);
  
    }
    
    
    
    
      function  描边3()	//描边
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("property"), stringIDToTypeID("layerEffects"));
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        d1.putUnitDouble(stringIDToTypeID("scale"), stringIDToTypeID("percentUnit"), 208.333333333333);
        var d2 = new ActionDescriptor();
        d2.putBoolean(stringIDToTypeID("enabled"), true);
        d2.putBoolean(stringIDToTypeID("present"), true);
        d2.putBoolean(stringIDToTypeID("showInDialog"), true);
        d2.putEnumerated(stringIDToTypeID("style"), stringIDToTypeID("frameStyle"), stringIDToTypeID("outsetFrame"));
        d2.putEnumerated(stringIDToTypeID("paintType"), stringIDToTypeID("frameFill"), stringIDToTypeID("solidColor"));
        d2.putEnumerated(stringIDToTypeID("mode"), stringIDToTypeID("blendMode"), stringIDToTypeID("normal"));
        d2.putUnitDouble(stringIDToTypeID("opacity"), stringIDToTypeID("percentUnit"), 100);
        d2.putUnitDouble(stringIDToTypeID("size"), stringIDToTypeID("pixelsUnit"), 6);
        var d3 = new ActionDescriptor();
        d3.putDouble(stringIDToTypeID("cyan"), 0);
        d3.putDouble(stringIDToTypeID("magenta"), 0);
        d3.putDouble(stringIDToTypeID("yellowColor"), 60);
        d3.putDouble(stringIDToTypeID("black"), 0);
        d2.putObject(stringIDToTypeID("color"), stringIDToTypeID("CMYKColorClass"), d3);
        d2.putBoolean(stringIDToTypeID("overprint"), false);
        d1.putObject(stringIDToTypeID("frameFX"), stringIDToTypeID("frameFX"), d2);
        d.putObject(stringIDToTypeID("to"), stringIDToTypeID("layerEffects"), d1);
        executeAction(stringIDToTypeID("set"), d, DialogModes.NO);
  
    }




     function  描边4()	//描边
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("property"), stringIDToTypeID("layerEffects"));
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        d1.putUnitDouble(stringIDToTypeID("scale"), stringIDToTypeID("percentUnit"), 208.333333333333);
        var d2 = new ActionDescriptor();
        d2.putBoolean(stringIDToTypeID("enabled"), true);
        d2.putBoolean(stringIDToTypeID("present"), true);
        d2.putBoolean(stringIDToTypeID("showInDialog"), true);
        d2.putEnumerated(stringIDToTypeID("style"), stringIDToTypeID("frameStyle"), stringIDToTypeID("outsetFrame"));
        d2.putEnumerated(stringIDToTypeID("paintType"), stringIDToTypeID("frameFill"), stringIDToTypeID("solidColor"));
        d2.putEnumerated(stringIDToTypeID("mode"), stringIDToTypeID("blendMode"), stringIDToTypeID("normal"));
        d2.putUnitDouble(stringIDToTypeID("opacity"), stringIDToTypeID("percentUnit"), 100);
        d2.putUnitDouble(stringIDToTypeID("size"), stringIDToTypeID("pixelsUnit"), 6);
        var d3 = new ActionDescriptor();
        d3.putDouble(stringIDToTypeID("cyan"), 0);
        d3.putDouble(stringIDToTypeID("magenta"), 0);
        d3.putDouble(stringIDToTypeID("yellowColor"), 0);
        d3.putDouble(stringIDToTypeID("black"), 60);
        d2.putObject(stringIDToTypeID("color"), stringIDToTypeID("CMYKColorClass"), d3);
        d2.putBoolean(stringIDToTypeID("overprint"), false);
        d1.putObject(stringIDToTypeID("frameFX"), stringIDToTypeID("frameFX"), d2);
        d.putObject(stringIDToTypeID("to"), stringIDToTypeID("layerEffects"), d1);
        executeAction(stringIDToTypeID("set"), d, DialogModes.NO);
  
    }




     function  描边5()	//描边
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("property"), stringIDToTypeID("layerEffects"));
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        d1.putUnitDouble(stringIDToTypeID("scale"), stringIDToTypeID("percentUnit"), 208.333333333333);
        var d2 = new ActionDescriptor();
        d2.putBoolean(stringIDToTypeID("enabled"), true);
        d2.putBoolean(stringIDToTypeID("present"), true);
        d2.putBoolean(stringIDToTypeID("showInDialog"), true);
        d2.putEnumerated(stringIDToTypeID("style"), stringIDToTypeID("frameStyle"), stringIDToTypeID("outsetFrame"));
        d2.putEnumerated(stringIDToTypeID("paintType"), stringIDToTypeID("frameFill"), stringIDToTypeID("solidColor"));
        d2.putEnumerated(stringIDToTypeID("mode"), stringIDToTypeID("blendMode"), stringIDToTypeID("normal"));
        d2.putUnitDouble(stringIDToTypeID("opacity"), stringIDToTypeID("percentUnit"), 100);
        d2.putUnitDouble(stringIDToTypeID("size"), stringIDToTypeID("pixelsUnit"), 6);
        var d3 = new ActionDescriptor();
        d3.putDouble(stringIDToTypeID("cyan"), 0);
        d3.putDouble(stringIDToTypeID("magenta"), 60);
        d3.putDouble(stringIDToTypeID("yellowColor"), 60);
        d3.putDouble(stringIDToTypeID("black"), 0);
        d2.putObject(stringIDToTypeID("color"), stringIDToTypeID("CMYKColorClass"), d3);
        d2.putBoolean(stringIDToTypeID("overprint"), false);
        d1.putObject(stringIDToTypeID("frameFX"), stringIDToTypeID("frameFX"), d2);
        d.putObject(stringIDToTypeID("to"), stringIDToTypeID("layerEffects"), d1);
        executeAction(stringIDToTypeID("set"), d, DialogModes.NO);
  
    }



     function  描边6()	//描边
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("property"), stringIDToTypeID("layerEffects"));
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        d1.putUnitDouble(stringIDToTypeID("scale"), stringIDToTypeID("percentUnit"), 208.333333333333);
        var d2 = new ActionDescriptor();
        d2.putBoolean(stringIDToTypeID("enabled"), true);
        d2.putBoolean(stringIDToTypeID("present"), true);
        d2.putBoolean(stringIDToTypeID("showInDialog"), true);
        d2.putEnumerated(stringIDToTypeID("style"), stringIDToTypeID("frameStyle"), stringIDToTypeID("outsetFrame"));
        d2.putEnumerated(stringIDToTypeID("paintType"), stringIDToTypeID("frameFill"), stringIDToTypeID("solidColor"));
        d2.putEnumerated(stringIDToTypeID("mode"), stringIDToTypeID("blendMode"), stringIDToTypeID("normal"));
        d2.putUnitDouble(stringIDToTypeID("opacity"), stringIDToTypeID("percentUnit"), 100);
        d2.putUnitDouble(stringIDToTypeID("size"), stringIDToTypeID("pixelsUnit"), 6);
        var d3 = new ActionDescriptor();
        d3.putDouble(stringIDToTypeID("cyan"), 60);
        d3.putDouble(stringIDToTypeID("magenta"), 60);
        d3.putDouble(stringIDToTypeID("yellowColor"), 0);
        d3.putDouble(stringIDToTypeID("black"), 0);
        d2.putObject(stringIDToTypeID("color"), stringIDToTypeID("CMYKColorClass"), d3);
        d2.putBoolean(stringIDToTypeID("overprint"), false);
        d1.putObject(stringIDToTypeID("frameFX"), stringIDToTypeID("frameFX"), d2);
        d.putObject(stringIDToTypeID("to"), stringIDToTypeID("layerEffects"), d1);
        executeAction(stringIDToTypeID("set"), d, DialogModes.NO);
  
    }

}    
      
      
      
      
      
      
      
      
      
      
      
      
     




    function 重写基码信息2() {
        
    app.activeDocument.suspendHistory("重写基码信息", "重写基码信息()");

}
 function 重写基码信息() {




var dialog = new Window("dialog"); 
dialog.text = "重写基码信息"; 
dialog.orientation = "column"; 
dialog.alignChildren = ["left","top"]; 
dialog.spacing = 10; 
dialog.margins = 16; 

// PANEL1
// ======
var panel1 = dialog.add("panel", undefined, undefined, {name: "panel1"}); 
panel1.text = "基码选择"; 
panel1.orientation = "column"; 
panel1.alignChildren = ["left","top"]; 
panel1.spacing = 10; 
panel1.margins = 10; 

// Get the active document
var doc = app.activeDocument;

// Find the specified layer group by name
var groupName = "P1-大货裁片";
var group = doc.layerSets.getByName(groupName);

var selectedRadioButton = null;

// Display layer names in the panel as radio buttons
for (var i = 0; i < group.artLayers.length; i++) {
    var layer = group.artLayers[i];
    var radioButton = panel1.add("radiobutton", undefined, layer.name);
    if (i === 0) {
        radioButton.value = true; // Select the first radio button initially
        selectedRadioButton = radioButton;
    }
    radioButton.onClick = function() {
        selectedRadioButton = this;
    };
}

var buttonsGroup = dialog.add("group", undefined);
buttonsGroup.orientation = "row";
buttonsGroup.alignChildren = ["center", "top"];

var confirmButton = buttonsGroup.add("button", undefined, undefined, {name: "confirmButton"}); 
confirmButton.text = "写入"; 
confirmButton.onClick = function() {
    
        var selectedText = selectedRadioButton.text;
        var parts = selectedText.split("-");  // 使用 "-" 作为分隔符，分割字符串
       
            var prefix = parts[0];
            var code = parts[1];
      
            var doc = app.activeDocument;

            // 遍历所有图层组
            var groupsContainingKeyword = [];
            for (var i = 0; i < doc.layerSets.length; i++) {
                var group = doc.layerSets[i];
                // 检查组的名称是否含有 "大货裁片"
                if (group.name.indexOf("大货裁片") !== -1) {
                    groupsContainingKeyword.push(group);
                }
            }
            dialog.close();
            // 遍历找到的组及其子图层
            for (var j = 0; j < groupsContainingKeyword.length; j++) {
                var foundGroup = groupsContainingKeyword[j];
               //  alert("找到的组名：" + foundGroup.name);
                var foundGroupName = foundGroup.name;
                var caipianGroup = app.activeDocument.layerSets.getByName(foundGroupName);
                app.activeDocument.activeLayer = caipianGroup;
                
                   for (var z = 0; z < foundGroup.artLayers.length; z++) {
                    var specificLayerName = foundGroup.artLayers[z].name;  // 获取图层的名称
                   if (specificLayerName.indexOf(code) !== -1) {  // 判断图层名称是否包含指定的 code
                  //  alert("找到匹配的图层：" + specificLayerName);
                    var 新图层名称 =  specificLayerName.split("-")
                    var 裁片名称 = 新图层名称[0]
                    var 尺码 = 新图层名称[1]
                    var 裁片组名称 =  裁片名称+"-大货裁片"      
                    var 获取裁片组子图层  = app.activeDocument.layerSets.getByName(裁片组名称).layers.getByName(specificLayerName);
                    app.activeDocument.activeLayer = 获取裁片组子图层;       
                    载入选区()
                   var 获取花样组裁片  = app.activeDocument.layers.getByName(裁片名称);
                    app.activeDocument.activeLayer = 获取花样组裁片;       
                    切换mask()
                    删除图层蒙版()
                    添加图层蒙版()
                }     
                }
        
            
     }
     选择图层基础信息()
     删除图层()

};
var cancelButton = buttonsGroup.add("button", undefined, undefined, {name: "cancelButton"}); 
cancelButton.text = "取消"; 
cancelButton.onClick = function() {
    dialog.close();
};





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




function 删除图层蒙版()	//删除图层蒙版
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("channel"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("delete"), d, DialogModes.NO);
    
    
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



function 选择图层基础信息()	//
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putName(stringIDToTypeID("layer"), "图层基础信息");
        d.putReference(stringIDToTypeID("null"), r);
        d.putBoolean(stringIDToTypeID("makeVisible"), false);
        var list = new ActionList();
        list.putInteger(43);
        d.putList(stringIDToTypeID("layerID"), list);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);

    }

function 删除图层()	//删除图层
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        var list = new ActionList();
        list.putInteger(44);
        list.putInteger(45);
        list.putInteger(46);
        list.putInteger(47);
        list.putInteger(43);
        d.putList(stringIDToTypeID("layerID"), list);
        executeAction(stringIDToTypeID("delete"), d, DialogModes.NO);
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




dialog.show();
} 
      
      
      
      
      
      
      
      
      
      
      
      
  ///////////////////////////////////////////////////////////////////////////////          
      
      function 领口对齐2() {
        
    app.activeDocument.suspendHistory("领口对齐", "领口对齐()");
}

 
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
   载入选区蒙版()
 // 应用图层蒙版();
 // 载入选区();

  var 边距 = 获取当前选区四边距();
  var 获取左右的中心坐标 = (边距.right - 边距.left) / 2 + 边距.left;
  $.writeln("中心坐标=：" + 获取左右的中心坐标);

  var currentDocument = app.activeDocument;
  var height = currentDocument.height.value;

  var 上边距新 = 0;
  var 左边距新 = 获取左右的中心坐标 ;
  var 下边距新 = height;
  var 右边距新 = 获取左右的中心坐标 + 1;

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

领窝边距 = 获取当前选区四边距();
获取到花样图层当前居中领口y坐标信息 = 领窝边距.top;
获取到花样图层当前居中领口x坐标信息 = 领窝边距.left;
  $.writeln("居中领口y坐标信息" + 获取到花样图层当前居中领口y坐标信息);
  $.writeln("居中领口x坐标信息" + 获取到花样图层当前居中领口x坐标信息);
  
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
  
  var selectedLayer =  app.activeDocument.activeLayer;
  var bounds = selectedLayer.bounds;

  
左left = bounds[0].value;
上top = bounds[1].value;
右right = bounds[2].value;
下bottom = bounds[3].value;
中心坐标centerX = (bounds[2].value - bounds[0].value) / 2 + bounds[0].value;

中心坐标centerY = (bounds[3].value - bounds[1].value) / 2 + bounds[1].value;

  $.writeln("中心坐标centerX" + 中心坐标centerX); 
   $.writeln("中心坐标centerY" +中心坐标centerY);
图层上边距新 = 0;
图层左边距新 = 中心坐标centerX  ;
图层下边距新 = height;
图层右边距新 = 中心坐标centerX  + 1;
  

  
    新建选区(图层上边距新, 图层左边距新, 图层下边距新, 图层右边距新);
    app.activeDocument.activeLayer = 当前裁片图层;
   载入选区交叉图层()
 裁片位置坐标 = 获取当前选区四边距();
 裁片位置坐标x=裁片位置坐标.left
裁片位置坐标y=裁片位置坐标.top
目标高度转毫米 = pixelsToMillimeters(获取到花样图层当前居中领口y坐标信息);
 目标宽度转毫米 = pixelsToMillimeters(获取到花样图层当前居中领口x坐标信息);
当前高度转毫米 = pixelsToMillimeters(裁片位置坐标y);
当前宽度转毫米 = pixelsToMillimeters(裁片位置坐标x);
位移距离PXy = 获取到花样图层当前居中领口y坐标信息 - 裁片位置坐标y;
位移距离PXx = 获取到花样图层当前居中领口x坐标信息 - 裁片位置坐标x;
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