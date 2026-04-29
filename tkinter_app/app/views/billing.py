import tkinter as tk
from tkinter import ttk, messagebox
from app.services.billing_service import BillingService
from app.utils.style import *

class BillingView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_PRIMARY)
        self.current_bill = None
        self._build_ui()
        self.refresh_table()

    def _build_ui(self):
        # Two panes
        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg=BG_PRIMARY, bd=0, sashwidth=4)
        paned.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left - Table
        left_frame = tk.Frame(paned, bg=BG_PRIMARY)
        paned.add(left_frame, minsize=500)
        
        filter_frame = tk.Frame(left_frame, bg=BG_PRIMARY)
        filter_frame.pack(fill="x", pady=10)
        tk.Label(filter_frame, text="Status Filter:", bg=BG_PRIMARY, fg=WHITE).pack(side="left")
        self.status_var = tk.StringVar(value="All")
        status_cb = ttk.Combobox(filter_frame, textvariable=self.status_var, values=["All", "pending", "paid"], state="readonly")
        status_cb.pack(side="left", padx=10)
        status_cb.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())
        
        cols = ("id", "booking_id", "customer", "room_charge", "extras", "total", "status")
        self.tree = ttk.Treeview(left_frame, columns=cols, show="headings")
        self.tree.heading("id", text="Bill ID")
        self.tree.heading("booking_id", text="Booking ID")
        self.tree.heading("customer", text="Customer")
        self.tree.heading("room_charge", text="Room Chg")
        self.tree.heading("extras", text="Extras")
        self.tree.heading("total", text="Total")
        self.tree.heading("status", text="Status")
        
        self.tree.column("id", width=50)
        self.tree.column("booking_id", width=80)
        self.tree.column("customer", width=120)
        self.tree.column("room_charge", width=80)
        self.tree.column("extras", width=80)
        self.tree.column("total", width=80)
        self.tree.column("status", width=80)
        
        self.tree.tag_configure('pending', foreground=WARNING_COLOR)
        self.tree.tag_configure('paid', foreground=SUCCESS_COLOR)
        
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        
        # Right - Details
        self.right_frame = tk.Frame(paned, bg=BG_SECONDARY, bd=2, relief="groove")
        paned.add(self.right_frame, minsize=400)
        self.right_frame.pack_propagate(False)
        
        tk.Label(self.right_frame, text="Bill Details", font=FONT_TITLE, bg=BG_SECONDARY, fg=WHITE).pack(pady=20)
        
        self.details_frame = tk.Frame(self.right_frame, bg=BG_SECONDARY)
        self.details_frame.pack(fill="both", expand=True, padx=20)
        
        self.lbl_booking = self._create_detail_row("Booking ID:", 0)
        self.lbl_customer = self._create_detail_row("Customer:", 1)
        self.lbl_room = self._create_detail_row("Room No:", 2)
        self.lbl_ci = self._create_detail_row("Check-in:", 3)
        self.lbl_co = self._create_detail_row("Check-out:", 4)
        self.lbl_room_chg = self._create_detail_row("Room Charges:", 5)
        self.lbl_extras = self._create_detail_row("Extra Charges:", 6)
        self.lbl_total = self._create_detail_row("Total Amount:", 7)
        self.lbl_status = self._create_detail_row("Payment Status:", 8)
        
        # Action Frame
        self.action_frame = tk.Frame(self.right_frame, bg=BG_SECONDARY)
        self.action_frame.pack(fill="x", pady=20, padx=20)
        
        # Extra charges form
        self.extras_frame = tk.Frame(self.action_frame, bg=BG_SECONDARY)
        tk.Label(self.extras_frame, text="Add Extras Amount:", bg=BG_SECONDARY, fg=WHITE).grid(row=0, column=0, sticky="w")
        self.ext_amt_var = tk.StringVar()
        tk.Entry(self.extras_frame, textvariable=self.ext_amt_var, width=10).grid(row=0, column=1, padx=5)
        
        tk.Label(self.extras_frame, text="Description:", bg=BG_SECONDARY, fg=WHITE).grid(row=1, column=0, sticky="w", pady=5)
        self.ext_desc_var = tk.StringVar()
        tk.Entry(self.extras_frame, textvariable=self.ext_desc_var, width=20).grid(row=1, column=1, padx=5, pady=5)
        
        btn_ext = tk.Button(self.extras_frame, text="Add Extras", command=self._add_extras)
        apply_button_style(btn_ext)
        btn_ext.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Payment form
        self.payment_frame = tk.Frame(self.action_frame, bg=BG_SECONDARY)
        tk.Label(self.payment_frame, text="Payment Method:", bg=BG_SECONDARY, fg=WHITE).grid(row=0, column=0, sticky="w")
        self.pay_method_var = tk.StringVar(value="cash")
        ttk.Combobox(self.payment_frame, textvariable=self.pay_method_var, values=["cash", "card", "online"], state="readonly", width=10).grid(row=0, column=1, padx=5)
        
        btn_pay = tk.Button(self.payment_frame, text="Mark as Paid", command=self._mark_paid)
        apply_button_style(btn_pay, "success")
        btn_pay.grid(row=1, column=0, columnspan=2, pady=10)

    def _create_detail_row(self, label_text, row):
        tk.Label(self.details_frame, text=label_text, bg=BG_SECONDARY, fg=TEXT_SECONDARY, font=FONT_BODY).grid(row=row, column=0, sticky="w", pady=8)
        val_lbl = tk.Label(self.details_frame, text="-", bg=BG_SECONDARY, fg=WHITE, font=FONT_BODY)
        val_lbl.grid(row=row, column=1, sticky="w", padx=10, pady=8)
        return val_lbl

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        bills = BillingService.get_all_bills()
        stat_filter = self.status_var.get()
        
        for b in bills:
            if stat_filter != "All" and b['payment_status'] != stat_filter:
                continue
                
            self.tree.insert("", "end", values=(
                b['bill_id'], b['booking_id'], b['customer_name'],
                f"{b['room_charges']:.2f}", f"{b['extra_charges']:.2f}", f"{b['total_amount']:.2f}",
                b['payment_status']
            ), tags=(b['payment_status'],))
            
        self._clear_details()

    def _on_select(self, event):
        sel = self.tree.selection()
        if not sel: return
        item = self.tree.item(sel[0])['values']
        booking_id = item[1]
        
        bill = BillingService.get_bill_details(booking_id)
        if bill:
            self.current_bill = bill
            self._update_details()

    def _update_details(self):
        b = self.current_bill
        self.lbl_booking.config(text=str(b['booking_id']))
        self.lbl_customer.config(text=b['customer_name'])
        self.lbl_room.config(text=b['room_number'])
        self.lbl_ci.config(text=b['check_in_date'])
        self.lbl_co.config(text=b['check_out_date'])
        self.lbl_room_chg.config(text=f"{b['room_charges']:.2f}")
        self.lbl_extras.config(text=f"{b['extra_charges']:.2f} ({b['extra_description']})")
        
        status = b['payment_status']
        color = SUCCESS_COLOR if status == 'paid' else WARNING_COLOR
        self.lbl_total.config(text=f"{b['total_amount']:.2f}", fg=color, font=("Segoe UI", 12, "bold"))
        self.lbl_status.config(text=status.upper(), fg=color)
        
        if status == 'pending':
            self.extras_frame.pack(side="left", fill="both", expand=True)
            self.payment_frame.pack(side="right", fill="both", expand=True)
        else:
            self.extras_frame.pack_forget()
            self.payment_frame.pack_forget()

    def _clear_details(self):
        self.current_bill = None
        for lbl in [self.lbl_booking, self.lbl_customer, self.lbl_room, self.lbl_ci, self.lbl_co, 
                    self.lbl_room_chg, self.lbl_extras, self.lbl_total, self.lbl_status]:
            lbl.config(text="-", fg=WHITE)
        self.extras_frame.pack_forget()
        self.payment_frame.pack_forget()

    def _add_extras(self):
        if not self.current_bill: return
        amt = self.ext_amt_var.get().strip()
        desc = self.ext_desc_var.get().strip()
        
        success, msg = BillingService.add_extras(self.current_bill['id'], amt, desc)
        if success:
            messagebox.showinfo("Success", msg)
            self.ext_amt_var.set("")
            self.ext_desc_var.set("")
            self.refresh_table()
        else:
            messagebox.showerror("Error", msg)

    def _mark_paid(self):
        if not self.current_bill: return
        method = self.pay_method_var.get()
        if messagebox.askyesno("Confirm", f"Mark this bill as paid via {method}?"):
            success, msg = BillingService.process_payment(self.current_bill['id'], method)
            if success:
                messagebox.showinfo("Success", msg)
                self.refresh_table()
            else:
                messagebox.showerror("Error", msg)
