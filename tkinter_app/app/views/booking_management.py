import tkinter as tk
from tkinter import ttk, messagebox
from app.services.booking_service import BookingService
from app.services.room_service import RoomService
from app.models.customer import CustomerModel
from app.utils.validators import Validators
from app.utils.style import *

class BookingManagementView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_PRIMARY)
        self._build_ui()

    def _build_ui(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.tab_all = tk.Frame(notebook, bg=BG_PRIMARY)
        self.tab_new = tk.Frame(notebook, bg=BG_PRIMARY)
        
        notebook.add(self.tab_all, text="All Bookings")
        notebook.add(self.tab_new, text="New Booking")
        
        self._build_all_bookings_tab()
        self._build_new_booking_tab()
        
        self.refresh_all_bookings()

    def _build_all_bookings_tab(self):
        # Search Bar
        search_frame = tk.Frame(self.tab_all, bg=BG_PRIMARY)
        search_frame.pack(fill="x", pady=10)
        
        tk.Label(search_frame, text="Search (Name or ID):", bg=BG_PRIMARY, fg=WHITE).pack(side="left")
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side="left", padx=10)
        
        search_btn = tk.Button(search_frame, text="Search", command=self.refresh_all_bookings)
        apply_button_style(search_btn)
        search_btn.config(width=10)
        search_btn.pack(side="left")
        
        # Table
        cols = ("id", "customer", "room", "checkin", "checkout", "status")
        self.tree = ttk.Treeview(self.tab_all, columns=cols, show="headings", height=15)
        
        self.tree.heading("id", text="Booking ID")
        self.tree.heading("customer", text="Customer Name")
        self.tree.heading("room", text="Room No.")
        self.tree.heading("checkin", text="Check-in")
        self.tree.heading("checkout", text="Check-out")
        self.tree.heading("status", text="Status")
        
        self.tree.tag_configure('confirmed', foreground="#2196f3") # Blue
        self.tree.tag_configure('checked_in', foreground=SUCCESS_COLOR)
        self.tree.tag_configure('checked_out', foreground=TEXT_SECONDARY)
        self.tree.tag_configure('cancelled', foreground=ERROR_COLOR)
        
        self.tree.pack(fill="both", expand=True, pady=10)
        
        # Buttons
        btn_frame = tk.Frame(self.tab_all, bg=BG_PRIMARY)
        btn_frame.pack(fill="x", pady=10)
        
        cancel_btn = tk.Button(btn_frame, text="Cancel Booking", command=self._cancel_booking)
        apply_button_style(cancel_btn, "danger")
        cancel_btn.pack(side="left", padx=10)
        
        ref_btn = tk.Button(btn_frame, text="Refresh", command=self.refresh_all_bookings)
        apply_button_style(ref_btn)
        ref_btn.pack(side="right", padx=10)

    def _build_new_booking_tab(self):
        # We will split it into two frames side by side
        left_frame = tk.Frame(self.tab_new, bg=BG_PRIMARY)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        right_frame = tk.Frame(self.tab_new, bg=BG_PRIMARY)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Section A: Customer Info (Left)
        tk.Label(left_frame, text="Customer Information", font=FONT_HEADING, bg=BG_PRIMARY, fg=HIGHLIGHT).grid(row=0, column=0, columnspan=2, sticky="w", pady=10)
        
        tk.Label(left_frame, text="CNIC Search:", bg=BG_PRIMARY, fg=WHITE).grid(row=1, column=0, sticky="w", pady=5)
        self.nb_cnic_var = tk.StringVar()
        tk.Entry(left_frame, textvariable=self.nb_cnic_var).grid(row=1, column=1, pady=5)
        
        s_btn = tk.Button(left_frame, text="Search", command=self._search_customer)
        apply_button_style(s_btn)
        s_btn.config(width=8, pady=2)
        s_btn.grid(row=1, column=2, padx=5)
        
        tk.Label(left_frame, text="Full Name:", bg=BG_PRIMARY, fg=WHITE).grid(row=2, column=0, sticky="w", pady=5)
        self.nb_name_var = tk.StringVar()
        tk.Entry(left_frame, textvariable=self.nb_name_var).grid(row=2, column=1, pady=5)
        
        tk.Label(left_frame, text="Phone:", bg=BG_PRIMARY, fg=WHITE).grid(row=3, column=0, sticky="w", pady=5)
        self.nb_phone_var = tk.StringVar()
        tk.Entry(left_frame, textvariable=self.nb_phone_var).grid(row=3, column=1, pady=5)
        
        tk.Label(left_frame, text="Email:", bg=BG_PRIMARY, fg=WHITE).grid(row=4, column=0, sticky="w", pady=5)
        self.nb_email_var = tk.StringVar()
        tk.Entry(left_frame, textvariable=self.nb_email_var).grid(row=4, column=1, pady=5)
        
        tk.Label(left_frame, text="Address:", bg=BG_PRIMARY, fg=WHITE).grid(row=5, column=0, sticky="w", pady=5)
        self.nb_address_txt = tk.Text(left_frame, height=3, width=20, font=FONT_BODY)
        self.nb_address_txt.grid(row=5, column=1, pady=5)

        # Section B: Room Selection (Right)
        tk.Label(right_frame, text="Room Selection", font=FONT_HEADING, bg=BG_PRIMARY, fg=HIGHLIGHT).grid(row=0, column=0, columnspan=2, sticky="w", pady=10)
        
        tk.Label(right_frame, text="Check-in (YYYY-MM-DD):", bg=BG_PRIMARY, fg=WHITE).grid(row=1, column=0, sticky="w", pady=5)
        self.nb_ci_var = tk.StringVar()
        tk.Entry(right_frame, textvariable=self.nb_ci_var).grid(row=1, column=1, pady=5)
        
        tk.Label(right_frame, text="Check-out (YYYY-MM-DD):", bg=BG_PRIMARY, fg=WHITE).grid(row=2, column=0, sticky="w", pady=5)
        self.nb_co_var = tk.StringVar()
        tk.Entry(right_frame, textvariable=self.nb_co_var).grid(row=2, column=1, pady=5)
        
        search_r_btn = tk.Button(right_frame, text="Search Available Rooms", command=self._search_rooms)
        apply_button_style(search_r_btn)
        search_r_btn.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.rtree = ttk.Treeview(right_frame, columns=("id", "room", "type", "price"), show="headings", height=5)
        self.rtree.heading("id", text="ID")
        self.rtree.heading("room", text="Room")
        self.rtree.heading("type", text="Type")
        self.rtree.heading("price", text="Price")
        self.rtree.column("id", width=30)
        self.rtree.column("room", width=50)
        self.rtree.column("type", width=80)
        self.rtree.column("price", width=80)
        self.rtree.grid(row=4, column=0, columnspan=2, pady=5)
        
        # Section C: Summary & Confirm (Right, below rooms)
        tk.Label(right_frame, text="Summary & Confirm", font=FONT_HEADING, bg=BG_PRIMARY, fg=HIGHLIGHT).grid(row=5, column=0, columnspan=2, sticky="w", pady=10)
        
        conf_btn = tk.Button(right_frame, text="Confirm Booking", command=self._confirm_booking)
        apply_button_style(conf_btn, "success")
        conf_btn.grid(row=6, column=0, columnspan=2, pady=20)

    def refresh_all_bookings(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        sv = self.search_var.get().lower()
        bookings = BookingService.get_all_bookings()
        
        for b in bookings:
            if sv and sv not in b['customer_name'].lower() and sv != str(b['booking_id']):
                continue
                
            self.tree.insert("", "end", values=(
                b['booking_id'], b['customer_name'], b['room_number'],
                b['check_in_date'], b['check_out_date'], b['status']
            ), tags=(b['status'],))

    def _cancel_booking(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a booking to cancel.")
            return
        
        item = self.tree.item(sel[0])['values']
        b_id = item[0]
        status = item[5]
        
        if status in ['cancelled', 'checked_out']:
            messagebox.showinfo("Info", f"Booking is already {status}.")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to cancel this booking?"):
            success, msg = BookingService.cancel_booking(b_id)
            if success:
                messagebox.showinfo("Success", msg)
                self.refresh_all_bookings()
            else:
                messagebox.showerror("Error", msg)

    def _search_customer(self):
        cnic = self.nb_cnic_var.get().strip()
        v, m = Validators.validate_cnic(cnic)
        if not v:
            messagebox.showerror("Validation Error", m)
            return
            
        customer = CustomerModel.get_customer_by_cnic(cnic)
        if customer:
            self.nb_name_var.set(customer['full_name'])
            self.nb_phone_var.set(customer['phone'])
            self.nb_email_var.set(customer['email'] or "")
            self.nb_address_txt.delete("1.0", "end")
            self.nb_address_txt.insert("1.0", customer['address'] or "")
            messagebox.showinfo("Found", "Customer details loaded.")
        else:
            messagebox.showinfo("Not Found", "Customer not found. Please enter details manually.")

    def _search_rooms(self):
        ci = self.nb_ci_var.get().strip()
        co = self.nb_co_var.get().strip()
        
        v, m = Validators.validate_date_range(ci, co)
        if not v:
            messagebox.showerror("Date Error", m)
            return
            
        for row in self.rtree.get_children():
            self.rtree.delete(row)
            
        rooms = RoomService.get_available_rooms(ci, co)
        if not rooms:
            messagebox.showinfo("No Rooms", "No available rooms for the selected dates.")
            return
            
        for r in rooms:
            self.rtree.insert("", "end", values=(r['id'], r['room_number'], r['type'].capitalize(), r['price_per_night']))

    def _confirm_booking(self):
        # Validate Customer
        cnic = self.nb_cnic_var.get().strip()
        name = self.nb_name_var.get().strip()
        phone = self.nb_phone_var.get().strip()
        email = self.nb_email_var.get().strip()
        address = self.nb_address_txt.get("1.0", "end").strip()
        
        v_cnic, m_cnic = Validators.validate_cnic(cnic)
        if not v_cnic: return messagebox.showerror("Error", m_cnic)
        v_name, m_name = Validators.validate_name(name)
        if not v_name: return messagebox.showerror("Error", m_name)
        v_phone, m_phone = Validators.validate_phone(phone)
        if not v_phone: return messagebox.showerror("Error", m_phone)
        if email:
            v_em, m_em = Validators.validate_email(email)
            if not v_em: return messagebox.showerror("Error", m_em)
            
        c_data = {
            'cnic': cnic, 'full_name': name, 'phone': phone, 'email': email, 'address': address
        }
        
        # Validate Room Selection
        sel = self.rtree.selection()
        if not sel:
            return messagebox.showerror("Error", "Please select a room from the table.")
        room_id = self.rtree.item(sel[0])['values'][0]
        
        # Validate Dates
        ci = self.nb_ci_var.get().strip()
        co = self.nb_co_var.get().strip()
        v_date, m_date = Validators.validate_date_range(ci, co)
        if not v_date: return messagebox.showerror("Error", m_date)
        
        # Service Call
        success, msg = BookingService.create_booking(c_data, room_id, ci, co)
        if success:
            messagebox.showinfo("Success", msg)
            self.refresh_all_bookings()
            # Clear forms
            self.nb_cnic_var.set("")
            self.nb_name_var.set("")
            self.nb_phone_var.set("")
            self.nb_email_var.set("")
            self.nb_address_txt.delete("1.0", "end")
            self.nb_ci_var.set("")
            self.nb_co_var.set("")
            for row in self.rtree.get_children():
                self.rtree.delete(row)
        else:
            messagebox.showerror("Error", msg)
