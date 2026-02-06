@echo off
cd /d "%~dp0"
echo Starting Web Interface...
".\venv\Scripts\streamlit.exe" run app.py
pause
