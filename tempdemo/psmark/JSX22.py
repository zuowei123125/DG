dxf22_jscode = """


//PS智能对象换图

function 模特换衣功能(){


var dialog = new Window("dialog"); 
    dialog.text = "模特批量替换"; 
    dialog.preferredSize.width = 400; 
    dialog.preferredSize.height = 150; 
    dialog.orientation = "column"; 
    dialog.alignChildren = ["center","top"]; 
    dialog.spacing = 10; 
    dialog.margins = 16; 

// GROUP1
// ======
var group1 = dialog.add("group"); 
    group1.orientation = "row"; 
    group1.alignChildren = ["left","center"]; 
    group1.spacing = 10; 
    group1.margins = 0; 

var statictext1 = group1.add("statictext"); 
    statictext1.text = "模板文件"; 
    statictext1.justify = "center"; 

var edittext1 = group1.add("edittext"); 
    edittext1.preferredSize.width = 250; 

var button1 = group1.add("button"); 
    button1.text = "选择文件"; 
    button1.justify = "center"; 

// GROUP2
// ======
var group2 = dialog.add("group"); 
    group2.orientation = "row"; 
    group2.alignChildren = ["left","center"]; 
    group2.spacing = 10; 
    group2.margins = 0; 

var statictext2 = group2.add("statictext"); 
    statictext2.text = "素材目录"; 
    statictext2.justify = "center"; 

var edittext2 = group2.add("edittext"); 
    edittext2.preferredSize.width = 250; 

var button2 = group2.add("button"); 
    button2.text = "选择目录"; 
    button2.justify = "center"; 

// GROUP3
// ======
var group3 = dialog.add("group"); 
    group3.orientation = "row"; 
    group3.alignChildren = ["left","center"]; 
    group3.spacing = 10; 
    group3.margins = 0; 

var statictext3 = group3.add("statictext"); 
    statictext3.text = "导出目录"; 
    statictext3.justify = "center"; 

var edittext3 = group3.add("edittext"); 
    edittext3.preferredSize.width = 250; 

var button3 = group3.add("button"); 
    button3.text = "选择目录"; 
    button3.justify = "center"; 


var group5 = dialog.add("group"); 
var cbox1 = group5.add("checkbox"); 
    cbox1.text = "是否遍历子文件夹素材"; 
    cbox1.value = true; 

var cbox2 = group5.add("checkbox"); 
    cbox2.text = "是否保存文件结构"; 
    cbox2.value = true; 

var cbox3 = group5.add("checkbox"); 
    cbox3.text = "切片导出"; 
    cbox3.value = false; 
    
// GROUP4
// ======
var group4 = dialog.add("group"); 
    group4.orientation = "row"; 
    group4.alignChildren = ["left","center"]; 
    group4.spacing = 10; 
    group4.margins = 0; 

var button4 = group4.add("button"); 
    button4.text = "执行"; 
    button4.justify = "center"; 

var button5 = group4.add("button"); 
    button5.text = "退出"; 
    button5.justify = "center"; 




    
    
button1.onClick = function()
{
    
    var inputFile= app.openDialog();
    if (inputFile != null) 
    {
        edittext1.text = decodeURI(inputFile);
    }

}

    
button2.onClick = function()
{
    
    var inputFolder = Folder.selectDialog("请选择素材目录：");
    if (inputFolder != null) 
    {
        edittext2.text = decodeURI(inputFolder);
    }

}



button3.onClick = function()
{
    
    var inputFolder = Folder.selectDialog("请选择导出目录：");
    if (inputFolder != null) 
    {
        edittext3.text = decodeURI(inputFolder);
    }

}

button4.onClick = function()
{
    模板路径 = edittext1.text;
    素材目录 = edittext2.text;
    导出目录 = edittext3.text;
    main(模板路径,素材目录,导出目录);
}

button5.onClick = function()
{
    
    dialog.close();
}


function main(模板路径,素材目录,导出目录)
{
    
    
    if(Folder(导出目录).exists==false){Folder(导出目录).create();}

    var doc = app.open(File(模板路径));
//~     素材文件列表 = Folder(素材目录).getFiles("*.psd");
    
    isSubFolders = cbox1.value;
    素材文件列表 = 遍历目录指定类型文件(素材目录,isSubFolders);
    

    alert("当前目录一共有"+素材文件列表.length+"个素材。","提示:");

    try
    {
        lay_替换对象图层名 = "替换对象";
        lay_替换对象 = app.activeDocument.artLayers.getByName(lay_替换对象图层名);
    }
    catch(e)
    {
        alert("未找到["+lay_替换对象图层名+"]智能对象图层！","提示:");
    }
    
    app.activeDocument.activeLayer = lay_替换对象;

    for(var i=0;i<素材文件列表.length;i++)
    {
        scpsd_path = 素材文件列表[i];
    //~     lay_替换对象.visible = false;
    
        素材名 = decodeURI(File(scpsd_path).name.replace(/(?:\.[^.]*$|$)/, ''));

        //替换内容
        var d = new ActionDescriptor();
        d.putPath(stringIDToTypeID("null"), new File(scpsd_path));
        executeAction(stringIDToTypeID("placedLayerReplaceContents"), d, DialogModes.NO);
        
        if(cbox2.value) //保持结构
        {
            结构导出目录 = 导出目录+"/" + getRelativePath(decodeURI(File(scpsd_path).path), 素材目录);
            
            if(Folder(结构导出目录).exists==false){Folder(结构导出目录).create();}
            
            保存路径 = 结构导出目录+"/"+素材名+".jpg";
            $.writeln(保存路径);
            
            if(cbox3.value) //按切片
            {
//~                 按切片导出图片(结构导出目录,app.activeDocument.name.replace(/(?:\.[^.]*$|$)/, ''));
                按切片导出图片(结构导出目录,素材名);
            }
            else
            {
                保存JPG(保存路径);
            }
        }
        else
        {
            if(cbox3.value) //按切片
            {
//~                 按切片导出图片(导出目录,app.activeDocument.name.replace(/(?:\.[^.]*$|$)/, ''));
                按切片导出图片(导出目录,素材名);
            }
            else
            {
                保存JPG(导出目录+"/"+素材名+".jpg");
            }
        
            
        }
    
    
    }

    doc.close(SaveOptions.DONOTSAVECHANGES);
    alert("处理完成！","提示:");
}



function getRelativePath(targetPath, basePath) 
{
  var targetFile = new File(targetPath);
  var baseFolder = new Folder(basePath);

  var relativePath = targetFile.getRelativeURI(baseFolder);

  return decodeURI(relativePath); // 解码 URI 编码的路径
}




function 保存JPG(jpg_save_path)
{
    // 以JPEG格式保存输出
    var jpegOptions = new JPEGSaveOptions();
    // 将jpeg质量设置得很低，使文件很小
    jpegOptions.quality = 12;

    app.activeDocument.saveAs(new File(jpg_save_path), jpegOptions,true);
}


function 遍历目录指定类型文件(inputFolder,isSubFolders)
{
    if(isSubFolders==undefined)
    {
        isSubFolders = true;
    }

    all_files_list = [];
    if (inputFolder != null) {

        filesArray = scanFolder(inputFolder);

        if (filesArray.length > 0) 
        {
            for (i = 0;i<filesArray.length;i++)
            {
               all_files_list.push(filesArray[i]);
            }
        }
    }

    return all_files_list;
    
    function scanFolder(folder) 
    {

        var filesArray = [],

        fileList = Folder(folder).getFiles();
        var file;

        

        for (var i = 0; i < fileList.length; i++) {

            file = fileList[i];

            if (file instanceof Folder) 
            {
                if(isSubFolders==false)
                {
                    continue;
                }
                else
                {
                    filesArray = filesArray.concat(scanFolder(file));
                }

            }
            else if (file instanceof File && file.name.match(/\.(jpg|tif|psd|png|)$/i)) 
            {

                filesArray.push(file);

            }

        }

        return filesArray;

    }

}



function 按切片导出图片(保存路径,替换词)
{
//~         alert(保存路径);
        var d = new ActionDescriptor();
        var d1 = new ActionDescriptor();
        d1.putEnumerated(charIDToTypeID("Op  "), charIDToTypeID("SWOp"), charIDToTypeID("OpSa"));
        d1.putBoolean(charIDToTypeID("DIDr"), true);
        
        d1.putPath(stringIDToTypeID("in"), new File(保存路径));

        d1.putString(charIDToTypeID("ovFN"), 替换词+".jpg");

        
        d1.putEnumerated(stringIDToTypeID("format"), charIDToTypeID("IRFm"), stringIDToTypeID("JPEG"));
        d1.putBoolean(charIDToTypeID("Intr"), false);
        d1.putInteger(stringIDToTypeID("quality"), 80);
        d1.putInteger(charIDToTypeID("QChS"), 0);
        d1.putInteger(charIDToTypeID("QCUI"), 0);
        d1.putBoolean(charIDToTypeID("QChT"), false);
        d1.putBoolean(charIDToTypeID("QChV"), false);
        d1.putBoolean(stringIDToTypeID("optimized"), true);
        d1.putInteger(charIDToTypeID("Pass"), 1);
        d1.putDouble(stringIDToTypeID("blur"), 0);
        d1.putBoolean(charIDToTypeID("Mtt "), true);
        d1.putBoolean(charIDToTypeID("EICC"), false);
        d1.putInteger(charIDToTypeID("MttR"), 255);
        d1.putInteger(charIDToTypeID("MttG"), 255);
        d1.putInteger(charIDToTypeID("MttB"), 255);
        d1.putBoolean(charIDToTypeID("SHTM"), false);
        d1.putBoolean(charIDToTypeID("SImg"), true);
        d1.putEnumerated(charIDToTypeID("SWsl"), charIDToTypeID("STsl"), charIDToTypeID("SLAl"));
        d1.putEnumerated(charIDToTypeID("SWch"), charIDToTypeID("STch"), charIDToTypeID("CHDc"));
        d1.putEnumerated(charIDToTypeID("SWmd"), charIDToTypeID("STmd"), charIDToTypeID("MDCC"));
        d1.putBoolean(charIDToTypeID("ohXH"), false);
        d1.putBoolean(charIDToTypeID("ohIC"), true);
        d1.putBoolean(charIDToTypeID("ohAA"), true);
        d1.putBoolean(charIDToTypeID("ohQA"), true);
        d1.putBoolean(charIDToTypeID("ohCA"), false);
        d1.putBoolean(charIDToTypeID("ohIZ"), true);
        d1.putEnumerated(charIDToTypeID("ohTC"), charIDToTypeID("SToc"), charIDToTypeID("OC03"));
        d1.putEnumerated(charIDToTypeID("ohAC"), charIDToTypeID("SToc"), charIDToTypeID("OC03"));
        d1.putInteger(charIDToTypeID("ohIn"), -1);
        d1.putEnumerated(charIDToTypeID("ohLE"), charIDToTypeID("STle"), charIDToTypeID("LE03"));
        d1.putEnumerated(charIDToTypeID("ohEn"), charIDToTypeID("STen"), charIDToTypeID("EN00"));
        d1.putBoolean(charIDToTypeID("olCS"), false);
        d1.putEnumerated(charIDToTypeID("olEC"), charIDToTypeID("STst"), charIDToTypeID("ST00"));
        d1.putEnumerated(charIDToTypeID("olWH"), charIDToTypeID("STwh"), charIDToTypeID("WH01"));
        d1.putEnumerated(charIDToTypeID("olSV"), charIDToTypeID("STsp"), charIDToTypeID("SP04"));
        d1.putEnumerated(charIDToTypeID("olSH"), charIDToTypeID("STsp"), charIDToTypeID("SP04"));
        var list = new ActionList();
        var d2 = new ActionDescriptor();
        d2.putEnumerated(charIDToTypeID("ncTp"), charIDToTypeID("STnc"), charIDToTypeID("NC00"));
        list.putObject(charIDToTypeID("SCnc"), d2);
        var d3 = new ActionDescriptor();
        d3.putEnumerated(charIDToTypeID("ncTp"), charIDToTypeID("STnc"), charIDToTypeID("NC19"));
        list.putObject(charIDToTypeID("SCnc"), d3);
        var d4 = new ActionDescriptor();
        d4.putEnumerated(charIDToTypeID("ncTp"), charIDToTypeID("STnc"), charIDToTypeID("NC28"));
        list.putObject(charIDToTypeID("SCnc"), d4);
        var d5 = new ActionDescriptor();
        d5.putEnumerated(charIDToTypeID("ncTp"), charIDToTypeID("STnc"), charIDToTypeID("NC24"));
        list.putObject(charIDToTypeID("SCnc"), d5);
        var d6 = new ActionDescriptor();
        d6.putEnumerated(charIDToTypeID("ncTp"), charIDToTypeID("STnc"), charIDToTypeID("NC24"));
        list.putObject(charIDToTypeID("SCnc"), d6);
        var d7 = new ActionDescriptor();
        d7.putEnumerated(charIDToTypeID("ncTp"), charIDToTypeID("STnc"), charIDToTypeID("NC24"));
        list.putObject(charIDToTypeID("SCnc"), d7);
        d1.putList(charIDToTypeID("olNC"), list);
        d1.putBoolean(charIDToTypeID("obIA"), false);
        d1.putString(charIDToTypeID("obIP"), "");
        d1.putEnumerated(charIDToTypeID("obCS"), charIDToTypeID("STcs"), charIDToTypeID("CS01"));
        var list1 = new ActionList();
        var d8 = new ActionDescriptor();
        d8.putEnumerated(charIDToTypeID("ncTp"), charIDToTypeID("STnc"), charIDToTypeID("NC01"));
        list1.putObject(charIDToTypeID("SCnc"), d8);
        var d9 = new ActionDescriptor();
        d9.putEnumerated(charIDToTypeID("ncTp"), charIDToTypeID("STnc"), charIDToTypeID("NC20"));
        list1.putObject(charIDToTypeID("SCnc"), d9);
        var d10 = new ActionDescriptor();
        d10.putEnumerated(charIDToTypeID("ncTp"), charIDToTypeID("STnc"), charIDToTypeID("NC02"));
        list1.putObject(charIDToTypeID("SCnc"), d10);
        var d11 = new ActionDescriptor();
        d11.putEnumerated(charIDToTypeID("ncTp"), charIDToTypeID("STnc"), charIDToTypeID("NC19"));
        list1.putObject(charIDToTypeID("SCnc"), d11);
        var d12 = new ActionDescriptor();
        d12.putEnumerated(charIDToTypeID("ncTp"), charIDToTypeID("STnc"), charIDToTypeID("NC06"));
        list1.putObject(charIDToTypeID("SCnc"), d12);
        var d13 = new ActionDescriptor();
        d13.putEnumerated(charIDToTypeID("ncTp"), charIDToTypeID("STnc"), charIDToTypeID("NC24"));
        list1.putObject(charIDToTypeID("SCnc"), d13);
        var d14 = new ActionDescriptor();
        d14.putEnumerated(charIDToTypeID("ncTp"), charIDToTypeID("STnc"), charIDToTypeID("NC24"));
        list1.putObject(charIDToTypeID("SCnc"), d14);
        var d15 = new ActionDescriptor();
        d15.putEnumerated(charIDToTypeID("ncTp"), charIDToTypeID("STnc"), charIDToTypeID("NC24"));
        list1.putObject(charIDToTypeID("SCnc"), d15);
        var d16 = new ActionDescriptor();
        d16.putEnumerated(charIDToTypeID("ncTp"), charIDToTypeID("STnc"), charIDToTypeID("NC22"));
        list1.putObject(charIDToTypeID("SCnc"), d16);
        d1.putList(charIDToTypeID("ovNC"), list1);
        d1.putBoolean(charIDToTypeID("ovCM"), false);
        d1.putBoolean(charIDToTypeID("ovCW"), true);
        d1.putBoolean(charIDToTypeID("ovCU"), true);
        d1.putBoolean(charIDToTypeID("ovSF"), true);
        d1.putBoolean(charIDToTypeID("ovCB"), true);
        

        
        d.putObject(stringIDToTypeID("using"), stringIDToTypeID("SaveForWeb"), d1);
        executeAction(stringIDToTypeID("export"), d, DialogModes.NO);
    
}



dialog.show();

}

"""