# -*- coding: utf-8 -*-

"""
Python version used in the project -> python3.13.7

Language -> English

Python Local Area Network ChatVerse client - GUI client for chat system

Copyright (C) 2025 Wenyu Xiangxiang Studio
Licensed under the MIT License
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
        
        # Initialize GUI
        self.init_gui()
        
        # Connect to server
        self.connect_to_server()
        
        # Start message processing thread
        threading.Thread(target=self.process_messages, daemon=True).start()
        
        # Start main loop
        self.root.mainloop()
    
    def init_gui(self):
        """Initialize client GUI interface"""
        self.root = tk.Tk()
        self.root.title("Network Chat Room [Client]")
        
        # Set window size and position
        self.root.geometry('500x400+500+300')
        self.root.resizable(False, False)
        
        # Message display area
        self.message_frame = tk.Frame(self.root)
        self.message_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.scrollbar = tk.Scrollbar(self.message_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.message_list = tk.Listbox(
            self.message_frame,
            yscrollcommand=self.scrollbar.set,
            font=('Microsoft YaHei', 10),
            bg="#ffffff",
            height=15
        )
        self.message_list.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.message_list.yview)
        
        # Bottom input area
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Nickname input interface
        self.nickname_frame = tk.Frame(self.input_frame)
        self.nickname_frame.pack(fill=tk.X)
        
        tk.Label(self.nickname_frame, text='Nickname:').pack(side=tk.LEFT)
        
        self.nickname_entry = tk.Entry(self.nickname_frame, width=40)
        self.nickname_entry.pack(side=tk.LEFT, padx=5)
        self.nickname_entry.bind("<Return>", self.set_nickname)
        self.nickname_entry.focus_set()
        
        self.join_button = tk.Button(
            self.nickname_frame,
            text="Join",
            command=self.set_nickname,
            width=8
        )
        self.join_button.pack(side=tk.LEFT)
        
        # Message input interface (initially hidden)
        self.chat_frame = tk.Frame(self.input_frame)
        
        tk.Label(self.chat_frame, text='Message:').pack(side=tk.LEFT)
        
        self.message_entry = tk.Entry(self.chat_frame, width=40)
        self.message_entry.pack(side=tk.LEFT, padx=5)
        self.message_entry.bind("<Return>", self.send_message)
        
        self.send_button = tk.Button(
            self.chat_frame,
            text="Send",
            command=self.send_message,
            width=8
        )
        self.send_button.pack(side=tk.LEFT)
        
        # Window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def connect_to_server(self):
        """Connect to the server"""
        try:
            self.client_socket.connect(self.server_addr)
            self.add_message("Connected to server, please enter your nickname")
        except Exception as e:
            self.add_message(f"Failed to connect to server: {str(e)}")
            self.join_button.config(state=tk.DISABLED)
    
    def set_nickname(self, event=None):
        """Set nickname and switch to chat interface"""
        nickname = self.nickname_entry.get().strip()
        if nickname:
            self.nickname = nickname
            try:
                self.client_socket.send(nickname.encode('utf-8'))
                
                # Switch to chat interface
                self.nickname_frame.pack_forget()
                self.chat_frame.pack(fill=tk.X)
                self.message_entry.focus_set()
                
                self.root.title(f"Chat Room - User: {nickname}")
                self.add_message(f"Welcome {nickname} to the chat room!")
                
                # Start message receiving thread
                threading.Thread(target=self.receive_messages, daemon=True).start()
                
            except Exception as e:
                self.add_message(f"Failed to set nickname: {str(e)}")
    
    def send_message(self, event=None):
        """Send message to server"""
        message = self.message_entry.get().strip()
        if message:
            try:
                self.client_socket.send(message.encode('utf-8'))
                self.add_message(f"{self.nickname}: {message}")
                self.message_entry.delete(0, tk.END)
            except Exception as e:
                self.add_message(f"Failed to send message: {str(e)}")
    
    def receive_messages(self):
        """Receive messages from server"""
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                
                message = data.decode('utf-8')
                self.add_message(message)
                
            except ConnectionResetError:
                self.add_message("Connection to server has been lost")
                break
            except Exception as e:
                self.add_message(f"Error receiving message: {str(e)}")
                break
    
    def add_message(self, message):
        """Add message to queue"""
        self.message_queue.put(message)
    
    def process_messages(self):
        """Process messages in queue (thread-safe)"""
        while True:
            if not self.message_queue.empty():
                message = self.message_queue.get()
                self.message_list.insert(tk.END, message)
                self.message_list.yview(tk.END)
            self.root.update_idletasks()
    
    def on_close(self):
        """Cleanup when window is closed"""
        if self.nickname:
            try:
                self.client_socket.send("exit".encode('utf-8'))
            except:
                pass
        self.client_socket.close()
        self.root.destroy()

if __name__ == '__main__':
    ChatClient()
