#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os

from PIL import Image
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QPushButton, QFileDialog, \
    QTextEdit, QVBoxLayout, QDialog

class ToolMenus:
    def __init__(self, main_window):
        self.main_window = main_window

    def convert_to_ico(self):
        # 图片转ICO格式功能
        file_dialog = QFileDialog(self.main_window)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg)")
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)

        if file_dialog.exec():
            file_paths = file_dialog.selectedFiles()
            for file_path in file_paths:
                try:
                    # 读取图片并转换为ico格式
                    img = Image.open(file_path)
                    ico_file_path = os.path.splitext(file_path)[0] + '.ico'  # 去除扩展名并添加.ico
                    img.save(ico_file_path, format='ICO')
                    self.main_window.debug_text_edit.append("图片转换ICO格式成功")
                except Exception as e:
                    self.main_window.debug_text_edit.append(f"Error processing {file_path}: {e}")

    def convert_to_binary_dialog(self):
        # 图片转十六进制窗口
        dialog = QDialog(self.main_window)
        dialog.setWindowTitle("图片转十六进制")

        # 添加编辑框和按钮用于选择图片
        file_label = QLabel("选择图片:")
        file_edit = QLabel()
        file_button = QPushButton("选择文件")
        file_button.clicked.connect(lambda: self.select_image(file_edit, dialog))

        # 添加文本框用于显示转换后的内容
        output_label = QLabel("转换结果:")
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(file_label)
        layout.addWidget(file_edit)
        layout.addWidget(file_button)
        layout.addWidget(output_label)
        layout.addWidget(self.output_text)

        dialog.setLayout(layout)
        dialog.exec()

    def select_image(self, file_edit, dialog):
        # 图片转十六进制功能
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.ico)")
        if file_dialog.exec():
            file_paths = file_dialog.selectedFiles()
            if file_paths:
                file_path = file_paths[0]
                pixmap_select_image = QPixmap(file_path)
                file_edit.setPixmap(pixmap_select_image.scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio))
                with open(file_path, 'rb') as f:
                    image_data = f.read()
                hex_data = image_data.hex()
                self.output_text.setPlainText(hex_data)
                dialog.adjustSize()