@echo off
chcp 65001 >nul
cd /d "%~dp0"
title 康伴 - AI 个人健康问答助手

echo.
echo  ==========================================
echo     康伴 · AI 个人健康问答助手
echo  ==========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo  [错误] 未检测到 Python。
    echo  请先安装 Python 3.10 或更高版本：
    echo  https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo  [1/2] 正在检查并安装依赖（首次运行需等待片刻）...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo  [错误] 依赖安装失败，请检查网络连接后重试。
    echo.
    pause
    exit /b 1
)

echo.
echo  [2/2] 正在启动应用，浏览器将自动打开...
echo  若浏览器未自动打开，请手动访问：http://localhost:8501
echo.
python -m streamlit run streamlit_app.py

pause
