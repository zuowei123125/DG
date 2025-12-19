dxf18_jscode = """

function 龙服的快速换图(){
// 强制使用 UTF-8 编码
#target photoshop
$.localize = true;

// 创建对话框
var dialog = new Window("dialog"); 
dialog.text = "快速换图特定版本"; 
dialog.orientation = "column"; 
dialog.alignChildren = ["left","top"]; 
dialog.spacing = 10; 
dialog.margins = 16; 

// 大货模板文件夹选择面板
var templatePanel = dialog.add("panel", undefined, "大货模板文件夹选择");
templatePanel.orientation = "row"; 
templatePanel.alignChildren = ["left","center"]; 
templatePanel.spacing = 10; 
templatePanel.margins = 10; 

// 大货模板文件夹路径文本框
var templatePathEditText = templatePanel.add('edittext', undefined, '', { properties: { readonly: true } });
templatePathEditText.preferredSize.width = 300;

// 大货模板路径选择按钮
var selectTemplateButton = templatePanel.add("button", undefined, "选择文件夹"); 
selectTemplateButton.onClick = function() {
    var selectedFolder = Folder.selectDialog("选择大货模板文件夹");
    if (selectedFolder != null) {
        templatePathEditText.text = selectedFolder.fsName;
      //  alert( templatePathEditText.text)
        updateFileNames(selectedFolder);
    }
};

// 切片裁片文件夹选择面板
var slicePanel = dialog.add("panel", undefined, "切片裁片文件夹选择");
slicePanel.orientation = "row"; 
slicePanel.alignChildren = ["left","center"]; 
slicePanel.spacing = 10; 
slicePanel.margins = 10; 

// 切片裁片文件夹路径文本框
var slicePathEditText = slicePanel.add('edittext', undefined, '', { properties: { readonly: true } });
slicePathEditText.preferredSize.width = 300;

// 切片裁片路径选择按钮
var selectSliceButton = slicePanel.add("button", undefined, "选择文件夹"); 
selectSliceButton.onClick = function() {
    var selectedFolder = Folder.selectDialog("选择切片裁片文件夹");
    if (selectedFolder != null) {
        slicePathEditText.text = selectedFolder.fsName;
        // 可以在这里执行切片裁片相关的操作
    }
};

// 大货裁片名称面板
var fileNamesPanel = dialog.add("panel", undefined, "大货裁片名称数量");
fileNamesPanel.orientation = "column"; 
fileNamesPanel.alignChildren = ["left","top"]; 
fileNamesPanel.spacing = 10; 
fileNamesPanel.margins = 10; 

// 存储文件名和输入框内容的数组
var userInputData = [];

// 更新文件名和输入框显示
function updateFileNames(folder) {
    // 移除之前的所有元素
    for (var i = fileNamesPanel.children.length - 1; i >= 0; i--) {
        fileNamesPanel.children[i].remove();
    }

    // 清空数组
    userInputData = [];

    var files = folder.getFiles();
    for (var i = 0; i < files.length; i++) {
        // 使用正则表达式提取文件名（去掉路径和后缀）
         完整文件路径=files[i].fsName
        var fileName = new File(files[i]).name.replace(/\.\w+$/, "");
        
        // 创建新的静态文本框
        var fileNameStaticText = fileNamesPanel.add('statictext', undefined, fileName);
        fileNameStaticText.preferredSize.width = 200;

        // 创建新的输入框
        var inputEditText = fileNamesPanel.add('edittext', undefined, '');
        inputEditText.preferredSize.width = 100;

        // 存储文件名和输入框内容
        userInputData.push({
            fileName: fileName,
            inputText: ''
        });
    }

    // 重新绘制对话框
    dialog.layout.layout(true);
    dialog.layout.resize();
}

// OK 和 Cancel 按钮
var buttonsGroup = dialog.add("group");
buttonsGroup.orientation = "row"; 
buttonsGroup.alignChildren = ["fill","top"]; 
buttonsGroup.spacing = 10; 
buttonsGroup.margins = 0; 

var okButton = buttonsGroup.add("button", undefined, "执行");
okButton.onClick = function() {
    // 在这里执行 OK 按钮的操作
    updateUserData();
    alertUserInput();
    dialog.close();
};

var cancelButton = buttonsGroup.add("button", undefined, "取消");
cancelButton.onClick = function() {
    // 在这里执行 Cancel 按钮的操作
    dialog.close();
};

// 显示对话框
dialog.show();

// 更新用户输入数据
function updateUserData() {
    for (var i = 1; i < fileNamesPanel.children.length; i += 2) {
        userInputData[(i - 1) / 2].inputText = fileNamesPanel.children[i].text;
    }
}
// 弹出用户输入的内容
function alertUserInput() {
    var userInput = "";
    for (var i = 0; i < userInputData.length; i++) {
        var 文件路径=templatePathEditText.text
        var  文件名=userInputData[i].fileName
        var 完整文件路径=文件路径+"/"+文件名+".tif"
      //  alert( 完整文件路径)
        var  文件数量= userInputData[i].inputText
        var 文件夹路径=slicePathEditText.text
        var 文件对象 = new File(完整文件路径);
        if (文件对象.exists) {
            app.open(文件对象);
        } else {
            //alert("文件不存在：" + 完整文件路径);
        }
       
         更换当前文档裁片组外链(文件夹路径)
         图层选择()
         activeDocument.activeLayer.textItem.contents=文件数量
         选择裁片图层()
         合并图层()
         另存为(文件夹路径)
         
activeDocument.close(SaveOptions.DONOTSAVECHANGES); 
      
       
    }
 
}

  alert("换图完成，请检查好文件进行打印大货！！！",dialog.text+"----关于");

 dialog.close();



function 另存为(文件夹路径)
{
文档名称=activeDocument.name.replace(/(?:\.[^.]*$|$)/, '');
saveIn=File(文件夹路径+ "/"+文档名称);
     tifSaveOpt = new TiffSaveOptions();
    tifSaveOpt.imageCompression = TIFFEncoding.TIFFLZW;
    tifSaveOpt.byteOrder = ByteOrder.IBM;
    asCopy=true
    app.activeDocument.saveAs(saveIn,tifSaveOpt,asCopy);
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
function 合并图层()	//合并图层
    {
 
        var d = new ActionDescriptor();
        executeAction(stringIDToTypeID("mergeLayersNew"), d, DialogModes.NO);
      
    }
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


function 图层选择()	//
    {
    try {
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putName(stringIDToTypeID("layer"), "数量");
        d.putReference(stringIDToTypeID("null"), r);
        d.putBoolean(stringIDToTypeID("makeVisible"), false);
        var list = new ActionList();
        list.putInteger(74);
        d.putList(stringIDToTypeID("layerID"), list);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
        }
    catch (e) {      
        alert("找不到数量图层",dialog.text+"----关于");

    }
   }


 }

"""