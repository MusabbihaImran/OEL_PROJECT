import tkinter as tk
from tkinter import ttk, messagebox
from app.services.feedback_service import FeedbackService
from app.utils.style import *

class FeedbackView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_PRIMARY)
        self._build_ui()
        self.refresh_data()

    def _build_ui(self):
        title = tk.Label(self, text="Customer Feedback", bg=BG_PRIMARY, fg=WHITE, font=FONT_TITLE)
        title.pack(pady=20)
        
        # New Feedback Form
        form_frame = tk.Frame(self, bg=BG_SECONDARY, bd=2, relief="groove")
        form_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(form_frame, text="Submit New Feedback", bg=BG_SECONDARY, fg=HIGHLIGHT, font=FONT_HEADING).grid(row=0, column=0, columnspan=4, pady=10, sticky="w", padx=10)
        
        tk.Label(form_frame, text="Booking ID:", bg=BG_SECONDARY, fg=WHITE).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.bid_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.bid_var).grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Customer Name:", bg=BG_SECONDARY, fg=WHITE).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.cname_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.cname_var).grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Rating (1-5):", bg=BG_SECONDARY, fg=WHITE).grid(row=1, column=2, padx=10, pady=5, sticky="e")
        self.rating_var = tk.IntVar(value=5)
        
        stars_frame = tk.Frame(form_frame, bg=BG_SECONDARY)
        stars_frame.grid(row=1, column=3, sticky="w")
        for i in range(1, 6):
            tk.Radiobutton(stars_frame, text=str(i), variable=self.rating_var, value=i, bg=BG_SECONDARY, fg=WHITE, selectcolor=BG_PRIMARY, activebackground=BG_SECONDARY, activeforeground=WHITE).pack(side="left")
            
        tk.Label(form_frame, text="Comment:", bg=BG_SECONDARY, fg=WHITE).grid(row=2, column=2, padx=10, pady=5, sticky="e")
        self.comment_txt = tk.Text(form_frame, height=3, width=30, font=FONT_BODY)
        self.comment_txt.grid(row=2, column=3, padx=10, pady=5)
        
        sub_btn = tk.Button(form_frame, text="Submit", command=self._submit)
        apply_button_style(sub_btn, "success")
        sub_btn.grid(row=3, column=0, columnspan=4, pady=15)
        
        # Table
        cols = ("id", "booking", "customer", "rating", "comment", "date")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("booking", text="Booking ID")
        self.tree.heading("customer", text="Customer Name")
        self.tree.heading("rating", text="Rating")
        self.tree.heading("comment", text="Comment")
        self.tree.heading("date", text="Date")
        
        self.tree.column("id", width=30)
        self.tree.column("booking", width=80)
        self.tree.column("customer", width=150)
        self.tree.column("rating", width=50)
        self.tree.column("comment", width=300)
        self.tree.column("date", width=120)
        
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Actions
        act_frame = tk.Frame(self, bg=BG_PRIMARY)
        act_frame.pack(fill="x", padx=20, pady=10)
        
        del_btn = tk.Button(act_frame, text="Delete Selected", command=self._delete)
        apply_button_style(del_btn, "danger")
        del_btn.pack(side="left")

    def refresh_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        feedbacks = FeedbackService.get_all_feedback()
        for f in feedbacks:
            stars = "★" * f['rating'] + "☆" * (5 - f['rating'])
            self.tree.insert("", "end", values=(
                f['id'], f['booking_id'], f['customer_name'],
                stars, f['comment'], f['created_at']
            ))

    def _submit(self):
        bid = self.bid_var.get().strip()
        cname = self.cname_var.get().strip()
        rating = str(self.rating_var.get())
        comment = self.comment_txt.get("1.0", "end").strip()
        
        success, msg = FeedbackService.submit_feedback(bid, cname, rating, comment)
        if success:
            messagebox.showinfo("Success", msg)
            self.bid_var.set("")
            self.cname_var.set("")
            self.rating_var.set(5)
            self.comment_txt.delete("1.0", "end")
            self.refresh_data()
        else:
            messagebox.showerror("Error", msg)

    def _delete(self):
        sel = self.tree.selection()
        if not sel:
            return messagebox.showwarning("Warning", "Select feedback to delete.")
            
        f_id = self.tree.item(sel[0])['values'][0]
        if messagebox.askyesno("Confirm", "Delete this feedback?"):
            success, msg = FeedbackService.delete_feedback(f_id)
            if success:
                messagebox.showinfo("Success", msg)
                self.refresh_data()
            else:
                messagebox.showerror("Error", msg)
