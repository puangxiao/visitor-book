import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtWidgets import QLineEdit, QTextEdit, QLabel, QPushButton
from PyQt6.QtCore import Qt
from qfluentwidgets import FluentWindow, PrimaryPushButton, PushButton, InfoBar, InfoBarPosition,FluentIcon



def get_work_dir():
    if hasattr(sys,"_MEIPASS"):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent
base = get_work_dir()
path = base / "files" / "visitor_book.txt"

path.parent.mkdir(parents=True,exist_ok=True)



class VisitorWin(FluentWindow):
    def __init__(self):
        super().__init__()
        self.new_name_list = []

        self.setWindowTitle("访客登记簿")
        self.resize(580, 460)


        self.homePage = QWidget()
        self.homePage.setObjectName("homePage")
        main_layout = QVBoxLayout(self.homePage)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(24, 24, 24, 24)

        #文字
        title_label = QLabel("访客姓名录入")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size:18px; font-weight:bold;")
        main_layout.addWidget(title_label)

        #姓名输入框
        input_layout = QHBoxLayout()
        name_label = QLabel("姓名：")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("输入访客姓名并回车")
        self.name_input.returnPressed.connect(self.add_name_func)
        input_layout.addWidget(name_label)
        input_layout.addWidget(self.name_input)
        main_layout.addLayout(input_layout)

        #只读的访客记录
        self.show_text_box = QTextEdit()
        self.show_text_box.setReadOnly(True)
        self.refresh_history()
        main_layout.addWidget(self.show_text_box)

        btn_layout = QHBoxLayout()
        #添加姓名按钮
        btn_add = PrimaryPushButton("添加姓名")
        btn_add.clicked.connect(self.add_name_func)
        #追加保存按钮
        btn_save_append = PushButton("保存-追加历史记录")
        btn_save_append.clicked.connect(lambda: self.save_func(mode=1))
        #重新保存按钮
        btn_save_cover = PushButton("保存-覆盖原有记录")
        btn_save_cover.clicked.connect(lambda: self.save_func(mode=2))

        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_save_append)
        btn_layout.addWidget(btn_save_cover)

        main_layout.addLayout(btn_layout)


        self.addSubInterface(
            self.homePage,
            FluentIcon.HOME,
            "访客登记主页"
        ) 

        self.refresh_history()
        self.render_all_text()





    def add_name_func(self):
        """将姓名存至列表"""
        input_name = self.name_input.text().strip()
        if not input_name:
            InfoBar.warning(
                title="输入提示",
                content="姓名不能为空！",
                position=InfoBarPosition.TOP,
                parent=self,
                duration=2000
            )
            return
        self.new_name_list.append(input_name)
        self.name_input.clear()
        self.render_all_text()


    def save_func(self, mode):
        """将姓名存至本地"""
        new_names_str = "\n".join(self.new_name_list)
        if mode == 1:
            old_content = self.history_text.rstrip("\n")
            all_text = f"{old_content}\n{new_names_str}\n"
        else:
           all_text = new_names_str + "\n" 


        if not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)

        try:
            path.write_text(all_text, encoding="utf-8")
        except Exception as err:
            InfoBar.error(
                title="保存失败",
                content=f"文件写入出错：{str(err)}",
                position=InfoBarPosition.TOP,
                parent=self,
                duration=3000
            )
            return


        
        InfoBar.info(
            title="保存完成",
            content="访客记录已保存成功",
            position=InfoBarPosition.TOP,
            parent=self,
            duration=2000
        )
        self.refresh_history()
        # 保存完成清空本次新增临时列表
        self.new_name_list.clear()
        self.render_all_text()


    def refresh_history(self):
        if path.exists():
            self.history_text = path.read_text(encoding="utf-8")
        else:
            self.history_text = ""


    def render_all_text(self):
        """读取磁盘历史"""
        if path.exists():
            old = path.read_text(encoding="utf-8")
        else:
            old = ""
        # 拼接历史 + 本次新增未保存姓名
        temp_new = "\n".join(self.new_name_list)
        if temp_new:
            full = old.rstrip("\n") + "\n" + temp_new
        else:
            full = old
        self.show_text_box.setText(full)




#执行
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VisitorWin()
    window.show()
    sys.exit(app.exec())
