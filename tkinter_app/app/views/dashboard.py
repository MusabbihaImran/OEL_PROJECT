import tkinter as tk
from tkinter import ttk
from app.services.auth import AuthService
from app.models.room import RoomModel
from app.models.booking import BookingModel
from app.models.billing_model import BillingModel
from app.utils.style import *

# Import other views to load into the dashboard
from app.views.room_availability import RoomAvailabilityView
from app.views.booking_management import BookingManagementView
from app.views.checkin_checkout import CheckinCheckoutView
from app.views.billing import BillingView
from app.views.feedback import FeedbackView

class DashboardWindow:
    """Main dashboard application window."""
    
    def __init__(self, root, on_logout_callback):
        self.root = root
        self.on_logout = on_logout_callback
        
        self.root.title("Hotel Management System - Dashboard")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=BG_PRIMARY)
        
        # Center the window
        self.root.eval('tk::PlaceWindow . center')
        
        # Configure global treeview style
        create_table_style()
        
        self._build_ui()

    def _build_ui(self):
        # Top bar
        top_bar = tk.Frame(self.root, bg=ACCENT, height=60)
        top_bar.pack(side="top", fill="x")
        top_bar.pack_propagate(False)
        
        title_lbl = tk.Label(top_bar, text="Hotel Management System", bg=ACCENT, fg=WHITE, font=FONT_TITLE)
        title_lbl.pack(side="left", padx=20, pady=10)
        
        user_lbl = tk.Label(top_bar, text=f"Logged in as: {AuthService.current_user['username']}", bg=ACCENT, fg=WHITE, font=FONT_BODY)
        user_lbl.pack(side="right", padx=20, pady=15)
        
        logout_btn = tk.Button(top_bar, text="Logout", command=self._handle_logout)
        apply_button_style(logout_btn, "danger")
        logout_btn.config(width=10)
        logout_btn.pack(side="right", padx=10, pady=10)
        
        # Sidebar
        sidebar = tk.Frame(self.root, bg=BG_SECONDARY, width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # Main Content Area
        self.content_area = tk.Frame(self.root, bg=BG_PRIMARY)
        self.content_area.pack(side="right", fill="both", expand=True)
        
        # Nav buttons
        self._create_nav_button(sidebar, "Dashboard Home", self._show_home)
        self._create_nav_button(sidebar, "Room Availability", lambda: self._load_view(RoomAvailabilityView))
        self._create_nav_button(sidebar, "Booking Management", lambda: self._load_view(BookingManagementView))
        self._create_nav_button(sidebar, "Check-in/Check-out", lambda: self._load_view(CheckinCheckoutView))
        self._create_nav_button(sidebar, "Billing", lambda: self._load_view(BillingView))
        self._create_nav_button(sidebar, "Customer Feedback", lambda: self._load_view(FeedbackView))
        
        # Initial view
        self._show_home()

    def _create_nav_button(self, parent, text, command):
        btn = tk.Button(parent, text=text, command=command)
        apply_button_style(btn)
        btn.config(width=18, anchor="w", padx=20)
        btn.pack(pady=5, padx=10, fill="x")

    def _clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def _load_view(self, ViewClass):
        self._clear_content()
        view = ViewClass(self.content_area)
        view.pack(fill="both", expand=True)

    def _show_home(self):
        self._clear_content()
        
        # Fetch stats
        rooms = RoomModel.get_all_rooms()
        total_rooms = len(rooms)
        avail_rooms = sum(1 for r in rooms if r['status'] == 'available')
        
        bookings = BookingModel.get_all_bookings()
        today = tk.StringVar(value="Today") # mock date comparison logic for simplicity in UI demo
        todays_bookings = len(bookings) # Just showing total for simple dashboard
        
        bills = BillingModel.get_all_bills()
        pending_payments = sum(1 for b in bills if b['payment_status'] == 'pending')
        
        lbl = tk.Label(self.content_area, text="Dashboard Overview", bg=BG_PRIMARY, fg=WHITE, font=FONT_TITLE)
        lbl.pack(pady=30)
        
        cards_frame = tk.Frame(self.content_area, bg=BG_PRIMARY)
        cards_frame.pack(pady=20)
        
        self._create_stat_card(cards_frame, "Total Rooms", str(total_rooms), 0, 0)
        self._create_stat_card(cards_frame, "Available Rooms", str(avail_rooms), 0, 1)
        self._create_stat_card(cards_frame, "Total Bookings", str(todays_bookings), 1, 0)
        self._create_stat_card(cards_frame, "Pending Payments", str(pending_payments), 1, 1)

    def _create_stat_card(self, parent, title, value, row, col):
        card = tk.Frame(parent, bg=BG_SECONDARY, width=250, height=150, bd=2, relief="groove")
        card.grid(row=row, column=col, padx=20, pady=20)
        card.pack_propagate(False)
        
        t_lbl = tk.Label(card, text=title, bg=BG_SECONDARY, fg=TEXT_SECONDARY, font=FONT_HEADING)
        t_lbl.pack(pady=(30, 10))
        
        v_lbl = tk.Label(card, text=value, bg=BG_SECONDARY, fg=HIGHLIGHT, font=("Segoe UI", 28, "bold"))
        v_lbl.pack()

    def _handle_logout(self):
        AuthService.logout()
        self.on_logout()
