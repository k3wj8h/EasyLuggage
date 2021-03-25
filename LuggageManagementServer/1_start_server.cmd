TITLE SERVER - Luggage Management

REM -- Activate and check virtual env
call .venv\Scripts\activate.bat
where python


REM -- Run flask application
set FLASK_APP=lms.py
python -m flask run
