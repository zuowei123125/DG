dxf8_jscode = """











function 批量化替换外链新(){

var dialog = new Window("dialog"); 
    dialog.text = "批量快速换图 "; 
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
    statictext1.text = "大货齐码裁片模板路径:"; 

var button1 = panel1.add("button", undefined, undefined, {name: "button1"}); 
    button1.text = "路径选择"; 
    button1.preferredSize.width = 300; 

var statictext2 = panel1.add("statictext", undefined, undefined, {name: "statictext2"}); 
    statictext2.text = "待套花样路径选择:"; 

var button2 = panel1.add("button", undefined, undefined, {name: "button2"}); 
    button2.text = "路径选择"; 
    button2.preferredSize.width = 300; 


var statictext3 = panel1.add("statictext", undefined, undefined, {name: "statictext3"}); 
    statictext3.text = "缓存切片裁片路径选择:"; 

var button3 = panel1.add("button", undefined, undefined, {name: "button3"}); 
    button3.text = "路径选择"; 
    button3.preferredSize.width = 300; 

var statictext4= panel1.add("statictext", undefined, undefined, {name: "statictext4"}); 
    statictext4.text = "大货成品路径选择:"; 

var button4 = panel1.add("button", undefined, undefined, {name: "button4"}); 
    button4.text = "路径选择"; 
    button4.preferredSize.width = 300; 

// PANEL2
// ======
var panel2 = panel1.add("panel", undefined, undefined, {name: "panel2"}); 
    panel2.text = "款号修改："; 
    panel2.orientation = "column"; 
    panel2.alignChildren = ["left","top"]; 
    panel2.spacing = 10; 
    panel2.margins = 10; 



// PANEL4
// ======


var statictext11 = panel2.add("statictext", undefined, undefined, {name: "statictext11"}); 
    statictext11.text = "是否拼合裁片组："; 

var checkbox1 =panel2.add("checkbox", undefined, undefined, {name: "checkbox1"}); 
    checkbox1.value = true; 
    checkbox1.text = "拼合"; 

    
    
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

var button8 = group2.add("button", undefined, undefined, {name: "button8"}); 
    button8.text = "关于我们"; 
    
button1.onClick=function(){
  
    button1.text =Folder.selectDialog ("大货齐码裁片模板路径:").fsName;


}


button2.onClick=function(){
  
     button2.text  =Folder.selectDialog ("待套花样路径选择:").fsName;
     
  }   
 button3.onClick=function(){
  
     button3.text  =Folder.selectDialog ("缓存切片裁片路径选择:").fsName;
     
         
    } 
   button4.onClick=function(){
  
     button4.text  =Folder.selectDialog ("大货成品路径选择:").fsName;
     
         
    } 
        


button8.onClick = function () {

alert("自由花型工作室 17520145271 脚本开发 裁片排版 花型开发 ",dialog.text+"----关于我们");
}






ok .onClick=function(){


                var 大货齐码裁片模板路径 = new Folder(button1.text);
                var 待套花样路径选择 =new Folder(button2.text);
                var 大货文件存放位置 =new Folder(button4.text);
                var 缓存切片裁片路径选择 = new Folder(button3.text);

                var myFiles1 =大货齐码裁片模板路径.getFiles("*.tif*");
                var myFiles2 =待套花样路径选择.getFiles("*.tif*");
      
                    
          




for (var i = 0; i <myFiles2.length; i++) 
{

     app.open(myFiles2[i])
   文档名称1=activeDocument.name.replace(/(?:\.[^.]*$|$)/, '');
    var 大货成品文件夹 =文档名称1
    花样标准化(130);
    文档另存(缓存切片裁片路径选择);
   app.activeDocument.close(SaveOptions.DONOTSAVECHANGES)
  
  
 var parentFolderPath =大货文件存放位置
var folderNames = 文档名称1

var folderPath = parentFolderPath + "/" + 文档名称1;
var folderObj = new Folder(folderPath);
$.writeln(folderObj);
folderObj.create();


     for (var j = 0; j <myFiles1.length; j++) {
    app.open(myFiles1[j])
    

    更换当前文档裁片组外链(缓存切片裁片路径选择);
    图层选择();
    app.activeDocument.activeLayer.textItem.contents = 文档名称1;
    选择裁片图层();
   
   // if (checkbox1.value == true) {
      合并图层();
另存为(folderObj,文档名称1)



    
    app.activeDocument.close(SaveOptions.DONOTSAVECHANGES);
  }
}

 









function 更换当前文档裁片组外链(缓存切片裁片路径选择)
{
    try
    {
        裁片组 = app.activeDocument.layerSets.getByName("裁片").layers;
    }
    catch(e)
    {
           alert("找不到裁片组");

    }

    for(var k=0;k<裁片组.length;k++)
    {
            裁片 = 裁片组[k];
            app.activeDocument.activeLayer = 裁片;
            if(裁片.kind == LayerKind.SMARTOBJECT)
            {
                更换链接智能对象路径(缓存切片裁片路径选择);
            }
    }
}


function 更换链接智能对象路径(缓存切片裁片路径选择)
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

    图片路径 = 缓存切片裁片路径选择 + "/" + 链接文件名;

    var d = new ActionDescriptor();
    d.putPath(stringIDToTypeID("null"), new File(图片路径));
    executeAction(stringIDToTypeID("placedLayerRelinkToFile"), d, DialogModes.NO);

}

function 另存为(folderObj,文档名称1)
{
文档名称=activeDocument.name.replace(/(?:\.[^.]*$|$)/, '');
saveIn=File(folderObj+ "/"+文档名称1+"-"+文档名称);
     tifSaveOpt = new TiffSaveOptions();
    tifSaveOpt.imageCompression = TIFFEncoding.TIFFLZW;
    tifSaveOpt.byteOrder = ByteOrder.IBM;
    asCopy=true
    app.activeDocument.saveAs(saveIn,tifSaveOpt,asCopy);
}




function 图层选择()	//a
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




function 存储在原来位置(myFolder)
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

function 花样标准化(扩展毫米数)
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

 }




function 文档另存(缓存切片裁片路径选择){
  
      var 导出目录 =缓存切片裁片路径选择;
      var  裁片组 = app.activeDocument.layerSets;



    for(var i=0;i<裁片组.length;i++)
    {

        app.activeDocument.duplicate("temp");

        复制文档裁片组 = app.activeDocument.layerSets;
        当前裁片组 = 复制文档裁片组[i];
        当前裁片组名 = 当前裁片组.name;
        花样图层 = 当前裁片组.layers[0];
        裁片图层 = 当前裁片组.layers[1];

        app.activeDocument.activeLayer = 花样图层;
        //把花样图层导出
        花样图层.grouped = false; //取消图层链接

        仅当前图层可见();

        //按花样图层大小裁剪文档
        app.activeDocument.crop(花样图层.bounds,0);

        //拼合图像只保留花样图层
        var d = new ActionDescriptor();
        executeAction(stringIDToTypeID("flattenImage"), d, DialogModes.NO);

        //保存为TIF
        var 文件路径 = 导出目录 + "/" + 当前裁片组名 + ".tif";
        tiffOptions = new TiffSaveOptions();
        app.activeDocument.saveAs(new File(文件路径), tiffOptions);
        app.activeDocument.close(SaveOptions.DONOTSAVECHANGES);
            
              }     



function 仅当前图层可见()
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

}
}

dialog.show()




}


/////////////////////////////////////////////////////////////////////////////////////////

// 检查是否有打开的文档

    function 码标添加2() {
        
    app.activeDocument.suspendHistory("码标添加", "码标放置()");
}


function 码标放置() {
app.activeDocument.layerSets.add().name = "码标";

app.preferences.rulerUnits = Units.PIXELS;
if (app.documents.length > 0) {
    var doc = app.activeDocument; // 获取当前文档

    // 查找名为"裁片"的组
    var cropGroup = doc.layerSets.getByName("裁片"); // 将“裁片”替换为您的组名称

    if (cropGroup) {
        // 遍历裁片组内的所有图层
        for (var i = 0; i < cropGroup.layers.length; i++) {
            var layer = cropGroup.layers[i];
            //alert("图层名称: " + layer.name);
         当前图层名称=layer.name
         parts = layer.name.split("_")
            // alert(parts[2])
         大货成品图层 = app.activeDocument.layerSets.getByName("裁片").layers.getByName(当前图层名称);
          app.activeDocument.activeLayer = 大货成品图层;
          切换mask();
         
          载入选区蒙版()
          大货成品图层边距 = 获取当前选区四边距();
          右边距=大货成品图层边距.right
       
   var currentDocument = app.activeDocument;         
  var height = currentDocument.height.value;        
  var 上边距新 = 0;
  var 左边距新 = 右边距 - 1;
  var 下边距新 = height;
  var 右边距新 = 右边距 + 1;
  新建选区(上边距新, 左边距新, 下边距新, 右边距新);
      选取交叉()	   
获取码标记点 = 获取当前选区四边距();     
码标记点下标记 = 获取码标记点.bottom
码标记点左标记 = 获取码标记点.left
码标x中心坐标=码标记点左标记
码标y中心坐标=码标记点下标记
$.writeln(码标x中心坐标);
$.writeln(码标y中心坐标);
 载入选区蒙版()
 收缩45像素()
   收缩45像素成品图层边距 = 获取当前选区四边距();
   收缩45像素右边距=收缩45像素成品图层边距.right
 var 收缩45像素上边距新 = 0;
  var 收缩45像素左边距新 = 0 ;
  var 收缩45像素下边距新 = height;
  var 收缩45像素右边距新 = 收缩45像素右边距-1 ;
 //$.writeln(收缩45像素上边距新);
 //$ .writeln(收缩45像素左边距新);
 //$.writeln(收缩45像素下边距新);
 //$.writeln(收缩45像素右边距新);
  减去选区(收缩45像素上边距新, 收缩45像素左边距新, 收缩45像素下边距新, 收缩45像素右边距新);
    //选取交叉()	   
    收缩45像素获取码标记点 = 获取当前选区四边距();    
    收缩45像素码标记点y标记 = 收缩45像素获取码标记点.bottom
    收缩45像素码标记点x标记 = 收缩45像素获取码标记点.left
  $.writeln(收缩45像素码标记点x标记);
$.writeln(收缩45像素码标记点y标记);

获取中心点1=获取中心点(收缩45像素码标记点x标记, 收缩45像素码标记点y标记, 码标x中心坐标, 码标y中心坐标)
$.writeln("中心点坐标: x = " + 获取中心点1.x + ", y = " + 获取中心点1.y);


var 码标高度转毫米y = pixelsToMillimeters(获取中心点1.y);
var 码标宽度转毫米x = pixelsToMillimeters(获取中心点1.x );

//alert(码标高度转毫米)
//alert(码标宽度转毫米)
var fileName = currentDocument.name;

// 去掉文件名的后缀名
var fileNameWithoutExtension = fileName.split('.').slice(0, -1).join('.');
var textLayer = currentDocument.artLayers.add();
textLayer.kind = LayerKind.TEXT;

// 设置文本图层的文本内容
textLayer.textItem.contents = fileNameWithoutExtension
textLayer.textItem.size = 10
var cmykColor = new SolidColor();
cmykColor.cmyk.cyan = 50;     // 青色通道值
cmykColor.cmyk.magenta = 40;  // 品红色通道值
cmykColor.cmyk.yellow = 50;  // 黄色通道值
cmykColor.cmyk.black = 70;    // 黑色通道值

// 将文本图层的颜色设置为上面创建的CMYK颜色
textLayer.textItem.color = cmykColor;

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


//app.activeDocument.activeLayer.translate(Number(当前图层的宽度中心) - Number(码标宽度转毫米), Number(当前图层的高度中心) - Number(码标高度转毫米));

app.activeDocument.activeLayer.translate(Number(码标宽度转毫米x) - Number(当前图层的宽度中心), Number(码标高度转毫米y) - Number(当前图层的高度中心));
app.preferences.rulerUnits = Units.PIXELS;
app.activeDocument.activeLayer.move(app.activeDocument.layerSets.getByName("码标"), ElementPlacement.INSIDE);


        }
    } else {
        alert("找不到名为“裁片”的组。");
    }
} else {
    alert("没有打开的文档。");
}
码标 = app.activeDocument.layerSets.getByName("码标")
app.activeDocument.activeLayer = 码标;
描边()
}


function 减去选区(上边距, 左边距, 下边距, 右边距)	//
    {
    
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("channel"), stringIDToTypeID("selection"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        d1.putUnitDouble(stringIDToTypeID("top"), stringIDToTypeID("pixelsUnit"), 上边距);
        d1.putUnitDouble(stringIDToTypeID("left"), stringIDToTypeID("pixelsUnit"), 左边距);
        d1.putUnitDouble(stringIDToTypeID("bottom"), stringIDToTypeID("pixelsUnit"), 下边距);
        d1.putUnitDouble(stringIDToTypeID("right"), stringIDToTypeID("pixelsUnit"), 右边距);
        d.putObject(stringIDToTypeID("to"), stringIDToTypeID("rectangle"), d1);
        executeAction(stringIDToTypeID("subtractFrom"), d, DialogModes.NO);
        }



function 收缩45像素()	//
    {
    
        var d = new ActionDescriptor();
        d.putUnitDouble(stringIDToTypeID("by"), stringIDToTypeID("pixelsUnit"), 45);
        d.putBoolean(stringIDToTypeID("selectionModifyEffectAtCanvasBounds"), false);
        executeAction(stringIDToTypeID("contract"), d, DialogModes.NO);
        }
    
    
    

function 获取中心点(x1, y1, x2, y2) {
    var centerX = (x1 + x2) / 2;
    var centerY = (y1 + y2) / 2;
    return { x: centerX, y: centerY };
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

function 选择组()	//
    {
    
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putName(stringIDToTypeID("layer"), "码标");
        d.putReference(stringIDToTypeID("null"), r);
        d.putBoolean(stringIDToTypeID("makeVisible"), false);
        var list = new ActionList();
        list.putInteger(153);
        d.putList(stringIDToTypeID("layerID"), list);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
   
    }
function 合并组()	//合并组
    {
 
        var d = new ActionDescriptor();
        executeAction(stringIDToTypeID("mergeLayersNew"), d, DialogModes.NO);
     
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

function 描边()	//描边
    {
    
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("property"), stringIDToTypeID("layerEffects"));
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        d1.putUnitDouble(stringIDToTypeID("scale"), stringIDToTypeID("percentUnit"), 208.333290947808);
        var d2 = new ActionDescriptor();
        d2.putBoolean(stringIDToTypeID("enabled"), true);
        d2.putBoolean(stringIDToTypeID("present"), true);
        d2.putBoolean(stringIDToTypeID("showInDialog"), true);
        d2.putEnumerated(stringIDToTypeID("style"), stringIDToTypeID("frameStyle"), stringIDToTypeID("outsetFrame"));
        d2.putEnumerated(stringIDToTypeID("paintType"), stringIDToTypeID("frameFill"), stringIDToTypeID("solidColor"));
        d2.putEnumerated(stringIDToTypeID("mode"), stringIDToTypeID("blendMode"), stringIDToTypeID("normal"));
        d2.putUnitDouble(stringIDToTypeID("opacity"), stringIDToTypeID("percentUnit"), 100);
        d2.putUnitDouble(stringIDToTypeID("size"), stringIDToTypeID("pixelsUnit"), 2);
        var d3 = new ActionDescriptor();
        d3.putDouble(stringIDToTypeID("cyan"), 0);
        d3.putDouble(stringIDToTypeID("magenta"), 0);
        d3.putDouble(stringIDToTypeID("yellowColor"), 0);
        d3.putDouble(stringIDToTypeID("black"), 0);
        d2.putObject(stringIDToTypeID("color"), stringIDToTypeID("CMYKColorClass"), d3);
        d2.putBoolean(stringIDToTypeID("overprint"), false);
        d1.putObject(stringIDToTypeID("frameFX"), stringIDToTypeID("frameFX"), d2);
        d.putObject(stringIDToTypeID("to"), stringIDToTypeID("layerEffects"), d1);
        executeAction(stringIDToTypeID("set"), d, DialogModes.NO);
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


function 选取交叉()	//
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





function 批量分辨率修改() {

var dialog = new Window("dialog"); 
dialog.text = "批量分辨率修改"; 
dialog.orientation = "row"; 
dialog.alignChildren = ["left","top"]; 
dialog.spacing = 10; 
dialog.margins = 16; 

// GROUP1
// ======
var group1 = dialog.add("group", undefined, {name: "group1"}); 
group1.orientation = "column"; 
group1.alignChildren = ["fill","top"]; 
group1.spacing = 10; 
group1.margins = 0; 

// PANEL1
// ======
var panel1 = group1.add("panel", undefined, undefined, {name: "panel1"}); 
panel1.text = "分辨率修改"; 
panel1.preferredSize.height = 100; 
panel1.orientation = "column"; 
panel1.alignChildren = ["left","top"]; 
panel1.spacing = 10; 
panel1.margins = 10; 

var statictext1 = panel1.add("statictext", undefined, undefined, {name: "statictext1"}); 

// GROUP2
// ======
var group2 = panel1.add("group", undefined, {name: "group2"}); 
group2.orientation = "row"; 
group2.alignChildren = ["left","center"]; 
group2.spacing = 10; 
group2.margins = 0; 

var edittext1 = group2.add('edittext {properties: {name: "edittext1"}}'); 
edittext1.preferredSize.width = 60; 

// GROUP1
// ======
var statictext2 = group1.add("group", undefined , {name: "statictext2"}); 

statictext2.orientation = "column"; 
statictext2.alignChildren = ["left","center"]; 
statictext2.spacing = 0; 

statictext2.add("statictext", undefined, ""); 
statictext2.add("statictext", undefined, "微信：17520145271"); 
statictext2.add("statictext", undefined, "软件开发 脚本开发"); 
statictext2.add("statictext", undefined, "by:jimi"); 

// GROUP3
// ======
var group3 = dialog.add("group", undefined, {name: "group3"}); 
group3.orientation = "column"; 
group3.alignChildren = ["fill","top"]; 
group3.spacing = 10; 
group3.margins = 0; 

var ok = group3.add("button", undefined, undefined, {name: "ok"}); 
ok.text = "执行"; 

var cancel = group3.add("button", undefined, undefined, {name: "cancel"}); 
cancel.text = "取消"; 

// 设置"执行"按钮的点击事件处理程序
ok.onClick = function() {
  var resolutionText = edittext1.text;
  var resolution = parseInt(resolutionText);

  if (!isNaN(resolution)) {
    // 获取所有打开的文档
var docs = app.documents;

// 遍历文档并输出它们的名称
for (var i = 0; i < docs.length; i++) {
  var doc = docs[i];
   app.activeDocument=doc

  var docName = doc.name;
  $.writeln("文档名称: " + docName);
    图像大小(resolution)
}
    
    // 关闭对话框
    dialog.close();
  } else {
    alert('请输入有效的分辨率值');
  }
};
function 图像大小(resolution)	//图像大小
    {

        var d = new ActionDescriptor();
        d.putUnitDouble(stringIDToTypeID("resolution"), stringIDToTypeID("densityUnit"), resolution);
        d.putBoolean(stringIDToTypeID("scaleStyles"), true);
        d.putBoolean(stringIDToTypeID("constrainProportions"), true);
        d.putEnumerated(charIDToTypeID("Intr"), stringIDToTypeID("interpolationType"), stringIDToTypeID("nearestNeighbor"));
        executeAction(stringIDToTypeID("imageSize"), d, DialogModes.NO);
    
    }


// 设置"取消"按钮的点击事件处理程序
cancel.onClick = function() {
  // 关闭对话框
  dialog.close();
};

dialog.show();
}




function 批量款号添加() {

var dialog = new Window("dialog"); 
dialog.text = "批量款号添加"; 
dialog.orientation = "row"; 
dialog.alignChildren = ["left","top"]; 
dialog.spacing = 10; 
dialog.margins = 16; 

// GROUP1
// ======
var group1 = dialog.add("group", undefined, {name: "group1"}); 
group1.orientation = "column"; 
group1.alignChildren = ["fill","top"]; 
group1.spacing = 10; 
group1.margins = 0; 

// PANEL1
// ======
var panel1 = group1.add("panel", undefined, undefined, {name: "panel1"}); 
panel1.text = "款号添加"; 
panel1.preferredSize.height = 100; 
panel1.orientation = "column"; 
panel1.alignChildren = ["left","top"]; 
panel1.spacing = 10; 
panel1.margins = 10; 

var statictext1 = panel1.add("statictext", undefined, undefined, {name: "statictext1"}); 

// GROUP2
// ======
var group2 = panel1.add("group", undefined, {name: "group2"}); 
group2.orientation = "row"; 
group2.alignChildren = ["left","center"]; 
group2.spacing = 10; 
group2.margins = 0; 

var edittext1 = group2.add('edittext {properties: {name: "edittext1"}}'); 
edittext1.preferredSize.width = 60; 

// GROUP1
// ======
var statictext2 = group1.add("group", undefined , {name: "statictext2"}); 
 
statictext2.orientation = "column"; 
statictext2.alignChildren = ["left","center"]; 
statictext2.spacing = 0; 

statictext2.add("statictext", undefined, ""); 
statictext2.add("statictext", undefined, "微信：17520145271"); 
statictext2.add("statictext", undefined, "软件开发 脚本开发"); 
statictext2.add("statictext", undefined, "by:jimi"); 

// GROUP3
// ======
var group3 = dialog.add("group", undefined, {name: "group3"}); 
group3.orientation = "column"; 
group3.alignChildren = ["fill","top"]; 
group3.spacing = 10; 
group3.margins = 0; 

var ok = group3.add("button", undefined, undefined, {name: "ok"}); 
ok.text = "执行"; 

var cancel = group3.add("button", undefined, undefined, {name: "cancel"}); 
cancel.text = "取消"; 

// 设置"执行"按钮的点击事件处理程序
ok.onClick = function() {
  var inputText = edittext1.text;

  // 获取所有打开的文档
  var docs = app.documents;

  // 遍历文档并在每个文档中创建新的文字图层并添加文本
  for (var i = 0; i < docs.length; i++) {
    var doc = docs[i];
    app.activeDocument = doc;

    // 在文档中创建新的文字图层并添加文本
   var textLayer = doc.artLayers.add();
        textLayer.kind = LayerKind.TEXT;
        textLayer.textItem.contents = inputText;
        textLayer.textItem.size = 80; // 将字体大小设置为80

        // 设置文本颜色
        var textColor = new SolidColor();
        textColor.rgb.red = 255; // 红色值 (0-255)
        textColor.rgb.green = 0;   // 绿色值 (0-255)
        textColor.rgb.blue = 0;    // 蓝色值 (0-255)
        textLayer.textItem.color = textColor;

        // 重命名图层
        app.activeDocument.activeLayer.name = "款号";

    
    
  }

  // 关闭对话框
  dialog.close();
};

// 设置"取消"按钮的点击事件处理程序
cancel.onClick = function() {
  // 关闭对话框
  dialog.close();
};



dialog.show();
}








//  photoshopscripts.wordpress.com

////////////////////////////////////
//       Split to Layers 1.0      //
//       2012, David Jensen       //
//                                //
//         With help from         //
//   pfaffenbichler and xbytor    //
//        at ps-scripts.com       //

#target photoshop
 function 图像分割() {
//更改以下 5 个值中的任何一个以自定义脚本的默认选项:

var showOptionsDialog = true; //设置为 false 以禁用对用户的提示.
var tolerance = 2;            // 将被忽略的透明像素的最大间隙，设置默认值.
var confirmThreshold = 20;    // 如果脚本要制作大量图层，提示用户确认这是可以的.
var suffix = ""          // 将此添加到新图层的图层名称中.  设置为空不添加.
var addCount = true;          // 在每个新层的末尾添加一个增量数字.


///////////////////////////////////////
///////////////////////////////////////
///////////////////////////////////////
///////////////////////////////////////
///////////////////////////////////////
var layerNamePreview=activeDocument.activeLayer.name + suffix;
if (addCount === true){
    layerNamePreview += "1";
}

var originalRulerUnits = app.preferences.rulerUnits;
app.preferences.rulerUnits = Units.POINTS;

bounds = activeDocument.activeLayer.bounds
var emptyLayer=false;
if (Number(bounds[0]) == 0 && Number(bounds[1]) == 0 && Number(bounds[2]) == 0 && Number(bounds[3]) == 0) {emptyLayer = true};

try{
    if (activeDocument.activeLayer.kind != undefined && activeDocument.activeLayer.isBackgroundLayer == false && emptyLayer == false){
        activeDocument.suspendHistory("图层分割", "main()");
    }else{
        alert( "未选择支持的图层类型.");
    }
}catch(err){
    alert(err)
}

app.preferences.rulerUnits = originalRulerUnits;

function main() {
        
    var ok=createDialog();
    if (ok===2){
        activeDocument.selection.deselect()
        return false;
    }
    baseLayer=activeDocument.activeLayer;
    activeDocument.quickMaskMode = false;
    activeDocument.selection.deselect()
    var layerName = activeDocument.activeLayer.name
    //if a selection can't be made, stop running the script
  
 
    var idCpTL = charIDToTypeID("CpTL");
    executeAction(idCpTL, undefined, DialogModes.NO);
    
    activeDocument.activeLayer.rasterize(RasterizeType.ENTIRELAYER)
    try{
        var idDlt = charIDToTypeID( "Dlt " );
        var desc120 = new ActionDescriptor();
        var idnull = charIDToTypeID( "null" );
        var ref112 = new ActionReference();
        var idChnl = charIDToTypeID( "Chnl" );
        var idChnl = charIDToTypeID( "Chnl" );
        var idMsk = charIDToTypeID( "Msk " );
        ref112.putEnumerated( idChnl, idChnl, idMsk );
        desc120.putReference( idnull, ref112 );
        var idAply = charIDToTypeID( "Aply" );
        desc120.putBoolean( idAply, true );
        executeAction( idDlt, desc120, DialogModes.NO );
    }catch(e){}
    
    
    
    activeDocument.activeLayer.name = layerName

    baseLayer=activeDocument.activeLayer


    
    makeSelection()

    var idMk = charIDToTypeID("Mk  ");
    var desc642 = new ActionDescriptor();
    var idNw = charIDToTypeID("Nw  ");
    var idDcmn = charIDToTypeID("Dcmn");
    desc642.putClass(idNw, idDcmn);
    var idUsng = charIDToTypeID("Usng");
    var ref535 = new ActionReference();
    var idChnl = charIDToTypeID("Chnl");
    var idOrdn = charIDToTypeID("Ordn");
    var idTrgt = charIDToTypeID("Trgt");
    ref535.putEnumerated(idChnl, idOrdn, idTrgt);
    desc642.putReference(idUsng, ref535);
    executeAction(idMk, desc642, DialogModes.NO);

    newDoc = activeDocument
    // =======================================================
    activeDocument.resizeImage("200%", "200%", undefined, ResampleMethod.NEARESTNEIGHBOR)

    // =======================================================
    var idsetd = charIDToTypeID("setd");
    var desc934 = new ActionDescriptor();
    var idnull = charIDToTypeID("null");
    var ref535 = new ActionReference();
    var idChnl = charIDToTypeID("Chnl");
    var idfsel = charIDToTypeID("fsel");
    ref535.putProperty(idChnl, idfsel);
    desc934.putReference(idnull, ref535);
    var idT = charIDToTypeID("T   ");
    var ref536 = new ActionReference();
    var idChnl = charIDToTypeID("Chnl");
    var idOrdn = charIDToTypeID("Ordn");
    var idTrgt = charIDToTypeID("Trgt");
    ref536.putEnumerated(idChnl, idOrdn, idTrgt);
    desc934.putReference(idT, ref536);
    executeAction(idsetd, desc934, DialogModes.NO);


    var idMk = charIDToTypeID("Mk  ");
    var desc403 = new ActionDescriptor();
    var idnull = charIDToTypeID("null");
    var ref288 = new ActionReference();
    var idPath = charIDToTypeID("Path");
    ref288.putClass(idPath);
    desc403.putReference(idnull, ref288);
    var idFrom = charIDToTypeID("From");
    var ref289 = new ActionReference();
    var idcsel = charIDToTypeID("csel");
    var idfsel = charIDToTypeID("fsel");
    var idfsel = charIDToTypeID("fsel");
    ref289.putProperty(idcsel, idfsel);
    desc403.putReference(idFrom, ref289);
    var idTlrn = charIDToTypeID("Tlrn");
    var idPxl = charIDToTypeID("#Pxl");
    desc403.putUnitDouble(idTlrn, idPxl, 0.500000);
    executeAction(idMk, desc403, DialogModes.NO);
    
    var subPathsLength = activeDocument.pathItems[0].subPathItems.length
    
    if (subPathsLength>confirmThreshold){
        var answer = confirm("基于"+subPathsLength+ "个拆分对象将创建图层. 你想继续吗?",true)
        if (answer === false){
            newDoc.close(SaveOptions.DONOTSAVECHANGES);
            activeDocument.quickMaskMode = false;
            activeDocument.selection.deselect();
            return 0;
        }
    
    }

    // =======================================================
    activeDocument.resizeImage("50%", "50%", undefined, ResampleMethod.NEARESTNEIGHBOR)

    var pathInfo = collectPathInfoFromDesc(activeDocument, activeDocument.pathItems[activeDocument.pathItems.length - 1])
    
    // =======================================================
    newDoc.close(SaveOptions.DONOTSAVECHANGES)

    // =======================================================
    activeDocument.quickMaskMode = false

    // =======================================================
    //make channel
    // =======================================================
    var idMk = charIDToTypeID("Mk  ");
    var desc6 = new ActionDescriptor();
    var idNw = charIDToTypeID("Nw  ");
    var desc7 = new ActionDescriptor();
    var idNm = charIDToTypeID("Nm  ");
    desc7.putString(idNm, "ContiguityMask");
    var idClrI = charIDToTypeID("ClrI");
    var idMskI = charIDToTypeID("MskI");
    var idMskA = charIDToTypeID("MskA");
    desc7.putEnumerated(idClrI, idMskI, idMskA);
    var idClr = charIDToTypeID("Clr ");
    var desc8 = new ActionDescriptor();
    var idRd = charIDToTypeID("Rd  ");
    desc8.putDouble(idRd, 255.000000);
    var idGrn = charIDToTypeID("Grn ");
    desc8.putDouble(idGrn, 0.000000);
    var idBl = charIDToTypeID("Bl  ");
    desc8.putDouble(idBl, 0.000000);
    var idRGBC = charIDToTypeID("RGBC");
    desc7.putObject(idClr, idRGBC, desc8);
    var idOpct = charIDToTypeID("Opct");
    desc7.putInteger(idOpct, 50);
    var idChnl = charIDToTypeID("Chnl");
    desc6.putObject(idNw, idChnl, desc7);
    var idUsng = charIDToTypeID("Usng");
    var ref5 = new ActionReference();
    var idChnl = charIDToTypeID("Chnl");
    var idfsel = charIDToTypeID("fsel");
    ref5.putProperty(idChnl, idfsel);
    desc6.putReference(idUsng, ref5);
    executeAction(idMk, desc6, DialogModes.NO);


    var layerCount = 1
    for (i = 0; i < subPathsLength; i++) {
        //deselect
        var idsetd = charIDToTypeID("setd");
        var desc279 = new ActionDescriptor();
        var idnull = charIDToTypeID("null");
        var ref137 = new ActionReference();
        var idChnl = charIDToTypeID("Chnl");
        var idfsel = charIDToTypeID("fsel");
        ref137.putProperty(idChnl, idfsel);
        desc279.putReference(idnull, ref137);
        var idT = charIDToTypeID("T   ");
        var idOrdn = charIDToTypeID("Ordn");
        var idNone = charIDToTypeID("None");
        desc279.putEnumerated(idT, idOrdn, idNone);
        executeAction(idsetd, desc279, DialogModes.NO);
        ///select alpha channel
        var idslct = charIDToTypeID("slct");
        var desc315 = new ActionDescriptor();
        var idnull = charIDToTypeID("null");
        var ref175 = new ActionReference();
        var idChnl = charIDToTypeID("Chnl");
        ref175.putName(idChnl, "ContiguityMask");
        desc315.putReference(idnull, ref175);
        executeAction(idslct, desc315, DialogModes.NO);
        //use magic wand
        var idsetd = charIDToTypeID("setd");
        var desc263 = new ActionDescriptor();
        var idnull = charIDToTypeID("null");
        var ref123 = new ActionReference();
        var idChnl = charIDToTypeID("Chnl");
        var idfsel = charIDToTypeID("fsel");
        ref123.putProperty(idChnl, idfsel);
        desc263.putReference(idnull, ref123);
        var idT = charIDToTypeID("T   ");
        var desc264 = new ActionDescriptor();
        var idHrzn = charIDToTypeID("Hrzn");
        var idRlt = charIDToTypeID("#Rlt");
        desc264.putUnitDouble(idHrzn, idRlt, pathInfo[i][0][0]);
        var idVrtc = charIDToTypeID("Vrtc");
        var idRlt = charIDToTypeID("#Rlt");

        desc264.putUnitDouble(idVrtc, idRlt, pathInfo[i][0][1]);
        var idPnt = charIDToTypeID("Pnt ");
        desc263.putObject(idT, idPnt, desc264);
        var idTlrn = charIDToTypeID("Tlrn");
        desc263.putInteger(idTlrn, 1);
        executeAction(idsetd, desc263, DialogModes.NO);

        var idslct = charIDToTypeID("slct");
        var desc346 = new ActionDescriptor();
        var idnull = charIDToTypeID("null");
        var ref205 = new ActionReference();
        var idChnl = charIDToTypeID("Chnl");
        var idChnl = charIDToTypeID("Chnl");
        var idRGB = charIDToTypeID("RGB ");
        ref205.putEnumerated(idChnl, idChnl, idRGB);
        desc346.putReference(idnull, ref205);
        var idMkVs = charIDToTypeID("MkVs");
        desc346.putBoolean(idMkVs, false);
        executeAction(idslct, desc346, DialogModes.NO);




        try {
            // =======================================================
            var idCpTL = charIDToTypeID("CpTL");
            executeAction(idCpTL, undefined, DialogModes.NO);

            try {
                var idrasterizeLayer = stringIDToTypeID("rasterizeLayer");
                var desc924 = new ActionDescriptor();
                var idnull = charIDToTypeID("null");
                var ref721 = new ActionReference();
                var idLyr = charIDToTypeID("Lyr ");
                var idOrdn = charIDToTypeID("Ordn");
                var idTrgt = charIDToTypeID("Trgt");
                ref721.putEnumerated(idLyr, idOrdn, idTrgt);
                desc924.putReference(idnull, ref721);
                var idWhat = charIDToTypeID("What");
                var idrasterizeItem = stringIDToTypeID("rasterizeItem");
                var idvectorMask = stringIDToTypeID("vectorMask");
                desc924.putEnumerated(idWhat, idrasterizeItem, idvectorMask);
                executeAction(idrasterizeLayer, desc924, DialogModes.NO);
            } catch (err) {}

            try {
                var idIntr = charIDToTypeID("Intr");
                var desc864 = new ActionDescriptor();
                var idnull = charIDToTypeID("null");
                var ref658 = new ActionReference();
                var idChnl = charIDToTypeID("Chnl");
                var idOrdn = charIDToTypeID("Ordn");
                var idTrgt = charIDToTypeID("Trgt");
                ref658.putEnumerated(idChnl, idOrdn, idTrgt);
                desc864.putReference(idnull, ref658);
                var idWith = charIDToTypeID("With");
                var ref659 = new ActionReference();
                var idChnl = charIDToTypeID("Chnl");
                var idfsel = charIDToTypeID("fsel");
                ref659.putProperty(idChnl, idfsel);
                desc864.putReference(idWith, ref659);
                executeAction(idIntr, desc864, DialogModes.NO);

                // =======================================================
                var idDlt = charIDToTypeID("Dlt ");
                var desc865 = new ActionDescriptor();
                var idnull = charIDToTypeID("null");
                var ref660 = new ActionReference();
                var idChnl = charIDToTypeID("Chnl");
                var idOrdn = charIDToTypeID("Ordn");
                var idTrgt = charIDToTypeID("Trgt");
                ref660.putEnumerated(idChnl, idOrdn, idTrgt);
                desc865.putReference(idnull, ref660);
                executeAction(idDlt, desc865, DialogModes.NO);

                // =======================================================
                var idMk = charIDToTypeID("Mk  ");
                var desc866 = new ActionDescriptor();
                var idNw = charIDToTypeID("Nw  ");
                var idChnl = charIDToTypeID("Chnl");
                desc866.putClass(idNw, idChnl);
                var idAt = charIDToTypeID("At  ");
                var ref661 = new ActionReference();
                var idChnl = charIDToTypeID("Chnl");
                var idChnl = charIDToTypeID("Chnl");
                var idMsk = charIDToTypeID("Msk ");
                ref661.putEnumerated(idChnl, idChnl, idMsk);
                desc866.putReference(idAt, ref661);
                var idUsng = charIDToTypeID("Usng");
                var idUsrM = charIDToTypeID("UsrM");
                var idRvlS = charIDToTypeID("RvlS");
                desc866.putEnumerated(idUsng, idUsrM, idRvlS);
                executeAction(idMk, desc866, DialogModes.NO);

            } catch (err) {}
            
            var finalSuffix=suffix;
            if (addCount===true)finalSuffix += layerCount;


            activeDocument.activeLayer.name = "P" + finalSuffix;
            layerCount++;
            
            
            activeDocument.activeLayer=baseLayer;
        } catch (e) {}
    }
    var idsetd = charIDToTypeID("setd");
    var desc1045 = new ActionDescriptor();
    var idnull = charIDToTypeID("null");
    var ref578 = new ActionReference();
    var idChnl = charIDToTypeID("Chnl");
    var idfsel = charIDToTypeID("fsel");
    ref578.putProperty(idChnl, idfsel);
    desc1045.putReference(idnull, ref578);
    var idT = charIDToTypeID("T   ");
    var idOrdn = charIDToTypeID("Ordn");
    var idNone = charIDToTypeID("None");
    desc1045.putEnumerated(idT, idOrdn, idNone);
    executeAction(idsetd, desc1045, DialogModes.NO);

    // =======================================================
    var idDlt = charIDToTypeID("Dlt ");
    var desc694 = new ActionDescriptor();
    var idnull = charIDToTypeID("null");
    var ref323 = new ActionReference();
    var idChnl = charIDToTypeID("Chnl");
    ref323.putName(idChnl, "ContiguityMask");
    desc694.putReference(idnull, ref323);
    executeAction(idDlt, desc694, DialogModes.NO);

    
    activeDocument.activeLayer.remove();
    


    var idHd = charIDToTypeID("Hd  ");
    var desc736 = new ActionDescriptor();
    var idnull = charIDToTypeID("null");
    var list22 = new ActionList();
    var ref541 = new ActionReference();
    var idLyr = charIDToTypeID("Lyr ");
    var idOrdn = charIDToTypeID("Ordn");
    var idTrgt = charIDToTypeID("Trgt");
    ref541.putEnumerated(idLyr, idOrdn, idTrgt);
    list22.putReference(ref541);
    desc736.putList(idnull, list22);
    executeAction(idHd, desc736, DialogModes.NO);

}

//   pfaffenbichler and xbytor    //
//        at ps-scripts.com       //
//      created this function     //
function collectPathInfoFromDesc(myDocument, thePath) {
    var myDocument = app.activeDocument;

    // based of functions from xbytor’s stdlib;
    var ref = new ActionReference();
    for (var l = 0; l < myDocument.pathItems.length; l++) {
        var thisPath = myDocument.pathItems[l];
        if (thisPath == thePath && thisPath.name == "Work Path") {
            ref.putProperty(cTID("Path"), cTID("WrPt"));
        };
        if (thisPath == thePath && thisPath.name != "Work Path" && thisPath.kind != PathKind.VECTORMASK) {
            ref.putIndex(cTID("Path"), l + 1);
        };
        if (thisPath == thePath && thisPath.kind == PathKind.VECTORMASK) {
            var idPath = charIDToTypeID("Path");
            var idPath = charIDToTypeID("Path");
            var idvectorMask = stringIDToTypeID("vectorMask");
            ref.putEnumerated(idPath, idPath, idvectorMask);
        };
    };
    var desc = app.executeActionGet(ref);
    var pname = desc.getString(cTID('PthN'));
    // create new array;
    var theArray = new Array;
    var pathComponents = desc.getObjectValue(cTID("PthC")).getList(sTID('pathComponents'));
    // for subpathitems;
    for (var m = 0; m < pathComponents.count; m++) {
        var listKey = pathComponents.getObjectValue(m).getList(sTID("subpathListKey"));
        // for subpathitem’s count;
        for (var n = 0; n < listKey.count; n++) {
            var points = listKey.getObjectValue(n).getList(sTID('points'));
            // get first point;
            var anchorObj = points.getObjectValue(0).getObjectValue(sTID("anchor"));
            var anchor = [anchorObj.getUnitDoubleValue(sTID('horizontal')), anchorObj.getUnitDoubleValue(sTID('vertical'))];
            var thisPoint = [anchor];
            theArray.push(thisPoint);
        };
    };
    // by xbytor, thanks to him;


    function cTID(s) {
        return cTID[s] || cTID[s] = app.charIDToTypeID(s);
    };

    function sTID(s) {
        return sTID[s] || sTID[s] = app.stringIDToTypeID(s);
    };
    // reset;
    return theArray;
};


function makePreviewSelection(){
    makeSelection()    
   // app.refresh()
    activeDocument.quickMaskMode = false;
}

function makeSelection(){
    try{
    
        var idsetd = charIDToTypeID("setd");
        var desc922 = new ActionDescriptor();
        var idnull = charIDToTypeID("null");
        var ref529 = new ActionReference();
        var idChnl = charIDToTypeID("Chnl");
        var idfsel = charIDToTypeID("fsel");
        ref529.putProperty(idChnl, idfsel);
        desc922.putReference(idnull, ref529);
        var idT = charIDToTypeID("T   ");
        var ref530 = new ActionReference();
        var idChnl = charIDToTypeID("Chnl");
        var idChnl = charIDToTypeID("Chnl");
        var idTrsp = charIDToTypeID("Trsp");
        ref530.putEnumerated(idChnl, idChnl, idTrsp);
        desc922.putReference(idT, ref530);
        executeAction(idsetd, desc922, DialogModes.NO);

    } catch (err) {
        return false;
    }


    try {
        var idIntr = charIDToTypeID("Intr");
        var desc846 = new ActionDescriptor();
        var idnull = charIDToTypeID("null");
        var ref639 = new ActionReference();
        var idChnl = charIDToTypeID("Chnl");
        var idChnl = charIDToTypeID("Chnl");
        var idMsk = charIDToTypeID("Msk ");
        ref639.putEnumerated(idChnl, idChnl, idMsk);
        desc846.putReference(idnull, ref639);
        var idWith = charIDToTypeID("With");
        var ref640 = new ActionReference();
        var idChnl = charIDToTypeID("Chnl");
        var idfsel = charIDToTypeID("fsel");
        ref640.putProperty(idChnl, idfsel);
        desc846.putReference(idWith, ref640);
        executeAction(idIntr, desc846, DialogModes.NO);


    } catch (err) {}

    try {
        // =======================================================
        var idIntW = charIDToTypeID("IntW");
        var desc787 = new ActionDescriptor();
        var idnull = charIDToTypeID("null");
        var ref572 = new ActionReference();
        var idChnl = charIDToTypeID("Chnl");
        var idfsel = charIDToTypeID("fsel");
        ref572.putProperty(idChnl, idfsel);
        desc787.putReference(idnull, ref572);
        var idT = charIDToTypeID("T   ");
        var ref573 = new ActionReference();
        var idPath = charIDToTypeID("Path");
        var idPath = charIDToTypeID("Path");
        var idvectorMask = stringIDToTypeID("vectorMask");
        ref573.putEnumerated(idPath, idPath, idvectorMask);
        var idLyr = charIDToTypeID("Lyr ");
        var idOrdn = charIDToTypeID("Ordn");
        var idTrgt = charIDToTypeID("Trgt");
        ref573.putEnumerated(idLyr, idOrdn, idTrgt);
        desc787.putReference(idT, ref573);
        var idVrsn = charIDToTypeID("Vrsn");
        desc787.putInteger(idVrsn, 1);
        var idvectorMaskParams = stringIDToTypeID("vectorMaskParams");
        desc787.putBoolean(idvectorMaskParams, true);
        executeAction(idIntW, desc787, DialogModes.NO);
    } catch (err) {}



    if (tolerance >= 2) {

        activeDocument.selection.expand(Math.floor(tolerance / 2))

    }


    activeDocument.quickMaskMode = true;


    var idThrs = charIDToTypeID("Thrs");
    var desc479 = new ActionDescriptor();
    var idLvl = charIDToTypeID("Lvl ");
    desc479.putInteger(idLvl, 1);
    executeAction(idThrs, desc479, DialogModes.NO);



    if (tolerance % 2 == 1) {

        var idMtnB = charIDToTypeID("MtnB");
        var desc213 = new ActionDescriptor();
        var idAngl = charIDToTypeID("Angl");
        desc213.putInteger(idAngl, 0);
        var idDstn = charIDToTypeID("Dstn");
        var idPxl = charIDToTypeID("#Pxl");
        desc213.putUnitDouble(idDstn, idPxl, 1.000000);
        executeAction(idMtnB, desc213, DialogModes.NO);

        // =======================================================
        var idMtnB = charIDToTypeID("MtnB");
        var desc214 = new ActionDescriptor();
        var idAngl = charIDToTypeID("Angl");
        desc214.putInteger(idAngl, 90);
        var idDstn = charIDToTypeID("Dstn");
        var idPxl = charIDToTypeID("#Pxl");
        desc214.putUnitDouble(idDstn, idPxl, 1.000000);
        executeAction(idMtnB, desc214, DialogModes.NO);


        // =======================================================
        var idThrs = charIDToTypeID("Thrs");
        var desc215 = new ActionDescriptor();
        var idLvl = charIDToTypeID("Lvl ");
        desc215.putInteger(idLvl, 1);
        executeAction(idThrs, desc215, DialogModes.NO);
    }
}   

function createDialog(){
        
    var dlg = new Window('dialog', 'PNG素材拆分图层');
    dlg.alignChildren ='left';

    dlg.gap = dlg.add('group')
    dlg.gap.orientation= 'row';
    dlg.gap.txt=dlg.gap.add('statictext', undefined,'间隙大于多少时拆分?');
    dlg.gap.input=dlg.gap.add('edittext', undefined,tolerance);
        dlg.gap.input.preferredSize = [20,20];
    dlg.gap.txt2=dlg.gap.add('statictext', undefined,'像素');
    dlg.gap.btnPreview= dlg.gap.add('button', undefined,'蒙版预览');
        dlg.gap.btnPreview.preferredSize = [55,20]
    
    dlg.naming = dlg.add('panel',undefined,'图层重命名') 
    dlg.naming.alignChildren ='left';
        dlg.naming.suffix = dlg.naming.add('group')
        dlg.naming.suffix.orientation= 'row';
        dlg.naming.suffix.txt=dlg.naming.suffix.add('statictext', undefined,'后缀:');
        dlg.naming.suffix.input=dlg.naming.suffix.add('edittext', undefined,suffix);
            dlg.naming.suffix.input.preferredSize = [60,20];

        dlg.naming.suffix.chkbox = dlg.naming.suffix.add('checkbox', undefined, '添加序号')
            dlg.naming.suffix.chkbox.value=addCount;
        
        dlg.naming.txtPreview = dlg.naming.add('statictext', undefined, layerNamePreview)
            dlg.naming.txtPreview.preferredSize = [200,20];
        
    dlg.btnPnl= dlg.add('group');
    dlg.btnPnl.alignment ='right';
    dlg.btnPnl.okBtn = dlg.btnPnl.add('button', undefined, '确定', {name:'ok'});
        dlg.btnPnl.okBtn.active=true;
    dlg.btnPnl.cancelBtn = dlg.btnPnl.add('button', undefined, '取消', {name:'cancel'});
      
    dlg.naming.suffix.input.onChanging= function(){
        layerNamePreview=activeDocument.activeLayer.name + dlg.naming.suffix.input.text
        if (dlg.naming.suffix.chkbox.value === true){
            layerNamePreview += "1"
        }
        dlg.naming.txtPreview.text =layerNamePreview
    }
    dlg.naming.suffix.chkbox.onClick = function(){
        layerNamePreview=activeDocument.activeLayer.name + dlg.naming.suffix.input.text
        if (dlg.naming.suffix.chkbox.value === true){
            layerNamePreview += "1"
        }
        dlg.naming.txtPreview.text = layerNamePreview;
    }

    
        
    
    dlg.gap.input.onChanging = function() {
        if (parseInt(dlg.gap.input.text) == 1){
            dlg.gap.txt2.text = '像素'
        }else{
            dlg.gap.txt2.text = '像素'
        }
        tolerance = parseInt (dlg.gap.input.text)
    }

    dlg.gap.btnPreview.onClick = function() {
        makePreviewSelection()   
    }
    
    x=dlg.show(); 
    
    tolerance = parseInt (dlg.gap.input.text)
    suffix = dlg.naming.suffix.input.text
    addCount=dlg.naming.suffix.chkbox.value
    
    return x;
}
}


"""
