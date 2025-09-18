@echo off
set PYTHONPATH=%PYTHONPATH%;%cd%
echo PYTHONPATH set to: %PYTHONPATH%
echo Running tests...
python -m pytest tests/ -v