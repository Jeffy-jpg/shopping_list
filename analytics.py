from typing import Any, Tuple

import customtkinter as ctk 
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class AnalyticsPanel(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width= 350, corner_radius= 8)
        self.grid_propagate(False)

        self.total_budget = 0.0

        self.grid_rowconfigure(0, weight=4)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=2)
        self.grid_rowconfigure(3, weight=1)



        #Frame One: The Pie Chart
        self.frame1 = ctk.CTkFrame(self, fg_color="transparent")
        self.frame1.grid(row=0, column =0, sticky ="nsew", padx=15, pady=10)

        self.no_data_label = ctk.CTkLabel(self.frame1, text ="check item to view spending breakdown",
                                          font=("Segoe UI", 12, "italic"), text_color= "#64748B")
        self.no_data_label.pack(expand=True)
        self.canvas = None

        #Frame Two: The Progress Bar
        self.frame2 = ctk.CTkFrame(self, fg_color="transparent")
        self.frame2.grid(row=1, column=0, sticky ="nsew", padx=15, pady=5)

        self.progress_bar = ctk.CTkProgressBar(self.frame2, height=15, fg_color= "#E2E8F0",
                                                progress_color="#10B981")
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=(10, 2))

        self.allowed_label = ctk.CTkLabel(self.frame2, text = "Total Allowed to Spend: $0.00", 
                                         font=("Segoe UI", 11), text_color = "#64748B")
        self.allowed_label.pack(anchor="w")

        #Frame Three: Readable Data 
        self.frame3 = ctk.CTkFrame(self, fg_color="transparent")
        self.frame3.grid(row=2, column=0, sticky= "nsew", padx=15, pady=5)

        self.spent_label = ctk.CTkLabel(self.frame3, text="Total Spend: $0.000",
                                        font=("Segoe UI", 14, "bold"), text_color="#EF4444")
        self.spent_label.pack(anchor="w", pady=2)

        self.remains_label = ctk.CTkLabel(self.frame3, text="Total Remaining: 0.00",
                                          font=("Segoe UI", 14, "bold"), text_color="#3B82F6")
        self.remains_label.pack(anchor="w", pady=2)

        #Frame Four: Budget Trip Entry: 
        self.frame4 = ctk.CTkFrame(self, fg_color="transparent")
        self.frame4.grid(row=3, column=0, sticky = "nsew", padx=15, pady=5)

        self.entry_label = ctk.CTkLabel(self.frame4, text="Set Trip Budget ($):",
                                         font=("Segoe UI", 12))
        self.entry_label.pack(side="left", padx=(0, 10))

        self.budget_entry = ctk.CTkEntry(self.frame4, placeholder_text="e.g 200", width=120)
        self.budget_entry.pack(side="left", fill="x", expand = True)
        self.budget_entry.bind("<KeyRelease>", self.on_budget_changed)

    def on_budget_changed(self, event):
        raw_val = self.budget_entry.get().strip()
        raw_val = raw_val.replace("$","")
        try: 
            self.total_budget = float(raw_val) if raw_val else 0.0
        except ValueError:
            self.total_budget = 0.0

        self.allowed_label.configure(text=f"Total Allowed to Spend: ${self.total_budget:.2f}")
        self.update_analytics()

    def update_analytics(self):
        list_panel = getattr(self.master, "list_frame", None)
        if not list_panel or not hasattr(list_panel, "shopping_data"):
            return

        data = list_panel.shopping_data

        category_spending = {}
        grand_total_spending = 0.0

        for category, items in data.items():
            category_total = 0.0
            for item in items: 
                if item.get("checked",False):
                    cost = item.get("quantity", 1) * item.get("price", 0.0)
                    category_total += cost

            if category_total > 0:
                category_spending[category] = category_total
            grand_total_spending += category_total

        remaining = self.total_budget - grand_total_spending

        self.spent_label.configure(text=f"Total Spent: ${grand_total_spending:.2f}")
        self.remains_label.configure(text=f"Remaining: ${remaining:.2f}")
        if remaining < 0:
            self.remains_label.configure(text_color="#EF4444")
        else:
            self.remains_label.configure(text_color = "#3B82F6")

        if self.total_budget > 0:
            progress_percentage = min(grand_total_spending / self.total_budget, 1.0)
            self.progress_bar.set(progress_percentage)
            if progress_percentage >=1.0:
                self.progress_bar.configure(progress_color = "#EF4444")
            else:
                self.progress_bar.configure(progress_Color = "#10B981")

        else: 
            self.progress_bar.set(0)


        if self.canvas: 
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

        if category_spending:
            self.no_data_label.pack_forget()

            fig, ax = plt.subplots(figsize=(3,3), facecolor="none")
            fig.patch.set_facecolor('none')
            ax.patch.set_facecolor('none')

            labels = list( category_spending.keys())
            sizes = list(category_spending.values())
            colors = ['#EF4444', '#06B6D4', '#6366F1',
                    '#84CC16', '#A855F7', '#1E293B',
                    '#64748B', '#F8FAFC', '#F1F5F9',
                    '#475569']

            ax.pie(sizes, labels = labels, colors = colors[:len(labels)], autopct='%1.1f%%', 
                   startangle = 140, textprops = {'fontsize':9, 'color': '#1E293B'})
            ax.axis('equal')
            plt.tight_layout()

            self.canvas = FigureCanvasTkAgg(fig, master=self.frame1) 
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill="both", expand=True)
            plt.close(fig)
        else:
            self.no_data_label.pack(expand=True)

