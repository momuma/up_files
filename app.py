import os
import logging
import socket
from flask import Flask, request, render_template
from flask_socketio import SocketIO
from tkinter import Tk
from tkinter.filedialog import askdirectory

# 添加文本颜色库
from colorama import init, Fore, Style

# 初始化 colorama
init(autoreset=True)

# 定义颜色代码
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

#初始文件夹选取路径
# 使用双反斜杠来表示 C: 盘根目录路径，像这样：
# my_path = r"c:\\"
# 不使用原始字符串，用正斜杠来表示路径分隔符（在 Windows 下 Python 也是可以识别这种表示方式的），如下
my_path = "C:/Users/x/WPSDrive/"

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
socketio = SocketIO(app)

def get_upload_folder():
    # 使用 Tkinter 打开文件夹选择对话框
    root = Tk()
    root.withdraw()  # 隐藏主窗口
    folder_selected = askdirectory(title="选择保存路径",initialdir=my_path)
    root.destroy()
    
    # 如果未选择路径，使用默认路径
    if not folder_selected:
        folder_selected = 'uploads'
    
    if not os.path.exists(folder_selected):
        os.makedirs(folder_selected)
    
    return folder_selected

UPLOAD_FOLDER = get_upload_folder()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('files[]')
    for file in files:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return {'status': 'success'}, 200

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # 连接一个不会被阻塞的外部地址
        s.connect(('10.254.254.254', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

if __name__ == '__main__':
    # 打印彩色文本
    print(Fore.GREEN +'运行后在弹出的窗口选取要保存图片的路径，如果没选可以关闭重新运行，默认保存路径是当前脚本下uploads文件夹')
    print(Fore.RED +'注意：选取图片过多时，单据添加后会无反应，不要多次单击添加，等待几秒选取图片窗口消失即可点击上传')
    host = '0.0.0.0'
    port = 80
    ip_address = get_ip_address()
    logging.info(f"Upload folder: {UPLOAD_FOLDER}")
    logging.info(f"Starting server on http://{ip_address}:{port}")
    logging.info("Ensure your devices are connected to the same network.")
    socketio.run(app, host=host, port=port)
