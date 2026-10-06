@echo off
REM ---------------------------------------------------------------
REM  Build a single-file Windows executable with PyInstaller.
REM  Usage:  tools\build.bat
REM  Output: dist\unit_converter.exe
REM ---------------------------------------------------------------
setlocal
cd /d "%~dp0.."

REM Pick a Python that has PyInstaller installed.
set "PY=%PYTHON%"
if not "%PY%"=="" goto :run
set "CANDIDATE=C:\Users\%USERNAME%\.workbuddy\binaries\python\envs\build314\Scripts\python.exe"
if exist "%CANDIDATE%" (
    set "PY=%CANDIDATE%"
) else (
    set "PY=python"
)

:run
echo Using python: %PY%
"%PY%" -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: PyInstaller is not available for this Python.
    echo Install it with:  "%PY%" -m pip install pyinstaller
    exit /b 1
)

echo [1/2] Smoke test the source...
"%PY%" src\unit_converter.py 100 cm m
if errorlevel 1 goto :fail

echo [2/2] Building executable...
"%PY%" -m PyInstaller --noconfirm --clean --onefile --name unit_converter src\unit_converter.py
if errorlevel 1 goto :fail

echo.
echo Done. Output: dist\unit_converter.exe
exit /b 0

:fail
echo BUILD FAILED
exit /b 1
