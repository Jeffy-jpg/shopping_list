import json
import os
import customtkinter as ctk
import inventory_db
from tkinter import messagebox
from datetime import datetime



class ShoppingListPanel (ctk.CTkFrame):
    def __init__(self,master):
        super().__init__(master, width = 500, corner_radius=8, fg_color="#1e1e1e")

        inventory_db.init_db()


        self.shopping_data = {}
        self.item_history = {}
        
        self.current_category = "Groceries"

        self.load_from_file()

        self.checkbox_widget = []
        self.row_frames = []

        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=15, padx=20)

        self.title_label = ctk.CTkLabel(self.header_frame, text=f"{self.current_category} Stock",
                                        font=("Segoe UI", 18, "bold"))
        self.title_label.pack(side="left", anchor="w")

        #TODO add commands to the import button
        self.import_btn = ctk.CTkButton(self.header_frame, text = "Import List", width=90,
                                          fg_color="#10B981", hover_color="#059669",
                                          font=("Segoe UI", 12, "bold"))
        self.import_btn.pack(side="right", padx=10)

        #TODO add command to the export button
        self.export_btn = ctk.CTkButton(self.header_frame, text= "Export List", width=90,
                                          fg_color="#10B981", hover_color="#059669",
                                          font=("Segoe UI", 12, "bold"))
        self.export_btn.pack(side="right", padx=10)

        self.open_add_btn = ctk.CTkButton(self.header_frame, text= "Add Item", width=90,
                                          fg_color="#10B981", hover_color="#059669",
                                          font=("Segoe UI", 12, "bold"), 
                                          command=self.open_add_popup)
        self.open_add_btn.pack(side="right", padx=10)

        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand = True, padx = 15, pady = (0,10))  
        
        self.refresh_list("Groceries")

    def refresh_list(self, category_name):
        category_name = category_name.capitalize()
        self.current_category = category_name
        self.title_label.configure(text=f"{category_name} List")

        for frame in self.row_frames:
            frame.destroy()
        self.row_frames.clear()
        self.checkbox_widget.clear()

        if category_name not in self.shopping_data:
            self.shopping_data[category_name] = []

        for index, item in enumerate(self.shopping_data[category_name]):
            item_name = item["name"]
            qty = item["quantity"]
            price = item["price"]

            item_row = ctk.CTkFrame(self.scroll_frame, fg_color="#4a4a4a")
            item_row.pack(pady=10, padx=5, fill="x")
            self.row_frames.append(item_row)


            item_label = ctk.CTkLabel(item_row, text =item_name, font =("segoe UI", 15, "bold"))
            item_label.pack(side="left", fill="x", expand=False, padx=10, pady=10)


            total_cost = qty * price
            info_text = f"Current Stock:{qty} || UnitPrice: {price}" 


            edit_btn = ctk.CTkButton(item_row, text ="✎", width=28, height=28,
                                     fg_color="#3B82F6", hover_color="#2563EB",
                                     font=("Segoe UI", 12),
                                     command=lambda i= index, it=item: self.open_edit_popup(i, it))
            edit_btn.pack(side="right", padx=(10), pady=10)

            info_label = ctk.CTkLabel(item_row, text = info_text,
                                      font=("Segoe UI", 12, "italic"),
                                      text_color="white")
            info_label.pack(side="right", padx=10, pady=10)

    def open_add_popup(self):
        AddItemModal(self)

    def open_edit_popup(self, index, item_dict):
        EditItemModal(self, index, item_dict)

    def update_item_details(self, index, updated_name, updated_qty, updated_price):
        item = self.shopping_data[self.current_category][index]
        old_qty = item ["quantity"]
        date_added = item.get("date_added", "")

        diff = updated_qty - old_qty
        if diff != 0:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item_id = f"{item['name']}_{date_added}"
            self.item_history.setdefault(item_id, []).append({
                "adj_method": "Manual Adjust",
                "difference": diff,
                "new_figure": updated_qty,
                "comment": "User Update",
                "date_updated": now
            })

        item["name"] = updated_name
        item["quantity"] = updated_qty
        item["price"] = updated_price
        self.save_to_file()
        self.refresh_list(self.current_category)

    def append_new_item(self, name, quantity, price, now):
        if self.current_category not in self.shopping_data:
            self.shopping_data[self.current_category] = []
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.shopping_data[self.current_category].append({
            "name":name,
            "date_added":now,
            "quantity": quantity,
            "price": price
        })
        item_id = f"{name}_{now}"
        self.item_history.setdefault(item_id, []).append({
            "adj_method": "Initial Stock",
            "difference": quantity,
            "new_figure": quantity,
            "comment": "Item added to inventory",
            "date_updated": now

        })

        self.save_to_file()
        self.refresh_list(self.current_category)

    def delete_item(self, index):
        self.shopping_data[self.current_category].pop(index)
        self.refresh_list(self.current_category)
        self.save_to_file()

    def delete_category_data(self, category_name):
        if category_name in self.shopping_data:
            del self.shopping_data[category_name]
            self.save_to_file()

    def save_to_file(self):
        try:
            inventory_db.save_all(self.shopping_data, self.item_history)
            print("Data sucessfully saved")

        except Exception as e: 
            print(f"Error saving file: {e}")


    def load_from_file(self):
        try:
            self.shopping_data, self.item_history = inventory_db.load_all()

            if self.shopping_data:
                self.current_category = list(self.shopping_data.keys())[0]
            print("File loaded Successfully")

        except Exception as e:
            print(f"Error Loading Data: {e}")               

