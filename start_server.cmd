@echo off

:: Activate virtual environment
call scripts\activate

:: Get the local IPv4 address dynamically
for /f "tokens=2 delims=:" %%A in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    set ip=%%A
)

:: Remove leading space
set ip=%ip:~1%

echo Detected IP: %ip%
echo.

:: Ask for PostgreSQL password BEFORE server starts
set /p db_pass=Enter PostgreSQL password: 
echo Password stored for this session only.
echo.

:: Run Django server on dynamic IP and port 7000
python manage.py runserver %ip%:7000

pause
