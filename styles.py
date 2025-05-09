DARK_THEME = """
/* Main Window */
QMainWindow {
    background-color: #1e1e2e;
    color: #f0f0f0;
    font-family: 'Segoe UI', Arial, sans-serif;
}

/* Control Buttons */
QPushButton {
    background-color: #3a3a5a;
    border: none;
    border-radius: 15px;
    padding: 8px 15px;
    color: white;
    font-size: 14px;
    min-width: 60px;
}

QPushButton:hover {
    background-color: #4a4a6a;
}

QPushButton:pressed {
    background-color: #2a2a4a;
}

/* Play/Pause Button */
QPushButton#playButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #7d5fff, stop:1 #5b7dff);
    border-radius: 20px;
    padding: 10px 20px;
    font-weight: bold;
    color: white;
}

QPushButton#playButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #8d6fff, stop:1 #6b8dff);
}

/* Progress Slider */
QSlider::groove:horizontal {
    height: 6px;
    background: #3a3a5a;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    width: 14px;
    height: 14px;
    background: #6a6a8a;
    border-radius: 7px;
    margin: -4px 0;
}

QSlider::sub-page:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #7d5fff, stop:1 #5b7dff);
    border-radius: 3px;
}

/* Volume Slider */
QSlider#volumeSlider::groove:horizontal {
    height: 4px;
    background: #3a3a5a;
    border-radius: 2px;
}

QSlider#volumeSlider::handle:horizontal {
    width: 12px;
    height: 12px;
    background: #6a6a8a;
    border-radius: 6px;
    margin: -4px 0;
}

QSlider#volumeSlider::sub-page:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #7d5fff, stop:1 #5b7dff);
    border-radius: 2px;
}

/* Playlist */
QListWidget {
    background-color: #2a2a3a;
    border: 1px solid #3a3a4a;
    border-radius: 8px;
    padding: 5px;
    font-size: 13px;
}

QListWidget::item {
    padding: 8px;
    border-bottom: 1px solid #3a3a4a;
}

QListWidget::item:selected {
    background-color: #4a4a6a;
    color: white;
}

/* Album Art */
QLabel#albumArt {
    border-radius: 10px;
    border: 2px solid #4a4a6a;
    background: #2a2a3a;
}

/* Search Bar */
QLineEdit {
    background-color: #2a2a3a;
    border: 1px solid #3a3a4a;
    border-radius: 15px;
    padding: 8px 15px;
    color: white;
    font-size: 13px;
}

QLineEdit:focus {
    border: 1px solid #5b7dff;
}

/* Time Labels */
QLabel#timeLabel {
    color: #8a8a9a;
    font-size: 12px;
}

/* Song Info */
QLabel#songInfo {
    color: white;
    font-size: 14px;
    font-weight: bold;
}

/* Menu Bar */
QMenuBar {
    background-color: #2a2a3a;
    color: white;
}

QMenuBar::item:selected {
    background-color: #4a4a6a;
}

QMenu {
    background-color: #2a2a3a;
    color: white;
    border: 1px solid #3a3a4a;
}

QMenu::item:selected {
    background-color: #4a4a6a;
}
"""

LIGHT_THEME = """
/* Main Window */
QMainWindow {
    background-color: #f5f5f7;
    color: #333333;
    font-family: 'Segoe UI', Arial, sans-serif;
}

/* Control Buttons */
QPushButton {
    background-color: #e0e0e5;
    border: none;
    border-radius: 15px;
    padding: 8px 15px;
    color: #333333;
    font-size: 14px;
    min-width: 60px;
}

QPushButton:hover {
    background-color: #d0d0d5;
}

QPushButton:pressed {
    background-color: #c0c0c5;
}

/* Play/Pause Button */
QPushButton#playButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #5b7dff, stop:1 #7d5fff);
    border-radius: 20px;
    padding: 10px 20px;
    font-weight: bold;
    color: white;
}

QPushButton#playButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #6b8dff, stop:1 #8d6fff);
}

/* Progress Slider */
QSlider::groove:horizontal {
    height: 6px;
    background: #e0e0e5;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    width: 14px;
    height: 14px;
    background: #5b7dff;
    border-radius: 7px;
    margin: -4px 0;
}

QSlider::sub-page:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #5b7dff, stop:1 #7d5fff);
    border-radius: 3px;
}

/* Volume Slider */
QSlider#volumeSlider::groove:horizontal {
    height: 4px;
    background: #e0e0e5;
    border-radius: 2px;
}

QSlider#volumeSlider::handle:horizontal {
    width: 12px;
    height: 12px;
    background: #5b7dff;
    border-radius: 6px;
    margin: -4px 0;
}

QSlider#volumeSlider::sub-page:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #5b7dff, stop:1 #7d5fff);
    border-radius: 2px;
}

/* Playlist */
QListWidget {
    background-color: #ffffff;
    border: 1px solid #d0d0d0;
    border-radius: 8px;
    padding: 5px;
    font-size: 13px;
}

QListWidget::item {
    padding: 8px;
    border-bottom: 1px solid #e0e0e5;
}

QListWidget::item:selected {
    background-color: #e0e0e5;
    color: #333333;
}

/* Album Art */
QLabel#albumArt {
    border-radius: 10px;
    border: 2px solid #d0d0d0;
    background: #ffffff;
}

/* Search Bar */
QLineEdit {
    background-color: #ffffff;
    border: 1px solid #d0d0d0;
    border-radius: 15px;
    padding: 8px 15px;
    color: #333333;
    font-size: 13px;
}

QLineEdit:focus {
    border: 1px solid #5b7dff;
}

/* Time Labels */
QLabel#timeLabel {
    color: #666666;
    font-size: 12px;
}

/* Song Info */
QLabel#songInfo {
    color: #333333;
    font-size: 14px;
    font-weight: bold;
}

/* Menu Bar */
QMenuBar {
    background-color: #ffffff;
    color: #333333;
}

QMenuBar::item:selected {
    background-color: #e0e0e5;
}

QMenu {
    background-color: #ffffff;
    color: #333333;
    border: 1px solid #d0d0d0;
}

QMenu::item:selected {
    background-color: #e0e0e5;
}
""" 