import sys
import pygame
import random

from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer


class DesktopPet(QLabel):

    def __init__(self):
        super().__init__()
        pygame.mixer.init()

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint
        )

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.pix = QPixmap("anqi.png")
        self.setPixmap(self.pix)
        self.resize(self.pix.width(), self.pix.height())

        self.drag_position = None

        # ========== 随机移动：初始给一个随机方向 ==========
        self.speed = 3 # 移动速度
        self.dx = random.choice([-self.speed, self.speed])  # X方向
        self.dy = random.choice([-self.speed, self.speed])  # Y方向
        # ================================================

        # 声音文件（我帮你修复了语法错误）
        self.sound_list = [
            "txdyh.mp3",
            "hxn.mp3",
            "wan.mp3",
            "ssg.mp3",  # 这里你之前写成mp5了，我修复
            "jyo.mp3"
        ]

        # 自动移动
        self.timer = QTimer()
        self.timer.timeout.connect(self.walk)
        self.timer.start(30)

        self.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)

    # 双击播放随机声音
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton and self.sound_list:
            sound_file = random.choice(self.sound_list)
            try:
                pygame.mixer.music.load(sound_file)
                pygame.mixer.music.play()
            except:
                print(f"播放失败：{sound_file}")

    # ========== 核心：上下左右随机移动 + 碰墙随机换方向 ==========
    def walk(self):
        x = self.x() + self.dx
        y = self.y() + self.dy

        w = self.width()
        h = self.height()
        screen_w = QApplication.desktop().screenGeometry().width()
        screen_h = QApplication.desktop().screenGeometry().height()

        # 碰到屏幕边缘 → 随机换方向
        if x <= 0 or x >= screen_w - w or y <= 0 or y >= screen_h - h:
            self.dx = random.choice([-self.speed, self.speed])
            self.dy = random.choice([-self.speed, self.speed])
            return

        self.move(x, y)


app = QApplication(sys.argv)
pet = DesktopPet()
sys.exit(app.exec_())