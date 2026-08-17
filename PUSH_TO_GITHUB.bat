@echo off
echo ============================================
echo   PUSH PROJECT TO GITHUB
echo ============================================
echo.
echo Running git status...
git status
echo.
echo Running git log -1 --oneline...
git log -1 --oneline
echo.
echo ============================================
echo Now pushing to GitHub:
echo   Repository: https://github.com/AkashSB242/Admission-Enrollment.git
echo   Branch: main
echo ============================================
echo.
git push -u origin main
echo.
if %errorlevel% EQU 0 (
    echo.
    echo ============================================
    echo [SUCCESS] Project pushed to GitHub!
    echo ============================================
    echo.
    echo Your repository URL: https://github.com/AkashSB242/Admission-Enrollment
) else (
    echo.
    echo [FAILED] Git push still has errors.
    echo.
    echo If this is a "remote-https" error:
    echo   1) Run FIX_GIT_HTTPS_RUN_AS_ADMIN.bat as Administrator first
    echo   2) Then run this file again
    echo.
    echo OR use GitHub Desktop - see README_PUSH_GUIDE.txt for instructions
    echo.
)
pause
