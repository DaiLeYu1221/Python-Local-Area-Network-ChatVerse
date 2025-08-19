# -*- coding: utf-8 -*-

"""
项目使用的Python版本 -> python3.13.7

语言 -> 中文

Python局域网聊天室服务器 - 多用户聊天服务器实现

版权所有 (C) 2025 文宇香香工作室
根据MIT许可证授权
"""

import socket
import tkinter as tk
import threading
from queue import Queue

class ChatServer:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_addr = ('127.0.0.1', 6666)
        self.connected_clients = {}  # {client_addr: (socket, nickname)}
        self.message_queue = Queue()
        
        # 初始化GUI
        self.init_gui()
        
        # 启动服务器
        self.start_server()
        
        # 启动消息处理线程
        threading.Thread(target=self.process_messages, daemon=True).start()
        
        # 启动主循环
        self.root.mainloop()
    
    def init_gui(self):
        """初始化服务器GUI界面"""
        self.root = tk.Tk()
        self.root.title("网络聊天室【服务端】")
        
        # 居中窗口
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width, window_height = 500, 400
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # 消息显示区域
        self.message_frame = tk.Frame(self.root)
        self.message_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.scrollbar = tk.Scrollbar(self.message_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.message_list = tk.Listbox(
            self.message_frame,
            yscrollcommand=self.scrollbar.set,
            font=('微软雅黑', 10),
            bg="#f0f0f0"
        )
        self.message_list.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.message_list.yview)
        
        # 添加初始消息
        self.add_message(f"服务器已启动，监听于 {self.server_addr[0]}:{self.server_addr[1]}")
    
    def start_server(self):
        """启动服务器监听"""
        try:
            self.server_socket.bind(self.server_addr)
            self.server_socket.listen(5)
            self.add_message("服务器已启动，等待客户端连接...")
            threading.Thread(target=self.accept_clients, daemon=True).start()
        except Exception as e:
            self.add_message(f"服务器启动失败: {str(e)}")
    
    def accept_clients(self):
        """接受客户端连接"""
        while True:
            try:
                client_socket, client_addr = self.server_socket.accept()
                nickname = client_socket.recv(1024).decode('utf-8')
                
                self.connected_clients[client_addr] = (client_socket, nickname)
                self.add_message(f"[{nickname}] 进入聊天室 (IP: {client_addr[0]})")
                
                # 启动客户端消息处理线程
                threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_addr, nickname),
                    daemon=True
                ).start()
                
            except Exception as e:
                self.add_message(f"客户端连接异常: {str(e)}")
                break
    
    def handle_client(self, client_socket, client_addr, nickname):
        """处理客户端消息"""
        try:
            while True:
                data = client_socket.recv(1024)
                if not data or data.decode('utf-8').lower() == 'exit':
                    break
                
                message = data.decode('utf-8')
                self.add_message(f"收到来自 [{nickname}] 的消息: {message}")
                
                # 广播消息给其他客户端
                self.broadcast_message(f"{nickname}: {message}", exclude=client_addr)
                
        except ConnectionResetError:
            self.add_message(f"[{nickname}] 异常断开连接")
        finally:
            self.remove_client(client_socket, client_addr, nickname)
    
    def broadcast_message(self, message, exclude=None):
        """广播消息给所有客户端（排除指定客户端）"""
        for addr, (sock, _) in self.connected_clients.items():
            if exclude is None or addr != exclude:
                try:
                    sock.send(message.encode('utf-8'))
                except Exception as e:
                    self.add_message(f"发送消息给客户端失败: {str(e)}")
    
    def remove_client(self, client_socket, client_addr, nickname):
        """移除断开连接的客户端"""
        if client_addr in self.connected_clients:
            del self.connected_clients[client_addr]
            self.add_message(f"[{nickname}] 已退出聊天室")
            client_socket.close()
    
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

if __name__ == '__main__':
    ChatServer()
