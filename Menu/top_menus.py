#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog, \
    QMessageBox

class TopMenus:
    def __init__(self, main_window):
        self.main_window = main_window

    def toggle_top(self, checked):
        # 窗口置顶
        if checked:
            self.main_window.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
            if self.main_window.debug_page.isVisible():
                self.main_window.debug_page.toggle_top(True)
            if self.main_window.commandoutput_window.isVisible():
                self.main_window.commandoutput_window.toggle_top(True)
        else:
            self.main_window.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, False)
            if self.main_window.debug_page.isVisible():
                self.main_window.debug_page.toggle_top(False)
            if self.main_window.commandoutput_window.isVisible():
                self.main_window.commandoutput_window.toggle_top(False)
        self.main_window.show()

    def create_spec_configuration(self):
        # 一键生成spec文件
        py_file = self.main_window.py_file_lineEdit.text()
        py_file_name = os.path.basename(py_file)
        ico_spec = None
        analysis_argument = f"['{py_file_name}']"
        if not py_file:
            QMessageBox.warning(self.main_window, '警告', '请选择py文件！', QMessageBox.StandardButton.Ok)
            return

        # 弹窗询问用户是否选择其他的.py文件
        reply = QMessageBox.question(self.main_window, '选择py文件', '是否多个py文件？',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            # 弹出文件选择对话框，允许用户选择多个文件
            files, _ = QFileDialog.getOpenFileNames(self.main_window, '选择.py文件', filter='Python Files (*.py)')

            if not files:
                QMessageBox.warning(self.main_window, '警告', '未选择任何文件！', QMessageBox.StandardButton.Ok)
                return

            # 以下为创建.spec文件的代码
            analysis_files = [f for f in files if f.endswith('.py')]
            analysis_argument = str(analysis_files)

        # 弹窗询问用户是否添加.ico图标
        icon_reply = QMessageBox.question(self.main_window, '添加.ico图标', '是否添加.ico图标？',
                                          QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                          QMessageBox.StandardButton.No)

        if icon_reply == QMessageBox.StandardButton.Yes:
            # 弹出文件选择对话框，允许用户选择.ico文件
            icon_file, _ = QFileDialog.getOpenFileName(self.main_window, '选择.ico文件', filter='Icon Files (*.ico)')
            if icon_file:
                ico_spec = f"['{icon_file}']"

        # 获取.py文件的路径和文件名
        py_file_directory = os.path.dirname(py_file)
        spec_file_name = os.path.splitext(py_file_name)[0] + ".spec"
        spec_file_path = os.path.join(py_file_directory, spec_file_name)

        # 创建.spec文件内容
        spec_content = f'''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

from PyInstaller.utils.hooks import collect_data_files

a = Analysis({analysis_argument},
             pathex=[],
             binaries=[],
             datas=collect_data_files('data'),
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='{os.path.splitext(py_file_name)[0]}',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          onefile=True,
          icon={ico_spec}
          )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='main')

'''
        # 写入.spec文件
        try:
            with open(spec_file_path, 'w', encoding='utf-8') as spec_file:
                spec_file.write(spec_content)
            QMessageBox.information(self.main_window, "完成", f"已成功生成 {spec_file_name} 文件！",
                                    QMessageBox.StandardButton.Ok)
        except Exception as e:
            QMessageBox.critical(self.main_window, "错误", f"生成 {spec_file_name} 文件时出错: {e}",
                                 QMessageBox.StandardButton.Ok)
