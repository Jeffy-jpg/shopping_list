import customtkinter as ctk
from tkinter import messagebox

class CategorySidebar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=250, corner_radius=0, fg_color= "transparent")


        self.categories = ["Groceries", "Hardware", "Clothing"]
        self.button_widget = []
        self.selected_category = 'Groceries'

        self.category_title = ctk.CTkLabel(self, text="Shopping Categories",
                                            font=("Segoe UI", 18, "bold"),
                                            fg_color="#FEF08A",
                                            text_color= "#1E293B", 
                                            corner_radius= 12)        
        self.category_title.pack(ipadx=16, ipady=6, pady=(0, 15), fill="x", padx=20)

        self.buttons_container = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_container.pack(fill="both", expand=True, padx=20)

        self.controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.controls_frame.pack(side="bottom", fill="x", padx=20, pady=(10,0))

        self.add_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        self.add_frame.pack(fill="x", pady=(0,10))

        self.cat_entry = ctk.CTkEntry(self.add_frame, placeholder_text="Add Category")
        self.cat_entry.pack(side="left", fill="x", expand=True, padx=(0,5))

        self.add_cat_button = ctk.CTkButton(self.add_frame, text= "+", width=40,
                                            fg_color="#10B981", hover_color="#059669",
                                            command=self.add_new_category)
        self.add_cat_button.pack(fill="x", pady=(0,10))

        self.del_cat_button=ctk.CTkButton(self.controls_frame, text = "Delete Selected Category",
                                          fg_color="#EF4444", hover_color="#DC2626",
                                          command=self.delete_current_category)
        self.del_cat_button.pack(fill="x", pady=(5,10))
    
        self.render_btn()

    def render_btn(self):
        for btn in self.button_widget:
            btn.destroy()

        self.button_widget.clear()

        for category_name in self.categories:
            if category_name == self.selected_category:
                fg_col = "#3B82F6"
                hover_col = "#2563EB"
            else:
                fg_col = "#475569"
                hover_col = "#334155"

            new_btn = ctk.CTkButton(self.buttons_container, text=category_name,
                                    font=("Segoe UI", 13),
                                    fg_color=fg_col,
                                    hover_color= hover_col,
                                    command=lambda name = category_name: self.category_clicked(name))

            new_btn.pack(pady=5, padx=20, fill="x")
            self.button_widget.append(new_btn)
            
    def add_new_category(self):       
        new_cat = self.cat_entry.get().strip().capitalize()

        if new_cat:
            if len(self.categories) >=10:
                messagebox.showwarning("Limit Reached!","You Cannot Add More Than 10 Categories.")
                return
            
            if new_cat not in self.categories:
                self.categories.append(new_cat)
                self.selected_category = new_cat
                self.cat_entry.delete(0, 'end') #this is to empty the entry slot
                self.render_btn()
                getattr(self.master, "change_category")(new_cat)
                print(f"Created Category: {new_cat}")

    def delete_current_category(self):
        if len(self.categories)<=1:
            messagebox.showwarning("Error", "You Must Have At Least One Category")
            return

        target = self.selected_category

        confirm = messagebox.askyesno("Confirmation",
                                       f"Are you sure you want to delete the category "
                                       f"{target} and all its items?"
                                       )
        if not confirm:
            return

        self.categories.remove(target)
        self.selected_category = self.categories[0]
        self.render_btn()

        getattr(self.master, "change_category")(self.selected_category)
        print(f"Deleted Category: {target}. Switched to: {self.selected_category}")

    def category_clicked(self, name):
        self.selected_category = name
        self.render_btn()
        getattr(self.master, "change_category")(name)
        print(f"Currently viewing {name}")