@echo off
echo =======================================================
echo   Cai dat Image to Vector Topbar Extension & Skill
echo =======================================================
echo.

set EXT_DIR=%USERPROFILE%\.vscode\extensions\image-to-vector-button
set SKILL_DIR=%USERPROFILE%\.gemini\skills\image-to-vector

echo [*] Dang sao chep Extension vao %EXT_DIR%...
if exist "%EXT_DIR%" rmdir /s /q "%EXT_DIR%"
xcopy /E /I /Y "%~dp0extension" "%EXT_DIR%" >nul

echo [*] Dang lien ket Skill vao Antigravity (%SKILL_DIR%)...
if not exist "%USERPROFILE%\.gemini\skills" mkdir "%USERPROFILE%\.gemini\skills"
if exist "%SKILL_DIR%" rmdir /s /q "%SKILL_DIR%"
mkdir "%SKILL_DIR%"
copy /Y "%~dp0SKILL.md" "%SKILL_DIR%\" >nul
xcopy /E /I /Y "%~dp0scripts" "%SKILL_DIR%\scripts\" >nul

echo.
echo [DONE] Cai dat thanh cong!
echo Khoi dong lai Antigravity, nut "Vectorize Image" se xuat hien tren Topbar.
pause
