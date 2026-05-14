@echo off
cd /d "%~dp0"

echo Starting A.L.F.R.E.D...
pause

start /min ollama serve
echo Ollama started
pause

python alfred.py
echo Python finished
pause