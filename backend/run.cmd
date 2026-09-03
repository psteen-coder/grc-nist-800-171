@echo off
echo Starting GRC NIST 800-171 Backend...
cd /d "%~dp0"
python -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause