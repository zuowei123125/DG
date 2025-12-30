dxf10_jscode = """




function 裁片射出宽高缩放模板按中心() {
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
    var 文档名称 = currentDocument.name;
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
      */
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
      图层按照缩放定位点进行宽高缩放(缩放定位点的X轴坐标,缩放定位点的Y轴坐标, 缩放比例高度)

    //  var 裁片 = app.activeDocument.layers.getByName(裁片名称);
     // app.activeDocument.activeLayer = 裁片;

     var 空白裁片模板 = app.activeDocument.layerSets.getByName(大货组名称).layers.getByName(实际裁片名称 );
  app.activeDocument.activeLayer = 空白裁片模板;
      载入选区()
var 裁片 = app.activeDocument.layers.getByName(裁片名称);
      app.activeDocument.activeLayer = 裁片
       主界面切换();
        添加图层蒙版();
        var 新名称 = "宽高缩放-" + 当前图层名称;
        app.activeDocument.activeLayer.name = 新名称;
        复制到文档(新名称, 文档名称);

         
      //添加图层蒙版()
    //  应用图层蒙版()
    //  裁片.copy();
      历史记录回退()
      app.activeDocument = currentDocument;
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
      
      图层选择(当前图层名称);
         app.preferences.rulerUnits = Units.MM;

        当前图层 = app.activeDocument.activeLayer;
        当前图层的底边 = 当前图层.bounds[3];
        当前图层的上边 = 当前图层.bounds[1];
        当前图层的高度 = 当前图层的底边 - 当前图层的上边;
        当前图层的左边 = 当前图层.bounds[0];
        当前图层的右边 = 当前图层.bounds[2];
        当前图层的宽度 = 当前图层的右边 - 当前图层的左边;
        当前图层的高度的一半 = 当前图层的高度 / 2;
        当前图层的宽度的一半 = 当前图层的宽度 / 2;
        当前图层的高度中心 = 当前图层的上边 + 当前图层的高度的一半;
        当前图层的宽度中心 = 当前图层的左边 + 当前图层的宽度的一半;

        var 成品裁片 = app.activeDocument.layers.getByName(新名称);
        app.activeDocument.activeLayer = 成品裁片;
        alb = app.activeDocument.activeLayer.bounds;
        当前x = (alb[0] + alb[2]) / 2;
        当前y = (alb[1] + alb[3]) / 2;
        置为顶层();
      
        app.activeDocument.activeLayer.translate(Number(当前图层的宽度中心) - Number(当前x), Number(当前图层的高度中心) - Number(当前y));
      //  app.refresh();
      
      
    //  载入选区();
      //粘贴图层();

      //取消选择();
     // app.refresh();
     // app.refresh();



app.preferences.rulerUnits = Units.PIXELS
   app.activeDocument = 主文档;
//历史记录回退缩放函数()
    }


  }
 app.activeDocument = currentDocument;
  前景色修改()
烧花线添加()//alert("当前码拍好")///////////////////////////////////这里可以填写添加烧花线函数
空置图层()
查找通码图层4()
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

function 主界面切换() {
    var d = new ActionDescriptor();
    var r = new ActionReference();
    r.putEnumerated(stringIDToTypeID("channel"), stringIDToTypeID("channel"), stringIDToTypeID("CMYK"));
    d.putReference(stringIDToTypeID("null"), r);
    d.putBoolean(stringIDToTypeID("makeVisible"), false);
    executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
}


function 复制到文档(新名称, 文档名称)	//
    {
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        var r1 = new ActionReference();
        r1.putName(stringIDToTypeID("document"), 文档名称);
        d.putReference(stringIDToTypeID("to"), r1);
        d.putString(stringIDToTypeID("name"), 新名称);
        d.putInteger(stringIDToTypeID("version"), 5);
        var list = new ActionList();
        list.putInteger(12);
        d.putList(stringIDToTypeID("ID"), list);
        executeAction(stringIDToTypeID("duplicate"), d, DialogModes.NO);
     
    }

function 空置图层()	//
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("selectNoLayers"), d, DialogModes.NO);

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

function 置为顶层() {
    var d = new ActionDescriptor();
    var r = new ActionReference();
    r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
    d.putReference(stringIDToTypeID("null"), r);
    var r1 = new ActionReference();
    r1.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("front"));
    d.putReference(stringIDToTypeID("to"), r1);
    executeAction(stringIDToTypeID("move"), d, DialogModes.NO);
}

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

function 图层按照缩放定位点进行宽高缩放(缩放定位点的X轴坐标,缩放定位点的Y轴坐标,缩放比例高度)	//自由变换
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
        d.putUnitDouble(stringIDToTypeID("width"), stringIDToTypeID("percentUnit"), 缩放比例高度);
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
        r.putOffset(stringIDToTypeID("historyState"), -5);
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
        r.putOffset(stringIDToTypeID("historyState"), -4);
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);

    }




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


function 查找通码图层4() {
	
app.activeDocument.suspendHistory("宽高缩放印花图层打包", "查找通码图层()");
}

function 查找通码图层() {





function 查找通码图层() {
  var 当前文档 = app.activeDocument;
  var 包含通码的图层数组 = [];

  for (var i = 0; i < 当前文档.layers.length; i++) {
    var 图层 = 当前文档.layers[i];
    if (图层.name.indexOf("宽高缩放") !== -1) {
      包含通码的图层数组.push(图层.name);
    }
  }

  return 包含通码的图层数组;
}

// 调用函数来查找包含通码的图层名称并放入数组
var 通码图层数组 = 查找通码图层();

// 打印包含通码的图层名称数组
for (var j = 0; j < 通码图层数组.length; j++) {
    var 成品裁片图层通码=通码图层数组[j]

    多选图层2(成品裁片图层通码)
  //$.writeln("包含通码的图层名称：" + 通码图层数组[j]);

}

图层编组()
名称更改()


function 多选图层2(成品裁片图层通码)	//
    {
    
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putName(stringIDToTypeID("layer"), 成品裁片图层通码);
        d.putReference(stringIDToTypeID("null"), r);
        d.putEnumerated(stringIDToTypeID("selectionModifier"), stringIDToTypeID("selectionModifierType"), stringIDToTypeID("addToSelection"));
        d.putBoolean(stringIDToTypeID("makeVisible"), false);
        var list = new ActionList();
        list.putInteger(4);
       
        d.putList(stringIDToTypeID("layerID"), list);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
  
    }


function 图层编组()	//图层编组
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putClass(stringIDToTypeID("layerSection"));
        d.putReference(stringIDToTypeID("null"), r);
        var r1 = new ActionReference();
        r1.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("from"), r1);
        d.putInteger(stringIDToTypeID("layerSectionStart"), 22);
        d.putInteger(stringIDToTypeID("layerSectionEnd"), 23);
        d.putString(stringIDToTypeID("name"), "组 1");
        executeAction(stringIDToTypeID("make"), d, DialogModes.NO);
      
    }

function 空置图层()	//
    {
 
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("selectNoLayers"), d, DialogModes.NO);
    
    }


function 名称更改()	//名称更改
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        d1.putString(stringIDToTypeID("name"), "裁片");
        d.putObject(stringIDToTypeID("to"), stringIDToTypeID("layer"), d1);
        executeAction(stringIDToTypeID("set"), d, DialogModes.NO);
  
    }




}  
      

        




"""