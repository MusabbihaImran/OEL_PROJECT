import tkinter as tk
from tkinter import messagebox
from app.services.auth import AuthService
from app.utils.style import *

class LoginWindow:
    """Handles the user login screen."""
    
    def __init__(self, root, on_success_callback):
        self.root = root
        self.on_success = on_success_callback
        
        self.root.title("Hotel Management System - Login")
        self.root.geometry(f"500x400")
        self.root.configure(bg=BG_PRIMARY)
        
        # Center the window
        self.root.eval('tk::PlaceWindow . center')
        
        self._build_ui()

    def _build_ui(self):
        # Title
        title_lbl = tk.Label(self.root, text="Hotel Management System")
        apply_label_style(title_lbl, "title")
        title_lbl.pack(pady=(40, 20))
        
        # Frame for form
        form_frame = tk.Frame(self.root, bg=BG_PRIMARY)
        form_frame.pack(pady=10)
        
        # Username
        user_lbl = tk.Label(form_frame, text="Username:")
        apply_label_style(user_lbl)
        user_lbl.grid(row=0, column=0, sticky="w", pady=10)
        
        self.user_entry = tk.Entry(form_frame)
        apply_entry_style(self.user_entry)
        self.user_entry.grid(row=0, column=1, pady=10, padx=10)
        
        # Password
        pwd_lbl = tk.Label(form_frame, text="Password:")
        apply_label_style(pwd_lbl)
        pwd_lbl.grid(row=1, column=0, sticky="w", pady=10)
        
        self.pwd_entry = tk.Entry(form_frame, show="*")
        apply_entry_style(self.pwd_entry)
        self.pwd_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # Show/Hide Toggle
        self.show_pwd = False
        self.toggle_btn = tk.Button(form_frame, text="Show", command=self._toggle_password)
        apply_button_style(self.toggle_btn)
        self.toggle_btn.config(width=5)
        self.toggle_btn.grid(row=1, column=2, padx=5)
        
        # Login Button
        self.login_btn = tk.Button(self.root, text="Login", command=self._handle_login)
        apply_button_style(self.login_btn, "primary")
        self.login_btn.pack(pady=20)
        
        # Error Label
        self.error_lbl = tk.Label(self.root, text="", fg=ERROR_COLOR, bg=BG_PRIMARY, font=FONT_BODY)
        self.error_lbl.pack()

    def _toggle_password(self):
        self.show_pwd = not self.show_pwd
        if self.show_pwd:
            self.pwd_entry.config(show="")
            self.toggle_btn.config(text="Hide")
        else:
            self.pwd_entry.config(show="*")
            self.toggle_btn.config(text="Show")

    def _handle_login(self):
        username = self.user_entry.get().strip()
        password = self.pwd_entry.get()
        
        if len(username) < 3:
            self.error_lbl.config(text="Username must be at least 3 characters.")
            return
        if not password:
            self.error_lbl.config(text="Password cannot be empty.")
            return
            
        user = AuthService.login(username, password)
        if user:
            self.error_lbl.config(text="")
            self.on_success()
        else:
            self.error_lbl.config(text="Invalid username or password.")
