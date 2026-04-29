import tkinter as tk
from tkinter import messagebox
from app.services.booking_service import BookingService
from app.models.booking import BookingModel
from app.models.customer import CustomerModel
from app.utils.style import *

class CheckinCheckoutView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_PRIMARY)
        self.current_booking = None
        self._build_ui()

    def _build_ui(self):
        title = tk.Label(self, text="Check-in / Check-out", bg=BG_PRIMARY, fg=WHITE, font=FONT_TITLE)
        title.pack(pady=20)
        
        # Search Bar
        search_frame = tk.Frame(self, bg=BG_PRIMARY)
        search_frame.pack(fill="x", padx=50, pady=10)
        
        tk.Label(search_frame, text="Enter Booking ID or CNIC:", bg=BG_PRIMARY, fg=WHITE).pack(side="left", padx=10)
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, width=25).pack(side="left", padx=10)
        
        search_btn = tk.Button(search_frame, text="Search", command=self._search)
        apply_button_style(search_btn)
        search_btn.config(width=10)
        search_btn.pack(side="left", padx=10)
        
        # Card Frame
        self.card_frame = tk.Frame(self, bg=BG_SECONDARY, bd=2, relief="groove")
        self.card_frame.pack(fill="both", expand=True, padx=50, pady=20)
        self.card_frame.pack_propagate(False)
        
        # Labels for details
        self.lbl_name = self._create_detail_row("Customer Name:", 0)
        self.lbl_cnic = self._create_detail_row("CNIC:", 1)
        self.lbl_room = self._create_detail_row("Room No:", 2)
        self.lbl_ci = self._create_detail_row("Check-in Date:", 3)
        self.lbl_co = self._create_detail_row("Check-out Date:", 4)
        self.lbl_status = self._create_detail_row("Status:", 5)
        
        # Action Buttons
        btn_frame = tk.Frame(self.card_frame, bg=BG_SECONDARY)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=40)
        
        self.btn_checkin = tk.Button(btn_frame, text="Check In", command=self._checkin)
        apply_button_style(self.btn_checkin, "success")
        self.btn_checkin.config(state="disabled")
        self.btn_checkin.pack(side="left", padx=20)
        
        self.btn_checkout = tk.Button(btn_frame, text="Check Out", command=self._checkout)
        apply_button_style(self.btn_checkout, "danger")
        self.btn_checkout.config(state="disabled")
        self.btn_checkout.pack(side="left", padx=20)

    def _create_detail_row(self, label_text, row):
        tk.Label(self.card_frame, text=label_text, bg=BG_SECONDARY, fg=TEXT_SECONDARY, font=FONT_HEADING).grid(row=row, column=0, sticky="w", padx=40, pady=15)
        val_lbl = tk.Label(self.card_frame, text="-", bg=BG_SECONDARY, fg=WHITE, font=FONT_HEADING)
        val_lbl.grid(row=row, column=1, sticky="w", padx=20, pady=15)
        return val_lbl

    def _search(self):
        val = self.search_var.get().strip()
        if not val:
            return messagebox.showerror("Error", "Please enter a Booking ID or CNIC.")
            
        booking = None
        if val.isdigit():
            # Try by ID
            booking = BookingModel.get_booking_by_id(int(val))
        else:
            # Try by CNIC
            customer = CustomerModel.get_customer_by_cnic(val)
            if customer:
                # Get their latest booking
                bookings = BookingModel.get_bookings_by_customer(customer['id'])
                if bookings:
                    b_id = bookings[-1]['id'] # Get the latest one
                    booking = BookingModel.get_booking_by_id(b_id)
                    
        if booking:
            self.current_booking = booking
            self._update_card()
        else:
            messagebox.showinfo("Not Found", "No booking found for the given criteria.")
            self.current_booking = None
            self._clear_card()

    def _update_card(self):
        b = self.current_booking
        self.lbl_name.config(text=b['customer_name'])
        self.lbl_cnic.config(text=b['cnic'])
        self.lbl_room.config(text=b['room_number'])
        self.lbl_ci.config(text=b['check_in_date'])
        self.lbl_co.config(text=b['check_out_date'])
        
        status = b['status']
        color = WHITE
        if status == 'confirmed': color = "#2196f3"
        elif status == 'checked_in': color = SUCCESS_COLOR
        elif status == 'checked_out': color = TEXT_SECONDARY
        elif status == 'cancelled': color = ERROR_COLOR
        
        self.lbl_status.config(text=status.upper(), fg=color)
        
        # Update buttons
        self.btn_checkin.config(state="normal" if status == "confirmed" else "disabled")
        self.btn_checkout.config(state="normal" if status == "checked_in" else "disabled")

    def _clear_card(self):
        self.lbl_name.config(text="-")
        self.lbl_cnic.config(text="-")
        self.lbl_room.config(text="-")
        self.lbl_ci.config(text="-")
        self.lbl_co.config(text="-")
        self.lbl_status.config(text="-", fg=WHITE)
        self.btn_checkin.config(state="disabled")
        self.btn_checkout.config(state="disabled")

    def _checkin(self):
        if not self.current_booking: return
        if messagebox.askyesno("Confirm", "Proceed with Check-in?"):
            success, msg = BookingService.check_in(self.current_booking['booking_id'])
            if success:
                messagebox.showinfo("Success", msg)
                self._search() # Refresh
            else:
                messagebox.showerror("Error", msg)

    def _checkout(self):
        if not self.current_booking: return
        if messagebox.askyesno("Confirm", "Proceed with Check-out?"):
            success, msg = BookingService.check_out(self.current_booking['booking_id'])
            if success:
                messagebox.showinfo("Success", msg)
                self._search() # Refresh
            else:
                messagebox.showerror("Error", msg)
