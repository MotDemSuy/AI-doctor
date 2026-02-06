@echo off
cd /d "%~dp0"
echo Running Ollama Connection Test...
".\venv\Scripts\python.exe" test_ollama.py
pause
