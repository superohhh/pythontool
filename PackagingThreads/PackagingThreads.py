#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
from PySide6.QtCore import QThread, Signal as pyqtSignal

class PackagingThread(QThread):
    # 打包逻辑子进程
    packaging_completed = pyqtSignal(str)
    output_ready = pyqtSignal(str)

    def __init__(self, selected_packaging, virtualenv_directory, pyinstaller_command, output_directory_pyinstaller, nuitka_command, output_directory_nuitka):
        super().__init__()
        self.selected_packaging = selected_packaging
        self.virtualenv_directory = virtualenv_directory
        self.pyinstaller_command = pyinstaller_command
        self.output_directory_pyinstaller = output_directory_pyinstaller
        self.nuitka_command = nuitka_command
        self.output_directory_nuitka = output_directory_nuitka

    def run(self):
        try:
            if self.selected_packaging == "pyinstaller":
                self.run_pyinstaller()
            elif self.selected_packaging == "nuitka":
                self.run_nuitka()
        except Exception as e:
            error_message = f"打包失败，错误信息: {str(e)}"
            self.packaging_completed.emit(error_message)

    def run_pyinstaller(self):
        try:
            if self.virtualenv_directory:
                activate_command = os.path.join(self.virtualenv_directory, 'Scripts', 'activate')
                command = f"\"{activate_command}\" && {' '.join(self.pyinstaller_command)}"
            else:
                command = ' '.join(self.pyinstaller_command)

            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, errors='ignore')
            # 读取命令输出并发送信号更新界面
            for line in process.stdout:
                self.output_ready.emit(line.strip())

            process.communicate()  # 等待子进程结束
            if process.returncode == 0:
                success_message = f"成功使用 Pyinstaller 打包，OUTPUT：{os.path.normpath(self.output_directory_pyinstaller)}"
                self.packaging_completed.emit(success_message)
            else:
                error_message = f"打包失败，错误码: {process.returncode}"
                self.packaging_completed.emit(error_message)
        except Exception as e:
            error_message = f"打包失败，错误信息: {str(e)}"
            self.packaging_completed.emit(error_message)

    def run_nuitka(self):
        try:
            if self.virtualenv_directory:
                activate_command = os.path.join(self.virtualenv_directory, 'Scripts', 'activate')
                nuitka_command_with_env = f"\"{activate_command}\" && {' '.join(self.nuitka_command)}"
                process = subprocess.Popen(nuitka_command_with_env, shell=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.STDOUT, stdin=subprocess.PIPE, universal_newlines=True,
                                           errors='ignore')
            else:
                process = subprocess.Popen(self.nuitka_command, shell=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.STDOUT, stdin=subprocess.PIPE, universal_newlines=True,
                                           errors='ignore')
            # 读取命令输出并发送信号更新界面
            for line in process.stdout:
                self.output_ready.emit(line.strip())

            process.communicate(input="y\n")  # 等待子进程结束
            if process.returncode == 0:
                success_message = f"成功使用 Nuitka 打包，OUTPUT：{os.path.normpath(self.output_directory_nuitka)}"
                self.packaging_completed.emit(success_message)
            else:
                error_message = f"打包失败，错误码: {process.returncode}"
                self.packaging_completed.emit(error_message)
        except Exception as e:
            error_message = f"打包失败，错误信息: {str(e)}"
            self.packaging_completed.emit(error_message)
