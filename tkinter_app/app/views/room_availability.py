import tkinter as tk
from tkinter import ttk, messagebox
from app.services.room_service import RoomService
from app.utils.validators import Validators
from app.utils.style import *

class RoomAvailabilityView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_PRIMARY)
        self._build_ui()
        self.refresh_data()

    def _build_ui(self):
        title = tk.Label(self, text="Room Availability", bg=BG_PRIMARY, fg=WHITE, font=FONT_TITLE)
        title.pack(pady=20)
        
        # Filter Bar
        filter_frame = tk.Frame(self, bg=BG_PRIMARY)
        filter_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(filter_frame, text="Type:", bg=BG_PRIMARY, fg=WHITE).pack(side="left", padx=5)
        self.type_filter = ttk.Combobox(filter_frame, values=["All", "single", "double", "suite", "deluxe"], state="readonly")
        self.type_filter.set("All")
        self.type_filter.pack(side="left", padx=5)
        
        tk.Label(filter_frame, text="Status:", bg=BG_PRIMARY, fg=WHITE).pack(side="left", padx=5)
        self.status_filter = ttk.Combobox(filter_frame, values=["All", "available", "occupied", "maintenance"], state="readonly")
        self.status_filter.set("All")
        self.status_filter.pack(side="left", padx=5)
        
        tk.Label(filter_frame, text="Floor:", bg=BG_PRIMARY, fg=WHITE).pack(side="left", padx=5)
        self.floor_filter = tk.Entry(filter_frame, width=5)
        self.floor_filter.pack(side="left", padx=5)
        
        filter_btn = tk.Button(filter_frame, text="Filter", command=self.refresh_data)
        apply_button_style(filter_btn)
        filter_btn.config(width=8)
        filter_btn.pack(side="left", padx=20)
        
        # Table
        columns = ("id", "room_number", "type", "floor", "price", "status")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("room_number", text="Room No.")
        self.tree.heading("type", text="Type")
        self.tree.heading("floor", text="Floor")
        self.tree.heading("price", text="Price/Night")
        self.tree.heading("status", text="Status")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("room_number", width=100, anchor="center")
        self.tree.column("type", width=100, anchor="center")
        self.tree.column("floor", width=80, anchor="center")
        self.tree.column("price", width=120, anchor="center")
        self.tree.column("status", width=100, anchor="center")
        
        self.tree.tag_configure('available', foreground=SUCCESS_COLOR)
        self.tree.tag_configure('occupied', foreground=ERROR_COLOR)
        self.tree.tag_configure('maintenance', foreground=WARNING_COLOR)
        
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Buttons
        btn_frame = tk.Frame(self, bg=BG_PRIMARY)
        btn_frame.pack(fill="x", padx=20, pady=20)
        
        add_btn = tk.Button(btn_frame, text="Add Room", command=self._open_add_modal)
        apply_button_style(add_btn, "success")
        add_btn.pack(side="left", padx=10)
        
        edit_btn = tk.Button(btn_frame, text="Edit Room", command=self._open_edit_modal)
        apply_button_style(edit_btn)
        edit_btn.pack(side="left", padx=10)
        
        del_btn = tk.Button(btn_frame, text="Delete Room", command=self._delete_room)
        apply_button_style(del_btn, "danger")
        del_btn.pack(side="left", padx=10)
        
        ref_btn = tk.Button(btn_frame, text="Refresh", command=self.refresh_data)
        apply_button_style(ref_btn)
        ref_btn.pack(side="right", padx=10)

    def refresh_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        t_f = self.type_filter.get()
        s_f = self.status_filter.get()
        fl_f = self.floor_filter.get().strip()
        
        rooms = RoomService.get_all_rooms()
        for r in rooms:
            if t_f != "All" and r['type'] != t_f: continue
            if s_f != "All" and r['status'] != s_f: continue
            if fl_f and str(r['floor']) != fl_f: continue
            
            self.tree.insert("", "end", values=(
                r['id'], r['room_number'], r['type'].capitalize(), 
                r['floor'], f"{r['price_per_night']:.2f}", r['status'].capitalize()
            ), tags=(r['status'],))

    def _open_add_modal(self):
        self._open_form_modal("Add Room")

    def _open_edit_modal(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a room to edit.")
            return
        item = self.tree.item(selected[0])['values']
        self._open_form_modal("Edit Room", item)

    def _open_form_modal(self, title, room_data=None):
        modal = tk.Toplevel(self)
        modal.title(title)
        modal.geometry("400x350")
        modal.configure(bg=BG_SECONDARY)
        modal.grab_set() # Make modal
        
        tk.Label(modal, text="Room Number:", bg=BG_SECONDARY, fg=WHITE).grid(row=0, column=0, pady=10, padx=10, sticky="w")
        rn_var = tk.StringVar(value=room_data[1] if room_data else "")
        tk.Entry(modal, textvariable=rn_var).grid(row=0, column=1, pady=10, padx=10)
        
        tk.Label(modal, text="Type:", bg=BG_SECONDARY, fg=WHITE).grid(row=1, column=0, pady=10, padx=10, sticky="w")
        type_var = tk.StringVar(value=room_data[2].lower() if room_data else "single")
        ttk.Combobox(modal, textvariable=type_var, values=["single", "double", "suite", "deluxe"], state="readonly").grid(row=1, column=1, pady=10, padx=10)
        
        tk.Label(modal, text="Price per Night:", bg=BG_SECONDARY, fg=WHITE).grid(row=2, column=0, pady=10, padx=10, sticky="w")
        price_var = tk.StringVar(value=room_data[4] if room_data else "")
        tk.Entry(modal, textvariable=price_var).grid(row=2, column=1, pady=10, padx=10)
        
        tk.Label(modal, text="Floor:", bg=BG_SECONDARY, fg=WHITE).grid(row=3, column=0, pady=10, padx=10, sticky="w")
        floor_var = tk.StringVar(value=room_data[3] if room_data else "")
        tk.Entry(modal, textvariable=floor_var).grid(row=3, column=1, pady=10, padx=10)
        
        def save():
            # Validate
            rn = rn_var.get()
            rt = type_var.get()
            pr = price_var.get()
            fl = floor_var.get()
            
            if not room_data:
                success, msg = RoomService.add_room(rn, rt, pr, fl)
            else:
                success, msg = RoomService.edit_room(room_data[0], room_number=rn, type=rt, price_per_night=pr, floor=fl)
                
            if success:
                messagebox.showinfo("Success", msg)
                modal.destroy()
                self.refresh_data()
            else:
                messagebox.showerror("Error", msg)
                
        btn = tk.Button(modal, text="Save", command=save)
        apply_button_style(btn, "success")
        btn.grid(row=4, column=0, columnspan=2, pady=20)

    def _delete_room(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a room to delete.")
            return
            
        item = self.tree.item(selected[0])['values']
        room_id = item[0]
        room_no = item[1]
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete Room {room_no}?"):
            success, msg = RoomService.delete_room(room_id)
            if success:
                messagebox.showinfo("Success", msg)
                self.refresh_data()
            else:
                messagebox.showerror("Error", msg)
