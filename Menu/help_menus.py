#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
from PySide6.QtWidgets import QPushButton, QFileDialog, \
    QTextEdit, QVBoxLayout, QMessageBox, QDialog, QHBoxLayout, QLabel, QLineEdit

current_version = "1.1.8"

class HelpMenus:
    def __init__(self, main_window):
        self.main_window = main_window

    def download_update(self, download_link):
        # 更新版本下载逻辑
        try:
            response = requests.get(download_link, stream=True)
            if response.status_code == 200:
                save_path = QFileDialog.getExistingDirectory(self.main_window, "选择保存路径")
                if save_path:
                    filename = os.path.basename(download_link)
                    file_path = os.path.join(save_path, filename)
                    with open(file_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=1024):
                            f.write(chunk)
                    QMessageBox.information(self.main_window, '更新', f"更新已下载完成，请安装。文件保存在：{file_path}")
                else:
                    QMessageBox.critical(self.main_window, '错误', '未选择保存路径。')
            else:
                QMessageBox.critical(self.main_window, '错误', f'下载更新文件失败。状态码: {response.status_code}')
        except Exception as e:
            QMessageBox.critical(self.main_window, '错误', f"下载更新时出错: {str(e)}")

    def check_update(self):
        # 更新版本检查逻辑
        try:
            response = requests.get("https://raw.githubusercontent.com/superohhh/pythontool/main/version.txt")
            if response.status_code == 200:
                version_info = response.text.splitlines()
                latest_version = version_info[0].strip()
                download_link = version_info[1].strip()
                if latest_version > current_version:
                    reply = QMessageBox.question(self.main_window, '更新提示', f"发现新版本 {latest_version}，是否下载更新？",
                                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                    if reply == QMessageBox.StandardButton.Yes:
                        self.download_update(download_link)
                else:
                    QMessageBox.information(self.main_window, '更新', '当前已经是最新版本。')
            else:
                QMessageBox.critical(self.main_window, '错误', f'检查更新失败。状态码: {response.status_code}')
        except Exception as e:
            QMessageBox.critical(self.main_window, '错误', f"检查更新时发生错误: {str(e)}")

    def show_usage_instructions(self):
        # 创建对话框
        self.dialog = QDialog(self.main_window)
        self.dialog.setWindowTitle("注意事项")
        self.dialog.setModal(True)

        # 使用说明文本列表
        self.instructions_texts_1 = [
            "基础部分：",
            "1、文件打包区域支持文件拖拽功能",
            "2、配置文件有错会导致点击开始打包之后崩溃删除配置文件即可",
            "3、pyinstaller和nuitka都是使用的是本地环境，不行就是环境没配置好",
            "4、参数保存按钮还会保存参数选中状态",
            "5、虚拟环境路径不要套娃太长会出错越短越好"
        ]

        self.instructions_texts_2 = [
            "加密功能：",
            "1、对称加密 ：使用相同的密钥来加密和解密数据",
            "2、非对称加密：使用一对密钥：公钥和私钥，公钥用于加密数据，私钥用于解密数据",
            "3、哈希函数：将任意长度的输入数据映射为固定长度的输出，单向的，不可逆的，用于验证数据的完整性、密码存储、数字签名等场景"
        ]

        self.instructions_texts_3 = [
            "AES 加密模式：",
            "1、ECB模式 ：最简单的加密模式，不使用IV",
            "2、CBC模式：常见的加密模式，但在并行加密方面存在一定的限制，使用IV",
            "3、CFB模式：可以实现部分加密和解密，适合流加密，使用IV",
            "4、OFB模式：与CFB模式一样可以实现部分加密和解密，使用IV",
            "5、CTR模式：并行加密模式，可以充分利用现代处理器的并行能力，速度较快，使用IV",
        ]
        # 创建大的文本框
        self.instructions_text_edit = QTextEdit()
        self.instructions_text_edit.setReadOnly(True)
        self.current_texts = self.instructions_texts_1
        self.update_text()

        # 设置单线边框样式
        self.instructions_text_edit.setStyleSheet("border: 1px solid black;")

        # 创建切换按钮
        self.toggle_button = QPushButton("切换")
        self.toggle_button.clicked.connect(self.toggle_text)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.instructions_text_edit)
        layout.addWidget(self.toggle_button)
        self.dialog.setLayout(layout)

        # 显示对话框
        self.dialog.exec_()

    def toggle_text(self):
        # 切换文本
        if self.current_texts == self.instructions_texts_1:
            self.current_texts = self.instructions_texts_2
        elif self.current_texts == self.instructions_texts_2:
            self.current_texts = self.instructions_texts_3
        else:
            self.current_texts = self.instructions_texts_1
        self.update_text()

    def update_text(self):
        # 更新文本框内容
        text = "\n".join(self.current_texts)
        self.instructions_text_edit.setPlainText(text)

    def open_mirror_source_dialog(self):
        dialog = QDialog(self.main_window)
        dialog.setWindowTitle("镜像源设置")
        dialog.resize(500, 200)  # 设置对话框初始大小

        layout = QVBoxLayout(dialog)

        labels = ["清华:", "阿里云:", "网易:", "华为云:", "百度云:", "腾讯云:", "豆瓣:", "中科大:"]
        contents = ["https://pypi.tuna.tsinghua.edu.cn/simple", "http://mirrors.aliyun.com/pypi/simple", "https://mirrors.163.com/pypi/simple", "https://mirrors.huaweicloud.com/repository/pypi/simple", "https://mirror.baidu.com/pypi/simple", "https://mirrors.cloud.tencent.com/pypi/simple", "http://pypi.douban.com/simple", "https://pypi.mirrors.ustc.edu.cn/simple"]

        for label, content in zip(labels, contents):
            h_layout = QHBoxLayout()
            label_widget = QLabel(label)
            h_layout.addWidget(label_widget)
            edit = QLineEdit()
            edit.setReadOnly(True)  # 设置编辑框为只读
            edit.setText(content)   # 设置编辑框的内容
            h_layout.addWidget(edit)

            # 添加替换按钮，并将编辑框和按钮一起添加到水平布局中
            replace_button = QPushButton("替换")
            replace_callback = self.create_replace_button_clicked_callback(content)
            replace_button.clicked.connect(replace_callback )
            h_layout.addWidget(replace_button)
            layout.addLayout(h_layout)
        dialog.exec()

    def create_replace_button_clicked_callback(self, text):
        return lambda: self.replace_text(text)

    def replace_text(self, text):
        self.main_window.mirrorLineEdit.setText(text)
        self.main_window.debug_page.mirror_edit.setText(text)

    def show_about_dialog(self):
        # 创建关于对话框并显示当前程序的版本信息
        about_text = f"当前版本：{current_version}\n哔哩哔哩\n爱吃肉的呆头猪"
        QMessageBox.about(self.main_window, "程序信息", about_text)