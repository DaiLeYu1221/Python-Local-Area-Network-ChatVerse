# -*- coding: utf-8 -*-

"""
Python version used in the project -> python3.13.7

Language -> English

Python Local Area Network ChatVerse - Multi-user chat server implementation

Copyright (C) 2025 Wenyu Xiangxiang Studio
Licensed under the MIT License
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
        
        # Initialize GUI
        self.init_gui()
        
        # Start server
        self.start_server()
        
        # Start message processing thread
        threading.Thread(target=self.process_messages, daemon=True).start()
        
        # Start main loop
        self.root.mainloop()
    
    def init_gui(self):
        """Initialize server GUI interface"""
        self.root = tk.Tk()
        self.root.title("Network Chat Room [Server]")
        
        # Center window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width, window_height = 500, 400
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Message display area
        self.message_frame = tk.Frame(self.root)
        self.message_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.scrollbar = tk.Scrollbar(self.message_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.message_list = tk.Listbox(
            self.message_frame,
            yscrollcommand=self.scrollbar.set,
            font=('Microsoft YaHei', 10),
            bg="#f0f0f0"
        )
        self.message_list.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.message_list.yview)
        
        # Add initial message
        self.add_message(f"Server started, listening on {self.server_addr[0]}:{self.server_addr[1]}")
    
    def start_server(self):
        """Start server listening"""
        try:
            self.server_socket.bind(self.server_addr)
            self.server_socket.listen(5)
            self.add_message("Server started, waiting for client connections...")
            threading.Thread(target=self.accept_clients, daemon=True).start()
        except Exception as e:
            self.add_message(f"Failed to start server: {str(e)}")
    
    def accept_clients(self):
        """Accept client connections"""
        while True:
            try:
                client_socket, client_addr = self.server_socket.accept()
                nickname = client_socket.recv(1024).decode('utf-8')
                
                self.connected_clients[client_addr] = (client_socket, nickname)
                self.add_message(f"[{nickname}] joined the chat room (IP: {client_addr[0]})")
                
                # Start client message handling thread
                threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_addr, nickname),
                    daemon=True
                ).start()
                
            except Exception as e:
                self.add_message(f"Client connection error: {str(e)}")
                break
    
    def handle_client(self, client_socket, client_addr, nickname):
        """Handle client messages"""
        try:
            while True:
                data = client_socket.recv(1024)
                if not data or data.decode('utf-8').lower() == 'exit':
                    break
                
                message = data.decode('utf-8')
                self.add_message(f"Received message from [{nickname}]: {message}")
                
                # Broadcast message to other clients
                self.broadcast_message(f"{nickname}: {message}", exclude=client_addr)
                
        except ConnectionResetError:
            self.add_message(f"[{nickname}] disconnected unexpectedly")
        finally:
            self.remove_client(client_socket, client_addr, nickname)
    
    def broadcast_message(self, message, exclude=None):
        """Broadcast message to all clients (excluding specified client)"""
        for addr, (sock, _) in self.connected_clients.items():
            if exclude is None or addr != exclude:
                try:
                    sock.send(message.encode('utf-8'))
                except Exception as e:
                    self.add_message(f"Failed to send message to client: {str(e)}")
    
    def remove_client(self, client_socket, client_addr, nickname):
        """Remove disconnected client"""
        if client_addr in self.connected_clients:
            del self.connected_clients[client_addr]
            self.add_message(f"[{nickname}] has left the chat room")
            client_socket.close()
    
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

if __name__ == '__main__':
    ChatServer()
