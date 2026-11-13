import customtkinter as ctk
from sidebar import CategorySidebar
from list import ShoppingListPanel
from tkinter import *
#from analytics import AnalyticsPanel

ctk.set_appearance_mode("dark")
#main window
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Shopping List")
        self.geometry("1000x600")
        self.resizable(False, False)

        #configure frames for window


        #configuring the grid
        #self.grid_columnconfigure(0, weight=1)
        #self.grid_columnconfigure(1, weight=2)
        #self.grid_columnconfigure(2, weight=3)
        #self.grid_rowconfigure(0, weight=1)


        #side_bar Frame
        self.sidebar_frame = CategorySidebar(self)
        self.sidebar_frame.pack(side="left", padx=(20,0), pady=20)

        #navigation bar

        self.nav_bar = ctk.CTkFrame(self, fg_color="Green", corner_radius=0)
        self.nav_bar.pack(side = "top",fill="both", expand = False)

        self.noti_btn = ctk.CTkButton(self.nav_bar, text = "notification", font=("arial", 15, "bold"))
        self.noti_btn.pack(side="right", pady = 10, padx = 10)

        #item list frame
        self.list_frame = ShoppingListPanel(self)
        self.list_frame.pack(side="right", padx=20, pady=20)

        #charts Frame
        #self.analytics_frame = AnalyticsPanel(self)
        #self.analytics_frame.grid(row=0, column = 2, sticky = "nsew", padx=(0,20), pady=20)

    def change_category(self, category_name):
        self.list_frame.refresh_list(category_name)


app = App()
app.mainloop()