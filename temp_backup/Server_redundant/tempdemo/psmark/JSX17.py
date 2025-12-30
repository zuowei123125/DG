dxf17_jscode = """



function 定位码批量化替换外链新(){

var dialog = new Window("dialog"); 
    dialog.text = "定位码批量快速换图 "; 
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
    //花样标准化(80);
   // 文档另存(缓存切片裁片路径选择);
   花样图层导出为TIF透明底(缓存切片裁片路径选择)
   app.activeDocument.close(SaveOptions.DONOTSAVECHANGES)
  
  
 var parentFolderPath =大货文件存放位置
//var folderNames = 文档名称1
/*
var folderPath = parentFolderPath + "/" + 文档名称1;
var folderObj = new Folder(folderPath);
$.writeln(folderObj);
folderObj.create();
*/

     for (var j = 0; j <myFiles1.length; j++) {
    app.open(myFiles1[j])
    

    更换当前文档裁片组外链(缓存切片裁片路径选择);
 //   图层选择();
//    app.activeDocument.activeLayer.textItem.contents = 文档名称1;
    选择裁片图层();
   
   // if (checkbox1.value == true) {
    合并图层();
    预设图案填充(缓存切片裁片路径选择)           

            
            
另存为(parentFolderPath,文档名称1)



    
    app.activeDocument.close(SaveOptions.DONOTSAVECHANGES);
  }
}

 





function 预设图案填充(缓存切片裁片路径选择)
    {

var file = new File(缓存切片裁片路径选择 + "/名称数据.json");
if (file.open('r')) {
    var content = file.read();
    file.close();

    // 移除双引号
    var content1 = content.replace(/"/g, '');

    // 移除[]并使用逗号分割字符串
    var 名称数组 = content1.replace(/^\s*\[|\]\s*$/g, '').split(',');

    for (var k = 0; k < 名称数组.length; k++) {
        var 名称 = 名称数组[k].replace(/^\s+|\s+$/g, ''); // 使用正则替代trim函数移除前后空格
        //alert(名称);
        var matches = 名称.match(/\(([^)]+)\)/);
        if (matches) {
            var 图案名称 = matches[1];
            var 素材填充 = app.activeDocument.layerSets.getByName("填充底图").layers.getByName(图案名称);
            app.activeDocument.activeLayer = 素材填充;
            载入选区();
            填充图案(名称);
        }
    }
} else {
    alert("找不到名称数据文件查看是否写入！");
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


function 填充图案(名称)	//新建图案填充图层
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putClass(stringIDToTypeID("contentLayer"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        var d2 = new ActionDescriptor();
        var d3 = new ActionDescriptor();
        d3.putString(stringIDToTypeID("name"), 名称);
        
        d2.putObject(stringIDToTypeID("pattern"), stringIDToTypeID("pattern"), d3);
        d1.putObject(stringIDToTypeID("type"), stringIDToTypeID("patternLayer"), d2);
        d.putObject(stringIDToTypeID("using"), stringIDToTypeID("contentLayer"), d1);
        executeAction(stringIDToTypeID("make"), d, DialogModes.NO);
       
    }

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


function 填充图案(图案名称)	//新建图案填充图层
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putClass(stringIDToTypeID("contentLayer"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        var d2 = new ActionDescriptor();
        var d3 = new ActionDescriptor();
        d3.putString(stringIDToTypeID("name"), 图案名称);
        d3.putString(stringIDToTypeID("ID"), 图案名称);
        d2.putObject(stringIDToTypeID("pattern"), stringIDToTypeID("pattern"), d3);
        d1.putObject(stringIDToTypeID("type"), stringIDToTypeID("patternLayer"), d2);
        d.putObject(stringIDToTypeID("using"), stringIDToTypeID("contentLayer"), d1);
        executeAction(stringIDToTypeID("make"), d, DialogModes.NO);
       
    }

function 花样图层导出为TIF透明底(导出目录) {

  app.preferences.rulerUnits = Units.MM;
var doc = app.activeDocument;
var 扩展毫米数=80
  
// 获取文档中的所有图层
var allLayers = doc.layers;
var 名称数组 = [];
// 循环遍历所有图层
for (var i = 0; i < allLayers.length; i++) {
    // 检查图层是否是图层组
    if (allLayers[i] instanceof LayerSet) {
        // 获取图层组中的所有子图层
       subLayers = allLayers[i].layers;
       图层组名称=allLayers[i].name
       文档名称=app.activeDocument.name
        文档名称去除后缀 = 文档名称.replace(/\.[^\.]+$/, "");
        // 检查图层组是否包含子图层
        if (subLayers.length > 0) {
            // 获取图层组中最后一个子图层的名称
            var lastSubLayer = subLayers[subLayers.length - 1];
            var lastSubLayerName = lastSubLayer.name;
            FastSubLayer = subLayers[0];
            FastSubLayername= FastSubLayer.name    
            // 输出图层组名称和最后一个子图层的名称
         
            
              if (图层组名称 === "填充底图") {
          for (var y = 0; y < subLayers.length; y++) {
                   // alert(subLayers[j].name);
             填充底图组内部循环名称 = subLayers[y].name
             填充底图循环素材 = app.activeDocument.layerSets.getByName("填充底图").layers.getByName(填充底图组内部循环名称);
              app.activeDocument.activeLayer = 填充底图循环素材;
              新建文档()
             // 合并图层() 
              载入选区()
              裁剪()
              名称=文档名称去除后缀+"-("+填充底图组内部循环名称 +")-填充底图"
               名称数组.push('"' + 名称 + '"');
              制作图案预设(名称)
              app.activeDocument.close(SaveOptions.DONOTSAVECHANGES);
              app.activeDocument=doc
            // 执行某一个操作（例如，设置图层组的可见性）
         //   alert("测试")
         } 
     
     
     // 手动创建JSON格式的字符串
var jsonStr = '[' + 名称数组.join(', ') + ']';

// 创建一个文件对象指向桌面

var file = new File(导出目录  + "/名称数据.json");

// 打开文件，写入JSON字符串，然后关闭文件
file.open('w');
file.write(jsonStr);
file.close();

            } else {
                // 执行别的操作（例如，隐藏其他图层组）
              
     
            
          空白裁片模板 = app.activeDocument.layerSets.getByName(图层组名称).layers.getByName(lastSubLayerName);
            app.activeDocument.activeLayer = 空白裁片模板;
             新建图层()
              app.activeDocument.activeLayer.name="最大白边值"
              裁片边界 = lastSubLayer.bounds;
              扩展值 = 毫米转像素(扩展毫米数); //50cm
              裁片边界_左 = 毫米转像素(裁片边界[0]) - 扩展值;
                
              裁片边界_上 = 毫米转像素(裁片边界[1]) - 扩展值;
              裁片边界_右 = 毫米转像素(裁片边界[2]) + 扩展值;
              裁片边界_下 = 毫米转像素(裁片边界[3]) + 扩展值;
              
                var selRegion = [
            [裁片边界_左,裁片边界_上],
            [裁片边界_右,裁片边界_上],
            [裁片边界_右,裁片边界_下],
            [裁片边界_左,裁片边界_下]
        ];
        app.activeDocument.selection.select(selRegion, SelectionType.REPLACE);
        背景切换();  
        恢复白底();
        填充();
        隐藏图层();
        裁片图层组 = app.activeDocument.layerSets.getByName(图层组名称)
        app.activeDocument.activeLayer =  裁片图层组 ;
        新建文档()
        空白裁片模板 = app.activeDocument.layerSets.getByName(图层组名称).layers.getByName(lastSubLayerName);
         app.activeDocument.activeLayer = 空白裁片模板;
         删除图层()
         最大白边值=app.activeDocument.layerSets.getByName(图层组名称).layers.getByName("最大白边值");
         app.activeDocument.activeLayer = 最大白边值;
         app.activeDocument.crop(最大白边值.bounds, 0);
               // 保存为TIF
        var 文件路径 = 导出目录 + "/" + 图层组名称 + ".tif";
        tiffOptions = new TiffSaveOptions();
        app.activeDocument.saveAs(new File(文件路径), tiffOptions);
        app.activeDocument.close(SaveOptions.DONOTSAVECHANGES);
         app.activeDocument=doc
         最大白边值=app.activeDocument.layerSets.getByName(图层组名称).layers.getByName(FastSubLayername);
         app.activeDocument.activeLayer = 最大白边值;
         //上移图层()
         多选图层()	
         转换为智能对象()
         添加图层蒙版()
       //  向下合并()
         转换为智能对象()
        // 重新链接到文件(文件路径)
                }
                
        }
    }
}

}
function 恢复白底()	//删除图层
    {
  
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("color"), stringIDToTypeID("colors"));
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("exchange"), d, DialogModes.NO);
    
    }

function 制作图案预设(名称)	//
    {
  
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putClass(stringIDToTypeID("pattern"));
        d.putReference(stringIDToTypeID("null"), r);
        var r1 = new ActionReference();
        r1.putProperty(stringIDToTypeID("property"), stringIDToTypeID("selection"));
        r1.putEnumerated(stringIDToTypeID("document"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("using"), r1);
        d.putString(stringIDToTypeID("name"), 名称);
        executeAction(stringIDToTypeID("make"), d, DialogModes.NO);
    
    }



function 合并图层()	//
    {
   
        var d = new ActionDescriptor();
        executeAction(stringIDToTypeID("mergeLayersNew"), d, DialogModes.NO);
      
    }

function 背景切换()	//
    {
    
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("color"), stringIDToTypeID("colors"));
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("reset"), d, DialogModes.NO);
      
    }


function 裁剪()	//裁剪
    {
    
        var d = new ActionDescriptor();
        d.putBoolean(stringIDToTypeID("delete"), true);
        executeAction(stringIDToTypeID("crop"), d, DialogModes.NO);
      
   
    }


function 重新链接到文件(文件路径)	//重新链接到文件
    {
   
        var d = new ActionDescriptor();
        d.putPath(stringIDToTypeID("null"), new File(文件路径));
        d.putInteger(stringIDToTypeID("layerID"), 94);
        executeAction(stringIDToTypeID("placedLayerRelinkToFile"), d, DialogModes.NO);
    
    }



function 转换为智能对象()	//转换为智能对象
    {
    
        var d = new ActionDescriptor();
        executeAction(stringIDToTypeID("newPlacedLayer"), d, DialogModes.NO);
      
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

function 上移图层()	//
    {
 
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("forwardEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putBoolean(stringIDToTypeID("makeVisible"), false);
        var list = new ActionList();
        list.putInteger(11);
        d.putList(stringIDToTypeID("layerID"), list);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);

    
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
 
 
 function 删除图层()	//删除图层
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        var list = new ActionList();
        list.putInteger(22);
        d.putList(stringIDToTypeID("layerID"), list);
        executeAction(stringIDToTypeID("delete"), d, DialogModes.NO);
      
    }

 
 
 
function 多选图层()	//
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putName(stringIDToTypeID("layer"), "最大白边值");
        d.putReference(stringIDToTypeID("null"), r);
        d.putEnumerated(stringIDToTypeID("selectionModifier"), stringIDToTypeID("selectionModifierType"), stringIDToTypeID("addToSelectionContinuous"));
        d.putBoolean(stringIDToTypeID("makeVisible"), false);
        var list = new ActionList();
      
        list.putInteger(115);
        d.putList(stringIDToTypeID("layerID"), list);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
        }
 

function 新建图层()	//新建图层
    {
    
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putClass(stringIDToTypeID("layer"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        d1.putBoolean(stringIDToTypeID("group"), true);
        d.putObject(stringIDToTypeID("using"), stringIDToTypeID("layer"), d1);
        d.putInteger(stringIDToTypeID("layerID"), 22);
        executeAction(stringIDToTypeID("make"), d, DialogModes.NO);
   
    }


function 填充()	//填充
    {
  
        var d = new ActionDescriptor();
        d.putEnumerated(stringIDToTypeID("using"), stringIDToTypeID("fillContents"), stringIDToTypeID("foregroundColor"));
        d.putUnitDouble(stringIDToTypeID("opacity"), stringIDToTypeID("percentUnit"), 100);
        d.putEnumerated(stringIDToTypeID("mode"), stringIDToTypeID("blendMode"), stringIDToTypeID("normal"));
        executeAction(stringIDToTypeID("fill"), d, DialogModes.NO); 
    }


function 隐藏图层()	//
    {
    
        var d = new ActionDescriptor();
        var list = new ActionList();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        list.putReference(r);
        d.putList(stringIDToTypeID("null"), list);
        executeAction(stringIDToTypeID("hide"), d, DialogModes.NO);
     
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

function 另存为(parentFolderPath,文档名称1)
{
文档名称=activeDocument.name.replace(/(?:\.[^.]*$|$)/, '');
saveIn=File(parentFolderPath+ "/"+文档名称1+"-"+文档名称);
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
        //alert("找不到款号图层",dialog.text+"----关于");

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










"""