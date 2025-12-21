@echo off
echo ========================================
echo    Enercon RAG - Knowledge Base
echo ========================================
echo.
echo Starting Pinecone Server...
start /B python "%~dp0pinecone_server.py"
timeout /t 3 /nobreak >nul
echo Opening App...
start "" "%~dp0pinecone_app.html"
echo.
echo Server running at ws://localhost:8765
echo Press any key to stop server...
pause >nul
taskkill /F /IM python.exe >nul 2>&1
