# Python局域网聊天室 Python Local Area Network ChatVerse

## 介绍 About
一个在局域网中的聊天室，启动服务端再在其他的设备上启动客户端即可使用，程序使用网络的6666端口。
A chat room within a local area network can be accessed by starting the server and then launching the client on other devices. The application uses port 6666 for network communication.

## 说明 Explanation
请选择程序语言以获得更好的体验，后缀_zh的文件为简体中文版，后缀_en的文件为英文版。
Please select a programming language for a better experience. Files with the suffix _zh are in Simplified Chinese, while files with the suffix _en are in English.

拓展名为.py的文件为Python源代码，拓展名为.exe的文件为Microsoft Windows®可执行文件。请根据需要选择不同的文件类型进行运行。
Files with the extension .py are Python source code files, while files with the extension .exe are Microsoft Windows® executable files. Please select the appropriate file type for execution as needed.

项目使用编程语言 ==> Python，
版本 ==> 3.13.7
The project utilizes the programming language ==> Python,
version ==> 3.13.7.

语言 ==> 中文/英文
Language ==> Chinese/English

# 依赖说明 Program dependency instructions

## 运行环境要求 Operating environment requirements
- Python 版本: 3.13.7 或兼容版本
- 操作系统: Windows/macOS/Linux（支持 Python 和 Tkinter 的系统）

- Python Version: 3.13.7 or compatible version
- Operating System: Windows/macOS/Linux (Python and Tkinter support systems)

## 所需 Python 标准库 Required Python Standard Library
程序仅使用 Python 标准库，无需安装额外第三方包：
- socket: 用于网络通信功能
- tkinter: 用于图形用户界面(GUI)
- threading: 用于多线程处理
- queue: 用于线程安全的消息队列

- Socket: Used for network communication functions
- tkinter: for graphical user interfaces (GUI)
- Threading: Used for multi-threading
- Queue: A message queue for thread security

## 安装与运行说明 Installation and operation instructions
1. 确保已安装指定版本的 Python
2. 无需安装依赖，直接运行服务器和客户端：
   - 服务器: python server_zh.py/exe
   - 客户端: python client_zh.py/exe

1. Ensure that the specified version of Python is installed
2. No need to install dependencies, run the server and client directly:
  - Server: Python server_en.py/exe
  - Client: Python client_en.py/exe

## 注意事项 Notes
- Tkinter 通常随 Python 一同安装，若运行时提示缺少 Tkinter：
  - Ubuntu/Debian: sudo apt-get install python3-tk
  - macOS: 可能需要通过 Homebrew 安装 python-tk
  - Windows: 重新安装 Python 并勾选 "Tcl/Tk" 组件 或 使用 'pip install Tkinter' 进行安装

- Tkinter is usually installed with Python, if the runtime prompts that Tkinter is missing:
  - Ubuntu/Debian: sudo apt-get install python3-tk
  - macOS: You may need to install python-tk via Homebrew
  - Windows: Reinstall Python and tick the "Tcl/Tk" component or use "pip install Tkinter" to install

版权所有 (C) 2025 文宇香香工作室
Copyright (C) 2025 Wenyu Xiangxiang Studio

根据MIT许可证授权
Authorized under the MIT License.
