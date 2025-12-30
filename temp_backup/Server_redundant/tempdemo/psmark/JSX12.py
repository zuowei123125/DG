dxf12_jscode = """





批量套数写入()

function 批量套数写入() {
  app.preferences.rulerUnits = Units.CM;
  var 主文档 = app.activeDocument;
  var 主文档名称 = 主文档.name;

  // 遍历当前打开的文档
  for (var i = 0; i < app.documents.length; i++) {
    var document = app.documents[i];
    var documentName = document.name;

    // 判断文档名称是否与主文档名称不相同
    if (documentName !== 主文档名称) {
      // 设置当前文档为活动文档
      app.activeDocument = document;

      var 匹配图层数组 = 遍历图层查找P1();

      // 遍历匹配图层数组
      for (var j = 0; j < 匹配图层数组.length; j++) {
        var 当前匹配图层 = 匹配图层数组[j];
}
        // 选中当前匹配图层
       

        // 获取当前选区
        var currentSelection = app.activeDocument.selection;

        // 确保当前选区不为空且为矩形选区
        if (currentSelection != null && currentSelection.hasOwnProperty('bounds')) {
          // 进行缩放操作
        
            app.activeDocument.activeLayer = 当前匹配图层;

        // 载入选区
            载入选区();
          // 获取当前选区的坐标
          var bounds = currentSelection.bounds;

          // 获取当前选区的宽度和高度（以 cm 为单位）
          var resolution = app.activeDocument.resolution;
          var widthInCM = (bounds[2].as("cm") - bounds[0].as("cm"));
          var heightInCM = (bounds[3].as("cm") - bounds[1].as("cm"));
          var 当前P1图层宽高信息 = "宽度：" + widthInCM.toFixed(2) + "cm，高度：" + heightInCM.toFixed(2) + "cm";

          // 获取当前裁片套数
          var 搜索关键词 = "P1";
          var 匹配的图层数量 = 获取匹配图层数量(搜索关键词);
          var 当前裁片套数 = "一段" + 匹配的图层数量 + "件";

          // 创建新图层并设置名称
        ///  var 新图层 = 主文档.artLayers.add();
      //  var  新图层 = "当前文档宽度缩水" + 宽度值 + "高度缩水" + 高度值;

          // 移动选区到新图层
        //  currentSelection.cut();
        //  app.activeDocument.paste();
         //  alert(当前裁片套数);
          // alert( 当前P1图层宽高信息);
          // 文件简介写入
             文件简介写入(当前裁片套数, 当前P1图层宽高信息 );
  
      //   这里删除了文件简介的写入将缩水值修改按钮
           // 调整图像尺寸(宽度值, 高度值);
            ////这里取消了保存功能 为了防止运行的时候变卡
            //activeDocument.save();
        } else {
         // alert("没有找到匹配的图层。");
        }
      
    }
  }
  app.activeDocument=主文档 
 // alert("写入信息成功","来自左威的提醒");
}

function 文件简介写入(当前裁片套数, 当前P1图层宽高信息) {
  var d = new ActionDescriptor();
  var r = new ActionReference();
  r.putProperty(stringIDToTypeID("property"), stringIDToTypeID("fileInfo"));
  r.putEnumerated(stringIDToTypeID("document"), stringIDToTypeID("ordinal"), stringIDToTypeID("targetEnum"));
  d.putReference(stringIDToTypeID("null"), r);
  var d1 = new ActionDescriptor();
  d1.putString(stringIDToTypeID("caption"), 当前裁片套数);
  d1.putString(stringIDToTypeID("keywords"), 当前P1图层宽高信息);
  d.putObject(stringIDToTypeID("to"), stringIDToTypeID("fileInfo"), d1);
  executeAction(stringIDToTypeID("set"), d, DialogModes.NO);
}




function 调整图像尺寸(宽度值, 高度值) {
  var 动作描述 = new ActionDescriptor();
  动作描述.putUnitDouble(stringIDToTypeID("width"), stringIDToTypeID("percentUnit"), 100 + 宽度值);
  动作描述.putUnitDouble(stringIDToTypeID("height"), stringIDToTypeID("percentUnit"), 100 + 高度值);
  动作描述.putEnumerated(charIDToTypeID("Intr"), stringIDToTypeID("interpolationType"), stringIDToTypeID("nearestNeighbor"));
  executeAction(stringIDToTypeID("imageSize"), 动作描述, DialogModes.NO);
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




function 遍历图层查找P1() {
  var 匹配图层数组 = [];
  var 文档 = app.activeDocument;

  // 遍历所有图层
  function 遍历所有图层(图层) {
    if (图层.typename === "LayerSet") {
      for (var i = 0; i < 图层.layers.length; i++) {
        遍历所有图层(图层.layers[i]);
      }
    } else {
      var 图层名分割数组 = 图层.name.split("-");  // 假设分割符是 "_"
      if (图层名分割数组[0] === "P1") {  // 精确匹配
        匹配图层数组.push(图层);
      }
    }
  }

  // 开始遍历
  for (var j = 0; j < 文档.layers.length; j++) {
    遍历所有图层(文档.layers[j]);
  }

  return 匹配图层数组;
}


function 获取匹配图层数量(搜索关键词) {
  var 匹配图层数量 = 0;

  // 递归遍历图层及其子图层
  function 遍历图层(图层) {
    if (图层.typename === "LayerSet") {
      for (var i = 0; i < 图层.layers.length; i++) {
        遍历图层(图层.layers[i]);
      }
    } else {
      // 进行模糊匹配和精确分割匹配
      if (图层.name.indexOf(搜索关键词) !== -1 && 精确分割匹配图层(图层.name, 搜索关键词)) {
        匹配图层数量++;
      }
    }
  }

  // 精确分割匹配图层名
  function 精确分割匹配图层(图层名, 搜索词) {
    var 图层名分割数组 = 图层名.split("-");  // 假设分割符是 "_"
    return 图层名分割数组[0] === 搜索词;
  }

  var 当前文档 = app.activeDocument;
  var 所有图层 = 当前文档.layers;

  for (var i = 0; i < 所有图层.length; i++) {
    遍历图层(所有图层[i]);
  }

  return 匹配图层数量;
}





"""