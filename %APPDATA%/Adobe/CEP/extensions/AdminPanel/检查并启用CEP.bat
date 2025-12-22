@echo off
chcp 65001 >nul
echo ========================================
echo   CEP 扩展调试模式检查工具
echo ========================================
echo.

echo [1] 检查当前 CEP 调试模式状态...
reg query "HKEY_CURRENT_USER\Software\Adobe\CSXS.8" /v PlayerDebugMode 2>nul
if %errorlevel% neq 0 (
    echo ❌ 未找到 CSXS.8 调试模式配置
) else (
    echo ✅ CSXS.8 配置已存在
)
echo.

echo [2] 启用 CEP 调试模式...
reg add "HKEY_CURRENT_USER\Software\Adobe\CSXS.8" /v PlayerDebugMode /t REG_SZ /d 1 /f >nul
reg add "HKEY_CURRENT_USER\Software\Adobe\CSXS.9" /v PlayerDebugMode /t REG_SZ /d 1 /f >nul
reg add "HKEY_CURRENT_USER\Software\Adobe\CSXS.10" /v PlayerDebugMode /t REG_SZ /d 1 /f >nul
reg add "HKEY_CURRENT_USER\Software\Adobe\CSXS.11" /v PlayerDebugMode /t REG_SZ /d 1 /f >nul

echo ✅ CEP 调试模式已启用（CSXS 8/9/10/11）
echo.

echo [3] 检查插件安装位置...
set "EXT_DIR=%APPDATA%\Adobe\CEP\extensions\AdminPanel"
if exist "%EXT_DIR%\" (
    echo ✅ 插件已安装到: %EXT_DIR%
    dir "%EXT_DIR%" /B
) else (
    echo ❌ 插件未安装，请运行安装命令
)
echo.

echo ========================================
echo   操作完成！
echo   请 [完全关闭 Photoshop] 后重新打开
echo ========================================
pause

