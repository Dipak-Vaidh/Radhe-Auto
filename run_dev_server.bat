@echo off
cd /d "%~dp0"
echo.
echo  Starting Radhe Cars dev server at http://127.0.0.1:8000/
echo  Keep this window OPEN while you use the site. Close it to stop the server.
echo  Staff login: http://127.0.0.1:8000/admin-panel/login/  (use hyphen admin-panel)
echo.
python manage.py runserver
echo.
pause
