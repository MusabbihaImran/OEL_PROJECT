import tkinter as tk
from tkinter import ttk

# Color palette - Dark Navy Theme
BG_PRIMARY = "#1a1a2e"       # dark navy background
BG_SECONDARY = "#16213e"     # slightly lighter navy
ACCENT = "#0f3460"           # deep blue accent
HIGHLIGHT = "#e94560"        # red-pink highlight color
TEXT_PRIMARY = "#eaeaea"     # near-white text
TEXT_SECONDARY = "#a8a8b3"   # muted grey text
SUCCESS_COLOR = "#4caf50"    # green for success states
WARNING_COLOR = "#ff9800"    # orange for warnings
ERROR_COLOR = "#f44336"      # red for errors
WHITE = "#ffffff"

# Fonts
FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_HEADING = ("Segoe UI", 14, "bold")
FONT_BODY = ("Segoe UI", 11)
FONT_SMALL = ("Segoe UI", 9)
FONT_BUTTON = ("Segoe UI", 11, "bold")

# Dimensions
BUTTON_WIDTH = 20
ENTRY_WIDTH = 30
PADDING_X = 20
PADDING_Y = 10
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 750

def _on_enter(e, widget, bg_color):
    """Hover effect enter"""
    widget['background'] = bg_color

def _on_leave(e, widget, bg_color):
    """Hover effect leave"""
    widget['background'] = bg_color

def apply_button_style(button_widget, style="primary"):
    """
    Styles a button widget with the correct bg/fg/activebackground from the palette.
    Styles: "primary", "danger", "success", "warning"
    Adds hover effects for visual attractiveness.
    """
    button_widget.config(
        font=FONT_BUTTON,
        fg=WHITE,
        width=BUTTON_WIDTH,
        relief="flat",
        cursor="hand2",
        bd=0,
        padx=10,
        pady=5
    )
    
    bg_color = ACCENT
    hover_color = HIGHLIGHT
    active_bg = HIGHLIGHT
    
    if style == "danger":
        bg_color = ERROR_COLOR
        hover_color = "#d32f2f"
        active_bg = "#d32f2f"
    elif style == "success":
        bg_color = SUCCESS_COLOR
        hover_color = "#388e3c"
        active_bg = "#388e3c"
    elif style == "warning":
        bg_color = WARNING_COLOR
        hover_color = "#f57c00"
        active_bg = "#f57c00"
    elif style == "highlight":
        bg_color = HIGHLIGHT
        hover_color = "#f06292"
        active_bg = "#f06292"
        
    button_widget.config(bg=bg_color, activebackground=active_bg, activeforeground=WHITE)
    button_widget.bind("<Enter>", lambda e: _on_enter(e, button_widget, hover_color))
    button_widget.bind("<Leave>", lambda e: _on_leave(e, button_widget, bg_color))

def apply_entry_style(entry_widget):
    """Styles an entry widget."""
    entry_widget.config(
        font=FONT_BODY,
        bg=BG_SECONDARY,
        fg=TEXT_PRIMARY,
        insertbackground=TEXT_PRIMARY,
        relief="flat",
        width=ENTRY_WIDTH
    )

def apply_label_style(label_widget, size="body"):
    """Styles a label widget based on size."""
    font_choice = FONT_BODY
    if size == "title":
        font_choice = FONT_TITLE
    elif size == "heading":
        font_choice = FONT_HEADING
    elif size == "small":
        font_choice = FONT_SMALL
        
    label_widget.config(
        font=font_choice,
        bg=BG_PRIMARY,
        fg=TEXT_PRIMARY
    )

def create_table_style():
    """
    Sets alternating row colors, header font, selection highlight for ttk.Treeview.
    Note: this configures the global ttk style for Treeview.
    """
    style = ttk.Style()
    style.theme_use("default")
    
    # Configure Treeview styling
    style.configure(
        "Treeview",
        background=BG_SECONDARY,
        foreground=TEXT_PRIMARY,
        rowheight=30,
        fieldbackground=BG_SECONDARY,
        font=FONT_BODY,
        borderwidth=0
    )
    
    # Configure selection
    style.map('Treeview', background=[('selected', ACCENT)], foreground=[('selected', WHITE)])
    
    # Configure headers
    style.configure(
        "Treeview.Heading",
        background=BG_PRIMARY,
        foreground=TEXT_PRIMARY,
        font=FONT_HEADING,
        relief="flat"
    )
    style.map('Treeview.Heading', background=[('active', ACCENT)])
