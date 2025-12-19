dxf24_jscode = """



// 设置单位为像素

function 自动米样拼贴(){

var dialog = new Window("dialog"); 

  
    dialog.text = "SO自动米样拼贴"; 
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
    statictext3.text = "幅宽(cm):"; 

var edittext2 = group3.add('edittext {properties: {name: "edittext2"}}'); 
    edittext2.preferredSize.width = 100; 



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
    
    






var dialog = new Window("dialog"); 
    dialog.text = "SO自动米样拼贴"; 
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
    panel2.text = "SO小样文档拼贴"; 
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
    statictext3.text = "幅宽(cm):"; 

var edittext2 = group3.add('edittext {properties: {name: "edittext2"}}'); 
    edittext2.preferredSize.width = 100; 




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
//function 创建拼贴图(导入文件夹路径, 文档宽度厘米) {

// 假设这些值是从某处获取或者用户输入的
var 导入文件夹路径 =new Folder (edittext1.text);
var 文档宽度厘米 =  Number(edittext2.text);
var 文档高度厘米 = 300; // 例如，50厘米
var 分辨率 = 200; // 分辨率设置为150 DPI

// 转换厘米到像素
var 厘米到像素的转换系数 = 2.54;
var 文档宽度像素 = 文档宽度厘米 / 厘米到像素的转换系数 * 分辨率;
var 文档高度像素 = 文档高度厘米 / 厘米到像素的转换系数 * 分辨率;

var 导入文件夹 = new Folder(导入文件夹路径);
var 文件列表 = 导入文件夹.getFiles("*.*");
var 文件名数组 = new Array();
var 文件宽度数组 = new Array();
var 文件高度数组 = new Array();


// 读取文件列表并获取文件信息
for (var 索引1 = 0; 索引1 < 文件列表.length; 索引1++) {
    var 文档 = app.open(文件列表[索引1]);
    文件名数组[索引1] = 文档.fullName;
    文件宽度数组[索引1] = parseInt(文档.width);
    文件高度数组[索引1] = parseInt(文档.height);
    文档.close();
}

// 根据高度对文件进行排序
for (var 索引1 = 文件高度数组.length - 1; 索引1 > 0; --索引1) {
    for (var 索引2 = 0; 索引2 < 索引1; ++索引2) {
        if (文件高度数组[索引2] > 文件高度数组[索引2 + 1])
            交换数组元素(索引2, 索引2 + 1);
    }
}

function 交换数组元素(索引1, 索引2) {
    var 临时 = 文件高度数组[索引1];
    文件高度数组[索引1] = 文件高度数组[索引2];
    文件高度数组[索引2] = 临时;

    var 临时2 = 文件宽度数组[索引1];
    文件宽度数组[索引1] = 文件宽度数组[索引2];
    文件宽度数组[索引2] = 临时2;

    var 临时3 = 文件名数组[索引1];
    文件名数组[索引1] = 文件名数组[索引2];
    文件名数组[索引2] = 临时3;
}

// 创建新文档并添加图片
var 新文档 = app.documents.add(文档宽度像素, 文档高度像素, 分辨率, "拼贴", NewDocumentMode.CMYK, DocumentFill.WHITE);
var 当前顶部 = 0;
var 当前左侧 = 0;
for (var 索引1 = 0; 索引1 < 文件名数组.length; 索引1++) {
    var 文档 = app.open(文件名数组[索引1]);
    文档.selection.selectAll();
    文档.selection.copy();
    文档.close();

    if ((当前左侧 + 文件宽度数组[索引1]) > 文档宽度像素) {
        当前左侧 = 0;
        当前顶部 += 文件高度数组[索引1 - 1];
    }

    var 边界 = [
        [当前左侧, 当前顶部],
        [当前左侧 + 文件宽度数组[索引1], 当前顶部],
        [当前左侧 + 文件宽度数组[索引1], 当前顶部 + 文件高度数组[索引1]],
        [当前左侧, 当前顶部 + 文件高度数组[索引1]]
    ];
    新文档.selection.select(边界, SelectionType.REPLACE, 0, true);
    新文档.paste();
    当前左侧 += 文件宽度数组[索引1];
}

// 选择输出文件夹并保存图片
var 输出文件夹 = new Folder(edittext1.text + "/拼贴");
if (!输出文件夹.exists) 输出文件夹.create();

// 设置TIFF保存选项
var tiffSaveOptions = new TiffSaveOptions();
tiffSaveOptions.imageCompression = TIFFEncoding.TIFFLZW; // 使用LZW压缩
tiffSaveOptions.byteOrder = ByteOrder.IBM; // 设置字节顺序为IBM（大端序）

// 定义保存的文件路径和名称
var 文件 = new File(输出文件夹 + "/combined.tif");

// 保存当前文档为TIFF格式
新文档.saveAs(文件, tiffSaveOptions, true, Extension.LOWERCASE);
裁切透明像素();

// 关闭文档，不保存更改
//新文档.close(SaveOptions.DONOTSAVECHANGES);
dialog.close();
alert("拼贴完成")

}

 function 裁切透明像素() {
    var 文档 = app.activeDocument; // 获取当前活动的文档

    // 裁切透明像素
    // TrimType.TOPLEFT 表示从图像的左上角开始裁切
    // 第二个参数 true 表示裁切顶部的透明像素
    // 第三个参数 true 表示裁切左侧的透明像素
    // 第四个参数 true 表示裁切底部的透明像素
    // 第五个参数 true 表示裁切右侧的透明像素
    文档.trim(TrimType.TOPLEFT, true, true, true, true);
}
   

dialog.show();

}


"""