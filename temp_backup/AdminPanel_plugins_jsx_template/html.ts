export function joinHtml(name:string,server:string){
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>${name}</title>
    <script>
        // 直接跳转到目标网址（带时间戳防止缓存）
        window.location.href = "https://app.aidg168.uk/?_t=" + Date.now();
    </script>
</head>
<body>
</body>
</html>`
}