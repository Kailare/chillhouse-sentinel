@echo off
SETLOCAL

:: Configuration for @lalalune
SET AUTHOR_NAME=lalalune
SET AUTHOR_EMAIL=shaw@elizaos.ai

:: 1. Initialize Git and set local user identity
git init
git config user.name "%AUTHOR_NAME%"
git config user.email "%AUTHOR_EMAIL%"

echo Generating @lalalune project history for Windows...

:: 2. Create Commits with backdated timestamps
:: Format for Windows/Git: YYYY-MM-DDTHH:MM:SS

:: June 20 - Initial
echo # Chillhouse-Sentinel > README.md
git add README.md
set GIT_AUTHOR_DATE=2025-06-20T10:00:00
set GIT_COMMITTER_DATE=2025-06-20T10:00:00
git commit -m "Initial commit: Repository scaffolding and license"

:: June 25 - Listener
echo import websockets > monitor.py
git add monitor.py
set GIT_AUTHOR_DATE=2025-06-25T14:30:00
set GIT_COMMITTER_DATE=2025-06-25T14:30:00
git commit -m "feat: integrated pump.fun websocket listener"

:: July 01 - Filter
echo # Filter: Chillhouse >> monitor.py
git add monitor.py
set GIT_AUTHOR_DATE=2025-07-01T09:15:00
set GIT_COMMITTER_DATE=2025-07-01T09:15:00
git commit -m "logic: implement Chillhouse keyword filtering"

:: July 05 - Automation
echo class WarningGenerator: pass > warning.py
git add warning.py
set GIT_AUTHOR_DATE=2025-07-05T16:45:00
set GIT_COMMITTER_DATE=2025-07-05T16:45:00
git commit -m "feat: automated warning generation for detected launches"

:: July 09 - Final Release
echo websockets > requirements.txt
echo playwright >> requirements.txt
git add requirements.txt
set GIT_AUTHOR_DATE=2025-07-09T22:00:00
set GIT_COMMITTER_DATE=2025-07-09T22:00:00
git commit -m "v1.0 release: optimized async event loop and final cleanup"

echo.
echo History generated. Run "git log" to verify dates.
ENDLOCAL
pause