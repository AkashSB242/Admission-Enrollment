@echo off
echo ============================================
echo   GIT HTTPS REMOTE HELPER FIX
echo ============================================
echo.

set "GIT_CORE=C:\Program Files\Git\mingw64\libexec\git-core"
set "GIT_CORE2=C:\Program Files\Git\libexec\git-core"

echo Checking admin privileges...
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo [ERROR] This script requires ADMINISTRATOR privileges.
    echo         Please RIGHT-CLICK this file and select:
    echo         "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo [OK] Running as Administrator
echo.

if exist "%GIT_CORE%\git-remote-http.exe" (
    echo Found git-remote-http.exe in %GIT_CORE%
    if NOT exist "%GIT_CORE%\git-remote-https.exe" (
        echo Creating git-remote-https.exe (copy)...
        copy "%GIT_CORE%\git-remote-http.exe" "%GIT_CORE%\git-remote-https.exe"
    ) else (
        echo git-remote-https.exe already exists!
    )
) else if exist "%GIT_CORE2%\git-remote-http.exe" (
    echo Found git-remote-http.exe in %GIT_CORE2%
    if NOT exist "%GIT_CORE2%\git-remote-https.exe" (
        echo Creating git-remote-https.exe (copy)...
        copy "%GIT_CORE2%\git-remote-http.exe" "%GIT_CORE2%\git-remote-https.exe"
    ) else (
        echo git-remote-https.exe already exists!
    )
) else (
    echo [WARNING] git-remote-http.exe not found in standard locations.
    echo           Recommendation: REINSTALL Git for Windows from:
    echo           https://git-scm.com/download/win
    pause
    exit /b 1
)

echo.
echo ============================================
echo [SUCCESS] Git HTTPS Helper should be fixed!
echo ============================================
echo.
echo You can now run:  git push -u origin main
echo.
pause
