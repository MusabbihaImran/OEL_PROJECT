import sys
import tkinter as tk
from tkinter import messagebox

from app import init_db
from app.views.login import LoginWindow
from app.views.dashboard import DashboardWindow

def main():
    # Initialize the SQLite database automatically on first run
    init_db.initialize()
    
    # Initialize Tkinter root (hidden initially)
    root = tk.Tk()
    root.withdraw()
        
    def show_dashboard():
        for widget in root.winfo_children():
            widget.destroy()
        root.deiconify() # show root
        DashboardWindow(root, show_login)

    def show_login():
        for widget in root.winfo_children():
            widget.destroy()
        root.deiconify() # show root
        LoginWindow(root, show_dashboard)

    # Start with Login
    show_login()
    
    # Mainloop
    root.mainloop()

if __name__ == "__main__":
    main()
