@echo off
cd /d D:\SIH
echo Checking git status...
git status
echo.
echo Pushing any pending changes...
git push
echo.
echo =====================================
echo GitHub Pages Setup Instructions:
echo =====================================
echo.
echo 1. Go to: https://github.com/2808rishu/something-new
echo 2. Click "Settings" tab
echo 3. Scroll down to "Pages" in left sidebar
echo 4. Under "Source", select "Deploy from a branch"
echo 5. Select "main" branch
echo 6. Select "/ (root)" folder
echo 7. Click "Save"
echo 8. Wait 2-3 minutes for deployment
echo 9. Visit: https://2808rishu.github.io/something-new/
echo.
echo =====================================
pause