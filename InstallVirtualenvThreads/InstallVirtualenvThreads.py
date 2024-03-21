#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
from PySide6.QtCore import QThread, Signal as pyqtSignal

class InstallVirtualenvThread(QThread):
    # 安装虚拟环境子进程
    install_completed = pyqtSignal(str)
    output_ready = pyqtSignal(str)

    def __init__(self, directory, mirror_source=None):
        super().__init__()
        self.directory = directory
        self.mirror_source = mirror_source

    def run(self):
        virtualenv_name = "venv"
        virtualenv_path = os.path.normpath(f"{self.directory}/{virtualenv_name}")

        try:
            install_commands = ["python", "-m", "venv", virtualenv_path]
            process = subprocess.Popen(install_commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, errors='ignore')

            for line in iter(process.stdout.readline, ''):
                self.output_ready.emit(line.strip())

            stdout, stderr = process.communicate()
            self.output_ready.emit(stdout.strip() + stderr.strip())

            if self.mirror_source:
                process = subprocess.Popen(
                    [f"{virtualenv_path}/Scripts/pip", "install", "pyinstaller", "--index-url", self.mirror_source],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, errors='ignore')

                for line in iter(process.stdout.readline, ''):
                    self.output_ready.emit(line.strip())

                stdout, stderr = process.communicate()
                self.output_ready.emit(stdout.strip() + stderr.strip())

                process = subprocess.Popen(
                    [f"{virtualenv_path}/Scripts/python", "-m", "pip", "install", "--upgrade", "pip", "--index-url",
                     self.mirror_source], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, errors='ignore')

                for line in iter(process.stdout.readline, ''):
                    self.output_ready.emit(line.strip())

                stdout, stderr = process.communicate()
                self.output_ready.emit(stdout.strip() + stderr.strip())
            else:
                process = subprocess.Popen([f"{virtualenv_path}/Scripts/pip", "install", "pyinstaller"],
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, errors='ignore')

                for line in iter(process.stdout.readline, ''):
                    self.output_ready.emit(line.strip())

                stdout, stderr = process.communicate()
                self.output_ready.emit(stdout.strip() + stderr.strip())

                process = subprocess.Popen(
                    [f"{virtualenv_path}/Scripts/python", "-m", "pip", "install", "--upgrade", "pip"],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, errors='ignore')

                for line in iter(process.stdout.readline, ''):
                    self.output_ready.emit(line.strip())

                stdout, stderr = process.communicate()
                self.output_ready.emit(stdout.strip() + stderr.strip())

            self.install_completed.emit(
                f"成功在目录 {self.directory} 中创建虚拟环境 {virtualenv_name}，并安装了 pyinstaller 库，pip 库已更新到最新版本")
        except subprocess.CalledProcessError as e:
            self.install_completed.emit(f"创建虚拟环境失败，错误信息: {e}")

