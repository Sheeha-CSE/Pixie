@echo off
title MarketMind — AI-Powered Marketing Assistant
color 0B
cls
echo ====================================================================
echo         MarketMind -- AI-Powered Marketing Assistant
echo ====================================================================
echo.
echo Starting Flask application with Groq AI integration...
echo Local Server: http://127.0.0.1:5000
echo.
echo Demo Accounts:
echo   - Business Owner: owner@marketmind.ai  (Password: owner123)
echo   - Student Marketer: alex@marketmind.ai (Password: employee123)
echo.
echo Pixie AI Assistant is accessible via the sparkling pink mascot widget!
echo ====================================================================
echo.

python -c "import sqlite3; from seed_data import seed_database; seed_database()"
python app.py

pause
