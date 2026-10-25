@echo off
setlocal
cd /d "%~dp0"
echo.
echo ================================================
echo   SEVENFALL 0.3 - WINDOWS DEVELOPMENT LAUNCHER
echo ================================================
echo.
echo This compiles a local pinned OpenRA SDK installation.
echo The campaign previews have not yet passed live match tests.
echo Red Alert data must be obtained legally, and is not bundled.
echo.
where py >nul 2>nul
if errorlevel 1 (
  echo Python 3 launcher not found. Install Python 3 and check PATH.
  goto error
)
echo [1/3] Running source and mission contract tests...
py -3 -m pip install -r requirements-test.txt
if errorlevel 1 goto error
py -3 -m unittest discover -s tests
if errorlevel 1 goto error
echo [2/3] Compiling pinned engine and checking all mod YAML...
py -3 scripts\build.py build
if errorlevel 1 goto error
echo [3/3] Opening Sevenfall...
py -3 scripts\build.py launch
if errorlevel 1 goto error
exit /b 0
:error
echo.
echo Sevenfall did not finish building or launching.
echo See BUILDING.md and tests/FIRST_WAR_RUNBOOK.md for help.
pause
exit /b 1
