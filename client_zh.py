# -*- coding: utf-8 -*-

"""
项目使用的Python版本 -> python3.13.7

语言 -> 中文

Python局域网聊天室客户端 - ChatVerse聊天系统的GUI客户端

版权所有 (C) 2025 文宇香香工作室
根据MIT许可证授权
"""

import socket
import tkinter as tk
import threading
from queue import Queue

class ChatClient:
    def __init__(self):
        self.server_addr = ('127.0.0.1', 6666)
        self.nickname = ""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message_queue = Queue()
        
        # 初始化GUI
        self.init_gui()
        
        # 连接服务器
        self.connect_to_server()
        
        # 启动消息处理线程
        threading.Thread(target=self.process_messages, daemon=True).start()
        
        # 启动主循环
        self.root.mainloop()
    
    def init_gui(self):
        """初始化客户端GUI界面"""
        self.root = tk.Tk()
        self.root.title("网络聊天室【客户端】")
        
        # 设置窗口大小和位置
        self.root.geometry('500x400+500+300')
        self.root.resizable(False, False)
        
        # 消息显示区域
        self.message_frame = tk.Frame(self.root)
        self.message_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.scrollbar = tk.Scrollbar(self.message_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.message_list = tk.Listbox(
            self.message_frame,
            yscrollcommand=self.scrollbar.set,
            font=('微软雅黑', 10),
            bg="#ffffff",
            height=15
        )
        self.message_list.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.message_list.yview)
        
        # 底部输入区域
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 昵称输入界面
        self.nickname_frame = tk.Frame(self.input_frame)
        self.nickname_frame.pack(fill=tk.X)
        
        tk.Label(self.nickname_frame, text='昵称:').pack(side=tk.LEFT)
        
        self.nickname_entry = tk.Entry(self.nickname_frame, width=40)
        self.nickname_entry.pack(side=tk.LEFT, padx=5)
        self.nickname_entry.bind("<Return>", self.set_nickname)
        self.nickname_entry.focus_set()
        
        self.join_button = tk.Button(
            self.nickname_frame,
            text="进入",
            command=self.set_nickname,
            width=8
        )
        self.join_button.pack(side=tk.LEFT)
        
        # 消息输入界面 (初始隐藏)
        self.chat_frame = tk.Frame(self.input_frame)
        
        tk.Label(self.chat_frame, text='消息:').pack(side=tk.LEFT)
        
        self.message_entry = tk.Entry(self.chat_frame, width=40)
        self.message_entry.pack(side=tk.LEFT, padx=5)
        self.message_entry.bind("<Return>", self.send_message)
        
        self.send_button = tk.Button(
            self.chat_frame,
            text="发送",
            command=self.send_message,
            width=8
        )
        self.send_button.pack(side=tk.LEFT)
        
        # 窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def connect_to_server(self):
        """连接服务器"""
        try:
            self.client_socket.connect(self.server_addr)
            self.add_message("已连接到服务器，请输入昵称")
        except Exception as e:
            self.add_message(f"无法连接服务器: {str(e)}")
            self.join_button.config(state=tk.DISABLED)
    
    def set_nickname(self, event=None):
        """设置昵称并切换到聊天界面"""
        nickname = self.nickname_entry.get().strip()
        if nickname:
            self.nickname = nickname
            try:
                self.client_socket.send(nickname.encode('utf-8'))
                
                # 切换到聊天界面
                self.nickname_frame.pack_forget()
                self.chat_frame.pack(fill=tk.X)
                self.message_entry.focus_set()
                
                self.root.title(f"聊天室 - 用户: {nickname}")
                self.add_message(f"欢迎 {nickname} 进入聊天室！")
                
                # 启动消息接收线程
                threading.Thread(target=self.receive_messages, daemon=True).start()
                
            except Exception as e:
                self.add_message(f"设置昵称失败: {str(e)}")
    
    def send_message(self, event=None):
        """发送消息到服务器"""
        message = self.message_entry.get().strip()
        if message:
            try:
                self.client_socket.send(message.encode('utf-8'))
                self.add_message(f"{self.nickname}: {message}")
                self.message_entry.delete(0, tk.END)
            except Exception as e:
                self.add_message(f"发送消息失败: {str(e)}")
    
    def receive_messages(self):
        """接收服务器消息"""
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                
                message = data.decode('utf-8')
                self.add_message(message)
                
            except ConnectionResetError:
                self.add_message("与服务器的连接已断开")
                break
            except Exception as e:
                self.add_message(f"接收消息错误: {str(e)}")
                break
    
    def add_message(self, message):
        """添加消息到队列"""
        self.message_queue.put(message)
    
    def process_messages(self):
        """处理消息队列中的消息（线程安全）"""
        while True:
            if not self.message_queue.empty():
                message = self.message_queue.get()
                self.message_list.insert(tk.END, message)
                self.message_list.yview(tk.END)
            self.root.update_idletasks()
    
    def on_close(self):
        """窗口关闭时的清理工作"""
        if self.nickname:
            try:
                self.client_socket.send("exit".encode('utf-8'))
            except:
                pass
        self.client_socket.close()
        self.root.destroy()

if __name__ == '__main__':
    ChatClient()
