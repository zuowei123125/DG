/**
 * 拖拽文件时，创建一个临时的预览图
 */
import { nodeFs, getOsPrefix } from "@/utils/nodeFs"
import g_config from "@/api/config/index";
/**
 * 通过canvas将svg转成png
 * @param {*} path 路径
 * @returns 返回base64字符串
 */
export function dragFile2png(path, number) {
    // debugger
    let outPath = g_config.path.dragPreview;    
    console.log(path, outPath);

    return new Promise((resolve, reject) => {
        var img = new Image();
        img.src = getOsPrefix() + path;
        img.onload = () => {
            var canvas = document.createElement('canvas');
            var c = canvas.getContext('2d');

            let width, height;
            let scale = img.width / 100;
            if (img.width > img.height) {
                width = 100;
                height = img.height / scale;
            } else {
                scale = img.height / 100;
                height = 100;
                width = img.width / scale;
            }


            canvas.width = width + 20;
            canvas.height = height + 10;
            //canvas画图片
            c.drawImage(img, 10, 10, width, height);
            c.strokeStyle = "#2961d9";
            c.lineWidth = 2;
            c.strokeRect(10, 10, width, height);

            if (number > 1) {
                c.beginPath();
                c.arc(width + 10, 10, 10, 0, Math.PI * 2, true);
                c.closePath();
                c.fillStyle = "rgba(255,0,0,1)";
                c.fill();

                c.fillStyle = "#fff";//文字的颜色
                c.textAlign = 'center';//对齐方式
                // c.font = '13px "微软雅黑"';       
                c.fillText(number, width + 10, 13);
            }


            //将图片添加到body中
            // console.log('转png', canvas.toDataURL('image/png'));
            let base64 = canvas.toDataURL('image/png')
            let temp = nodeFs.sync.writeBase64(outPath, base64.split('base64,')[1]);
            temp.err == 1 ? reject(temp.msg) : resolve({ outPath });
        }

        img.onerror = (err) => {
            reject(err);//转换失败
        }
    })
}