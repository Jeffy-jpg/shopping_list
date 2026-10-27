import json
import os
import customtkinter as ctk
from typing import Tuple


class ShoppingListPanel (ctk.CTkFrame):
    def __init__(self,master):
        super().__init__(master, width=350, corner_radius=8)

        self.DATA_FILE = "shopping_data.json"


        self.shopping_data = {
            "Groceries": [{"name":"milk", "checked": False, "quantity":1, "price":2.50 }],
            "Hardware": [{"name":"hammer", "checked": False, "quantity":1, "price":15.00 }],
            "Clothing":[{"name":"T-Shirt", "checked": False, "quantity":1, "price":50.00 }]
        }
        self.current_category = "Groceries"

        self.load_from_file()

        self.checkbox_widget = []
        self.row_frames = []

        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=15, padx=20)

        self.title_label = ctk.CTkLabel(self.header_frame, text=f"{self.current_category} List",
                                        font=("Segoe UI", 18, "bold"))
        self.title_label.pack(side="left", anchor="w")

        self.open_add_btn = ctk.CTkButton(self.header_frame, text= "Add Item", width=90,
                                          fg_color="#10B981", hover_color="#059669",
                                          font=("Segoe UI", 12, "bold"), 
                                          command=self.open_add_popup)
        self.open_add_btn.pack(side="right")

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
            is_checked = item["checked"]
            qty = item["quantity"]
            price = item["price"]

            item_row = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            item_row.pack(pady=5, padx=5, fill="x")
            self.row_frames.append(item_row)

            cb = ctk.CTkCheckBox(item_row, text = item_name, font=("segoe UI", 13))
            if is_checked:
                cb.select()

            cb.configure(command=lambda i= index, c=cb: self.toggle_item(i,c))
            cb.pack(side="left", fill="x", expand=True)
            self.checkbox_widget.append(cb)

            total_cost = qty * price
            info_text = f"x{qty} | ${total_cost:.2f}" if price > 0 else f"x{qty}" 

            info_label = ctk.CTkLabel(item_row, text = info_text,
                                      font=("Segoe UI", 12, "italic"),
                                      text_color="#64748B")
            info_label.pack(side="left", padx=10)

            edit_btn = ctk.CTkButton(item_row, text ="✎", width=28, height=28,
                                     fg_color="#3B82F6", hover_color="#2563EB",
                                     font=("Segoe UI", 12),
                                     command=lambda i= index, it=item: self.open_edit_popup(i, it))
            edit_btn.pack(side="right", padx=(5,0))

    def open_add_popup(self):
        AddItemModal(self)

    def open_edit_popup(self, index, item_dict):
        EditItemModal(self, index, item_dict)

    def update_item_details(self, index, updated_name, updated_qty, updated_price):
        self.shopping_data[self.current_category][index]["name"]=updated_name
        self.shopping_data[self.current_category][index]["quantity"] = updated_qty
        self.shopping_data[self.current_category][index]["price"]= updated_price
        self.save_to_file()
        self.refresh_list(self.current_category)

    def append_new_item(self, name, quantity, price):
        if self.current_category not in self.shopping_data:
            self.shopping_data[self.current_category] = []
        self.shopping_data[self.current_category].append({
            "name":name,
            "checked":False,
            "quantity": quantity,
            "price": price
        })
        self.save_to_file()
        self.refresh_list(self.current_category)
    
    def toggle_item(self, index, checkbox_widget):
        new_state = checkbox_widget.get() == 1
        self.shopping_data[self.current_category][index]["checked"] = new_state
        self.save_to_file()

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
            with open(self.DATA_FILE, "w") as f:
                json.dump(self.shopping_data, f, indent=4)
            print("Data Successfully Saved")

        except Exception as e: 
            print(f"Error saving file: {e}")

    def load_from_file(self):
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r") as f:
                    self.shopping_data = json.load(f)

                if self.shopping_data:
                    self.current_category = list(self.shopping_data.keys())[0]
                print("Successfully Loaded Data")

            except Exception as e:
                print(f"Error Loading Data: {e}")
                



class AddItemModal(ctk.CTkToplevel):
    def __init__(self, parent_panel):
        super().__init__(parent_panel)
        self.parent_panel = parent_panel

        self.title("Add Item To List")
        self.geometry("300x250")
        self.resizable(False, False)

        self.attributes("-topmost", True)
        self.grab_set()

        lbl = ctk.CTkLabel(self, text="New Item Details", font=("Segoe UI", 16, "bold"))
        lbl.pack(pady=10)

        self.name_entry = ctk.CTkEntry(self,placeholder_text="Item Name")
        self.name_entry.pack(fill="x", padx=30, pady=5)

        self.qty_entry = ctk.CTkEntry(self, placeholder_text="Quantity")
        self.qty_entry.insert(0,"1")
        self.qty_entry.pack(fill="x", padx=30, pady=5)

        self.price_entry = ctk.CTkEntry(self, placeholder_text="Price ($)")
        self.price_entry.pack(fill="x", pady=30, padx=5)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=30, pady=5)

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

            self.parent_panel.append_new_item(name, quantity, price)
            self.destroy()

class EditItemModal(ctk.CTkToplevel):
    def __init__(self, parent_panel, item_idex, item_dict):
        super().__init__(parent_panel)

        self.parent_panel = parent_panel
        self.item_index = item_idex

        self.title("Edit Item Details")
        self.geometry("300x290")
        self.resizable(False, False)

        self.attributes("-topmost", True)
        self.grab_set()

        lbl = ctk.CTkLabel(self, text="Modify Item", font=("Segoe UI", 16, "bold"))
        lbl.pack(pady=10)

        self.name_entry = ctk.CTkEntry(self, placeholder_text="Item Name")
        self.name_entry.insert(0, item_dict["name"])
        self.name_entry.pack(fill="x", padx=30, pady=5)

        self.qty_entry = ctk.CTkEntry(self, placeholder_text="Quantity")
        self.qty_entry.insert(0, str(item_dict["quantity"]))
        self.qty_entry.pack(fill="x", padx=30, pady=5)

        self.price_entry = ctk.CTkEntry(self, placeholder_text="Price ($)")
        self.price_entry.insert(0, str(item_dict["price"]))
        self.price_entry.pack(fill="x", padx=30, pady=5)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=30, pady=(15,5))

        cancel_btn = ctk.CTkButton(btn_frame, text="cancel", width= 110,
                                  fg_color="#64748B", command=self.destroy)
        cancel_btn.pack(side="left")

        save_btn = ctk.CTkButton(btn_frame, text="Save Changes", width=110, fg_color="#10B981",
                                 hover_color="#059669", command=self.save_data)
        save_btn.pack(side="right")

        del_frame =ctk.CTkFrame(self, fg_color="transparent")
        del_frame.pack(fill="x", padx=30, pady=5)

        del_btn= ctk.CTkButton(del_frame, text="🗑 Delete Item", fg_color="#EF4444",
                               hover_color="#DC2626", font=("Segoe UI", 12, "bold"),
                               command=self.delete_data)
        del_btn.pack(fill="x")

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
        self.parent_panel.delete_item(self.item_index)
        self.destroy()