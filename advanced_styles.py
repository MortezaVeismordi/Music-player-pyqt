from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QRect, QPoint, QSize
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QPushButton
from PyQt5.QtGui import QColor

# Advanced UI Styles
ADVANCED_STYLES = """
/* Glassmorphism Player Bar */
QWidget#playerBar {
    background: rgba(30, 30, 46, 0.85);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 15px 15px 0 0;
}

/* Dynamic Play Button */
QPushButton#playButton {
    background: qradialgradient(
        cx:0.5, cy:0.5,
        radius: 0.5,
        fx:0.5, fy:0.5,
        stop:0 #7d5fff, stop:1 #5b7dff
    );
    border-radius: 25px;
    min-width: 50px;
    min-height: 50px;
    border: 2px solid rgba(255, 255, 255, 0.2);
}

QPushButton#playButton:hover {
    background: qradialgradient(
        cx:0.5, cy:0.5,
        radius: 0.5,
        fx:0.5, fy:0.5,
        stop:0 #8d6fff, stop:1 #6b8dff
    );
}

/* Rainbow Progress Slider */
QSlider::groove:horizontal {
    height: 8px;
    background: rgba(90, 90, 120, 0.3);
    border-radius: 4px;
}

QSlider::sub-page:horizontal {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #FF5F5F, stop:0.25 #FFD75F,
        stop:0.5 #5FFF7D, stop:0.75 #5B7DFF,
        stop:1 #D75FFF
    );
    border-radius: 4px;
}

QSlider::handle:horizontal {
    width: 16px;
    height: 16px;
    background: white;
    border-radius: 8px;
    margin: -4px 0;
    border: 2px solid #7d5fff;
}

/* 3D Album Art */
QLabel#albumArt {
    border-radius: 15px;
    border: 3px solid rgba(255, 255, 255, 0.1);
    background: rgba(40, 40, 60, 0.7);
}

/* Interactive Playlist */
QListWidget::item:selected {
    background: rgba(123, 95, 255, 0.3);
    border-left: 3px solid #7d5fff;
    color: white;
    font-weight: bold;
}

QListWidget::item:hover {
    background: rgba(123, 95, 255, 0.1);
}

/* Volume Slider */
QSlider#volumeSlider::groove:horizontal {
    height: 4px;
    background: rgba(90, 90, 120, 0.3);
    border-radius: 2px;
}

QSlider#volumeSlider::sub-page:horizontal {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #7d5fff, stop:1 #5b7dff
    );
    border-radius: 2px;
}

QSlider#volumeSlider::handle:horizontal {
    width: 12px;
    height: 12px;
    background: white;
    border-radius: 6px;
    margin: -4px 0;
    border: 2px solid #7d5fff;
}

/* Control Buttons */
QPushButton#controlButton {
    background: rgba(90, 90, 120, 0.3);
    border: none;
    border-radius: 15px;
    padding: 8px;
    min-width: 30px;
    min-height: 30px;
}

QPushButton#controlButton:hover {
    background: rgba(123, 95, 255, 0.3);
}

QPushButton#controlButton:pressed {
    background: rgba(123, 95, 255, 0.5);
}

/* Search Bar */
QLineEdit#searchBar {
    background: rgba(90, 90, 120, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    padding: 8px 15px;
    color: white;
}

QLineEdit#searchBar:focus {
    border: 1px solid #7d5fff;
    background: rgba(90, 90, 120, 0.3);
}
"""

class AnimatedButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_animations()
        self._scale = 1.0

    def setup_animations(self):
        # Hover animation
        self.hover_anim = QPropertyAnimation(self, b"geometry")
        self.hover_anim.setDuration(200)
        self.hover_anim.setEasingCurve(QEasingCurve.OutQuad)

        # Pulse animation
        self.pulse_anim = QPropertyAnimation(self, b"pos")
        self.pulse_anim.setDuration(1000)
        self.pulse_anim.setLoopCount(-1)
        self.pulse_anim.setEasingCurve(QEasingCurve.InOutQuad)

    def enterEvent(self, event):
        # Store original geometry
        original_geometry = self.geometry()
        
        # Calculate new geometry with slight expansion
        new_geometry = QRect(
            original_geometry.x() - 2,
            original_geometry.y() - 2,
            original_geometry.width() + 4,
            original_geometry.height() + 4
        )
        
        # Start hover animation
        self.hover_anim.setStartValue(original_geometry)
        self.hover_anim.setEndValue(new_geometry)
        self.hover_anim.start()
        
        super().enterEvent(event)

    def leaveEvent(self, event):
        # Return to original size
        original_geometry = self.geometry()
        new_geometry = QRect(
            original_geometry.x() + 2,
            original_geometry.y() + 2,
            original_geometry.width() - 4,
            original_geometry.height() - 4
        )
        
        self.hover_anim.setStartValue(original_geometry)
        self.hover_anim.setEndValue(new_geometry)
        self.hover_anim.start()
        
        super().leaveEvent(event)

    def startPulse(self):
        # Store original position
        self._original_pos = self.pos()
        
        # Set up pulse animation
        self.pulse_anim.setStartValue(self._original_pos)
        self.pulse_anim.setEndValue(QPoint(self._original_pos.x(), self._original_pos.y() - 2))
        self.pulse_anim.start()

    def stopPulse(self):
        self.pulse_anim.stop()
        if hasattr(self, '_original_pos'):
            self.move(self._original_pos)

def create_shadow_effect(widget, blur_radius=15, color=Qt.black, offset=(0, 3)):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur_radius)
    shadow.setColor(color)
    shadow.setOffset(*offset)
    widget.setGraphicsEffect(shadow)
    return shadow

def extract_colors_from_art(image_path):
    """Extract dominant colors from album art"""
    from PIL import Image
    import colorsys
    
    try:
        img = Image.open(image_path)
        img = img.resize((50, 50))
        colors = img.getcolors(50*50)
        
        if not colors:
            return "#7d5fff"
        
        dominant_color = max(colors, key=lambda x: x[0])[1]
        r, g, b = dominant_color
        
        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
        base_color = f"hsl({int(h*360)}, {int(s*100)}%, {int(l*100)}%)"
        
        return base_color
    except:
        return "#7d5fff" 