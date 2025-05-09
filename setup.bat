@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing build tools...
python -m pip install --upgrade pip
python -m pip install setuptools wheel

echo Installing requirements...
pip install -r requirements.txt

echo Setup complete! You can now run the music player with:
echo python music_player.py 