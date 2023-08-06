import time
import zmq
import msgpack
import sys
import tty
import termios
import subprocess
import threading
import os
import shutil

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.connect("ipc:///tmp/frontend")  # 绑定到端口
input_str = ""
filename = "/userdata/log_info/workstation_log/info/workstation_log.INFO"

def get_key():
    # 保存终端属性
    old_settings = termios.tcgetattr(sys.stdin)

    try:
        # 设置终端属性
        tty.setcbreak(sys.stdin.fileno())
        # 读取一个字符
        ch = sys.stdin.read(1)
    finally:
        # 恢复终端属性
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

    return ch

def print_to_screen(text):
    # 获取当前终端大小
    rows, columns = shutil.get_terminal_size()
    # 将文本按照终端大小分割成多行
    lines = text.split("\n")
    output = ""
    for line in lines:
        # 将每一行的长度调整至终端大小
        output += line[:columns] + "\n"

    # 将光标移动到最后一行
    sys.stdout.write("\033[{};0H".format(rows) + "\033[s")
    # 输出文本到终端上
    sys.stdout.write(output[:-1])
    # 将光标向上移动n-1行，使光标停留在最后一行的最后一个字符位置
    sys.stdout.write("\033[{}A".format(len(lines)-2))
    sys.stdout.flush()

# 获取键盘输入，并显示到终端
def get_keyboard_input():
    global input_str
    while True:
        topic = "/workstation/shell"  # 获取用户输入的topic
        key = get_key()
        if key == '\x08': # 如果按下 Backspace，则删除最后一个字符
            input_str = input_str[:-1]
        elif key == '\n': # 如果按下 Enter，则输出当前输入的字符串，并清空input_str
            print(key)
            input_str = ""
        else: # 其他情况，则将键值添加到input_str中
            input_str += key
        info = {'data': key}
        msg2send = msgpack.dumps(info)
        socket.send_multipart([topic.encode(), msg2send])  # 发送带有topic的消息

def show_file_contents():
    with open(filename, "r") as f:
        # 获取文件的初始大小
        st_size = os.stat(filename).st_size

        while True:
            # 获取文件的当前大小
            cu_size = os.stat(filename).st_size
            # 如果文件大小发生变化，则读取新的内容
            if cu_size != st_size:
                f.seek(st_size)
                new_content = f.read()
                print(new_content, end="")
                # 更新文件的大小
                st_size = cu_size
            # 休眠1秒
            time.sleep(1)

def show_input_str():
    global input_str
    while True:
        print_to_screen(input_str)
        time.sleep(0.5)

def main():
    # 开启两个线程，分别处理键盘输入和文件显示
    t1 = threading.Thread(target=get_keyboard_input)
    t2 = threading.Thread(target=show_file_contents)
    t3 = threading.Thread(target=show_input_str)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

if __name__ == '__main__':
    main()