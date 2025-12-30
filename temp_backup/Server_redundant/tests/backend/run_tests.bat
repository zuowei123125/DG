@echo off
chcp 65001 >nul
echo ========================================
echo   DesignerCEP 后端API测试套件
echo ========================================
echo.

echo [1/3] 检查Python环境...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python未安装！
    pause
    exit /b 1
)

echo.
echo [2/3] 安装测试依赖...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败！
    pause
    exit /b 1
)

echo.
echo [3/3] 运行测试...
echo ========================================
pytest -v --cov=../../Server/app/api/v1 --cov-report=html --html=report.html --self-contained-html

echo.
echo ========================================
echo 测试完成！
echo 查看报告:
echo   - HTML报告: report.html
echo   - 覆盖率报告: htmlcov/index.html
echo ========================================
pause

