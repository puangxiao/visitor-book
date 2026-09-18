import sys
from pathlib import Path


def get_work_dir():
    if hasattr(sys,"_MEIPASS"):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent
base = get_work_dir
path = base / "files" / "visitor_book.txt"
path.parent.mkdir(parents=True,exist_ok=True)
if path.exists():
    last=path.read_text(encoding="utf-8")
else:
    last=""
say="请输入姓名（完成所有名字输入后，请按q退出）："
names=""
user_input=input(say)
while user_input != "q":
    names += user_input+"\n"
    user_input=input(say)
while True:
    a=input("你要保存上次的记录吗？1.是的 2.否")
    if a =="1":
        path.write_text(last+names,encoding="utf-8")
        break
    elif a=="2":
        path.write_text(names,encoding="utf-8")
        break
    else:
        print("输入无效，请重新输入！")