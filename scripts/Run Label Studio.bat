@echo off
title Annotation Tool
cd /d "%~dp0"

echo ============================================
echo Starting the annotation tool...
echo.
echo Please keep this window open while annotating.
echo When you are finished, return to this window
echo and press Ctrl+C, then Y, to stop Label Studio.
echo ============================================
echo.

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    python run.py
    goto end
)

where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    py run.py
    goto end
)

echo.
echo ERROR: Python was not found.
echo Please contact the project coordinator.
echo.

:end
echo.
echo Annotation tool has stopped.
pause