class AddItemModal(ctk.CTkToplevel):
    def __init__(self, parent_panel):
        super().__init__(parent_panel)
        self.parent_panel = parent_panel

        self.title("Add Item To List")
        self.resizable(False, False)

        self.attributes("-topmost", True)
        self.grab_set()

        lbl = ctk.CTkLabel(self, text="New Item Details", font=("Segoe UI", 16, "bold"))
        lbl.pack(pady=10)

        #NAME ENTRY AND LABEL
        self.name_label =ctk.CTkLabel(self, text="Item Name:", font=("Segoe UI", 12, "bold"))
        self.name_label.pack(anchor = "w", expand=True, padx=30, pady=(5,0))
        self.name_entry = ctk.CTkEntry(self,placeholder_text="Item Name")
        self.name_entry.pack(fill="x", padx=30, pady=(0,5))  

        #QUANTITY ENTRY AND LABEL
        self.qty_label = ctk.CTkLabel(self,  text="Quantity:", font=("Segoe UI", 12, "bold"))
        self.qty_label.pack(anchor = "w", expand=True, padx=30, pady=(5,0))
        self.qty_entry = ctk.CTkEntry(self, placeholder_text="Quantity")
        self.qty_entry.insert(0,"1")
        self.qty_entry.pack(fill="x", padx=30, pady=(0,5))

        #PRICE ENTRY AND LABEL
        self.price_label = ctk.CTkLabel(self,  text="Price:", font=("Segoe UI", 12, "bold"))
        self.price_label.pack(anchor = "w", expand=True, padx=30, pady=(5,0))        
        self.price_entry = ctk.CTkEntry(self, placeholder_text="Price ($)")
        self.price_entry.pack(fill="x", pady=(0,5), padx=30, expand =False)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=30, pady=20)

        cancel_btn = ctk.CTkButton(btn_frame, text="Cancel", width=110, fg_color="#64748B",
                                   command=self.destroy)
        cancel_btn.pack(side="left")

        save_btn = ctk.CTkButton(btn_frame, text = "Add Item", width=110, fg_color="#059669",
                               command=self.add_data)
        save_btn.pack(side="right")

    def add_data(self):
        name = self.name_entry.get().strip()
        qty_str = self.qty_entry.get().strip()
        price_str = self.price_entry.get().strip()

        if name:
            try: 
                quantity = int(qty_str) if qty_str else 1
            except ValueError:
                quantity = 1

            try:
                price = float(price_str) if price_str else 0.0
            except ValueError:
                price = 0.0

            self.parent_panel.append_new_item(name, quantity, price, "2026-11-25") #TODO replace with date function
            self.destroy()

