dxf5_jscode = """





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

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


function 花样标准化2() {
    
    app.activeDocument.suspendHistory("花样标准化", "花样标准化()");
}



function 花样标准化()
{
    var 扩展毫米数=130
    app.preferences.rulerUnits = Units.MM;
    
    裁片组 = app.activeDocument.layerSets;

    for(var z=0;z<裁片组.length;z++)
    {
        当前裁片组 = 裁片组[z];
        花样图层 = 当前裁片组.layers[0];
        裁片图层 = 当前裁片组.layers[1];

        裁片边界 = 裁片图层.bounds;
    //~     alert(毫米转像素(50))
//~         扩展值 = 毫米转像素(50); //50cm
        扩展值 = 毫米转像素(扩展毫米数); //50cm
        裁片边界_左 = 毫米转像素(裁片边界[0]) - 扩展值;
        裁片边界_上 = 毫米转像素(裁片边界[1]) - 扩展值;
        裁片边界_右 = 毫米转像素(裁片边界[2]) + 扩展值;
        裁片边界_下 = 毫米转像素(裁片边界[3]) + 扩展值;


        //左上右下点XY坐标
        var selRegion = [
            [裁片边界_左,裁片边界_上],
            [裁片边界_右,裁片边界_上],
            [裁片边界_右,裁片边界_下],
            [裁片边界_左,裁片边界_下]
        ];

        app.activeDocument.activeLayer = 花样图层;
        app.activeDocument.selection.select(selRegion, SelectionType.REPLACE);
       按选区添加蒙版();

        //制作一个白底衬底图
        //新建一个图层
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putClass(stringIDToTypeID("layer"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putInteger(stringIDToTypeID("layerID"), 198);
        executeAction(stringIDToTypeID("make"), d, DialogModes.NO);
        白底图层 = app.activeDocument.activeLayer;
        白底图层.name = "白底";

        app.activeDocument.selection.select(selRegion, SelectionType.REPLACE);

        var c = new SolidColor();
        c.rgb.hexValue = "FFFFFF";
        app.activeDocument.selection.fill(c);

        花样图层.grouped = false;
        白底图层.move(花样图层,ElementPlacement.PLACEAFTER);


        app.activeDocument.activeLayer = 花样图层;
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putName(stringIDToTypeID("layer"), "白底");
        d.putReference(stringIDToTypeID("null"), r);
        d.putEnumerated(stringIDToTypeID("selectionModifier"), stringIDToTypeID("selectionModifierType"), stringIDToTypeID("addToSelectionContinuous"));
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);

        app.activeDocument.activeLayer.merge(); //合并当前选择图层
        app.activeDocument.activeLayer.grouped = true;
  }

 }

function 毫米转像素(毫米)
{
    //厘米转像素
    doc_w = app.activeDocument.width;
    //用户设定的厘米数 支持小数
    user_mm = UnitValue(毫米,"mm");
    user_px = user_mm.as("px")*app.activeDocument.resolution/72;
    return user_px;
}
 



function 按选区添加蒙版()       //先创建出选区 然后按选区添加出一个蒙版
{

        var d = new ActionDescriptor();
        d.putClass(stringIDToTypeID("new"), stringIDToTypeID("channel"));
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("channel"), stringIDToTypeID("channel"), stringIDToTypeID("mask"));
        d.putReference(stringIDToTypeID("at"), r);
        d.putEnumerated(stringIDToTypeID("using"), stringIDToTypeID("userMaskEnabled"), stringIDToTypeID("revealSelection"));
        executeAction(stringIDToTypeID("make"), d, DialogModes.NO);
   
    


  }
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////







///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


function 花样标准化3() {
    
    app.activeDocument.suspendHistory("花样标准化扩展值8cm", "花样标准化80()");
}



function 花样标准化80()
{
    var 扩展毫米数=80
    app.preferences.rulerUnits = Units.MM;
    
    裁片组 = app.activeDocument.layerSets;

    for(var z=0;z<裁片组.length;z++)
    {
        当前裁片组 = 裁片组[z];
        花样图层 = 当前裁片组.layers[0];
        裁片图层 = 当前裁片组.layers[1];

        裁片边界 = 裁片图层.bounds;
    //~     alert(毫米转像素(50))
//~         扩展值 = 毫米转像素(50); //50cm
        扩展值 = 毫米转像素(扩展毫米数); //50cm
        裁片边界_左 = 毫米转像素(裁片边界[0]) - 扩展值;
        
        裁片边界_上 = 毫米转像素(裁片边界[1]) - 扩展值;
        裁片边界_右 = 毫米转像素(裁片边界[2]) + 扩展值;
        裁片边界_下 = 毫米转像素(裁片边界[3]) + 扩展值;


        //左上右下点XY坐标
        var selRegion = [
            [裁片边界_左,裁片边界_上],
            [裁片边界_右,裁片边界_上],
            [裁片边界_右,裁片边界_下],
            [裁片边界_左,裁片边界_下]
        ];

        app.activeDocument.activeLayer = 花样图层;
        app.activeDocument.selection.select(selRegion, SelectionType.REPLACE);
       按选区添加蒙版();

        //制作一个白底衬底图
        //新建一个图层
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putClass(stringIDToTypeID("layer"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putInteger(stringIDToTypeID("layerID"), 198);
        executeAction(stringIDToTypeID("make"), d, DialogModes.NO);
        白底图层 = app.activeDocument.activeLayer;
        白底图层.name = "白底";

        app.activeDocument.selection.select(selRegion, SelectionType.REPLACE);

        var c = new SolidColor();
        c.rgb.hexValue = "FFFFFF";
        app.activeDocument.selection.fill(c);

        花样图层.grouped = false;
        白底图层.move(花样图层,ElementPlacement.PLACEAFTER);


        app.activeDocument.activeLayer = 花样图层;
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putName(stringIDToTypeID("layer"), "白底");
        d.putReference(stringIDToTypeID("null"), r);
        d.putEnumerated(stringIDToTypeID("selectionModifier"), stringIDToTypeID("selectionModifierType"), stringIDToTypeID("addToSelectionContinuous"));
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);

        app.activeDocument.activeLayer.merge(); //合并当前选择图层
        app.activeDocument.activeLayer.grouped = true;
  }

 }

function 毫米转像素(毫米)
{
    //厘米转像素
    doc_w = app.activeDocument.width;
    //用户设定的厘米数 支持小数
    user_mm = UnitValue(毫米,"mm");
    user_px = user_mm.as("px")*app.activeDocument.resolution/72;
    return user_px;
}
 



function 按选区添加蒙版()       //先创建出选区 然后按选区添加出一个蒙版
{

        var d = new ActionDescriptor();
        d.putClass(stringIDToTypeID("new"), stringIDToTypeID("channel"));
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("channel"), stringIDToTypeID("channel"), stringIDToTypeID("mask"));
        d.putReference(stringIDToTypeID("at"), r);
        d.putEnumerated(stringIDToTypeID("using"), stringIDToTypeID("userMaskEnabled"), stringIDToTypeID("revealSelection"));
        executeAction(stringIDToTypeID("make"), d, DialogModes.NO);
   
    


  }
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////







// 调用函数// 调用函数// 调用函数// 调用函数// 调用函数// 调用函数// 调用函数// 调用函数// 调用函数// 调用函数// 调用函数// 调用函数// 调用函数// 调用函数

function 花样图层导出() {
    var 导出目录 = Folder.selectDialog("选择外链素材目录");
    if (!导出目录) {
        alert("未选择导出目录。操作已取消。");
        return;
    }

    花样图层导出为TIF(导出目录);
    花样图层替换为外链智能对象(导出目录);
}

function 花样图层导出为TIF(导出目录) {
    裁片组 = app.activeDocument.layerSets;

    for (var i = 0; i < 裁片组.length; i++) {
        app.activeDocument.duplicate("temp");

        复制文档裁片组 = app.activeDocument.layerSets;
        当前裁片组 = 复制文档裁片组[i];
        当前裁片组名 = 当前裁片组.name;
        花样图层 = 当前裁片组.layers[0];
        裁片图层 = 当前裁片组.layers[1];

        app.activeDocument.activeLayer = 花样图层;
        // 把花样图层导出
        花样图层.grouped = false; // 取消图层链接

        仅当前图层可见();

        // 按花样图层大小裁剪文档
        app.activeDocument.crop(花样图层.bounds, 0);

        // 拼合图像只保留花样图层
        var d = new ActionDescriptor();
        executeAction(stringIDToTypeID("flattenImage"), d, DialogModes.NO);

        // 保存为TIF
        var 文件路径 = 导出目录 + "/" + 当前裁片组名 + ".tif";
        tiffOptions = new TiffSaveOptions();
        app.activeDocument.saveAs(new File(文件路径), tiffOptions);
        app.activeDocument.close(SaveOptions.DONOTSAVECHANGES);
    }
}

function 花样图层替换为外链智能对象(外链素材目录) {
    裁片组 = app.activeDocument.layerSets;

    for (var i = 0; i < 裁片组.length; i++) {
        当前裁片组 = 裁片组[i];
        裁片组名 = 当前裁片组.name;
        花样图层 = 当前裁片组.layers[0];
        裁片图层 = 当前裁片组.layers[1];
        app.activeDocument.activeLayer = 花样图层;

        置入链接的智能对象(外链素材目录 + "/" + 裁片组名 + ".tif");
        外链花样图层 = app.activeDocument.activeLayer;

        // 置入之后要跟原来的花样图层中心对齐
        花样图层_中心x = (花样图层.bounds[2] + 花样图层.bounds[0]) / 2;
        花样图层_中心y = (花样图层.bounds[3] + 花样图层.bounds[1]) / 2;
        外链花样图层_中心x = (外链花样图层.bounds[2] + 外链花样图层.bounds[0]) / 2;
        外链花样图层_中心y = (外链花样图层.bounds[3] + 外链花样图层.bounds[1]) / 2;
        中心x差值 = 花样图层_中心x - 外链花样图层_中心x;
        中心y差值 = 花样图层_中心y - 外链花样图层_中心y;
        外链花样图层.translate(中心x差值, 中心y差值);

        app.activeDocument.activeLayer.grouped = true;
        花样图层.remove(); // 删除之前的花样图层
    }
}

function 置入链接的智能对象(图片路径) {
    if (!图片路径) {
        return;
    }

    var d = new ActionDescriptor();
    d.putInteger(stringIDToTypeID("ID"), 186);
    d.putPath(stringIDToTypeID("null"), new File(图片路径));
    d.putBoolean(stringIDToTypeID("linked"), true);
    d.putEnumerated(stringIDToTypeID("freeTransformCenterState"), stringIDToTypeID("quadCenterState"), stringIDToTypeID("QCSAverage"));
    var d1 = new ActionDescriptor();
    d1.putUnitDouble(stringIDToTypeID("horizontal"), stringIDToTypeID("distanceUnit"), 0);
    d1.putUnitDouble(stringIDToTypeID("vertical"), stringIDToTypeID("distanceUnit"), 0);
    d.putObject(stringIDToTypeID("offset"), stringIDToTypeID("offset"), d1);
    executeAction(stringIDToTypeID("placeEvent"), d, DialogModes.NO);
}

function 仅当前图层可见()	//图层可见性
    {
   
        var d = new ActionDescriptor();
        var list = new ActionList();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        list.putReference(r);
        d.putList(stringIDToTypeID("null"), list);
        d.putBoolean(stringIDToTypeID("toggleOptionsPalette"), true);
        executeAction(stringIDToTypeID("show"), d, DialogModes.NO);
    
    }



// 调用函数// 调用函数// 调用函数// 调用函数// 调用函数// 调用函数// 调用函数// 调用函数// 调用函数// 调用函数// 调用函数// 调用函数// 调用函数// 调用函数


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function 替换外链新(){

var dialog = new Window("dialog"); 
    dialog.text = "快速换图"; 
    dialog.orientation = "row"; 
    dialog.alignChildren = ["left","top"]; 
    dialog.spacing = 10; 
    dialog.margins = 16; 

// GROUP1
// ======
var group1 = dialog.add("group", undefined, {name: "group1"}); 
    group1.preferredSize.width = 183; 
    group1.orientation = "column"; 
    group1.alignChildren = ["fill","top"]; 
    group1.spacing = 10; 
    group1.margins = 0; 

// PANEL1
// ======
var panel1 = group1.add("panel", undefined, undefined, {name: "panel1"}); 
    panel1.text = "文件夹选择"; 
    panel1.preferredSize.height = 205; 
    panel1.orientation = "column"; 
    panel1.alignChildren = ["left","top"]; 
    panel1.spacing = 10; 
    panel1.margins = 10; 

var statictext1 = panel1.add("statictext", undefined, undefined, {name: "statictext1"}); 
    statictext1.text = "大货裁片模板路径:"; 

var button1 = panel1.add("button", undefined, undefined, {name: "button1"}); 
    button1.text = "路径选择"; 
    button1.preferredSize.width = 300; 

var statictext2 = panel1.add("statictext", undefined, undefined, {name: "statictext2"}); 
    statictext2.text = "切片裁片路径选择:"; 

var button2 = panel1.add("button", undefined, undefined, {name: "button2"}); 
    button2.text = "路径选择"; 
    button2.preferredSize.width = 300; 

// PANEL2
// ======
var panel2 = panel1.add("panel", undefined, undefined, {name: "panel2"}); 
    panel2.text = "款号修改："; 
    panel2.orientation = "column"; 
    panel2.alignChildren = ["left","top"]; 
    panel2.spacing = 10; 
    panel2.margins = 10; 

var edittext1 = panel2.add('edittext {properties: {name: "edittext1"}}'); 
    
    edittext1.preferredSize.width = 200; 


// PANEL4
// ======


var statictext11 = panel2.add("statictext", undefined, undefined, {name: "statictext11"}); 
    statictext11.text = "是否拼合裁片组："; 

var checkbox1 =panel2.add("checkbox", undefined, undefined, {name: "checkbox1"}); 
    checkbox1.value = true; 
    checkbox1.text = "拼合"; 

/*
var statictext12 = panel2.add("statictext", undefined, undefined, {name: "statictext12"}); 
    statictext12.text = "有袋修改："; 

var checkbox2 =panel2.add("checkbox", undefined, undefined, {name: "checkbox2"}); 
    checkbox2.value = false; 
    checkbox2.text = "有袋";
    */
    
    
var statictext13 = panel2.add("statictext", undefined, undefined, {name: "statictext13"}); 
    statictext13.text = "存储位置："; 

var checkbox3 =panel2.add("checkbox", undefined, undefined, {name: "checkbox3"}); 
    checkbox3.value = false; 
    checkbox3.text = "模板位置";
    
    
// GROUP2
// ======
var group2 = dialog.add("group", undefined, {name: "group2"}); 
    group2.orientation = "column"; 
    group2.alignChildren = ["fill","top"]; 
    group2.spacing = 10; 
    group2.margins = 0; 

var ok = group2.add("button", undefined, undefined, {name: "ok"}); 
    ok.text = "执行"; 

var cancel = group2.add("button", undefined, undefined, {name: "cancel"}); 
    cancel.text = "取消"; 

var button3 = group2.add("button", undefined, undefined, {name: "button3"}); 
    button3.text = "关于我们"; 
button1.onClick=function(){
  
    button1.text =Folder.selectDialog ("大货裁片模板路径:").fsName;


}


button2.onClick=function(){
  
     button2.text  =Folder.selectDialog ("切片裁片路径选择:").fsName;
}
button3.onClick = function () {

  alert("自由花型工作室 17520145271 脚本开发 裁片排版 花型开发 ",dialog.text+"----关于我们");
}




ok .onClick=function(){

//~     //~ if (myEditText!="") {
var myFolder=new Folder(button1.text)
//打开文件夹中的每一个文件开始处理

var myFiles=myFolder.getFiles ("*.tif*")


for(i=0 ;i< myFiles.length;i++){
//开始处理每一个文件

  //断判是文件格式
 if(myFiles[i] instanceof File)
 app.open(myFiles[i]) 
var 款号面料=String (edittext1.text); //宽；
var 文件夹路径=button2.text
更换当前文档裁片组外链(文件夹路径)
图层选择()
activeDocument.activeLayer.textItem.contents=款号面料
选择裁片图层()
        if( checkbox1.value == true)
        {
            合并图层()
        }
        else
        {
          ;
        }

/*
        if( checkbox2.value == false)
        {
            无袋修改();

       }
        else
        {
        有袋修改();
        }
    
    */
    
      


    if( checkbox3.value == false)
        {
      另存为(文件夹路径,款号面料);

       }
        else
        {
        存储在原来位置(myFolder);
        }
    
    
    







activeDocument.close(SaveOptions.DONOTSAVECHANGES);
}

  alert("换图完成，请检查好文件进行打印大货！！！",dialog.text+"----关于");

 dialog.close();






function 更换当前文档裁片组外链(文件夹路径)
{
    try
    {
        裁片组 = app.activeDocument.layerSets.getByName("裁片").layers;
    }
    catch(e)
    {
           alert("找不到裁片组",dialog.text+"----提示");

    }

    for(var i=0;i<裁片组.length;i++)
    {
            裁片 = 裁片组[i];
            app.activeDocument.activeLayer = 裁片;
            if(裁片.kind == LayerKind.SMARTOBJECT)
            {
                更换链接智能对象路径(文件夹路径);
            }
    }
}


function 更换链接智能对象路径(文件夹路径)
{
    //获取当前图层外链的智能对象路径
    //先获取链接的文件名
    var r = new ActionReference();
    r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
    //~ r.putName(charIDToTypeID("Lyr "), "◆左袖口"); //按名称查找
    descLayer = executeActionGet(r);
    res = descLayer.getObjectValue(stringIDToTypeID("smartObject"));

    链接文件名 = res.getString(stringIDToTypeID("fileReference"));
    //$.writeln(链接文件名);

    //~ 链接文件路径 = res.getPath(stringIDToTypeID("link"));
    //~ $.writeln(链接文件路径);

    图片路径 = 文件夹路径 + "/" + 链接文件名;

    var d = new ActionDescriptor();
    d.putPath(stringIDToTypeID("null"), new File(图片路径));
    executeAction(stringIDToTypeID("placedLayerRelinkToFile"), d, DialogModes.NO);

}

function 另存为(文件夹路径,款号面料)
{
文档名称=activeDocument.name.replace(/(?:\.[^.]*$|$)/, '');
saveIn=File(文件夹路径+ "/"+文档名称+"-"+款号面料);
     tifSaveOpt = new TiffSaveOptions();
    tifSaveOpt.imageCompression = TIFFEncoding.TIFFLZW;
    tifSaveOpt.byteOrder = ByteOrder.IBM;
    asCopy=true
    app.activeDocument.saveAs(saveIn,tifSaveOpt,asCopy);
}




function 图层选择()	//
    {
    try {
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putName(stringIDToTypeID("layer"), "款号");
        d.putReference(stringIDToTypeID("null"), r);
        d.putBoolean(stringIDToTypeID("makeVisible"), false);
        var list = new ActionList();
        list.putInteger(74);
        d.putList(stringIDToTypeID("layerID"), list);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
        }
    catch (e) {      
        alert("找不到款号图层",dialog.text+"----关于");

    }
   }

///////////////////////////////////////////////////////////////////////////////




function 合并图层()	//合并图层
    {
 
        var d = new ActionDescriptor();
        executeAction(stringIDToTypeID("mergeLayersNew"), d, DialogModes.NO);
      
    }

function 选择裁片图层()	//
    {
    try {
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putName(stringIDToTypeID("layer"), "裁片");
        d.putReference(stringIDToTypeID("null"), r);
        d.putBoolean(stringIDToTypeID("makeVisible"), false);
        var list = new ActionList();
        list.putInteger(74);
        d.putList(stringIDToTypeID("layerID"), list);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
        }
    catch (e) {      
        alert("找不到裁片图层",dialog.text+"----关于");

    }


}

}


    
    

function 有袋修改()

{
选择点位()
 
 
 var 当前图层=app.activeDocument.activeLayer
 var 当前图层名称=当前图层.name
 if( 当前图层名称=="口袋点位")
 显示图层()


选择口袋遮挡()
     if( 当前图层名称=="口袋遮挡")
        隐藏图层遮挡()
         隐藏图层遮挡()
//  提示();	


}

function 无袋修改()
{
选择点位()
 var 当前图层=app.activeDocument.activeLayer
 var 当前图层名称=当前图层.name
 if( 当前图层名称=="口袋点位");
   隐藏口袋点位()
选择口袋遮挡();
if( 当前图层名称=="口袋遮挡");
显示图层();
 //提示();

}




function 选择点位()	//
    {
    try {
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putName(stringIDToTypeID("layer"), "口袋点位");
        d.putReference(stringIDToTypeID("null"), r);
        d.putBoolean(stringIDToTypeID("makeVisible"), false);
        var list = new ActionList();
        list.putInteger(32);
        d.putList(stringIDToTypeID("layerID"), list);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
        }
    catch (e) {
    }

}

function 显示图层()	//名称更改
    {
    try {
        var d = new ActionDescriptor();
        var list = new ActionList();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        list.putReference(r);
        d.putList(stringIDToTypeID("null"), list);
        executeAction(stringIDToTypeID("show"), d, DialogModes.NO);
        }
    catch (e) {
    }
 }



    





function 选择口袋遮挡()	//
    {
    try {
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putName(stringIDToTypeID("layer"), "口袋遮挡");
        d.putReference(stringIDToTypeID("null"), r);
        d.putBoolean(stringIDToTypeID("makeVisible"), false);
        var list = new ActionList();
        list.putInteger(32);
        d.putList(stringIDToTypeID("layerID"), list);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
        }
    catch (e) {
    }
}



function 隐藏图层遮挡()	//
    {
    try {
        var d = new ActionDescriptor();
        var list = new ActionList();
        var r = new ActionReference();
        r.putName(stringIDToTypeID("layer"), "口袋遮挡");
        list.putReference(r);
        d.putList(stringIDToTypeID("null"), list);
        executeAction(stringIDToTypeID("hide"), d, DialogModes.NO);
        }
    catch (e) {
    }

}

function 隐藏口袋点位()	//
    {
    try {
        var d = new ActionDescriptor();
        var list = new ActionList();
        var r = new ActionReference();
        r.putName(stringIDToTypeID("layer"), "口袋点位");
        list.putReference(r);
        d.putList(stringIDToTypeID("null"), list);
        executeAction(stringIDToTypeID("hide"), d, DialogModes.NO);
        }
    catch (e) {
    }

}





function 存储在原来位置(文件路径)
{
    tiffOptions = new TiffSaveOptions();

    try
    {
        app.activeDocument.saveAs(new File(文件路径), tiffOptions);
    }
    catch(e)
    {
        alert(文件太大无法保存)
    }
   }

dialog.show()

//给领海数码修改的by2023/6/19  景鸣
}
 ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////






















function 裁片射出模板() {
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

      var parts = 当前图层名称.split("-");
      if (parts.length > 0) {
        var 裁片名称 = parts[0];
        app.activeDocument = 主文档;
        前景色修改()
        初始化模板裁片名称 = 当前图层名称.split("-");
        初始化码数裁片名称 = 当前图层名称.split("_");
        大货组名称 = 初始化模板裁片名称[0] + "-大货裁片";
        实际裁片名称 = 初始化模板裁片名称[0] + "-" + 初始化码数裁片名称[2];

        var 空白裁片模板 = app.activeDocument.layerSets.getByName(大货组名称).layers.getByName(实际裁片名称);
        app.activeDocument.activeLayer = 空白裁片模板;

        载入选区();
        var 裁片 = app.activeDocument.layers.getByName(裁片名称);
        app.activeDocument.activeLayer = 裁片;
        主界面切换();
        添加图层蒙版();
        var 新名称 = "通码-" +当前图层名称;
        app.activeDocument.activeLayer.name = 新名称;
        复制到文档(新名称, 文档名称);
        历史记录回退();
        app.activeDocument = currentDocument;
        
           var 裁片名称 = 当前图层名称.split("_");

        if (裁片名称.length > 1) {
          var 角度信息 = 裁片名称[1];

          if (角度信息 === "180" || 角度信息 === "-180") {
            app.activeDocument.activeLayer.rotate(180);
          } else if (角度信息 === "-90") {
            逆时针90旋转();
          } else if (角度信息 === "90") {
            顺时针90旋转();
          } else {
            // 如果以上条件都不满足，则执行默认的代码
          }
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
       
      }
    }
烧花线添加();
空置图层()
查找通码图层2()
  }

  
  //alert("排版完成，请检查文件！！！");
  app.activeDocument = 主文档;
}



function 粘贴图层()	//粘贴图层
    {
   
        var d = new ActionDescriptor();
        executeAction(stringIDToTypeID("paste"), d, DialogModes.NO);
  

    }

function 空置图层()	//
    {

        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("selectNoLayers"), d, DialogModes.NO);

    }


function 获取当前图层信息() {
  var 当前图层 = app.activeDocument.activeLayer;
  var 底边 = 当前图层.bounds[3];
  var 上边 = 当前图层.bounds[1];
  var 高度 = 底边 - 上边;
  var 左边 = 当前图层.bounds[0];
  var 右边 = 当前图层.bounds[2];
  var 宽度 = 右边 - 左边;
  var 高度的一半 = 高度 / 2;
  var 宽度的一半 = 宽度 / 2;
  var 高度中心 = 上边 + 高度的一半;
  var 宽度中心 = 左边 + 宽度的一半;

  return {
    底边: 底边,
    上边: 上边,
    高度: 高度,
    左边: 左边,
    右边: 右边,
    宽度: 宽度,
    高度的一半: 高度的一半,
    宽度的一半: 宽度的一半,
    高度中心: 高度中心,
    宽度中心: 宽度中心
  };
}


function 复制图层()	//
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        var r1 = new ActionReference();
        r1.putName(stringIDToTypeID("document"), "M.psd");
        d.putReference(stringIDToTypeID("to"), r1);
        d.putString(stringIDToTypeID("name"), "P1");
        d.putInteger(stringIDToTypeID("version"), 5);
        var list = new ActionList();
        list.putInteger(12);
        d.putList(stringIDToTypeID("ID"), list);
        executeAction(stringIDToTypeID("duplicate"), d, DialogModes.NO);
      
    }


function 复制图层()	//复制图层
    {
  
        var d = new ActionDescriptor();
        executeAction(stringIDToTypeID("copyEvent"), d, DialogModes.NO);
   
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




function 图层选择2(新图层名称)	//
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putName(stringIDToTypeID("layer"), 新图层名称);
        d.putReference(stringIDToTypeID("null"), r);
        d.putBoolean(stringIDToTypeID("makeVisible"), false);
        var list = new ActionList();
        list.putInteger(6);
        d.putList(stringIDToTypeID("layerID"), list);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
     
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

function  切换图层蒙版()	//
    {
 
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("channel"), stringIDToTypeID("channel"), stringIDToTypeID("mask"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putBoolean(stringIDToTypeID("makeVisible"), false);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
   
   
    }


function 主界面切换() {
    var d = new ActionDescriptor();
    var r = new ActionReference();
    r.putEnumerated(stringIDToTypeID("channel"), stringIDToTypeID("channel"), stringIDToTypeID("CMYK"));
    d.putReference(stringIDToTypeID("null"), r);
    d.putBoolean(stringIDToTypeID("makeVisible"), false);
    executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
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
        r.putOffset(stringIDToTypeID("historyState"), -3);
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


function 查找通码图层2() {
	
app.activeDocument.suspendHistory("印花图层打包", "查找通码图层()");
}

function 查找通码图层() {





function 查找通码图层() {
  var 当前文档 = app.activeDocument;
  var 包含通码的图层数组 = [];

  for (var i = 0; i < 当前文档.layers.length; i++) {
    var 图层 = 当前文档.layers[i];
    if (图层.name.indexOf("通码") !== -1) {
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
      




    function 下摆对齐2() {
        
    app.activeDocument.suspendHistory("下摆对齐", "下摆对齐()");
}
 
 function 下摆对齐() {
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
获取到花样图层当前居中领口y坐标信息 = 领窝边距.bottom;
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
裁片位置坐标y=裁片位置坐标.bottom
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