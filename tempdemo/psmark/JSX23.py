dxf23_jscode = """






function 自动连晒(){
var dialog = new Window("dialog"); 

    dialog.text = "S/O样自动连晒";
    //dialog.text = "SO自动米样拼贴"; 
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
    panel1.text = "源图像"; 
    panel1.preferredSize.width = 388; 
    panel1.preferredSize.height = 205; 
    panel1.orientation = "column"; 
    panel1.alignChildren = ["left","top"]; 
    panel1.spacing = 10; 
    panel1.margins = 10; 

var statictext1 = panel1.add("statictext", undefined, undefined, {name: "statictext1"}); 
    statictext1.text = "使用:"; 

// GROUP2
// ======
var group2 = panel1.add("group", undefined, {name: "group2"}); 
    group2.orientation = "row"; 
    group2.alignChildren = ["left","center"]; 
    group2.spacing = 10; 
    group2.margins = 0; 

var button1 = group2.add("button", undefined, undefined, {name: "button1"}); 
    button1.text = "选取"; 

var edittext1 = group2.add('edittext {properties: {name: "edittext1"}}'); 
    edittext1.text = "[选择图像文件夹]"; 
    edittext1.preferredSize.width = 300; 

// PANEL2
// ======
var panel2 = group1.add("panel", undefined, undefined, {name: "panel2"}); 
    panel2.text = "SO小样文档"; 
    panel2.preferredSize.height = 160; 
    panel2.orientation = "column"; 
    panel2.alignChildren = ["left","top"]; 
    panel2.spacing = 10; 
    panel2.margins = 10; 

var statictext2 = panel2.add("statictext", undefined, undefined, {name: "statictext2"}); 
    statictext2.text = "设定:"; 

// GROUP3
// ======
var group3 = panel2.add("group", undefined, {name: "group3"}); 
    group3.orientation = "row"; 
    group3.alignChildren = ["left","center"]; 
    group3.spacing = 10; 
    group3.margins = 0; 

var statictext3 = group3.add("statictext", undefined, undefined, {name: "statictext3"}); 
    statictext3.text = "宽度(cm):"; 

var edittext2 = group3.add('edittext {properties: {name: "edittext2"}}'); 
    edittext2.preferredSize.width = 100; 

var statictext4 = group3.add("statictext", undefined, undefined, {name: "statictext4"}); 
    statictext4.text = "高度(cm):"; 

var edittext3 = group3.add('edittext {properties: {name: "edittext3"}}'); 
    edittext3.preferredSize.width = 100; 

// GROUP4
// ======
var group4 = panel2.add("group", undefined, {name: "group4"}); 
    group4.orientation = "row"; 
    group4.alignChildren = ["left","center"]; 
    group4.spacing = 10; 
    group4.margins = 0; 

// GROUP5
// ======
var group5 = group1.add("group", undefined, {name: "group5"}); 
    group5.orientation = "row"; 
    group5.alignChildren = ["left","center"]; 
    group5.spacing = 10; 
    group5.margins = 0; 

// PANEL3
// ======


// GROUP7
// ======
var group7 = dialog.add("group", undefined, {name: "group7"}); 
    group7.orientation = "column"; 
    group7.alignChildren = ["fill","top"]; 
    group7.spacing = 10; 
    group7.margins = 0; 

var ok = group7.add("button", undefined, undefined, {name: "ok"}); 
    ok.text = "确认"; 

var cancel = group7.add("button", undefined, undefined, {name: "cancel"}); 
    cancel.text = "取消"; 
    
    



button1.onClick = function () {
    // 打开文件夹选择对话框
    var selectedFolder = Folder.selectDialog("选择图像文件夹");

    // 检查用户是否取消了选择
    if (selectedFolder) {
        // 将选择的文件夹路径显示在输入框中
        edittext1.text = selectedFolder.fsName;
    }
};

ok.onClick = function () {
    app.preferences.rulerUnits = Units.PIXELS;
    var 素材图片文件夹 = new Folder(edittext1.text);
    var 遍历tiff = 素材图片文件夹.getFiles("*.*");

    // 新建文件夹
    var 新文件夹 = new Folder(edittext1.text + "/SO小样拼贴");
    新文件夹.create();
    var 新加字文件夹 = new Folder(edittext1.text + "/SO小样拼贴加字");
   新加字文件夹.create();

   
 宽度=Number (edittext2.text);
 高度=Number (edittext3.text);


    for (var i = 0; i < 遍历tiff.length; i++) {
        if (遍历tiff[i] instanceof File) {
            app.open(遍历tiff[i]);
            app.activeDocument.flatten();
            var 当前文档 = app.activeDocument;
            var 当前文档名称 = 当前文档.name;
            图像大小()
            预设图案(当前文档名称);
            app.activeDocument.crop([UnitValue("0px"), UnitValue("0px"), UnitValue(宽度, "cm"), UnitValue(高度, "cm")]);
            填充图案(当前文档名称);
            app.activeDocument.flatten();
            画布扩展()
            // 保存新的图像文件到新建的文件夹中
            var 保存路径 = 新文件夹 + "/" + 当前文档名称;
            var tifSaveOpt = new TiffSaveOptions();
            tifSaveOpt.imageCompression = TIFFEncoding.TIFFLZW;
            tifSaveOpt.byteOrder = ByteOrder.IBM;
            var asCopy = true;
            app.activeDocument.saveAs(new File(保存路径), tifSaveOpt, asCopy);
            创建并处理文本图层();
            app.activeDocument.flatten();
            var 保存路径 = 新加字文件夹 + "/" + 当前文档名称;
            var tifSaveOpt = new TiffSaveOptions();
            tifSaveOpt.imageCompression = TIFFEncoding.TIFFLZW;
            tifSaveOpt.byteOrder = ByteOrder.IBM;
            var asCopy = true;
            app.activeDocument.saveAs(new File(保存路径), tifSaveOpt, asCopy);
            app.activeDocument.close(SaveOptions.DONOTSAVECHANGES);
           
            
            
            
            
            
            
        }
    }
//alert("小样连晒完成")
dialog.close();
// 创建并保存拼贴图像(新文件夹,  幅宽)
};



function 预设图案(当前文档名称)	//
    {
    
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putClass(stringIDToTypeID("pattern"));
        d.putReference(stringIDToTypeID("null"), r);
        var r1 = new ActionReference();
        r1.putProperty(stringIDToTypeID("property"), stringIDToTypeID("selection"));
        r1.putEnumerated(stringIDToTypeID("document"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("using"), r1);
        d.putString(stringIDToTypeID("name"), 当前文档名称);
        executeAction(stringIDToTypeID("make"), d, DialogModes.NO);
    
    }


function 填充图案(当前文档名称)	//
    {
    
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putClass(stringIDToTypeID("contentLayer"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        var d2 = new ActionDescriptor();
        var d3 = new ActionDescriptor();
        d3.putString(stringIDToTypeID("name"), 当前文档名称);
      
        d2.putObject(stringIDToTypeID("pattern"), stringIDToTypeID("pattern"), d3);
        d1.putObject(stringIDToTypeID("type"), stringIDToTypeID("patternLayer"), d2);
        d.putObject(stringIDToTypeID("using"), stringIDToTypeID("contentLayer"), d1);
        executeAction(stringIDToTypeID("make"), d, DialogModes.NO);
       
    }


function 图像大小()		//图像大小
    {
 
        var d = new ActionDescriptor();
        d.putUnitDouble(stringIDToTypeID("resolution"), stringIDToTypeID("densityUnit"), 200);
        d.putBoolean(stringIDToTypeID("scaleStyles"), true);
        d.putBoolean(stringIDToTypeID("constrainProportions"), true);
        d.putEnumerated(charIDToTypeID("Intr"), stringIDToTypeID("interpolationType"), stringIDToTypeID("nearestNeighbor"));
        executeAction(stringIDToTypeID("imageSize"), d, DialogModes.NO);
        }



function 画布扩展()	//
    {
    
        var d = new ActionDescriptor();
        d.putBoolean(stringIDToTypeID("relative"), true);
        d.putUnitDouble(stringIDToTypeID("width"), stringIDToTypeID("distanceUnit"), 14.4);
        d.putUnitDouble(stringIDToTypeID("height"), stringIDToTypeID("distanceUnit"), 14.4);
        d.putEnumerated(stringIDToTypeID("horizontal"), stringIDToTypeID("horizontalLocation"), stringIDToTypeID("center"));
        d.putEnumerated(stringIDToTypeID("vertical"), stringIDToTypeID("verticalLocation"), stringIDToTypeID("center"));
        d.putEnumerated(stringIDToTypeID("canvasExtensionColorType"), stringIDToTypeID("canvasExtensionColorType"), stringIDToTypeID("color"));
        var d1 = new ActionDescriptor();
        d1.putDouble(stringIDToTypeID("red"), 255);
        d1.putDouble(stringIDToTypeID("green"), 255);
        d1.putDouble(stringIDToTypeID("blue"), 255);
        d.putObject(stringIDToTypeID("canvasExtensionColor"), stringIDToTypeID("RGBColor"), d1);
        executeAction(stringIDToTypeID("canvasSize"), d, DialogModes.NO);
    
    }





function 创建并处理文本图层() {
    // 新建图层
    var textLayer = activeDocument.artLayers.add();

    // 将新建图层变成文本图层
    textLayer.kind = LayerKind.TEXT;

    // 将文本内容改为当前文档name
    textLayer.textItem.contents = activeDocument.name;

    // 字体大小固定值
    var 固定字体大小 = 30; // 例如，30像素
    textLayer.textItem.size = 固定字体大小;

    // 文字字体固定值
    textLayer.textItem.font = "微软雅黑";

    // 计算并调整文本位置
    var x = activeDocument.width - textLayer.bounds[2];
    var y = textLayer.bounds[1];
    textLayer.translate(x, -y);

    // 偏移
    textLayer.translate(UnitValue("-1cm"), UnitValue("+0.5cm"));

    // 复制并栅格化图层
    var copyLayer = textLayer.duplicate();
    copyLayer.rasterize(RasterizeType.ENTIRELAYER);

    // 设置固定颜色值
    var 固定颜色 = new SolidColor();
    固定颜色.rgb.red = 255;   // 红色分量
    固定颜色.rgb.green = 255; // 绿色分量
    固定颜色.rgb.blue = 255;  // 蓝色分量

    activeDocument.activeLayer = copyLayer;
    activeDocument.selection.fill(固定颜色, ColorBlendMode.NORMAL, 100, true);

    // 白边
    activeDocument.activeLayer.applyMinimum(10);
    后移一层()
    向上选择()
    向下合并()
    名称更改字体()
    缩小字体图层至文档一半()
    多选背景()
    底对齐()
    水平居中对齐()
}

// 调用函数





function 后移一层()	//
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

function 向上选择()	//
    {
    
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("forwardEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putBoolean(stringIDToTypeID("makeVisible"), false);
        var list = new ActionList();
        list.putInteger(19);
        d.putList(stringIDToTypeID("layerID"), list);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
   
    }
function 向下合并()	//向下合并
    {
 
        var d = new ActionDescriptor();
        executeAction(stringIDToTypeID("mergeLayersNew"), d, DialogModes.NO);
    
    }


function 名称更改字体()	//名称更改
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        var d1 = new ActionDescriptor();
        d1.putString(stringIDToTypeID("name"), "字体");
        d.putObject(stringIDToTypeID("to"), stringIDToTypeID("layer"), d1);
        executeAction(stringIDToTypeID("set"), d, DialogModes.NO);
     
    }



function 缩小字体图层至文档一半() {
    var 文档 = app.activeDocument;
    var 字体图层 = null;

    // 遍历文档中的图层以找到名为"字体"的图层
    for (var i = 0; i < 文档.artLayers.length; i++) {
        if (文档.artLayers[i].name === "字体") {
            字体图层 = 文档.artLayers[i];
            break;
        }
    }

    if (字体图层 !== null) {
        // 获取文档的宽度的一半
        var 目标宽度 = 文档.width / 2;

        // 获取图层的当前宽度
        var 图层宽度 = 字体图层.bounds[2] - 字体图层.bounds[0];

        // 计算缩放比例
        var 缩放比例 = 目标宽度 / 图层宽度 * 100;

        // 缩放图层
        字体图层.resize(缩放比例, 缩放比例, AnchorPosition.MIDDLECENTER);
    } else {
        alert("未找到名为'字体'的图层");
    }
}


function 多选背景()	//自由变换
    {
  
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putName(stringIDToTypeID("layer"), "背景");
        d.putReference(stringIDToTypeID("null"), r);
        d.putEnumerated(stringIDToTypeID("selectionModifier"), stringIDToTypeID("selectionModifierType"), stringIDToTypeID("addToSelection"));
        d.putBoolean(stringIDToTypeID("makeVisible"), false);
        var list = new ActionList();
        list.putInteger(1);
        list.putInteger(13);
        d.putList(stringIDToTypeID("layerID"), list);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
     
    }




function 底对齐()	//底对齐
    {
  
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putEnumerated(stringIDToTypeID("using"), stringIDToTypeID("alignDistributeSelector"), stringIDToTypeID("ADSBottoms"));
        d.putBoolean(stringIDToTypeID("alignToCanvas"), false);
        executeAction(stringIDToTypeID("align"), d, DialogModes.NO);
        
    }



function 水平居中对齐()	//水平居中对齐
    {   
      
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putEnumerated(stringIDToTypeID("using"), stringIDToTypeID("alignDistributeSelector"), stringIDToTypeID("ADSCentersH"));
        d.putBoolean(stringIDToTypeID("alignToCanvas"), false);
        executeAction(stringIDToTypeID("align"), d, DialogModes.NO);

    }



// 设置单位为像素





dialog.show();

    }






"""