class EditItemModal(ctk.CTkToplevel):
    def __init__(self, parent_panel, item_idex, item_dict):
        super().__init__(parent_panel)

        self.parent_panel = parent_panel
        self.item_index = item_idex

        self.title("Edit Item Details")
        #self.geometry("300x290")
        self.resizable(False, False)

        self.attributes("-topmost", True)
        self.grab_set()

        self.mainframe = ctk.CTkFrame(self, fg_color= "transparent", corner_radius=0)
        self.mainframe.pack(padx=10, pady=10, fill ="both", expand=True)

        lbl = ctk.CTkLabel(self.mainframe, text="Modify Item", font=("Segoe UI", 16, "bold"))
        lbl.pack(pady=10)

        #Item name section
        self.name_label=ctk.CTkLabel(self.mainframe, text="Item Name:",
                                      font=("Segoe UI", 12, "bold"))
        self.name_label.pack(anchor="w", expand=True, padx=30, pady=(5,0))
        self.name_entry = ctk.CTkEntry(self.mainframe, placeholder_text="Item Name")
        self.name_entry.insert(0, item_dict["name"])
        self.name_entry.pack(fill="x", padx=30, pady=(0,5))

        #quantity section
        self.qty_label=ctk.CTkLabel(self.mainframe, text="Quantity:",
                                      font=("Segoe UI", 12, "bold"))
        self.qty_label.pack(anchor="w", expand=True, padx=30, pady=(5,0))
        self.qty_entry = ctk.CTkEntry(self.mainframe, placeholder_text="Quantity")
        self.qty_entry.insert(0, str(item_dict["quantity"]))
        self.qty_entry.pack(fill="x", padx=30, pady=(0,5))

        #price section
        self.price_label=ctk.CTkLabel(self.mainframe, text="Price:",
                                      font=("Segoe UI", 12, "bold"))
        self.price_label.pack(anchor="w", expand=True, padx=30, pady=(5,0))
        self.price_entry = ctk.CTkEntry(self.mainframe, placeholder_text="Price ($)")
        self.price_entry.insert(0, str(item_dict["price"]))
        self.price_entry.pack(fill="x", padx=30, pady=(0,5))

        btn_frame = ctk.CTkFrame(self.mainframe, fg_color="transparent")
        btn_frame.pack(fill="x", padx=30, pady=(15,5))

        cancel_btn = ctk.CTkButton(btn_frame, text="cancel", width= 110,
                                  fg_color="#64748B", command=self.destroy)
        cancel_btn.pack(side="left", padx=(5,0))

        save_btn = ctk.CTkButton(btn_frame, text="Save Changes", width=110, fg_color="#10B981",
                                 hover_color="#059669", command=self.save_data)
        save_btn.pack(side="right", padx= (5,5))

        del_frame =ctk.CTkFrame(self, fg_color="transparent", width=110)
        del_frame.pack(fill="x", padx=30, pady=5)

        del_btn= ctk.CTkButton(del_frame, text="🗑 Delete Item", fg_color="#EF4444",
                               hover_color="#DC2626", font=("Segoe UI", 12, "bold"),
                               command=self.delete_data)
        del_btn.pack(fill="x",pady=5)

    def save_data(self):
        name = self.name_entry.get().strip()
        qty_str = self.qty_entry.get().strip()
        price_str = self.price_entry.get().strip()

        if name:
            try:
                quantity = int(qty_str) if qty_str else 1
            except ValueError:
                quantity =1 

            try: 
                price = float(price_str) if price_str else 0.0
            except ValueError:
                price = 0.0

            self.parent_panel.update_item_details(self.item_index, name, quantity, price)
            self.destroy()

    def delete_data(self):
        confirm = messagebox.askyesno("Confirmation",
                                      f"Are you sure you want to delete this item?")
        if confirm: 
            self.parent_panel.delete_item(self.item_index)
            self.destroy()
            return