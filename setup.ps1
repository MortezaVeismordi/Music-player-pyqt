Write-Host "Creating virtual environment..."
python -m venv venv

Write-Host "Activating virtual environment..."
.\venv\Scripts\Activate.ps1

Write-Host "Installing build tools..."
python -m pip install --upgrade pip
python -m pip install setuptools wheel

Write-Host "Installing requirements..."
pip install -r requirements.txt

Write-Host "Setup complete! You can now run the music player with:"
Write-Host "python music_player.py" 