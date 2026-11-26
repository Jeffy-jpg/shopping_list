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
        self.resizable(True, True)

        #configure frames for window


        #configuring the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=9)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight = 9)


        #side_bar Frame
        self.sidebar_frame = CategorySidebar(self)
        self.sidebar_frame.grid(column =0, rowspan=2, sticky ="nsew", padx=(20,0), pady=20)

        #navigation bar
        self.nav_bar = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.nav_bar.grid(row= 0, column =2, columnspan=2,  sticky ="nsew", padx=20, pady =(20, 0))

        self.noti_btn = ctk.CTkButton(self.nav_bar, text = "🕭", font=("arial", 20, "bold"), corner_radius= 8)
        self.noti_btn.pack(side="right", pady = 10, padx = 10, ipadx = 10, ipady =5)

        #item list frame
        self.list_frame = ShoppingListPanel(self)
        self.list_frame.grid(row =1, column = 2, rowspan=2, columnspan = 2, padx=20, pady=20, sticky ="nsew")


    def change_category(self, category_name):
        self.list_frame.refresh_list(category_name)


app = App()
app.mainloop()