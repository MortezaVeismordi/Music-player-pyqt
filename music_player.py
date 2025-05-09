import sys
import os
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QListWidget, QLabel, 
                            QSlider, QStyle, QFileDialog, QMessageBox, QLineEdit,
                            QGraphicsDropShadowEffect, QInputDialog, QComboBox)
from PyQt5.QtCore import Qt, QUrl, QTimer, QSize, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QIcon, QPixmap, QDragEnterEvent, QDropEvent, QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import pygame
from styles import DARK_THEME, LIGHT_THEME
from advanced_styles import (ADVANCED_STYLES, AnimatedButton, create_shadow_effect,
                           extract_colors_from_art)

class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Professional Music Player")
        self.setMinimumSize(800, 600)
        
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Player state
        self.current_playlist = []
        self.current_index = 0
        self.is_playing = False
        self.is_repeat = False
        self.is_shuffle = False
        self.dark_mode = True
        self.playlists = {"Default": []}  # Dictionary to store playlists with a default playlist
        self.current_playlist_name = "Default"
        self.is_sliding = False  # Flag to track if user is sliding the progress bar
        self.slider_position = 0  # Store the last slider position
        self.start_time = 0  # Store the time when the song started playing
        
        # Create UI
        self.init_ui()
        
        # Setup timer for progress updates
        self.timer = QTimer()
        self.timer.setInterval(100)  # Update more frequently for smoother progress
        self.timer.timeout.connect(self.update_progress)
        
        # Apply initial theme
        self.set_theme("dark")
        
    def init_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Playlist management section
        playlist_section = QHBoxLayout()
        
        # Playlist selector
        self.playlist_selector = QComboBox()
        self.playlist_selector.setObjectName("playlistSelector")
        self.playlist_selector.currentTextChanged.connect(self.switch_playlist)
        playlist_section.addWidget(self.playlist_selector)
        
        # Create playlist button
        self.create_playlist_btn = AnimatedButton("Create Playlist")
        self.create_playlist_btn.setObjectName("controlButton")
        self.create_playlist_btn.clicked.connect(self.create_playlist)
        playlist_section.addWidget(self.create_playlist_btn)
        
        # Delete playlist button
        self.delete_playlist_btn = AnimatedButton("Delete Playlist")
        self.delete_playlist_btn.setObjectName("controlButton")
        self.delete_playlist_btn.clicked.connect(self.delete_playlist)
        playlist_section.addWidget(self.delete_playlist_btn)
        
        layout.addLayout(playlist_section)
        
        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setObjectName("searchBar")
        self.search_bar.setPlaceholderText("Search in playlist...")
        self.search_bar.textChanged.connect(self.search_playlist)
        layout.addWidget(self.search_bar)
        
        # Playlist
        self.playlist_widget = QListWidget()
        self.playlist_widget.setAcceptDrops(True)
        self.playlist_widget.dragEnterEvent = self.dragEnterEvent
        self.playlist_widget.dropEvent = self.dropEvent
        self.playlist_widget.itemDoubleClicked.connect(self.play_selected)
        layout.addWidget(self.playlist_widget)
        
        # Update playlist selector
        self.update_playlist_selector()
        
        # Player bar container
        player_bar = QWidget()
        player_bar.setObjectName("playerBar")
        player_layout = QVBoxLayout(player_bar)
        
        # Album art
        self.album_art = QLabel()
        self.album_art.setObjectName("albumArt")
        self.album_art.setFixedSize(200, 200)
        self.album_art.setAlignment(Qt.AlignCenter)
        create_shadow_effect(self.album_art)
        player_layout.addWidget(self.album_art)
        
        # Song info
        self.song_info = QLabel("No song playing")
        self.song_info.setObjectName("songInfo")
        self.song_info.setAlignment(Qt.AlignCenter)
        player_layout.addWidget(self.song_info)
        
        # Progress bar
        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.setRange(0, 0)
        self.progress_slider.sliderMoved.connect(self.set_position)
        player_layout.addWidget(self.progress_slider)
        
        # Time labels
        time_layout = QHBoxLayout()
        self.current_time = QLabel("00:00")
        self.current_time.setObjectName("timeLabel")
        self.total_time = QLabel("00:00")
        self.total_time.setObjectName("timeLabel")
        time_layout.addWidget(self.current_time)
        time_layout.addStretch()
        time_layout.addWidget(self.total_time)
        player_layout.addLayout(time_layout)
        
        # Control buttons
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(15)
        
        # Previous button
        self.prev_btn = AnimatedButton()
        self.prev_btn.setObjectName("controlButton")
        self.prev_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.prev_btn.clicked.connect(self.play_previous)
        controls_layout.addWidget(self.prev_btn)
        
        # Play/Pause button
        self.play_btn = AnimatedButton()
        self.play_btn.setObjectName("playButton")
        self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_btn.clicked.connect(self.play_pause)
        controls_layout.addWidget(self.play_btn)
        
        # Next button
        self.next_btn = AnimatedButton()
        self.next_btn.setObjectName("controlButton")
        self.next_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.next_btn.clicked.connect(self.play_next)
        controls_layout.addWidget(self.next_btn)
        
        # Repeat button
        self.repeat_btn = AnimatedButton()
        self.repeat_btn.setObjectName("controlButton")
        self.repeat_btn.setIcon(self.style().standardIcon(QStyle.SP_ArrowRight))
        self.repeat_btn.setIconSize(QSize(20, 20))
        self.repeat_btn.setCheckable(True)
        self.repeat_btn.clicked.connect(self.toggle_repeat)
        controls_layout.addWidget(self.repeat_btn)
        
        # Shuffle button
        self.shuffle_btn = AnimatedButton()
        self.shuffle_btn.setObjectName("controlButton")
        self.shuffle_btn.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        self.shuffle_btn.setIconSize(QSize(20, 20))
        self.shuffle_btn.setCheckable(True)
        self.shuffle_btn.clicked.connect(self.toggle_shuffle)
        controls_layout.addWidget(self.shuffle_btn)
        
        # Volume slider
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setObjectName("volumeSlider")
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.set_volume)
        controls_layout.addWidget(self.volume_slider)
        
        player_layout.addLayout(controls_layout)
        layout.addWidget(player_bar)
        
        # Menu bar
        self.create_menu_bar()
        
        # Set initial volume
        pygame.mixer.music.set_volume(0.5)
        
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        open_action = file_menu.addAction("Open File")
        open_action.triggered.connect(self.open_file)
        
        open_folder_action = file_menu.addAction("Open Folder")
        open_folder_action.triggered.connect(self.open_folder)
        
        file_menu.addSeparator()
        
        save_playlist_action = file_menu.addAction("Save Playlist")
        save_playlist_action.triggered.connect(self.save_playlist)
        
        load_playlist_action = file_menu.addAction("Load Playlist")
        load_playlist_action.triggered.connect(self.load_playlist)
        
        # Playlist menu
        playlist_menu = menubar.addMenu("Playlists")
        
        create_playlist_action = playlist_menu.addAction("Create New Playlist")
        create_playlist_action.triggered.connect(self.create_playlist)
        
        delete_playlist_action = playlist_menu.addAction("Delete Playlist")
        delete_playlist_action.triggered.connect(self.delete_playlist)
        
        # Theme menu
        theme_menu = menubar.addMenu("Theme")
        
        light_theme_action = theme_menu.addAction("Light Theme")
        light_theme_action.triggered.connect(lambda: self.set_theme("light"))
        
        dark_theme_action = theme_menu.addAction("Dark Theme")
        dark_theme_action.triggered.connect(lambda: self.set_theme("dark"))
        
    def update_playlist_selector(self):
        """Update the playlist selector combobox with current playlists"""
        self.playlist_selector.clear()
        self.playlist_selector.addItems(self.playlists.keys())
        self.playlist_selector.setCurrentText(self.current_playlist_name)
        
    def switch_playlist(self, playlist_name):
        """Switch to a different playlist"""
        if playlist_name in self.playlists:
            self.current_playlist_name = playlist_name
            self.current_playlist = self.playlists[playlist_name]
            self.playlist_widget.clear()
            for file_path in self.current_playlist:
                self.playlist_widget.addItem(os.path.basename(file_path))
            self.setWindowTitle(f"Professional Music Player - {playlist_name}")
            
    def create_playlist(self):
        name, ok = QInputDialog.getText(self, "Create Playlist", "Enter playlist name:")
        if ok and name:
            if name in self.playlists:
                QMessageBox.warning(self, "Error", "A playlist with this name already exists!")
                return
                
            self.playlists[name] = []
            self.current_playlist_name = name
            self.current_playlist = self.playlists[name]
            self.playlist_widget.clear()
            self.update_playlist_selector()
            self.setWindowTitle(f"Professional Music Player - {name}")
            
    def delete_playlist(self):
        if len(self.playlists) <= 1:
            QMessageBox.warning(self, "Warning", "Cannot delete the last playlist!")
            return
            
        name, ok = QInputDialog.getItem(self, "Delete Playlist", 
                                      "Select playlist to delete:",
                                      list(self.playlists.keys()), 0, False)
        if ok and name:
            if name == "Default":
                QMessageBox.warning(self, "Warning", "Cannot delete the Default playlist!")
                return
                
            del self.playlists[name]
            if self.current_playlist_name == name:
                self.current_playlist_name = "Default"
                self.current_playlist = self.playlists["Default"]
                self.playlist_widget.clear()
                for file_path in self.current_playlist:
                    self.playlist_widget.addItem(os.path.basename(file_path))
            self.update_playlist_selector()
            self.setWindowTitle(f"Professional Music Player - {self.current_playlist_name}")
            
    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Music File", "", 
                                                 "Music Files (*.mp3 *.wav *.ogg)")
        if file_name:
            self.add_to_playlist(file_name)
            
    def open_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Music Folder")
        if folder:
            for file in os.listdir(folder):
                if file.endswith(('.mp3', '.wav', '.ogg')):
                    self.add_to_playlist(os.path.join(folder, file))
                    
    def add_to_playlist(self, file_path):
        if file_path not in self.current_playlist:
            self.current_playlist.append(file_path)
            self.playlist_widget.addItem(os.path.basename(file_path))
            
    def play_selected(self, item):
        try:
            self.current_index = self.playlist_widget.row(item)
            self.play_current()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not play selected song: {str(e)}")
            
    def play_current(self):
        if not self.current_playlist:
            return
            
        try:
            current_file = self.current_playlist[self.current_index]
            if not os.path.exists(current_file):
                QMessageBox.warning(self, "Error", f"File not found: {os.path.basename(current_file)}")
                self.remove_current_song()
                return
                
            # Stop current playback if any
            pygame.mixer.music.stop()
            
            # Load and play the new file
            pygame.mixer.music.load(current_file)
            pygame.mixer.music.play()
            
            # Update player state
            self.is_playing = True
            self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            self.timer.start()
            
            # Reset progress
            self.slider_position = 0
            self.progress_slider.setValue(0)
            self.current_time.setText("00:00")
            
            # Update song info and album art
            self.update_song_info()
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not play file: {str(e)}")
            self.remove_current_song()
            
    def remove_current_song(self):
        """Remove the current song from the playlist"""
        if not self.current_playlist:
            return
            
        try:
            # Remove from playlist widget
            self.playlist_widget.takeItem(self.current_index)
            
            # Remove from current playlist
            del self.current_playlist[self.current_index]
            
            # Update current index
            if self.current_playlist:
                self.current_index = min(self.current_index, len(self.current_playlist) - 1)
            else:
                self.current_index = 0
                self.is_playing = False
                self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
                self.timer.stop()
                self.song_info.setText("No song playing")
                self.album_art.clear()
                
        except Exception as e:
            print(f"Error removing song: {str(e)}")
            
    def play_pause(self):
        """Toggle between play and pause states"""
        if not self.current_playlist:
            return
            
        try:
            if self.is_playing:
                pygame.mixer.music.pause()
                self.is_playing = False
                self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
                self.play_btn.stopPulse()
                self.timer.stop()
            else:
                pygame.mixer.music.unpause()
                self.is_playing = True
                self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
                self.play_btn.startPulse()
                self.start_time = pygame.time.get_ticks() - (self.slider_position * 1000)  # Update start time
                self.timer.start()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error during play/pause: {str(e)}")
            self.is_playing = False
            self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.play_btn.stopPulse()
            self.timer.stop()
            
    def play_next(self):
        if not self.current_playlist:
            return
            
        if self.is_shuffle:
            import random
            self.current_index = random.randint(0, len(self.current_playlist) - 1)
        else:
            self.current_index = (self.current_index + 1) % len(self.current_playlist)
            
        self.play_current()
        
    def play_previous(self):
        if not self.current_playlist:
            return
            
        if self.is_shuffle:
            import random
            self.current_index = random.randint(0, len(self.current_playlist) - 1)
        else:
            self.current_index = (self.current_index - 1) % len(self.current_playlist)
            
        self.play_current()
        
    def toggle_repeat(self):
        """Toggle repeat mode"""
        self.is_repeat = not self.is_repeat
        self.repeat_btn.setChecked(self.is_repeat)
        
        # Update button appearance
        if self.is_repeat:
            self.repeat_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    border-radius: 15px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            # Change icon to show repeat is active
            self.repeat_btn.setIcon(self.style().standardIcon(QStyle.SP_ArrowRight))
        else:
            self.repeat_btn.setStyleSheet("")
            # Reset icon
            self.repeat_btn.setIcon(self.style().standardIcon(QStyle.SP_ArrowRight))
            
    def toggle_shuffle(self):
        """Toggle shuffle mode"""
        self.is_shuffle = not self.is_shuffle
        self.shuffle_btn.setChecked(self.is_shuffle)
        
        # Update button appearance
        if self.is_shuffle:
            self.shuffle_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    border-radius: 15px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            # Change icon to show shuffle is active
            self.shuffle_btn.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        else:
            self.shuffle_btn.setStyleSheet("")
            # Reset icon
            self.shuffle_btn.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
            
    def set_volume(self, value):
        try:
            volume = value / 100.0
            pygame.mixer.music.set_volume(volume)
        except Exception as e:
            print(f"Error setting volume: {str(e)}")
            
    def update_progress(self):
        if not self.is_playing or not self.current_playlist or self.is_sliding:
            return
            
        try:
            # Get current position from pygame mixer
            current_pos = pygame.mixer.music.get_pos() / 1000.0
            
            # If we're sliding, use the slider position
            if self.is_sliding:
                current_pos = self.slider_position
            else:
                # Add the slider position to get the actual position
                current_pos += self.slider_position
                
            # Ensure current position is within valid range
            if 0 <= current_pos <= self.progress_slider.maximum():
                self.progress_slider.setValue(int(current_pos))
                self.current_time.setText(self.format_time(current_pos))
                
                # Check if song has ended
                if current_pos >= self.progress_slider.maximum():
                    if self.is_repeat:
                        # Restart the current song
                        self.play_current()
                    else:
                        # Play next song
                        self.play_next()
                    
        except Exception as e:
            print(f"Error updating progress: {str(e)}")
            self.timer.stop()
            
    def set_position(self, position):
        """Set the playback position"""
        if self.is_playing and self.current_playlist:
            try:
                # Stop current playback
                pygame.mixer.music.stop()
                
                # Load and play from new position
                pygame.mixer.music.load(self.current_playlist[self.current_index])
                pygame.mixer.music.play(start=position)
                
                # Update timing variables
                self.slider_position = position
                self.progress_slider.setValue(position)
                self.current_time.setText(self.format_time(position))
                
            except Exception as e:
                print(f"Error setting position: {str(e)}")
                
    def format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
        
    def update_song_info(self):
        if not self.current_playlist:
            return
            
        try:
            current_file = self.current_playlist[self.current_index]
            if not os.path.exists(current_file):
                self.remove_current_song()
                return
                
            # Set default values
            title = "Unknown Title"
            artist = "Unknown Artist"
            duration = 0
            
            try:
                audio = mutagen.File(current_file)
                if audio is not None:
                    # Try to get metadata
                    if hasattr(audio, 'tags'):
                        if hasattr(audio.tags, 'get'):
                            # Try to get title
                            try:
                                title = audio.tags.get('TIT2', ['Unknown Title'])[0]
                            except:
                                title = "Unknown Title"
                                
                            # Try to get artist
                            try:
                                artist = audio.tags.get('TPE1', ['Unknown Artist'])[0]
                            except:
                                artist = "Unknown Artist"
                                
                        # Try to get album art
                        if hasattr(audio.tags, 'getall'):
                            try:
                                for tag in audio.tags.getall('APIC'):
                                    if tag.type == 3:  # Front cover
                                        pixmap = QPixmap()
                                        pixmap.loadFromData(tag.data)
                                        self.album_art.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
                                        break
                            except:
                                self.album_art.clear()
                                
                    # Try to get duration
                    try:
                        duration = audio.info.length
                    except:
                        duration = 0
                        
            except Exception as e:
                print(f"Error reading metadata: {str(e)}")
                # If metadata reading fails, use filename as title
                title = os.path.basename(current_file)
                artist = "Unknown Artist"
                duration = 0
                
            # Update UI with available information
            self.song_info.setText(f"{title} - {artist}")
            self.progress_slider.setRange(0, int(duration))
            self.total_time.setText(self.format_time(duration))
            
            # Reset progress
            self.progress_slider.setValue(0)
            self.current_time.setText("00:00")
            self.start_time = pygame.time.get_ticks()
            
        except Exception as e:
            print(f"Error updating song info: {str(e)}")
            self.song_info.setText("Error reading song info")
            self.album_art.clear()
            self.progress_slider.setRange(0, 0)
            self.total_time.setText("00:00")
            self.current_time.setText("00:00")
            
    def save_playlist(self):
        if not self.playlists:
            QMessageBox.warning(self, "Warning", "No playlists to save!")
            return
            
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Playlists", "", 
                                                 "Playlist Files (*.json)")
        if file_name:
            with open(file_name, 'w') as f:
                json.dump(self.playlists, f)
                
    def load_playlist(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Playlists", "", 
                                                 "Playlist Files (*.json)")
        if file_name:
            try:
                with open(file_name, 'r') as f:
                    loaded_playlists = json.load(f)
                    if "Default" not in loaded_playlists:
                        loaded_playlists["Default"] = []
                    self.playlists = loaded_playlists
                    self.current_playlist_name = "Default"
                    self.current_playlist = self.playlists["Default"]
                    self.playlist_widget.clear()
                    for file_path in self.current_playlist:
                        self.playlist_widget.addItem(os.path.basename(file_path))
                    self.update_playlist_selector()
                    self.setWindowTitle(f"Professional Music Player - {self.current_playlist_name}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not load playlists: {str(e)}")
                
    def search_playlist(self, text):
        for i in range(self.playlist_widget.count()):
            item = self.playlist_widget.item(i)
            item.setHidden(text.lower() not in item.text().lower())
            
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            
    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith(('.mp3', '.wav', '.ogg')):
                self.add_to_playlist(file_path)
                
    def set_theme(self, theme):
        if theme == "dark":
            self.setStyleSheet(DARK_THEME + ADVANCED_STYLES)
            self.dark_mode = True
        else:
            self.setStyleSheet(LIGHT_THEME + ADVANCED_STYLES)
            self.dark_mode = False
            
    def fade_in(self, widget):
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(500)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.start()
        
    def fade_out(self, widget):
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(500)
        animation.setStartValue(1)
        animation.setEndValue(0)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.start()
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.play_pause()
        elif event.key() == Qt.Key_Right:
            self.play_next()
        elif event.key() == Qt.Key_Left:
            self.play_previous()
        elif event.key() == Qt.Key_Up:
            self.volume_slider.setValue(min(100, self.volume_slider.value() + 5))
        elif event.key() == Qt.Key_Down:
            self.volume_slider.setValue(max(0, self.volume_slider.value() - 5))
            
    def update_dynamic_theme(self, base_color):
        dynamic_theme = f"""
            QSlider::sub-page:horizontal {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 {base_color}, 
                    stop:1 {base_color}88
                );
            }}
            QPushButton#playButton {{
                background: {base_color};
            }}
        """
        self.setStyleSheet(self.styleSheet() + dynamic_theme)
        
    def slider_pressed(self):
        """Called when user starts sliding the progress bar"""
        self.is_sliding = True
        self.timer.stop()
        
    def slider_released(self):
        """Called when user releases the progress bar"""
        self.is_sliding = False
        if self.is_playing:
            self.timer.start()
        self.set_position(self.slider_position)
        
    def slider_value_changed(self, value):
        """Called when the slider value changes"""
        if self.is_sliding:
            self.slider_position = value
            self.current_time.setText(self.format_time(value))
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = MusicPlayer()
    player.show()
    sys.exit(app.exec_()) 