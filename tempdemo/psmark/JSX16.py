dxf16_jscode = """






function 快速定位码链接() {
    
    app.activeDocument.suspendHistory("快速定位码链接", "花样图层导出()");
}




function 花样图层导出() {
    var 导出目录 = Folder.selectDialog("选择外链素材目录");
    if (!导出目录) {
        alert("未选择导出目录。操作已取消。");
        return;
    }
    花样图层导出为TIF透明底(导出目录)
   // 花样图层导出为TIF(导出目录);
  
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
            var lastSubLayerName = lastSubLayer.name;
            FastSubLayer = subLayers[0];
            FastSubLayername= FastSubLayer.name  
       
            //alert(SastSubLayerName)
            // 输出图层组名称和最后一个子图层的名称
          
            
              if (图层组名称 === "填充底图") {
               for (var j = 0; j < subLayers.length; j++) {
                   // alert(subLayers[j].name);
             填充底图组内部循环名称 = subLayers[j].name
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
        释放剪贴蒙版()
        栅格化图层()
        选择下一图层()
        新建图层()
         背景切换();  
        恢复白底();
        填充();
        选择上一图层()
        添加图层蒙版()
        向下合并()
         转换为智能对象()
         重新链接到文件(文件路径)
        创建剪贴蒙版()
         
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



function 创建剪贴蒙版()	//创建剪贴蒙版

    {
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("groupEvent"), d, DialogModes.NO);
       
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

function mergeLayersNew_72799682617188()	//
    {
    
        var d = new ActionDescriptor();
        executeAction(stringIDToTypeID("mergeLayersNew"), d, DialogModes.NO);
     
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

function 图层可见性show()	//图层可见性
    {
    
        var d = new ActionDescriptor();
        var list = new ActionList();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        list.putReference(r);
        d.putList(stringIDToTypeID("null"), list);
        executeAction(stringIDToTypeID("show"), d, DialogModes.NO);
     
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

 
 
 
function 多选图层(SastSubLayerName)	//
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



function 释放剪贴蒙版()	//释放剪贴蒙版
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("ungroup"), d, DialogModes.NO);
     
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

function 向下合并()	//向下合并
    {
    
        var d = new ActionDescriptor();
        executeAction(stringIDToTypeID("mergeLayersNew"), d, DialogModes.NO);
      
    }
    
function 栅格化图层()	//栅格化图层
    {
  
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("rasterizeLayer"), d, DialogModes.NO);

    }

function 选择下一图层()	//
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("backwardEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putBoolean(stringIDToTypeID("makeVisible"), false);
        var list = new ActionList();
        list.putInteger(314);
        d.putList(stringIDToTypeID("layerID"), list);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
     
    }

function 选择上一图层()	//
    {
  
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putEnumerated(stringIDToTypeID("layer"), stringIDToTypeID("ordinal"), stringIDToTypeID("forwardEnum"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putBoolean(stringIDToTypeID("makeVisible"), false);
        var list = new ActionList();
        list.putInteger(369);
        d.putList(stringIDToTypeID("layerID"), list);
        executeAction(stringIDToTypeID("select"), d, DialogModes.NO);
    
    }
function 新建图层()	//新建图层
    {
   
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putClass(stringIDToTypeID("layer"));
        d.putReference(stringIDToTypeID("null"), r);
        d.putInteger(stringIDToTypeID("layerID"), 373);
        executeAction(stringIDToTypeID("make"), d, DialogModes.NO);
     
    }


function 恢复白底()	//删除图层
    {
  
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("color"), stringIDToTypeID("colors"));
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("exchange"), d, DialogModes.NO);
    
    }

function 背景切换()	//
    {
    
        var d = new ActionDescriptor();
        var r = new ActionReference();
        r.putProperty(stringIDToTypeID("color"), stringIDToTypeID("colors"));
        d.putReference(stringIDToTypeID("null"), r);
        executeAction(stringIDToTypeID("reset"), d, DialogModes.NO);
      
    }

function 填充()	//填充
    {
  
        var d = new ActionDescriptor();
        d.putEnumerated(stringIDToTypeID("using"), stringIDToTypeID("fillContents"), stringIDToTypeID("foregroundColor"));
        d.putUnitDouble(stringIDToTypeID("opacity"), stringIDToTypeID("percentUnit"), 100);
        d.putEnumerated(stringIDToTypeID("mode"), stringIDToTypeID("blendMode"), stringIDToTypeID("normal"));
        executeAction(stringIDToTypeID("fill"), d, DialogModes.NO); 
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


































"""