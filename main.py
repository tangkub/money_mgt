# main.py

# Modules
import tkinter as tk
from tkinter import CENTER, font, messagebox, ttk
from PIL import Image, ImageTk
import sqlite3
from sqlite3 import Error
import os
import datetime
import re



# CONSTANT
FONT_HEAD = ("Helvetica", "24", "bold", "underline")
FONT_L = ("Helvetica", "14")
FONT_M = ("Helvetica", "12")
FONT_S = ("Helvetica", "8")
COLOR_1 = "#FEF5ED"
COLOR_2 = "#D3E4CD"
COLOR_3 = "#ADC2A9"
COLOR_4 = "#99A799"

# Current path
current_path = os.path.dirname(os.path.abspath(__file__))

# Connect database
def connect_db(path=current_path):
    connection = None
    try:
        connection = sqlite3.connect(os.path.join(path, 'database/database.sqlite'))
        print("Connection to SQLite DB successful")
        return connection
    except Error as e:
        print(f"The error '{e}' occurred")

# Function to execute query
def execute_query(query):
    connection = connect_db()
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        connection.close()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

# Function to read query
def execute_read_query(query):
    connection = connect_db()
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        connection.close()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

# Create table: users
create_users_tables = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
"""
execute_query(create_users_tables)

# Create table: budget
create_budget_tables = """
CREATE TABLE IF NOT EXISTS budget (
    bg_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bg_date TEXT,
    bg_exp_type TEXT,
    bg_exp_amt REAL,
    bg_sub_type TEXT,
    bg_sub_amt REAL,
    bg_inc_type TEXT,
    bg_inc_amt REAL,
    bg_sav_group TEXT,
    bg_sav_amt REAL,
    bg_inv_purpose TEXT,
    bg_inv_amt REAL,
    bg_description TEXT,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);
"""
execute_query(create_budget_tables)

# Create table: expense
create_expense_tables = """
CREATE TABLE IF NOT EXISTS expense (
    exp_id INTEGER PRIMARY KEY AUTOINCREMENT,
    exp_date TEXT,
    exp_type TEXT,
    exp_amt REAL,
    exp_description TEXT,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);
"""
execute_query(create_expense_tables)



# Main app
class MoneyApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Window
        self.title("Money Management System")
        self.minsize(width=500, height=300)
        self.geometry("1000x600")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # self.wm_attributes("-transparentcolor", 'grey')

        # Container
        container = tk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        # Multiple pages
        self.frames = {}
        pages = [Login, Register, Menu,
                BudgetExp, BudgetSub, BudgetInc, BudgetSav, BudgetInv,
                Summary,
                ExpenseView, ExpenseAdd, ExpenseUpdate, ExpenseDelete,
                SubscriptionView, SubscriptionAdd, SubscriptionUpdate, SubscriptionDelete,
                IncomeView, IncomeAdd, IncomeUpdate, IncomeDelete,
                SavingView, SavingAdd, SavingUpdate, SavingDelete,
                InvestView, InvestAdd, InvestUpdate, InvestDelete,
                Export]
        for page in pages:
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")

        # Starter page
        self.ShowFrame(Login)

    # Display the chosen page
    def ShowFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()



# Base frame for all pages
class Background(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(master, *args, **kwargs)

        # Add background
        current_path = os.path.dirname(os.path.abspath(__file__))
        self.image = Image.open(os.path.join(current_path, 'img/background.jpg'))
        self.img_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.img_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.lbl_background = tk.Label(self, image=self.background_image, bg="white")
        self.lbl_background.bind('<Configure>', self.Resizing)
        self.lbl_background.place(x=0, y=0, relwidth=1, relheight=1)

    # Resize background image responding to window size
    def Resizing(self, event):
        new_width = event.width
        new_height = event.height
        self.image = self.img_copy.resize((new_width, new_height))
        self.background_image = ImageTk.PhotoImage(self.image)
        self.lbl_background.config(image = self.background_image)
        self.lbl_background.image = self.background_image



class Login(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        # to call another class function
        self.controller = controller

        # Label
        self.lbl_user = tk.Label(self, text="User :",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_pass = tk.Label(self, text="Password :",
            bg=COLOR_1,  fg=COLOR_4, font=FONT_L)

        self.lbl_user.grid(row=1, column=1, sticky="e",
             ipadx=3, ipady=3,
             padx=(100, 5), pady=(220, 10))
        self.lbl_pass.grid(row=2, column=1, sticky="e",
            ipadx=3, ipady=3,
            padx=(100, 5), pady=(0, 0))

        # Entry
        self.ent_user = tk.Entry(self, font=FONT_M)
        self.ent_pass = tk.Entry(self, font=FONT_M, show="*")

        self.ent_user.grid(row=1, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5, 5), pady=(220, 10))
        self.ent_pass.grid(row=2, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5, 5), pady=(0, 10))

        # Button
        self.btn_login = tk.Button(self, text="Login",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:self.LoginSystem())
        self.btn_cancel = tk.Button(self, text="Cancel",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:self.ClearText())
        self.btn_register = tk.Button(self, text="Register",
            font=FONT_S, relief="flat",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            command=lambda:controller.ShowFrame(Register))

        self.btn_login.grid(row=3, column=2,
            ipadx=10)
        self.btn_cancel.grid(row=3, column=3,
            ipadx=10)
        self.btn_register.grid(row=4, column=2, columnspan=2, sticky="ew",
            pady=10)

    def LoginSystem(self):
        # to futher use
        global input_user
        global input_id

        # get user's input
        input_user = self.ent_user.get()
        input_pwd = self.ent_pass.get()

        # get user's database
        select_users = "SELECT * FROM users"
        users = execute_read_query(select_users)

        # check user & password
        for user in users:
            if input_user == user[1]:
                if input_pwd == user[2]:
                    # get user id
                    select_user_id = f"SELECT user_id FROM users WHERE username = '{input_user}'"
                    users_id = execute_read_query(select_user_id)
                    input_id = users_id[0][0]

                    # login success
                    self.controller.ShowFrame(Menu)
                    self.ClearText()
                    return None
                messagebox.showwarning("Login", "Your password may be incorrect.")
        messagebox.showwarning("Login", "Your username may be incorrect.")

    def ClearText(self):
        self.ent_user.delete(0, tk.END)
        self.ent_pass.delete(0, tk.END)



class Register(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        # Label
        self.lbl_register = tk.Label(self, text="Register",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        self.lbl_user = tk.Label(self, text="User :",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_pass = tk.Label(self, text="Password :",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_repass = tk.Label(self, text="Repeat-Password :",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)

        self.lbl_register.grid(row=0, column=0,
            ipadx=10, ipady=7)
        self.lbl_user.grid(row=2, column=1, sticky="e",
            ipadx=3, ipady=3,
            padx=(0, 5), pady=(100, 10))
        self.lbl_pass.grid(row=3, column=1, sticky="e",
            ipadx=3, ipady=3,
            padx=(0, 5), pady=(0, 10))
        self.lbl_repass.grid(row=4, column=1, sticky="e",
            ipadx=3, ipady=3,
            padx=(0, 5), pady=(0, 10))

        # Entry
        self.ent_user = tk.Entry(self, font=FONT_M)
        self.ent_pass = tk.Entry(self, font=FONT_M, show="*")
        self.ent_repass = tk.Entry(self, font=FONT_M, show="*")

        self.ent_user.grid(row=2, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(0, 5), pady=(100, 10))
        self.ent_pass.grid(row=3, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(0, 5), pady=(0, 10))
        self.ent_repass.grid(row=4, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(0, 5), pady=(0, 10))

        # Button
        self.btn_register = tk.Button(self, text="Submit",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:self.RegisterSystem())
        self.btn_cancel = tk.Button(self, text="Cancel",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:self.ClearText())
        self.btn_back = tk.Button(self, text="<< Back",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(Login))

        self.btn_register.grid(row=5, column=2,
            ipadx=10)
        self.btn_cancel.grid(row=5, column=3,
            ipadx=10)
        self.btn_back.grid(row=1, column=0, sticky="w",
            ipadx=10,
            padx=(10, 0), pady=(10, 0))

    def RegisterSystem(self):
        # get user's input
        input_user = self.ent_user.get()
        input_pwd = self.ent_pass.get()
        input_repwd = self.ent_repass.get()

        # checking status
        check = {"user": False, "password": False}

        # check user's duplication (input vs DB)
        select_username = "SELECT username FROM users"
        users = execute_read_query(select_username)
        username_list = [input_user != user[0] for user in users]
        check["user"] = True if all(username_list) else False

        # check pwd vs repwd
        check["password"] = True if input_pwd == input_repwd else False

        # final check
        if check["user"] == True and check["password"] == True:
            # register success
            insert_users = f"""
            INSERT INTO users (username, password)
            VALUES ('{input_user}', '{input_pwd}');
            """
            execute_query(insert_users)
            self.ClearText()
            messagebox.showinfo("Registration", "Register completed!")
        elif check["user"] == False and check["password"] == True:
            messagebox.showwarning("Registration", "That username is taken.")
        elif check["user"] == True and check["password"] == False:
            messagebox.showwarning("Registration", "Those passwords didn't match.")
        elif check["user"] == False and check["password"] == False:
            messagebox.showwarning("Registration", "That username is taken and those passwords didn't match.")
        else:
            print("Something wrong!")

    def ClearText(self):
        self.ent_user.delete(0, tk.END)
        self.ent_pass.delete(0, tk.END)
        self.ent_repass.delete(0, tk.END)



class Menu(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        # Label
        lbl_menu = tk.Label(self, text="Menu",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        lbl_menu.grid(row=0, column=0,
            ipadx=10, ipady=7)

        # Button
        btn_budget = tk.Button(self, text="Budget",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=8, height=2,
            command=lambda:controller.ShowFrame(BudgetExp))
        btn_summary = tk.Button(self, text="Summary",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=8, height=2,
            command=lambda:controller.ShowFrame(Summary))
        btn_income = tk.Button(self, text="Income",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=8, height=2,
            command=lambda:controller.ShowFrame(IncomeView))

        btn_expense = tk.Button(self, text="Expense",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=8, height=2,
            command=lambda:controller.ShowFrame(ExpenseView))
        btn_subscription = tk.Button(self, text="Subscription",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=8, height=2,
            command=lambda:controller.ShowFrame(SubscriptionView))
        btn_tax = tk.Button(self, text="Tax",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=8, height=2,
            command=lambda:controller.ShowFrame(Tax))

        btn_saving = tk.Button(self, text="Saving",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=8, height=2,
            command=lambda:controller.ShowFrame(SavingView))
        btn_invest = tk.Button(self, text="Invest",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=8, height=2,
            command=lambda:controller.ShowFrame(InvestView))
        btn_export = tk.Button(self, text="Export",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=8, height=2,
            command=lambda:controller.ShowFrame(Export))

        btn_back = tk.Button(self, text="<< Logout",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(Login))

        btn_budget.grid(row=2, column=1,
            ipadx=10,
            padx=(50, 0), pady=(100,0))
        btn_summary.grid(row=2, column=2,
            ipadx=10,
            padx=(15, 0), pady=(100,0))
        btn_income.grid(row=2, column=3,
            ipadx=10,
            padx=(15, 0), pady=(100,0))

        btn_expense.grid(row=3, column=1,
            ipadx=10,
            padx=(50, 0), pady=(15,0))
        btn_subscription.grid(row=3, column=2,
            ipadx=10,
            padx=(15, 0), pady=(15,0))
        btn_tax.grid(row=3, column=3,
            ipadx=10,
            padx=(15, 0), pady=(15,0))

        btn_saving.grid(row=4, column=1,
            ipadx=10,
            padx=(50, 0), pady=(15,0))
        btn_invest.grid(row=4, column=2,
            ipadx=10,
            padx=(15, 0), pady=(15,0))
        btn_export.grid(row=4, column=3,
            ipadx=10,
            padx=(15, 0), pady=(15,0))

        btn_back.grid(row=1, column=0,
            ipadx=10,
            padx=(15, 0), pady=(15, 0))



class BudgetExp(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        ############ Left nav ############
        # Label
        self.lbl_budget = tk.Label(self, text="Budget",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        self.lbl_expense = tk.Label(self, text="Expense",
            bg=COLOR_3, fg=COLOR_1, font=FONT_M)

        self.lbl_budget.grid(row=0, column=0,
            ipadx=10, ipady=7)
        self.lbl_expense.grid(row=2, column=0,
            ipadx=15, ipady=7,
            padx=(15, 0), pady=(20,0))

        # Button
        self.btn_subscription = tk.Button(self, text="Subscription",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=10,
            command=lambda:controller.ShowFrame(BudgetSub))
        self.btn_income = tk.Button(self, text="Income",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=10,
            command=lambda:controller.ShowFrame(BudgetInc))
        self.btn_saving = tk.Button(self, text="Saving",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=10,
            command=lambda:controller.ShowFrame(BudgetSav))
        self.btn_invest = tk.Button(self, text="Invest",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=10,
            command=lambda:controller.ShowFrame(BudgetInv))
        self.btn_back = tk.Button(self, text="<< Menu",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,command=lambda:controller.ShowFrame(Menu))

        self.btn_subscription.grid(row=3, column=0,
            ipady=4,
            padx=(15,0), pady=(5,0))
        self.btn_income.grid(row=4, column=0,
            ipady=4,
            padx=(15,0), pady=(5,0))
        self.btn_saving.grid(row=5, column=0,
            ipady=4,
            padx=(15,0), pady=(5,0))
        self.btn_invest.grid(row=6, column=0,
            ipady=4,
            padx=(15,0), pady=(5,0))

        self.btn_back.grid(row=1, column=0,
        padx=(15,0), pady=(15,0))

        ############ Content############
        # Label
        self.lbl_type = tk.Label(self, text="Type",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_amount = tk.Label(self, text="Amount",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_description = tk.Label(self, text="Description",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_num1 = tk.Label(self, text="1)",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_num2 = tk.Label(self, text="2)",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_num3 = tk.Label(self, text="3)",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)

        self.lbl_type.grid(row=1, column=2)
        self.lbl_amount.grid(row=1, column=3)
        self.lbl_description.grid(row=1, column=4)
        self.lbl_num1.grid(row=2, column=1,
            padx=(20,0))
        self.lbl_num2.grid(row=3, column=1,
            padx=(20,0))
        self.lbl_num3.grid(row=4, column=1,
            padx=(20,0))

        # Entry
        self.ent_type1 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_type2 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_type3 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_amount1 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_amount2 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_amount3 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_description1 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_description2 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_description3 = tk.Entry(self, font=FONT_M,
            width=12)

        self.ent_type1.grid(row=2, column=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_type2.grid(row=3, column=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_type3.grid(row=4, column=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_amount1.grid(row=2, column=3,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_amount2.grid(row=3, column=3,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_amount3.grid(row=4, column=3,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_description1.grid(row=2, column=4,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_description2.grid(row=3, column=4,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_description3.grid(row=4, column=4,
            ipadx=3, ipady=3,
            padx=(5,0))

        # Buttton
        self.btn_submit = tk.Button(self, text="Submit",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:self.SubmitBudgetExp())
        self.btn_cancel = tk.Button(self, text="Cancel",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:self.ClearText())

        self.btn_submit.grid(row=5, column=2)
        self.btn_cancel.grid(row=5, column=3)

        # Table
        columns = ('date', 'type', 'amount', 'description')
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.grid(row=7, column=2, columnspan=3, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=7, column=5, sticky="ns")

        self.tree.heading('date', text='Date', anchor=tk.CENTER)
        self.tree.column('date', width=120, minwidth=120,
            anchor=tk.CENTER, stretch=False)

        self.tree.heading('type', text='Type', anchor=tk.CENTER)
        self.tree.column('type', width=100, minwidth=100,
            anchor=tk.CENTER, stretch=False)

        self.tree.heading('amount', text='Amount', anchor=tk.CENTER)
        self.tree.column('amount', width=100, minwidth=100,
            anchor=tk.CENTER, stretch=False)

        self.tree.heading('description', text='Description', anchor=tk.CENTER)
        self.tree.column('description', width=100, minwidth=100,
            anchor=tk.CENTER, stretch=False)

    def SubmitBudgetExp(self):
        # get user input
        input1 = {}
        input2 = {}
        input3 = {}

        input1["type"] = self.ent_type1.get()
        input2["type"] = self.ent_type2.get()
        input3["type"] = self.ent_type3.get()

        input1["amount"] = self.ent_amount1.get()
        input2["amount"] = self.ent_amount2.get()
        input3["amount"] = self.ent_amount3.get()

        input1["description"] = self.ent_description1.get()
        input2["description"] = self.ent_description2.get()
        input3["description"] = self.ent_description3.get()

        # check user input
        if (input1["type"] and input1["amount"]) or \
            (input2["type"] and input2["amount"]) or \
            (input3["type"] and input3["amount"]):
            # get the current datetime
            CurrentDateTime = datetime.datetime.now()
            CurrentDateTime = CurrentDateTime.strftime("%Y-%m-%d %H:%M:%S")
            # insert data
            if (input1["type"] and input1["amount"]):
                insert_budget1 = f"""
                INSERT INTO budget (user_id, bg_date, bg_exp_type, bg_exp_amt, bg_description)
                VALUES ({input_id}, '{CurrentDateTime}', '{input1["type"]}', {float(input1["amount"])}, '{input1["description"]}');
                """
                execute_query(insert_budget1)
            if (input2["type"] and input2["amount"]):
                insert_budget2 = f"""
                INSERT INTO budget (user_id, bg_date, bg_exp_type, bg_exp_amt, bg_description)
                VALUES ({input_id}, '{CurrentDateTime}', '{input2["type"]}', {float(input2["amount"])}, '{input2["description"]}');
                """
                execute_query(insert_budget2)
            if (input3["type"] and input3["amount"]):
                insert_budget3 = f"""
                INSERT INTO budget (user_id, bg_date, bg_exp_type, bg_exp_amt, bg_description)
                VALUES ({int(input_id)}, '{CurrentDateTime}', '{input3["type"]}', {float(input3["amount"])}, '{input3["description"]}');
                """
                execute_query(insert_budget3)

            # clear entire table
            for i in self.tree.get_children():
                self.tree.delete(i)
            # Show budget data
            self.DisplayTable()
        else:
            messagebox.showwarning("Budget Setup", "Please enter your budget.")

    def ClearText(self):
        self.ent_type1.delete(0, tk.END)
        self.ent_type2.delete(0, tk.END)
        self.ent_type3.delete(0, tk.END)

        self.ent_amount1.delete(0, tk.END)
        self.ent_amount2.delete(0, tk.END)
        self.ent_amount3.delete(0, tk.END)

        self.ent_description1.delete(0, tk.END)
        self.ent_description2.delete(0, tk.END)
        self.ent_description3.delete(0, tk.END)

    def DisplayTable(self):
        # get data from budget
        select_budget = f"""SELECT bg_date, bg_exp_type, bg_exp_amt, bg_description FROM budget
        WHERE user_id = {input_id}
        AND bg_exp_type is not null AND bg_exp_amt is not null
        ORDER BY bg_date DESC LIMIT 100
        """
        budgets = execute_read_query(select_budget)

        # add data to table
        for budget in budgets:
            self.tree.insert('', tk.END, values=budget)

class BudgetSub(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        ############ Left nav ############
        # Label
        self.lbl_budget = tk.Label(self, text="Budget",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        self.lbl_subscription = tk.Label(self, text="Subscription",
            bg=COLOR_3, fg=COLOR_1, font=FONT_M)

        self.lbl_budget.grid(row=0, column=0,
            ipadx=10, ipady=7)
        self.lbl_subscription.grid(row=3, column=0,
            ipadx=5, ipady=7,
            padx=(15, 0), pady=(5,0))

        # Button
        self.btn_expense = tk.Button(self, text="Expense",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=10,
            command=lambda:controller.ShowFrame(BudgetExp))
        self.btn_income = tk.Button(self, text="Income",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=10,
            command=lambda:controller.ShowFrame(BudgetInc))
        self.btn_saving = tk.Button(self, text="Saving",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=10,
            command=lambda:controller.ShowFrame(BudgetSav))
        self.btn_invest = tk.Button(self, text="Invest",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=10,
            command=lambda:controller.ShowFrame(BudgetInv))
        self.btn_back = tk.Button(self, text="<< Menu",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,command=lambda:controller.ShowFrame(Menu))

        self.btn_expense.grid(row=2, column=0,
            ipady=4,
            padx=(15,0), pady=(20,0))
        self.btn_income.grid(row=4, column=0,
            ipady=4,
            padx=(15,0), pady=(5,0))
        self.btn_saving.grid(row=5, column=0,
            ipady=4,
            padx=(15,0), pady=(5,0))
        self.btn_invest.grid(row=6, column=0,
            ipady=4,
            padx=(15,0), pady=(5,0))

        self.btn_back.grid(row=1, column=0,
        padx=(15,0), pady=(15,0))

        ############ Content############
        # Label
        self.lbl_type = tk.Label(self, text="Type",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_amount = tk.Label(self, text="Amount",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_description = tk.Label(self, text="Description",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_num1 = tk.Label(self, text="1)",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_num2 = tk.Label(self, text="2)",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_num3 = tk.Label(self, text="3)",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)

        self.lbl_type.grid(row=1, column=2)
        self.lbl_amount.grid(row=1, column=3)
        self.lbl_description.grid(row=1, column=4)
        self.lbl_num1.grid(row=2, column=1,
            padx=(20,0))
        self.lbl_num2.grid(row=3, column=1,
            padx=(20,0))
        self.lbl_num3.grid(row=4, column=1,
            padx=(20,0))

        # Entry
        self.ent_type1 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_type2 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_type3 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_amount1 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_amount2 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_amount3 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_description1 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_description2 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_description3 = tk.Entry(self, font=FONT_M,
            width=12)

        self.ent_type1.grid(row=2, column=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_type2.grid(row=3, column=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_type3.grid(row=4, column=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_amount1.grid(row=2, column=3,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_amount2.grid(row=3, column=3,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_amount3.grid(row=4, column=3,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_description1.grid(row=2, column=4,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_description2.grid(row=3, column=4,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_description3.grid(row=4, column=4,
            ipadx=3, ipady=3,
            padx=(5,0))

        # Buttton
        self.btn_submit = tk.Button(self, text="Submit",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:self.SubmitBudgetSub())
        self.btn_cancel = tk.Button(self, text="Cancel",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:self.ClearText())

        self.btn_submit.grid(row=5, column=2)
        self.btn_cancel.grid(row=5, column=3)

        # Table
        columns = ('date', 'type', 'amount', 'description')
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.grid(row=7, column=2, columnspan=3, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=7, column=5, sticky="ns")

        self.tree.heading('date', text='Date', anchor=tk.CENTER)
        self.tree.column('date', width=120, minwidth=120,
            anchor=tk.CENTER, stretch=False)

        self.tree.heading('type', text='Type', anchor=tk.CENTER)
        self.tree.column('type', width=100, minwidth=100,
            anchor=tk.CENTER, stretch=False)

        self.tree.heading('amount', text='Amount', anchor=tk.CENTER)
        self.tree.column('amount', width=100, minwidth=100,
            anchor=tk.CENTER, stretch=False)

        self.tree.heading('description', text='Description', anchor=tk.CENTER)
        self.tree.column('description', width=100, minwidth=100,
            anchor=tk.CENTER, stretch=False)

    def SubmitBudgetSub(self):
        # get user input
        input1 = {}
        input2 = {}
        input3 = {}

        input1["type"] = self.ent_type1.get()
        input2["type"] = self.ent_type2.get()
        input3["type"] = self.ent_type3.get()

        input1["amount"] = self.ent_amount1.get()
        input2["amount"] = self.ent_amount2.get()
        input3["amount"] = self.ent_amount3.get()

        input1["description"] = self.ent_description1.get()
        input2["description"] = self.ent_description2.get()
        input3["description"] = self.ent_description3.get()

        # check user input
        if (input1["type"] and input1["amount"]) or \
            (input2["type"] and input2["amount"]) or \
            (input3["type"] and input3["amount"]):
            # get the current datetime
            CurrentDateTime = datetime.datetime.now()
            CurrentDateTime = CurrentDateTime.strftime("%Y-%m-%d %H:%M:%S")
            # insert data
            if (input1["type"] and input1["amount"]):
                insert_budget1 = f"""
                INSERT INTO budget (user_id, bg_date, bg_sub_type, bg_sub_amt, bg_description)
                VALUES ({input_id}, '{CurrentDateTime}', '{input1["type"]}', {float(input1["amount"])}, '{input1["description"]}');
                """
                execute_query(insert_budget1)
            if (input2["type"] and input2["amount"]):
                insert_budget2 = f"""
                INSERT INTO budget (user_id, bg_date, bg_sub_type, bg_sub_amt, bg_description)
                VALUES ({input_id}, '{CurrentDateTime}', '{input2["type"]}', {float(input2["amount"])}, '{input2["description"]}');
                """
                execute_query(insert_budget2)
            if (input3["type"] and input3["amount"]):
                insert_budget3 = f"""
                INSERT INTO budget (user_id, bg_date, bg_sub_type, bg_sub_amt, bg_description)
                VALUES ({int(input_id)}, '{CurrentDateTime}', '{input3["type"]}', {float(input3["amount"])}, '{input3["description"]}');
                """
                execute_query(insert_budget3)

            # clear entire table
            for i in self.tree.get_children():
                self.tree.delete(i)
            # Show budget data
            self.DisplayTable()
        else:
            messagebox.showwarning("Budget Setup", "Please enter your budget.")

    def ClearText(self):
        self.ent_type1.delete(0, tk.END)
        self.ent_type2.delete(0, tk.END)
        self.ent_type3.delete(0, tk.END)

        self.ent_amount1.delete(0, tk.END)
        self.ent_amount2.delete(0, tk.END)
        self.ent_amount3.delete(0, tk.END)

        self.ent_description1.delete(0, tk.END)
        self.ent_description2.delete(0, tk.END)
        self.ent_description3.delete(0, tk.END)

    def DisplayTable(self):
        # get data from budget
        select_budget = f"""SELECT bg_date, bg_sub_type, bg_sub_amt, bg_description FROM budget
        WHERE user_id = {input_id}
        AND bg_sub_type is not null AND bg_sub_amt is not null
        ORDER BY bg_date DESC LIMIT 100
        """
        budgets = execute_read_query(select_budget)

        # add data to table
        for budget in budgets:
            self.tree.insert('', tk.END, values=budget)

class BudgetInc(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        ############ Left nav ############
        # Label
        self.lbl_budget = tk.Label(self, text="Budget",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        self.lbl_income = tk.Label(self, text="Income",
            bg=COLOR_3, fg=COLOR_1, font=FONT_M)

        self.lbl_budget.grid(row=0, column=0,
            ipadx=10, ipady=7)
        self.lbl_income.grid(row=4, column=0,
            ipadx=20, ipady=7,
            padx=(15, 0), pady=(5,0))

        # Button
        self.btn_expense = tk.Button(self, text="Expense",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=10,
            command=lambda:controller.ShowFrame(BudgetExp))
        self.btn_subscription = tk.Button(self, text="Subscription",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=10,
            command=lambda:controller.ShowFrame(BudgetSub))
        self.btn_saving = tk.Button(self, text="Saving",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=10,
            command=lambda:controller.ShowFrame(BudgetSav))
        self.btn_invest = tk.Button(self, text="Invest",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=10,
            command=lambda:controller.ShowFrame(BudgetInv))
        self.btn_back = tk.Button(self, text="<< Menu",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,command=lambda:controller.ShowFrame(Menu))

        self.btn_expense.grid(row=2, column=0,
            ipady=4,
            padx=(15,0), pady=(20,0))
        self.btn_subscription.grid(row=3, column=0,
            ipady=4,
            padx=(15,0), pady=(5,0))
        self.btn_saving.grid(row=5, column=0,
            ipady=4,
            padx=(15,0), pady=(5,0))
        self.btn_invest.grid(row=6, column=0,
            ipady=4,
            padx=(15,0), pady=(5,0))

        self.btn_back.grid(row=1, column=0,
        padx=(15,0), pady=(15,0))

        ############ Content############
        # Label
        self.lbl_type = tk.Label(self, text="Type",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_amount = tk.Label(self, text="Amount",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_description = tk.Label(self, text="Description",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_num1 = tk.Label(self, text="1)",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)

        self.lbl_type.grid(row=1, column=2)
        self.lbl_amount.grid(row=1, column=3)
        self.lbl_description.grid(row=1, column=4)
        self.lbl_num1.grid(row=2, column=1,
            padx=(20,0))

        # Entry
        self.ent_type1 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_amount1 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_description1 = tk.Entry(self, font=FONT_M,
            width=12)

        self.ent_type1.grid(row=2, column=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_amount1.grid(row=2, column=3,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_description1.grid(row=2, column=4,
            ipadx=3, ipady=3,
            padx=(5,0))

        # Buttton
        self.btn_submit = tk.Button(self, text="Submit",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:self.SubmitBudgetInc())
        self.btn_cancel = tk.Button(self, text="Cancel",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:self.ClearText())

        self.btn_submit.grid(row=3, column=2)
        self.btn_cancel.grid(row=3, column=3)

        # Table
        columns = ('date', 'type', 'amount', 'description')
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.grid(row=7, column=2, columnspan=3, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=7, column=5, sticky="ns")

        self.tree.heading('date', text='Date', anchor=tk.CENTER)
        self.tree.column('date', width=120, minwidth=120,
            anchor=tk.CENTER, stretch=False)

        self.tree.heading('type', text='Type', anchor=tk.CENTER)
        self.tree.column('type', width=100, minwidth=100,
            anchor=tk.CENTER, stretch=False)

        self.tree.heading('amount', text='Amount', anchor=tk.CENTER)
        self.tree.column('amount', width=100, minwidth=100,
            anchor=tk.CENTER, stretch=False)

        self.tree.heading('description', text='Description', anchor=tk.CENTER)
        self.tree.column('description', width=100, minwidth=100,
            anchor=tk.CENTER, stretch=False)

    def SubmitBudgetInc(self):
        # get user input
        input1 = {}
        input1["type"] = self.ent_type1.get()
        input1["amount"] = self.ent_amount1.get()
        input1["description"] = self.ent_description1.get()

        # check user input
        if (input1["type"] and input1["amount"]):
            # get the current datetime
            CurrentDateTime = datetime.datetime.now()
            CurrentDateTime = CurrentDateTime.strftime("%Y-%m-%d %H:%M:%S")
            # insert data
            if (input1["type"] and input1["amount"]):
                insert_budget1 = f"""
                INSERT INTO budget (user_id, bg_date, bg_inc_type, bg_inc_amt, bg_description)
                VALUES ({input_id}, '{CurrentDateTime}', '{input1["type"]}', {float(input1["amount"])}, '{input1["description"]}');
                """
                execute_query(insert_budget1)

            # clear entire table
            for i in self.tree.get_children():
                self.tree.delete(i)
            # Show budget data
            self.DisplayTable()
        else:
            messagebox.showwarning("Budget Setup", "Please enter your budget.")

    def ClearText(self):
        self.ent_type1.delete(0, tk.END)
        self.ent_amount1.delete(0, tk.END)
        self.ent_description1.delete(0, tk.END)

    def DisplayTable(self):
        # get data from budget
        select_budget = f"""SELECT bg_date, bg_inc_type, bg_inc_amt, bg_description FROM budget
        WHERE user_id = {input_id}
        AND bg_inc_type is not null AND bg_inc_amt is not null
        ORDER BY bg_date DESC LIMIT 100
        """
        budgets = execute_read_query(select_budget)

        # add data to table
        for budget in budgets:
            self.tree.insert('', tk.END, values=budget)

class BudgetSav(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        ############ Left nav ############
        # Label
        self.lbl_budget = tk.Label(self, text="Budget",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        self.lbl_saving = tk.Label(self, text="Saving",
            bg=COLOR_3, fg=COLOR_1, font=FONT_M)

        self.lbl_budget.grid(row=0, column=0,
            ipadx=10, ipady=7)
        self.lbl_saving.grid(row=5, column=0,
            ipadx=20, ipady=7,
            padx=(15, 0), pady=(5,0))

        # Button
        self.btn_expense = tk.Button(self, text="Expense",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=10,
            command=lambda:controller.ShowFrame(BudgetExp))
        self.btn_subscription = tk.Button(self, text="Subscription",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=10,
            command=lambda:controller.ShowFrame(BudgetSub))
        self.btn_income = tk.Button(self, text="Income",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=10,
            command=lambda:controller.ShowFrame(BudgetInc))
        self.btn_invest = tk.Button(self, text="Invest",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=10,
            command=lambda:controller.ShowFrame(BudgetInv))
        self.btn_back = tk.Button(self, text="<< Menu",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,command=lambda:controller.ShowFrame(Menu))

        self.btn_expense.grid(row=2, column=0,
            ipady=4,
            padx=(15,0), pady=(20,0))
        self.btn_subscription.grid(row=3, column=0,
            ipady=4,
            padx=(15,0), pady=(5,0))
        self.btn_income.grid(row=4, column=0,
            ipady=4,
            padx=(15,0), pady=(5,0))
        self.btn_invest.grid(row=6, column=0,
            ipady=4,
            padx=(15,0), pady=(5,0))

        self.btn_back.grid(row=1, column=0,
            padx=(15,0), pady=(15,0))

        ############ Content############
        # Label
        self.lbl_group = tk.Label(self, text="Group",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_amount = tk.Label(self, text="Amount",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_description = tk.Label(self, text="Description",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_num1 = tk.Label(self, text="1)",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_num2 = tk.Label(self, text="2)",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_num3 = tk.Label(self, text="3)",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)

        self.lbl_group.grid(row=1, column=2)
        self.lbl_amount.grid(row=1, column=3)
        self.lbl_description.grid(row=1, column=4)
        self.lbl_num1.grid(row=2, column=1,
            padx=(20,0))
        self.lbl_num2.grid(row=3, column=1,
            padx=(20,0))
        self.lbl_num3.grid(row=4, column=1,
            padx=(20,0))

        # Entry
        self.ent_group1 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_group2 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_group3 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_amount1 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_amount2 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_amount3 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_description1 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_description2 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_description3 = tk.Entry(self, font=FONT_M,
            width=12)

        self.ent_group1.grid(row=2, column=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_group2.grid(row=3, column=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_group3.grid(row=4, column=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_amount1.grid(row=2, column=3,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_amount2.grid(row=3, column=3,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_amount3.grid(row=4, column=3,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_description1.grid(row=2, column=4,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_description2.grid(row=3, column=4,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_description3.grid(row=4, column=4,
            ipadx=3, ipady=3,
            padx=(5,0))

        # Buttton
        self.btn_submit = tk.Button(self, text="Submit",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:self.SubmitBudgetSav())
        self.btn_cancel = tk.Button(self, text="Cancel",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:self.ClearText())

        self.btn_submit.grid(row=5, column=2)
        self.btn_cancel.grid(row=5, column=3)

        # Table
        columns = ('date', 'group', 'amount', 'description')
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.grid(row=7, column=2, columnspan=3, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=7, column=5, sticky="ns")

        self.tree.heading('date', text='Date', anchor=tk.CENTER)
        self.tree.column('date', width=120, minwidth=120,
            anchor=tk.CENTER, stretch=False)

        self.tree.heading('group', text='Type', anchor=tk.CENTER)
        self.tree.column('group', width=100, minwidth=100,
            anchor=tk.CENTER, stretch=False)

        self.tree.heading('amount', text='Amount', anchor=tk.CENTER)
        self.tree.column('amount', width=100, minwidth=100,
            anchor=tk.CENTER, stretch=False)

        self.tree.heading('description', text='Description', anchor=tk.CENTER)
        self.tree.column('description', width=100, minwidth=100,
            anchor=tk.CENTER, stretch=False)

    def SubmitBudgetSav(self):
        # get user input
        input1 = {}
        input2 = {}
        input3 = {}

        input1["group"] = self.ent_group1.get()
        input2["group"] = self.ent_group2.get()
        input3["group"] = self.ent_group3.get()

        input1["amount"] = self.ent_amount1.get()
        input2["amount"] = self.ent_amount2.get()
        input3["amount"] = self.ent_amount3.get()

        input1["description"] = self.ent_description1.get()
        input2["description"] = self.ent_description2.get()
        input3["description"] = self.ent_description3.get()

        # check user input
        if (input1["group"] and input1["amount"]) or \
            (input2["group"] and input2["amount"]) or \
            (input3["group"] and input3["amount"]):
            # get the current datetime
            CurrentDateTime = datetime.datetime.now()
            CurrentDateTime = CurrentDateTime.strftime("%Y-%m-%d %H:%M:%S")
            # insert data
            if (input1["group"] and input1["amount"]):
                insert_budget1 = f"""
                INSERT INTO budget (user_id, bg_date, bg_sav_group, bg_sav_amt, bg_description)
                VALUES ({input_id}, '{CurrentDateTime}', '{input1["group"]}', {float(input1["amount"])}, '{input1["description"]}');
                """
                execute_query(insert_budget1)
            if (input2["group"] and input2["amount"]):
                insert_budget2 = f"""
                INSERT INTO budget (user_id, bg_date, bg_sav_group, bg_sav_amt, bg_description)
                VALUES ({input_id}, '{CurrentDateTime}', '{input2["group"]}', {float(input2["amount"])}, '{input2["description"]}');
                """
                execute_query(insert_budget2)
            if (input3["group"] and input3["amount"]):
                insert_budget3 = f"""
                INSERT INTO budget (user_id, bg_date, bg_sav_group, bg_sav_amt, bg_description)
                VALUES ({int(input_id)}, '{CurrentDateTime}', '{input3["group"]}', {float(input3["amount"])}, '{input3["description"]}');
                """
                execute_query(insert_budget3)

            # clear entire table
            for i in self.tree.get_children():
                self.tree.delete(i)
            # Show budget data
            self.DisplayTable()
        else:
            messagebox.showwarning("Budget Setup", "Please enter your budget.")

    def ClearText(self):
        self.ent_group1.delete(0, tk.END)
        self.ent_group2.delete(0, tk.END)
        self.ent_group3.delete(0, tk.END)

        self.ent_amount1.delete(0, tk.END)
        self.ent_amount2.delete(0, tk.END)
        self.ent_amount3.delete(0, tk.END)

        self.ent_description1.delete(0, tk.END)
        self.ent_description2.delete(0, tk.END)
        self.ent_description3.delete(0, tk.END)

    def DisplayTable(self):
        # get data from budget
        select_budget = f"""SELECT bg_date, bg_sav_group, bg_sav_amt, bg_description FROM budget
        WHERE user_id = {input_id}
        AND bg_sav_group is not null AND bg_sav_amt is not null
        ORDER BY bg_date DESC LIMIT 100
        """
        budgets = execute_read_query(select_budget)

        # add data to table
        for budget in budgets:
            self.tree.insert('', tk.END, values=budget)

class BudgetInv(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        ############ Left nav ############
        # Label
        self.lbl_budget = tk.Label(self, text="Budget",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        self.lbl_invest = tk.Label(self, text="Invest",
            bg=COLOR_3, fg=COLOR_1, font=FONT_M)

        self.lbl_budget.grid(row=0, column=0,
            ipadx=10, ipady=7)
        self.lbl_invest.grid(row=6, column=0,
            ipadx=30, ipady=7,
            padx=(15, 0), pady=(5,0))

        # Button
        self.btn_expense = tk.Button(self, text="Expense",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=10,
            command=lambda:controller.ShowFrame(BudgetExp))
        self.btn_subscription = tk.Button(self, text="Subscription",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=10,
            command=lambda:controller.ShowFrame(BudgetSub))
        self.btn_income = tk.Button(self, text="Income",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=10,
            command=lambda:controller.ShowFrame(BudgetInc))
        self.btn_saving = tk.Button(self, text="Saving",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=10,
            command=lambda:controller.ShowFrame(BudgetSav))
        self.btn_back = tk.Button(self, text="<< Menu",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(Menu))

        self.btn_expense.grid(row=2, column=0,
            ipady=4,
            padx=(15,0), pady=(20,0))
        self.btn_subscription.grid(row=3, column=0,
            ipady=4,
            padx=(15,0), pady=(5,0))
        self.btn_income.grid(row=4, column=0,
            ipady=4,
            padx=(15,0), pady=(5,0))
        self.btn_saving.grid(row=5, column=0,
            ipady=4,
            padx=(15,0), pady=(5,0))

        self.btn_back.grid(row=1, column=0,
            padx=(15,0), pady=(15,0))

        ############ Content############
        # Label
        self.lbl_purpose = tk.Label(self, text="Purpose",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_amount = tk.Label(self, text="Amount",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_description = tk.Label(self, text="Description",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_num1 = tk.Label(self, text="1)",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_num2 = tk.Label(self, text="2)",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_num3 = tk.Label(self, text="3)",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)

        self.lbl_purpose.grid(row=1, column=2)
        self.lbl_amount.grid(row=1, column=3)
        self.lbl_description.grid(row=1, column=4)
        self.lbl_num1.grid(row=2, column=1,
            padx=(20,0))
        self.lbl_num2.grid(row=3, column=1,
            padx=(20,0))
        self.lbl_num3.grid(row=4, column=1,
            padx=(20,0))

        # Entry
        self.ent_purpose1 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_purpose2 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_purpose3 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_amount1 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_amount2 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_amount3 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_description1 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_description2 = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_description3 = tk.Entry(self, font=FONT_M,
            width=12)

        self.ent_purpose1.grid(row=2, column=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_purpose2.grid(row=3, column=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_purpose3.grid(row=4, column=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_amount1.grid(row=2, column=3,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_amount2.grid(row=3, column=3,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_amount3.grid(row=4, column=3,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_description1.grid(row=2, column=4,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_description2.grid(row=3, column=4,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_description3.grid(row=4, column=4,
            ipadx=3, ipady=3,
            padx=(5,0))

        # Buttton
        self.btn_submit = tk.Button(self, text="Submit",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:self.SubmitBudgetInv())
        self.btn_cancel = tk.Button(self, text="Cancel",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:self.ClearText())

        self.btn_submit.grid(row=5, column=2)
        self.btn_cancel.grid(row=5, column=3)

        # Table
        columns = ('date', 'purpose', 'amount', 'description')
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.grid(row=7, column=2, columnspan=3, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=7, column=5, sticky="ns")

        self.tree.heading('date', text='Date', anchor=tk.CENTER)
        self.tree.column('date', width=120, minwidth=120,
            anchor=tk.CENTER, stretch=False)

        self.tree.heading('purpose', text='Type', anchor=tk.CENTER)
        self.tree.column('purpose', width=100, minwidth=100,
            anchor=tk.CENTER, stretch=False)

        self.tree.heading('amount', text='Amount', anchor=tk.CENTER)
        self.tree.column('amount', width=100, minwidth=100,
            anchor=tk.CENTER, stretch=False)

        self.tree.heading('description', text='Description', anchor=tk.CENTER)
        self.tree.column('description', width=100, minwidth=100,
            anchor=tk.CENTER, stretch=False)

    def SubmitBudgetInv(self):
        # get user input
        input1 = {}
        input2 = {}
        input3 = {}

        input1["purpose"] = self.ent_purpose1.get()
        input2["purpose"] = self.ent_purpose2.get()
        input3["purpose"] = self.ent_purpose3.get()

        input1["amount"] = self.ent_amount1.get()
        input2["amount"] = self.ent_amount2.get()
        input3["amount"] = self.ent_amount3.get()

        input1["description"] = self.ent_description1.get()
        input2["description"] = self.ent_description2.get()
        input3["description"] = self.ent_description3.get()

        # check user input
        if (input1["purpose"] and input1["amount"]) or \
            (input2["purpose"] and input2["amount"]) or \
            (input3["purpose"] and input3["amount"]):
            # get the current datetime
            CurrentDateTime = datetime.datetime.now()
            CurrentDateTime = CurrentDateTime.strftime("%Y-%m-%d %H:%M:%S")
            # insert data
            if (input1["purpose"] and input1["amount"]):
                insert_budget1 = f"""
                INSERT INTO budget (user_id, bg_date, bg_inv_purpose, bg_inv_amt, bg_description)
                VALUES ({input_id}, '{CurrentDateTime}', '{input1["purpose"]}', {float(input1["amount"])}, '{input1["description"]}');
                """
                execute_query(insert_budget1)
            if (input2["purpose"] and input2["amount"]):
                insert_budget2 = f"""
                INSERT INTO budget (user_id, bg_date, bg_inv_purpose, bg_inv_amt, bg_description)
                VALUES ({input_id}, '{CurrentDateTime}', '{input2["purpose"]}', {float(input2["amount"])}, '{input2["description"]}');
                """
                execute_query(insert_budget2)
            if (input3["purpose"] and input3["amount"]):
                insert_budget3 = f"""
                INSERT INTO budget (user_id, bg_date, bg_inv_purpose, bg_inv_amt, bg_description)
                VALUES ({int(input_id)}, '{CurrentDateTime}', '{input3["purpose"]}', {float(input3["amount"])}, '{input3["description"]}');
                """
                execute_query(insert_budget3)

            # clear entire table
            for i in self.tree.get_children():
                self.tree.delete(i)
            # Show budget data
            self.DisplayTable()
        else:
            messagebox.showwarning("Budget Setup", "Please enter your budget.")

    def ClearText(self):
        self.ent_purpose1.delete(0, tk.END)
        self.ent_purpose2.delete(0, tk.END)
        self.ent_purpose3.delete(0, tk.END)

        self.ent_amount1.delete(0, tk.END)
        self.ent_amount2.delete(0, tk.END)
        self.ent_amount3.delete(0, tk.END)

        self.ent_description1.delete(0, tk.END)
        self.ent_description2.delete(0, tk.END)
        self.ent_description3.delete(0, tk.END)

    def DisplayTable(self):
        # get data from budget
        select_budget = f"""SELECT bg_date, bg_inv_purpose, bg_inv_amt, bg_description FROM budget
        WHERE user_id = {input_id}
        AND bg_inv_purpose is not null AND bg_inv_amt is not null
        ORDER BY bg_date DESC LIMIT 100
        """
        budgets = execute_read_query(select_budget)

        # add data to table
        for budget in budgets:
            self.tree.insert('', tk.END, values=budget)



class Summary(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        # Label
        lbl_summary = tk.Label(self, text="Summary",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        lbl_date = tk.Label(self, text="Date",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_tide = tk.Label(self, text="~",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_periodicity = tk.Label(self, text="Periodicity",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)

        lbl_summary.grid(row=0, column=0,
            ipadx=10, ipady=7)
        lbl_date.grid(row=2, column=1, sticky="e")
        lbl_tide.grid(row=2, column=3,
            padx=(5,0))
        lbl_periodicity.grid(row=3, column=1, sticky="e")

        # Entry
        ent_strt_dt = tk.Entry(self, font=FONT_M,
            width=12)
        ent_end_dt = tk.Entry(self, font=FONT_M,
            width=12)

        ent_strt_dt.grid(row=2, column=2,
            ipadx=3, ipady=3,
            padx=(15,0))
        ent_end_dt.grid(row=2, column=4,
            ipadx=3, ipady=3,
            padx=(5,0))

        # Button
        btn_submit = tk.Button(self, text="Submit",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")
        btn_cancel = tk.Button(self, text="Cancel",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")
        btn_back = tk.Button(self, text="<< Menu",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(Menu))

        btn_submit.grid(row=2, column=5,
            padx=(5,0))
        btn_cancel.grid(row=3, column=5,
            padx=(5,0))
        btn_back.grid(row=1, column=0,
            padx=(15,0), pady=(15,0))

        # Checkbox
        var_expense = tk.IntVar()
        var_subscription = tk.IntVar()
        var_saving = tk.IntVar()
        var_invest = tk.IntVar()
        var_income = tk.IntVar()
        var_budget = tk.IntVar()

        chk_expense = tk.Checkbutton(self, text="Expense",
                                justify="left", variable=var_expense,
                                bg=COLOR_3, fg=COLOR_1, font=FONT_M)
        chk_subscription = tk.Checkbutton(self, text="Subscription",
                                justify="left", variable=var_subscription,
                                bg=COLOR_3, fg=COLOR_1, font=FONT_M)
        chk_saving = tk.Checkbutton(self, text="Saving",
                                justify="left", variable=var_saving,
                                bg=COLOR_3, fg=COLOR_1, font=FONT_M)
        chk_invest = tk.Checkbutton(self, text="Invest",
                                justify="left", variable=var_invest,
                                bg=COLOR_3, fg=COLOR_1, font=FONT_M)
        chk_income = tk.Checkbutton(self, text="Income",
                                justify="left", variable=var_income,
                                bg=COLOR_3, fg=COLOR_1, font=FONT_M)
        chk_budget = tk.Checkbutton(self, text="Budget",
                                justify="left", variable=var_budget,
                                bg=COLOR_3, fg=COLOR_1, font=FONT_M)

        chk_expense.grid(row=2, column=0, sticky="w",
            padx=(30,0), pady=(20,0))
        chk_subscription.grid(row=3, column=0, sticky="w",
            padx=(30,0), pady=(5,0))
        chk_saving.grid(row=4, column=0, sticky="w",
            padx=(30,0), pady=(5,0))
        chk_invest.grid(row=5, column=0, sticky="w",
            padx=(30,0), pady=(5,0))
        chk_income.grid(row=6, column=0, sticky="w",
            padx=(30,0), pady=(5,0))
        chk_budget.grid(row=7, column=0, sticky="w",
            padx=(30,0), pady=(5,0))

        # Optionmenu
        OPTIONS = ["Daily", "Monthly", "Yearly"]
        var_default = tk.StringVar()
        var_default.set(OPTIONS[1])

        opt_periodicity = tk.OptionMenu(self, var_default, *OPTIONS)
        opt_periodicity.config(bg=COLOR_3, fg=COLOR_1, font=FONT_M)
        opt_periodicity.grid(row=3, column=2)

        # Graph



class ExpenseView(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        ############ Left nav ############
        # Label
        self.lbl_expense = tk.Label(self, text="Expense",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        self.lbl_view = tk.Label(self, text="View",
            bg=COLOR_3, fg=COLOR_1, font=FONT_M)

        self.lbl_expense.grid(row=0, column=0,
            ipadx=10, ipady=7)
        self.lbl_view.grid(row=2, column=0,
            ipadx=15, ipady=5,
            padx=(15, 0), pady=(15,0))

        # Button
        self.btn_add = tk.Button(self, text="Add",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(ExpenseAdd))
        self.btn_update = tk.Button(self, text="Update",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(ExpenseUpdate))
        self.btn_delete = tk.Button(self, text="Delete",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(ExpenseDelete))

        self.btn_back = tk.Button(self, text="<< Menu",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,command=lambda:controller.ShowFrame(Menu))

        self.btn_add.grid(row=3, column=0,
            padx=(15,0), pady=(5,0))
        self.btn_update.grid(row=4, column=0,
            padx=(15,0), pady=(5,0))
        self.btn_delete.grid(row=5, column=0,
            padx=(15,0), pady=(5,0))

        self.btn_back.grid(row=1, column=0,
            padx=(15,0), pady=(15,0))

        ############ Content############
        # Label
        self.lbl_date = tk.Label(self, text="Date",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_tide = tk.Label(self, text="~",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)

        self.lbl_date.grid(row=2, column=1)
        self.lbl_tide.grid(row=2, column=3,
            padx=(5,0))

        # Entry
        self.ent_strt_dt = tk.Entry(self, font=FONT_M,
            width=12)
        self.ent_end_dt = tk.Entry(self, font=FONT_M,
            width=12)

        self.ent_strt_dt.grid(row=2, column=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_end_dt.grid(row=2, column=4,
            ipadx=3, ipady=3,
            padx=(5,0))

        self.ent_strt_dt.insert(0, datetime.datetime.now().strftime("%Y-%m-%d")) # initial start date
        self.ent_end_dt.insert(0, datetime.datetime.now().strftime("%Y-%m-%d")) # initial end date

        # Buttton
        self.btn_submit = tk.Button(self, text="Submit",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:self.SubmitExpenseView())
        self.btn_submit.grid(row=2, column=5,
            padx=(5,0))

        # Table
        columns = ('date', 'type', 'amount', 'description')
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.grid(row=6, column=1, columnspan=5, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=6, column=6, sticky="ns")

        self.tree.heading('date', text='Date', anchor=tk.CENTER)
        self.tree.column('date', width=120, minwidth=120,
            anchor=tk.CENTER, stretch=False)

        self.tree.heading('type', text='Type', anchor=tk.CENTER)
        self.tree.column('type', width=100, minwidth=100,
            anchor=tk.CENTER, stretch=False)

        self.tree.heading('amount', text='Amount', anchor=tk.CENTER)
        self.tree.column('amount', width=100, minwidth=100,
            anchor=tk.CENTER, stretch=False)

        self.tree.heading('description', text='Description', anchor=tk.CENTER)
        self.tree.column('description', width=100, minwidth=100,
            anchor=tk.CENTER, stretch=False)

    def SubmitExpenseView(self):
        # get user input
        input1 = {}
        input1["start_date"] = self.ent_strt_dt.get()
        input1["end_date"] = self.ent_end_dt.get()

        # check user input
        if input1["start_date"] and input1["end_date"] and \
            re.findall("^\d{4}-\d{2}-\d{2}$", input1["start_date"]) and \
            re.findall("^\d{4}-\d{2}-\d{2}$", input1["end_date"]):

            # clear entire table
            for i in self.tree.get_children():
                self.tree.delete(i)

            # Show expense data
            self.DisplayTable(input1["start_date"], input1["end_date"])
        else:
            messagebox.showwarning("Expense View", "Please enter date as yyyy-mm-dd.")

    def DisplayTable(self, strt_dt, end_dt):
        # get data from budget
        select_expense = f"""SELECT exp_date, exp_type, exp_amt, exp_description FROM expense
        WHERE user_id = {input_id}
        AND DATE(SUBSTR(exp_date, 1, 10)) BETWEEN DATE('{strt_dt}') AND DATE('{end_dt}')
        ORDER BY exp_date DESC LIMIT 100
        """
        expenses = execute_read_query(select_expense)

        # add data to table
        for exp in expenses:
            self.tree.insert('', tk.END, values=exp)

class ExpenseAdd(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        ############ Left nav ############
        # Label
        self.lbl_expense = tk.Label(self, text="Expense",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        self.lbl_add = tk.Label(self, text="Add",
            bg=COLOR_3, fg=COLOR_1, font=FONT_M)

        self.lbl_expense.grid(row=0, column=0,
            ipadx=10, ipady=7)
        self.lbl_add.grid(row=3, column=0,
            ipadx=18, ipady=4,
            padx=(15, 0), pady=(5,0))

        # Button
        self.btn_view = tk.Button(self, text="View",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(ExpenseView))
        self.btn_update = tk.Button(self, text="Update",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(ExpenseUpdate))
        self.btn_delete = tk.Button(self, text="Delete",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(ExpenseDelete))

        self.btn_back = tk.Button(self, text="<< Menu",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,command=lambda:controller.ShowFrame(Menu))

        self.btn_view.grid(row=2, column=0,
            padx=(15,0), pady=(15,0))
        self.btn_update.grid(row=4, column=0,
            padx=(15,0), pady=(5,0))
        self.btn_delete.grid(row=5, column=0,
            padx=(15,0), pady=(5,0))

        self.btn_back.grid(row=1, column=0,
            padx=(15,0), pady=(15,0))

        ############ Content############
        # Label
        self.lbl_date = tk.Label(self, text="Date",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_type = tk.Label(self, text="Type",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_amount = tk.Label(self, text="Amount",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        self.lbl_description = tk.Label(self, text="Description",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)

        self.lbl_date.grid(row=2, column=1, sticky="e")
        self.lbl_type.grid(row=3, column=1, sticky="e")
        self.lbl_amount.grid(row=4, column=1, sticky="e")
        self.lbl_description.grid(row=5, column=1, sticky="e")

        # Entry
        self.ent_date = tk.Entry(self, font=FONT_M)
        self.ent_type = tk.Entry(self, font=FONT_M)
        self.ent_amount = tk.Entry(self, font=FONT_M)
        self.ent_description = tk.Entry(self, font=FONT_M)

        self.ent_date.grid(row=2, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_type.grid(row=3, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_amount.grid(row=4, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        self.ent_description.grid(row=5, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))

        self.ent_date.insert(0, datetime.datetime.now().strftime("%Y-%m-%d")) # initial date

        # Buttton
        self.btn_submit = tk.Button(self, text="Submit",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:self.SubmitExpenseAdd())
        self.btn_cancel = tk.Button(self, text="Cancel",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:self.ClearText())

        self.btn_submit.grid(row=6, column=2,
            pady=(5,0))
        self.btn_cancel.grid(row=6, column=3,
            pady=(5,0))

    def SubmitExpenseAdd(self):
        pass
        # get user input
        input1 = {}
        input1["date"] = self.ent_date.get()
        input1["type"] = self.ent_type.get()
        input1["amount"] = self.ent_amount.get()
        input1["description"] = self.ent_description.get()

        # check user input and insert data
        if input1["date"] and input1["type"] and input1["amount"] and \
            re.findall("^\d{4}-\d{2}-\d{2}$", input1["date"]):
            input1["date"] = input1["date"] + " " + datetime.datetime.now().strftime("%H:%M:%S") # add current time
            insert_exp = f"""
            INSERT INTO expense (user_id, exp_date, exp_type, exp_amt, exp_description)
            VALUES ({input_id}, '{input1["date"]}', '{input1["type"]}', {float(input1["amount"])}, '{input1["description"]}');
            """
            execute_query(insert_exp)
            messagebox.showinfo("Expense Add", "Your expense added.")
        else:
            messagebox.showwarning("Expense Add", "Please enter date as yyyy-mm-dd, type and amount.")

    def ClearText(self):
        self.ent_date.delete(0, tk.END)
        self.ent_type.delete(0, tk.END)
        self.ent_amount.delete(0, tk.END)
        self.ent_description.delete(0, tk.END)
        self.ent_date.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))

class ExpenseUpdate(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        ############ Left nav ############
        # Label
        lbl_expense = tk.Label(self, text="Expense",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        lbl_update = tk.Label(self, text="Update",
            bg=COLOR_3, fg=COLOR_1, font=FONT_M)

        lbl_expense.grid(row=0, column=0,
            ipadx=10, ipady=7)
        lbl_update.grid(row=4, column=0,
            ipadx=8, ipady=4,
            padx=(15, 0), pady=(5,0))

        # Button
        btn_view = tk.Button(self, text="View",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(ExpenseView))
        btn_add = tk.Button(self, text="Add",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(ExpenseAdd))
        btn_delete = tk.Button(self, text="Delete",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(ExpenseDelete))

        btn_back = tk.Button(self, text="<< Menu",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,command=lambda:controller.ShowFrame(Menu))

        btn_view.grid(row=2, column=0,
            padx=(15,0), pady=(15,0))
        btn_add.grid(row=3, column=0,
            padx=(15,0), pady=(5,0))
        btn_delete.grid(row=5, column=0,
            padx=(15,0), pady=(5,0))

        btn_back.grid(row=1, column=0,
        padx=(15,0), pady=(15,0))

        ############ Content############
        # Label
        lbl_id = tk.Label(self, text="ID",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_date = tk.Label(self, text="Date",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_type = tk.Label(self, text="Type",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_amount = tk.Label(self, text="Amount",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_description = tk.Label(self, text="Description",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)

        lbl_id.grid(row=2, column=1, sticky="e")
        lbl_date.grid(row=3, column=1, sticky="e")
        lbl_type.grid(row=4, column=1, sticky="e")
        lbl_amount.grid(row=5, column=1, sticky="e")
        lbl_description.grid(row=6, column=1, sticky="e")

        # Entry
        ent_id = tk.Entry(self, font=FONT_M)
        ent_date = tk.Entry(self, font=FONT_M)
        ent_type = tk.Entry(self, font=FONT_M)
        ent_amount = tk.Entry(self, font=FONT_M)
        ent_description = tk.Entry(self, font=FONT_M)

        ent_id.grid(row=2, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_date.grid(row=3, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_type.grid(row=4, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_amount.grid(row=5, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_description.grid(row=6, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))

        # Buttton
        btn_submit = tk.Button(self, text="Submit",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")
        btn_cancel = tk.Button(self, text="Cancel",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")

        btn_submit.grid(row=7, column=2,
            pady=(5,0))
        btn_cancel.grid(row=7, column=3,
            pady=(5,0))

class ExpenseDelete(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        ############ Left nav ############
        # Label
        lbl_expense = tk.Label(self, text="Expense",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        lbl_delete = tk.Label(self, text="Delete",
            bg=COLOR_3, fg=COLOR_1, font=FONT_M)

        lbl_expense.grid(row=0, column=0,
            ipadx=10, ipady=7)
        lbl_delete.grid(row=5, column=0,
            ipadx=10, ipady=4,
            padx=(15, 0), pady=(5,0))

        # Button
        btn_view = tk.Button(self, text="View",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(ExpenseView))
        btn_add = tk.Button(self, text="Add",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(ExpenseAdd))
        btn_update = tk.Button(self, text="Update",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(ExpenseUpdate))

        btn_back = tk.Button(self, text="<< Menu",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,command=lambda:controller.ShowFrame(Menu))

        btn_view.grid(row=2, column=0,
            padx=(15,0), pady=(15,0))
        btn_add.grid(row=3, column=0,
            padx=(15,0), pady=(5,0))
        btn_update.grid(row=4, column=0,
            padx=(15,0), pady=(5,0))

        btn_back.grid(row=1, column=0,
        padx=(15,0), pady=(15,0))

        ############ Content############
        # Label
        lbl_id = tk.Label(self, text="ID",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_id.grid(row=2, column=1, sticky="e")

        # Entry
        ent_id = tk.Entry(self, font=FONT_M)

        ent_id.grid(row=2, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))

        # Buttton
        btn_submit = tk.Button(self, text="Submit",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")
        btn_cancel = tk.Button(self, text="Cancel",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")

        btn_submit.grid(row=3, column=2,
            pady=(5,0))
        btn_cancel.grid(row=3, column=3,
            pady=(5,0))



class SubscriptionView(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        ############ Left nav ############
        # Label
        lbl_subscription = tk.Label(self, text="Subscription",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        lbl_view = tk.Label(self, text="View",
            bg=COLOR_3, fg=COLOR_1, font=FONT_M)

        lbl_subscription.grid(row=0, column=0,
            ipadx=10, ipady=7)
        lbl_view.grid(row=2, column=0,
            ipadx=15, ipady=5,
            padx=(15, 0), pady=(15,0))

        # Button
        btn_add = tk.Button(self, text="Add",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(SubscriptionAdd))
        btn_update = tk.Button(self, text="Update",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(SubscriptionUpdate))
        btn_delete = tk.Button(self, text="Delete",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(SubscriptionDelete))

        btn_back = tk.Button(self, text="<< Menu",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,command=lambda:controller.ShowFrame(Menu))

        btn_add.grid(row=3, column=0,
            padx=(15,0), pady=(5,0))
        btn_update.grid(row=4, column=0,
            padx=(15,0), pady=(5,0))
        btn_delete.grid(row=5, column=0,
            padx=(15,0), pady=(5,0))

        btn_back.grid(row=1, column=0,
        padx=(15,0), pady=(15,0))

        ############ Content############
        # Label
        lbl_date = tk.Label(self, text="Date",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_tide = tk.Label(self, text="~",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)

        lbl_date.grid(row=2, column=1)
        lbl_tide.grid(row=2, column=3,
            padx=(5,0))

        # Entry
        ent_strt_dt = tk.Entry(self, font=FONT_M,
            width=12)
        ent_end_dt = tk.Entry(self, font=FONT_M,
            width=12)

        ent_strt_dt.grid(row=2, column=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_end_dt.grid(row=2, column=4,
            ipadx=3, ipady=3,
            padx=(5,0))

        # Buttton
        btn_submit = tk.Button(self, text="Submit",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")
        btn_submit.grid(row=2, column=5,
            padx=(5,0))

        # Table: TreeView

class SubscriptionAdd(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        ############ Left nav ############
        # Label
        lbl_subscription = tk.Label(self, text="Subscription",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        lbl_add = tk.Label(self, text="Add",
            bg=COLOR_3, fg=COLOR_1, font=FONT_M)

        lbl_subscription.grid(row=0, column=0,
            ipadx=10, ipady=7)
        lbl_add.grid(row=3, column=0,
            ipadx=18, ipady=4,
            padx=(15, 0), pady=(5,0))

        # Button
        btn_view = tk.Button(self, text="View",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(SubscriptionView))
        btn_update = tk.Button(self, text="Update",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(SubscriptionUpdate))
        btn_delete = tk.Button(self, text="Delete",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(SubscriptionDelete))

        btn_back = tk.Button(self, text="<< Menu",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,command=lambda:controller.ShowFrame(Menu))

        btn_view.grid(row=2, column=0,
            padx=(15,0), pady=(15,0))
        btn_update.grid(row=4, column=0,
            padx=(15,0), pady=(5,0))
        btn_delete.grid(row=5, column=0,
            padx=(15,0), pady=(5,0))

        btn_back.grid(row=1, column=0,
        padx=(15,0), pady=(15,0))

        ############ Content############
        # Label
        lbl_date = tk.Label(self, text="Date",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_type = tk.Label(self, text="Type",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_amount = tk.Label(self, text="Amount",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_description = tk.Label(self, text="Description",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)

        lbl_date.grid(row=2, column=1, sticky="e")
        lbl_type.grid(row=3, column=1, sticky="e")
        lbl_amount.grid(row=4, column=1, sticky="e")
        lbl_description.grid(row=5, column=1, sticky="e")

        # Entry
        ent_date = tk.Entry(self, font=FONT_M)
        ent_type = tk.Entry(self, font=FONT_M)
        ent_amount = tk.Entry(self, font=FONT_M)
        ent_description = tk.Entry(self, font=FONT_M)

        ent_date.grid(row=2, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_type.grid(row=3, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_amount.grid(row=4, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_description.grid(row=5, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))

        # Buttton
        btn_submit = tk.Button(self, text="Submit",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")
        btn_cancel = tk.Button(self, text="Cancel",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")

        btn_submit.grid(row=6, column=2,
            pady=(5,0))
        btn_cancel.grid(row=6, column=3,
            pady=(5,0))

class SubscriptionUpdate(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        ############ Left nav ############
        # Label
        lbl_subscription = tk.Label(self, text="Subscription",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        lbl_update = tk.Label(self, text="Update",
            bg=COLOR_3, fg=COLOR_1, font=FONT_M)

        lbl_subscription.grid(row=0, column=0,
            ipadx=10, ipady=7)
        lbl_update.grid(row=4, column=0,
            ipadx=8, ipady=4,
            padx=(15, 0), pady=(5,0))

        # Button
        btn_view = tk.Button(self, text="View",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(SubscriptionView))
        btn_add = tk.Button(self, text="Add",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(SubscriptionAdd))
        btn_delete = tk.Button(self, text="Delete",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(SubscriptionDelete))

        btn_back = tk.Button(self, text="<< Menu",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,command=lambda:controller.ShowFrame(Menu))

        btn_view.grid(row=2, column=0,
            padx=(15,0), pady=(15,0))
        btn_add.grid(row=3, column=0,
            padx=(15,0), pady=(5,0))
        btn_delete.grid(row=5, column=0,
            padx=(15,0), pady=(5,0))

        btn_back.grid(row=1, column=0,
        padx=(15,0), pady=(15,0))

        ############ Content############
        # Label
        lbl_id = tk.Label(self, text="ID",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_date = tk.Label(self, text="Date",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_type = tk.Label(self, text="Type",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_amount = tk.Label(self, text="Amount",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_description = tk.Label(self, text="Description",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)

        lbl_id.grid(row=2, column=1, sticky="e")
        lbl_date.grid(row=3, column=1, sticky="e")
        lbl_type.grid(row=4, column=1, sticky="e")
        lbl_amount.grid(row=5, column=1, sticky="e")
        lbl_description.grid(row=6, column=1, sticky="e")

        # Entry
        ent_id = tk.Entry(self, font=FONT_M)
        ent_date = tk.Entry(self, font=FONT_M)
        ent_type = tk.Entry(self, font=FONT_M)
        ent_amount = tk.Entry(self, font=FONT_M)
        ent_description = tk.Entry(self, font=FONT_M)

        ent_id.grid(row=2, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_date.grid(row=3, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_type.grid(row=4, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_amount.grid(row=5, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_description.grid(row=6, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))

        # Buttton
        btn_submit = tk.Button(self, text="Submit",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")
        btn_cancel = tk.Button(self, text="Cancel",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")

        btn_submit.grid(row=7, column=2,
            pady=(5,0))
        btn_cancel.grid(row=7, column=3,
            pady=(5,0))

class SubscriptionDelete(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        ############ Left nav ############
        # Label
        lbl_subscription = tk.Label(self, text="Subscription",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        lbl_delete = tk.Label(self, text="Delete",
            bg=COLOR_3, fg=COLOR_1, font=FONT_M)

        lbl_subscription.grid(row=0, column=0,
            ipadx=10, ipady=7)
        lbl_delete.grid(row=5, column=0,
            ipadx=10, ipady=4,
            padx=(15, 0), pady=(5,0))

        # Button
        btn_view = tk.Button(self, text="View",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(SubscriptionView))
        btn_add = tk.Button(self, text="Add",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(SubscriptionAdd))
        btn_update = tk.Button(self, text="Update",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(SubscriptionUpdate))

        btn_back = tk.Button(self, text="<< Menu",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,command=lambda:controller.ShowFrame(Menu))

        btn_view.grid(row=2, column=0,
            padx=(15,0), pady=(15,0))
        btn_add.grid(row=3, column=0,
            padx=(15,0), pady=(5,0))
        btn_update.grid(row=4, column=0,
            padx=(15,0), pady=(5,0))

        btn_back.grid(row=1, column=0,
        padx=(15,0), pady=(15,0))

        ############ Content############
        # Label
        lbl_id = tk.Label(self, text="ID",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_id.grid(row=2, column=1, sticky="e")

        # Entry
        ent_id = tk.Entry(self, font=FONT_M)

        ent_id.grid(row=2, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))

        # Buttton
        btn_submit = tk.Button(self, text="Submit",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")
        btn_cancel = tk.Button(self, text="Cancel",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")

        btn_submit.grid(row=3, column=2,
            pady=(5,0))
        btn_cancel.grid(row=3, column=3,
            pady=(5,0))



class Tax(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)



class IncomeView(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        ############ Left nav ############
        # Label
        lbl_income = tk.Label(self, text="Income",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        lbl_view = tk.Label(self, text="View",
            bg=COLOR_3, fg=COLOR_1, font=FONT_M)

        lbl_income.grid(row=0, column=0,
            ipadx=10, ipady=7)
        lbl_view.grid(row=2, column=0,
            ipadx=15, ipady=5,
            padx=(15, 0), pady=(15,0))

        # Button
        btn_add = tk.Button(self, text="Add",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(IncomeAdd))
        btn_update = tk.Button(self, text="Update",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(IncomeUpdate))
        btn_delete = tk.Button(self, text="Delete",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(IncomeDelete))

        btn_back = tk.Button(self, text="<< Menu",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,command=lambda:controller.ShowFrame(Menu))

        btn_add.grid(row=3, column=0,
            padx=(15,0), pady=(5,0))
        btn_update.grid(row=4, column=0,
            padx=(15,0), pady=(5,0))
        btn_delete.grid(row=5, column=0,
            padx=(15,0), pady=(5,0))

        btn_back.grid(row=1, column=0,
        padx=(15,0), pady=(15,0))

        ############ Content############
        # Label
        lbl_date = tk.Label(self, text="Date",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_tide = tk.Label(self, text="~",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)

        lbl_date.grid(row=2, column=1)
        lbl_tide.grid(row=2, column=3,
            padx=(5,0))

        # Entry
        ent_strt_dt = tk.Entry(self, font=FONT_M,
            width=12)
        ent_end_dt = tk.Entry(self, font=FONT_M,
            width=12)

        ent_strt_dt.grid(row=2, column=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_end_dt.grid(row=2, column=4,
            ipadx=3, ipady=3,
            padx=(5,0))

        # Buttton
        btn_submit = tk.Button(self, text="Submit",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")
        btn_submit.grid(row=2, column=5,
            padx=(5,0))

        # Table: TreeView

class IncomeAdd(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        ############ Left nav ############
        # Label
        lbl_income = tk.Label(self, text="Income",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        lbl_add = tk.Label(self, text="Add",
            bg=COLOR_3, fg=COLOR_1, font=FONT_M)

        lbl_income.grid(row=0, column=0,
            ipadx=10, ipady=7)
        lbl_add.grid(row=3, column=0,
            ipadx=18, ipady=4,
            padx=(15, 0), pady=(5,0))

        # Button
        btn_view = tk.Button(self, text="View",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(IncomeView))
        btn_update = tk.Button(self, text="Update",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(IncomeUpdate))
        btn_delete = tk.Button(self, text="Delete",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(IncomeDelete))

        btn_back = tk.Button(self, text="<< Menu",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,command=lambda:controller.ShowFrame(Menu))

        btn_view.grid(row=2, column=0,
            padx=(15,0), pady=(15,0))
        btn_update.grid(row=4, column=0,
            padx=(15,0), pady=(5,0))
        btn_delete.grid(row=5, column=0,
            padx=(15,0), pady=(5,0))

        btn_back.grid(row=1, column=0,
        padx=(15,0), pady=(15,0))

        ############ Content############
        # Label
        lbl_date = tk.Label(self, text="Date",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_type = tk.Label(self, text="Type",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_amount = tk.Label(self, text="Amount",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_description = tk.Label(self, text="Description",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)

        lbl_date.grid(row=2, column=1, sticky="e")
        lbl_type.grid(row=3, column=1, sticky="e")
        lbl_amount.grid(row=4, column=1, sticky="e")
        lbl_description.grid(row=5, column=1, sticky="e")

        # Entry
        ent_date = tk.Entry(self, font=FONT_M)
        ent_type = tk.Entry(self, font=FONT_M)
        ent_amount = tk.Entry(self, font=FONT_M)
        ent_description = tk.Entry(self, font=FONT_M)

        ent_date.grid(row=2, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_type.grid(row=3, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_amount.grid(row=4, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_description.grid(row=5, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))

        # Buttton
        btn_submit = tk.Button(self, text="Submit",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")
        btn_cancel = tk.Button(self, text="Cancel",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")

        btn_submit.grid(row=6, column=2,
            pady=(5,0))
        btn_cancel.grid(row=6, column=3,
            pady=(5,0))

class IncomeUpdate(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        ############ Left nav ############
        # Label
        lbl_income = tk.Label(self, text="Income",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        lbl_update = tk.Label(self, text="Update",
            bg=COLOR_3, fg=COLOR_1, font=FONT_M)

        lbl_income.grid(row=0, column=0,
            ipadx=10, ipady=7)
        lbl_update.grid(row=4, column=0,
            ipadx=8, ipady=4,
            padx=(15, 0), pady=(5,0))

        # Button
        btn_view = tk.Button(self, text="View",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(IncomeView))
        btn_add = tk.Button(self, text="Add",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(IncomeAdd))
        btn_delete = tk.Button(self, text="Delete",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(IncomeDelete))

        btn_back = tk.Button(self, text="<< Menu",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,command=lambda:controller.ShowFrame(Menu))

        btn_view.grid(row=2, column=0,
            padx=(15,0), pady=(15,0))
        btn_add.grid(row=3, column=0,
            padx=(15,0), pady=(5,0))
        btn_delete.grid(row=5, column=0,
            padx=(15,0), pady=(5,0))

        btn_back.grid(row=1, column=0,
        padx=(15,0), pady=(15,0))

        ############ Content############
        # Label
        lbl_id = tk.Label(self, text="ID",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_date = tk.Label(self, text="Date",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_type = tk.Label(self, text="Type",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_amount = tk.Label(self, text="Amount",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_description = tk.Label(self, text="Description",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)

        lbl_id.grid(row=2, column=1, sticky="e")
        lbl_date.grid(row=3, column=1, sticky="e")
        lbl_type.grid(row=4, column=1, sticky="e")
        lbl_amount.grid(row=5, column=1, sticky="e")
        lbl_description.grid(row=6, column=1, sticky="e")

        # Entry
        ent_id = tk.Entry(self, font=FONT_M)
        ent_date = tk.Entry(self, font=FONT_M)
        ent_type = tk.Entry(self, font=FONT_M)
        ent_amount = tk.Entry(self, font=FONT_M)
        ent_description = tk.Entry(self, font=FONT_M)

        ent_id.grid(row=2, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_date.grid(row=3, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_type.grid(row=4, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_amount.grid(row=5, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_description.grid(row=6, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))

        # Buttton
        btn_submit = tk.Button(self, text="Submit",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")
        btn_cancel = tk.Button(self, text="Cancel",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")

        btn_submit.grid(row=7, column=2,
            pady=(5,0))
        btn_cancel.grid(row=7, column=3,
            pady=(5,0))

class IncomeDelete(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        ############ Left nav ############
        # Label
        lbl_income = tk.Label(self, text="Income",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        lbl_delete = tk.Label(self, text="Delete",
            bg=COLOR_3, fg=COLOR_1, font=FONT_M)

        lbl_income.grid(row=0, column=0,
            ipadx=10, ipady=7)
        lbl_delete.grid(row=5, column=0,
            ipadx=10, ipady=4,
            padx=(15, 0), pady=(5,0))

        # Button
        btn_view = tk.Button(self, text="View",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(IncomeView))
        btn_add = tk.Button(self, text="Add",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(IncomeAdd))
        btn_update = tk.Button(self, text="Update",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(IncomeUpdate))

        btn_back = tk.Button(self, text="<< Menu",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,command=lambda:controller.ShowFrame(Menu))

        btn_view.grid(row=2, column=0,
            padx=(15,0), pady=(15,0))
        btn_add.grid(row=3, column=0,
            padx=(15,0), pady=(5,0))
        btn_update.grid(row=4, column=0,
            padx=(15,0), pady=(5,0))

        btn_back.grid(row=1, column=0,
        padx=(15,0), pady=(15,0))

        ############ Content############
        # Label
        lbl_id = tk.Label(self, text="ID",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_id.grid(row=2, column=1, sticky="e")

        # Entry
        ent_id = tk.Entry(self, font=FONT_M)

        ent_id.grid(row=2, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))

        # Buttton
        btn_submit = tk.Button(self, text="Submit",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")
        btn_cancel = tk.Button(self, text="Cancel",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")

        btn_submit.grid(row=3, column=2,
            pady=(5,0))
        btn_cancel.grid(row=3, column=3,
            pady=(5,0))



class SavingView(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        ############ Left nav ############
        # Label
        lbl_saving = tk.Label(self, text="Saving",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        lbl_view = tk.Label(self, text="View",
            bg=COLOR_3, fg=COLOR_1, font=FONT_M)

        lbl_saving.grid(row=0, column=0,
            ipadx=10, ipady=7)
        lbl_view.grid(row=2, column=0,
            ipadx=15, ipady=5,
            padx=(15, 0), pady=(15,0))

        # Button
        btn_add = tk.Button(self, text="Add",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(SavingAdd))
        btn_update = tk.Button(self, text="Update",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(SavingUpdate))
        btn_delete = tk.Button(self, text="Delete",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(SavingDelete))

        btn_back = tk.Button(self, text="<< Menu",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,command=lambda:controller.ShowFrame(Menu))

        btn_add.grid(row=3, column=0,
            padx=(15,0), pady=(5,0))
        btn_update.grid(row=4, column=0,
            padx=(15,0), pady=(5,0))
        btn_delete.grid(row=5, column=0,
            padx=(15,0), pady=(5,0))

        btn_back.grid(row=1, column=0,
        padx=(15,0), pady=(15,0))

        ############ Content############
        # Label
        lbl_date = tk.Label(self, text="Date",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_tide = tk.Label(self, text="~",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)

        lbl_date.grid(row=2, column=1)
        lbl_tide.grid(row=2, column=3,
            padx=(5,0))

        # Entry
        ent_strt_dt = tk.Entry(self, font=FONT_M,
            width=12)
        ent_end_dt = tk.Entry(self, font=FONT_M,
            width=12)

        ent_strt_dt.grid(row=2, column=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_end_dt.grid(row=2, column=4,
            ipadx=3, ipady=3,
            padx=(5,0))

        # Buttton
        btn_submit = tk.Button(self, text="Submit",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")
        btn_submit.grid(row=2, column=5,
            padx=(5,0))

        # Table: TreeView

class SavingAdd(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        ############ Left nav ############
        # Label
        lbl_saving = tk.Label(self, text="Saving",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        lbl_add = tk.Label(self, text="Add",
            bg=COLOR_3, fg=COLOR_1, font=FONT_M)

        lbl_saving.grid(row=0, column=0,
            ipadx=10, ipady=7)
        lbl_add.grid(row=3, column=0,
            ipadx=18, ipady=4,
            padx=(15, 0), pady=(5,0))

        # Button
        btn_view = tk.Button(self, text="View",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(SavingView))
        btn_update = tk.Button(self, text="Update",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(SavingUpdate))
        btn_delete = tk.Button(self, text="Delete",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(SavingDelete))

        btn_back = tk.Button(self, text="<< Menu",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,command=lambda:controller.ShowFrame(Menu))

        btn_view.grid(row=2, column=0,
            padx=(15,0), pady=(15,0))
        btn_update.grid(row=4, column=0,
            padx=(15,0), pady=(5,0))
        btn_delete.grid(row=5, column=0,
            padx=(15,0), pady=(5,0))

        btn_back.grid(row=1, column=0,
        padx=(15,0), pady=(15,0))

        ############ Content############
        # Label
        lbl_date = tk.Label(self, text="Date",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_group = tk.Label(self, text="Group",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_amount = tk.Label(self, text="Amount",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_description = tk.Label(self, text="Description",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)

        lbl_date.grid(row=2, column=1, sticky="e")
        lbl_group.grid(row=3, column=1, sticky="e")
        lbl_amount.grid(row=4, column=1, sticky="e")
        lbl_description.grid(row=5, column=1, sticky="e")

        # Entry
        ent_date = tk.Entry(self, font=FONT_M)
        ent_type = tk.Entry(self, font=FONT_M)
        ent_amount = tk.Entry(self, font=FONT_M)
        ent_description = tk.Entry(self, font=FONT_M)

        ent_date.grid(row=2, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_type.grid(row=3, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_amount.grid(row=4, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_description.grid(row=5, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))

        # Buttton
        btn_submit = tk.Button(self, text="Submit",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")
        btn_cancel = tk.Button(self, text="Cancel",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")

        btn_submit.grid(row=6, column=2,
            pady=(5,0))
        btn_cancel.grid(row=6, column=3,
            pady=(5,0))

class SavingUpdate(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        ############ Left nav ############
        # Label
        lbl_saving = tk.Label(self, text="Saving",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        lbl_update = tk.Label(self, text="Update",
            bg=COLOR_3, fg=COLOR_1, font=FONT_M)

        lbl_saving.grid(row=0, column=0,
            ipadx=10, ipady=7)
        lbl_update.grid(row=4, column=0,
            ipadx=8, ipady=4,
            padx=(15, 0), pady=(5,0))

        # Button
        btn_view = tk.Button(self, text="View",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(SavingView))
        btn_add = tk.Button(self, text="Add",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(SavingAdd))
        btn_delete = tk.Button(self, text="Delete",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(SavingDelete))

        btn_back = tk.Button(self, text="<< Menu",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,command=lambda:controller.ShowFrame(Menu))

        btn_view.grid(row=2, column=0,
            padx=(15,0), pady=(15,0))
        btn_add.grid(row=3, column=0,
            padx=(15,0), pady=(5,0))
        btn_delete.grid(row=5, column=0,
            padx=(15,0), pady=(5,0))

        btn_back.grid(row=1, column=0,
        padx=(15,0), pady=(15,0))

        ############ Content############
        # Label
        lbl_id = tk.Label(self, text="ID",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_date = tk.Label(self, text="Date",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_group = tk.Label(self, text="Group",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_amount = tk.Label(self, text="Amount",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_description = tk.Label(self, text="Description",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)

        lbl_id.grid(row=2, column=1, sticky="e")
        lbl_date.grid(row=3, column=1, sticky="e")
        lbl_group.grid(row=4, column=1, sticky="e")
        lbl_amount.grid(row=5, column=1, sticky="e")
        lbl_description.grid(row=6, column=1, sticky="e")

        # Entry
        ent_id = tk.Entry(self, font=FONT_M)
        ent_date = tk.Entry(self, font=FONT_M)
        ent_type = tk.Entry(self, font=FONT_M)
        ent_amount = tk.Entry(self, font=FONT_M)
        ent_description = tk.Entry(self, font=FONT_M)

        ent_id.grid(row=2, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_date.grid(row=3, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_type.grid(row=4, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_amount.grid(row=5, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_description.grid(row=6, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))

        # Buttton
        btn_submit = tk.Button(self, text="Submit",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")
        btn_cancel = tk.Button(self, text="Cancel",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")

        btn_submit.grid(row=7, column=2,
            pady=(5,0))
        btn_cancel.grid(row=7, column=3,
            pady=(5,0))

class SavingDelete(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        ############ Left nav ############
        # Label
        lbl_saving = tk.Label(self, text="Saving",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        lbl_delete = tk.Label(self, text="Delete",
            bg=COLOR_3, fg=COLOR_1, font=FONT_M)

        lbl_saving.grid(row=0, column=0,
            ipadx=10, ipady=7)
        lbl_delete.grid(row=5, column=0,
            ipadx=10, ipady=4,
            padx=(15, 0), pady=(5,0))

        # Button
        btn_view = tk.Button(self, text="View",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(SavingView))
        btn_add = tk.Button(self, text="Add",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(SavingAdd))
        btn_update = tk.Button(self, text="Update",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(SavingUpdate))

        btn_back = tk.Button(self, text="<< Menu",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,command=lambda:controller.ShowFrame(Menu))

        btn_view.grid(row=2, column=0,
            padx=(15,0), pady=(15,0))
        btn_add.grid(row=3, column=0,
            padx=(15,0), pady=(5,0))
        btn_update.grid(row=4, column=0,
            padx=(15,0), pady=(5,0))

        btn_back.grid(row=1, column=0,
        padx=(15,0), pady=(15,0))

        ############ Content############
        # Label
        lbl_id = tk.Label(self, text="ID",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_id.grid(row=2, column=1, sticky="e")

        # Entry
        ent_id = tk.Entry(self, font=FONT_M)

        ent_id.grid(row=2, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))

        # Buttton
        btn_submit = tk.Button(self, text="Submit",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")
        btn_cancel = tk.Button(self, text="Cancel",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")

        btn_submit.grid(row=3, column=2,
            pady=(5,0))
        btn_cancel.grid(row=3, column=3,
            pady=(5,0))



class InvestView(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        ############ Left nav ############
        # Label
        lbl_invest = tk.Label(self, text="Invest",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        lbl_view = tk.Label(self, text="View",
            bg=COLOR_3, fg=COLOR_1, font=FONT_M)

        lbl_invest.grid(row=0, column=0,
            ipadx=10, ipady=7)
        lbl_view.grid(row=2, column=0,
            ipadx=15, ipady=5,
            padx=(15, 0), pady=(15,0))

        # Button
        btn_add = tk.Button(self, text="Add",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(InvestAdd))
        btn_update = tk.Button(self, text="Update",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(InvestUpdate))
        btn_delete = tk.Button(self, text="Delete",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(InvestDelete))

        btn_back = tk.Button(self, text="<< Menu",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,command=lambda:controller.ShowFrame(Menu))

        btn_add.grid(row=3, column=0,
            padx=(15,0), pady=(5,0))
        btn_update.grid(row=4, column=0,
            padx=(15,0), pady=(5,0))
        btn_delete.grid(row=5, column=0,
            padx=(15,0), pady=(5,0))

        btn_back.grid(row=1, column=0,
        padx=(15,0), pady=(15,0))

        ############ Content############
        # Label
        lbl_date = tk.Label(self, text="Date",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_tide = tk.Label(self, text="~",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)

        lbl_date.grid(row=2, column=1)
        lbl_tide.grid(row=2, column=3,
            padx=(5,0))

        # Entry
        ent_strt_dt = tk.Entry(self, font=FONT_M,
            width=12)
        ent_end_dt = tk.Entry(self, font=FONT_M,
            width=12)

        ent_strt_dt.grid(row=2, column=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_end_dt.grid(row=2, column=4,
            ipadx=3, ipady=3,
            padx=(5,0))

        # Buttton
        btn_submit = tk.Button(self, text="Submit",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")
        btn_submit.grid(row=2, column=5,
            padx=(5,0))

        # Table: TreeView

class InvestAdd(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        ############ Left nav ############
        # Label
        lbl_invest = tk.Label(self, text="Invest",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        lbl_add = tk.Label(self, text="Add",
            bg=COLOR_3, fg=COLOR_1, font=FONT_M)

        lbl_invest.grid(row=0, column=0,
            ipadx=10, ipady=7)
        lbl_add.grid(row=3, column=0,
            ipadx=18, ipady=4,
            padx=(15, 0), pady=(5,0))

        # Button
        btn_view = tk.Button(self, text="View",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(InvestView))
        btn_update = tk.Button(self, text="Update",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(InvestUpdate))
        btn_delete = tk.Button(self, text="Delete",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(InvestDelete))

        btn_back = tk.Button(self, text="<< Menu",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,command=lambda:controller.ShowFrame(Menu))

        btn_view.grid(row=2, column=0,
            padx=(15,0), pady=(15,0))
        btn_update.grid(row=4, column=0,
            padx=(15,0), pady=(5,0))
        btn_delete.grid(row=5, column=0,
            padx=(15,0), pady=(5,0))

        btn_back.grid(row=1, column=0,
        padx=(15,0), pady=(15,0))

        ############ Content############
        # Label
        lbl_date = tk.Label(self, text="Date",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_purpose = tk.Label(self, text="Purpose",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_amount = tk.Label(self, text="Amount",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_description = tk.Label(self, text="Description",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)

        lbl_date.grid(row=2, column=1, sticky="e")
        lbl_purpose.grid(row=3, column=1, sticky="e")
        lbl_amount.grid(row=4, column=1, sticky="e")
        lbl_description.grid(row=5, column=1, sticky="e")

        # Entry
        ent_date = tk.Entry(self, font=FONT_M)
        ent_type = tk.Entry(self, font=FONT_M)
        ent_amount = tk.Entry(self, font=FONT_M)
        ent_description = tk.Entry(self, font=FONT_M)

        ent_date.grid(row=2, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_type.grid(row=3, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_amount.grid(row=4, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_description.grid(row=5, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))

        # Buttton
        btn_submit = tk.Button(self, text="Submit",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")
        btn_cancel = tk.Button(self, text="Cancel",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")

        btn_submit.grid(row=6, column=2,
            pady=(5,0))
        btn_cancel.grid(row=6, column=3,
            pady=(5,0))

class InvestUpdate(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        ############ Left nav ############
        # Label
        lbl_invest= tk.Label(self, text="Invest",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        lbl_update = tk.Label(self, text="Update",
            bg=COLOR_3, fg=COLOR_1, font=FONT_M)

        lbl_invest.grid(row=0, column=0,
            ipadx=10, ipady=7)
        lbl_update.grid(row=4, column=0,
            ipadx=8, ipady=4,
            padx=(15, 0), pady=(5,0))

        # Button
        btn_view = tk.Button(self, text="View",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(InvestView))
        btn_add = tk.Button(self, text="Add",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(InvestAdd))
        btn_delete = tk.Button(self, text="Delete",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(InvestDelete))

        btn_back = tk.Button(self, text="<< Menu",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,command=lambda:controller.ShowFrame(Menu))

        btn_view.grid(row=2, column=0,
            padx=(15,0), pady=(15,0))
        btn_add.grid(row=3, column=0,
            padx=(15,0), pady=(5,0))
        btn_delete.grid(row=5, column=0,
            padx=(15,0), pady=(5,0))

        btn_back.grid(row=1, column=0,
        padx=(15,0), pady=(15,0))

        ############ Content############
        # Label
        lbl_id = tk.Label(self, text="ID",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_date = tk.Label(self, text="Date",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_purpose = tk.Label(self, text="Purpose",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_amount = tk.Label(self, text="Amount",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_description = tk.Label(self, text="Description",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)

        lbl_id.grid(row=2, column=1, sticky="e")
        lbl_date.grid(row=3, column=1, sticky="e")
        lbl_purpose.grid(row=4, column=1, sticky="e")
        lbl_amount.grid(row=5, column=1, sticky="e")
        lbl_description.grid(row=6, column=1, sticky="e")

        # Entry
        ent_id = tk.Entry(self, font=FONT_M)
        ent_date = tk.Entry(self, font=FONT_M)
        ent_type = tk.Entry(self, font=FONT_M)
        ent_amount = tk.Entry(self, font=FONT_M)
        ent_description = tk.Entry(self, font=FONT_M)

        ent_id.grid(row=2, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_date.grid(row=3, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_type.grid(row=4, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_amount.grid(row=5, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_description.grid(row=6, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))

        # Buttton
        btn_submit = tk.Button(self, text="Submit",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")
        btn_cancel = tk.Button(self, text="Cancel",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")

        btn_submit.grid(row=7, column=2,
            pady=(5,0))
        btn_cancel.grid(row=7, column=3,
            pady=(5,0))

class InvestDelete(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        ############ Left nav ############
        # Label
        lbl_invest = tk.Label(self, text="Invest",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        lbl_delete = tk.Label(self, text="Delete",
            bg=COLOR_3, fg=COLOR_1, font=FONT_M)

        lbl_invest.grid(row=0, column=0,
            ipadx=10, ipady=7)
        lbl_delete.grid(row=5, column=0,
            ipadx=10, ipady=4,
            padx=(15, 0), pady=(5,0))

        # Button
        btn_view = tk.Button(self, text="View",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(InvestView))
        btn_add = tk.Button(self, text="Add",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(InvestAdd))
        btn_update = tk.Button(self, text="Update",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(InvestUpdate))

        btn_back = tk.Button(self, text="<< Menu",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,command=lambda:controller.ShowFrame(Menu))

        btn_view.grid(row=2, column=0,
            padx=(15,0), pady=(15,0))
        btn_add.grid(row=3, column=0,
            padx=(15,0), pady=(5,0))
        btn_update.grid(row=4, column=0,
            padx=(15,0), pady=(5,0))

        btn_back.grid(row=1, column=0,
        padx=(15,0), pady=(15,0))

        ############ Content############
        # Label
        lbl_id = tk.Label(self, text="ID",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_id.grid(row=2, column=1, sticky="e")

        # Entry
        ent_id = tk.Entry(self, font=FONT_M)

        ent_id.grid(row=2, column=2, columnspan=2,
            ipadx=3, ipady=3,
            padx=(5,0))

        # Buttton
        btn_submit = tk.Button(self, text="Submit",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")
        btn_cancel = tk.Button(self, text="Cancel",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")

        btn_submit.grid(row=3, column=2,
            pady=(5,0))
        btn_cancel.grid(row=3, column=3,
            pady=(5,0))



class Export(Background):
    def __init__(self, parent, controller):
        super().__init__(self, parent)

        # Label
        lbl_export = tk.Label(self, text="Export",
            bg=COLOR_1, fg=COLOR_3, font=FONT_HEAD)
        lbl_date = tk.Label(self, text="Date",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)
        lbl_tide = tk.Label(self, text="~",
            bg=COLOR_1, fg=COLOR_4, font=FONT_L)

        lbl_export.grid(row=0, column=0,
            ipadx=10, ipady=7)
        lbl_date.grid(row=2, column=1,
            padx=(5,0))
        lbl_tide.grid(row=2, column=3,
            padx=(5,0))

        # Entry
        ent_strt_dt =tk.Entry(self, font=FONT_M)
        ent_end_dt =tk.Entry(self, font=FONT_M)

        ent_strt_dt.grid(row=2, column=2,
            ipadx=3, ipady=3,
            padx=(5,0))
        ent_end_dt.grid(row=2, column=4,
            ipadx=3, ipady=3,
            padx=(5,0))

        # Button
        btn_submit = tk.Button(self, text="Submit",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")
        btn_cancel = tk.Button(self, text="Cancel",
            font=FONT_M, relief="ridge",
            bg=COLOR_4, fg=COLOR_1,
            width=7,
            command="#")
        btn_back = tk.Button(self, text="<< Menu",
            font=FONT_M, relief="ridge",
            activebackground=COLOR_4, activeforeground=COLOR_1,
            width=7,
            command=lambda:controller.ShowFrame(Menu))

        btn_submit.grid(row=3, column=2)
        btn_cancel.grid(row=3, column=4)
        btn_back.grid(row=1, column=0,
            padx=(15,0), pady=(15,0))

        # Radiobutton
        var_radio = tk.IntVar()

        rad_expense = tk.Radiobutton(self, text="Expense", justify="left",
                                    variable=var_radio, value=1,
                                    bg=COLOR_3, fg=COLOR_1, font=FONT_M)
        rad_subscription = tk.Radiobutton(self, text="Income", justify="left",
                                    variable=var_radio, value=2,
                                    bg=COLOR_3, fg=COLOR_1, font=FONT_M)
        rad_income = tk.Radiobutton(self, text="Income", justify="left",
                                    variable=var_radio, value=3,
                                    bg=COLOR_3, fg=COLOR_1, font=FONT_M)
        rad_saving = tk.Radiobutton(self, text="Saving", justify="left",
                                    variable=var_radio, value=4,
                                    bg=COLOR_3, fg=COLOR_1, font=FONT_M)
        rad_invest = tk.Radiobutton(self, text="Invest", justify="left",
                                    variable=var_radio, value=5,
                                    bg=COLOR_3, fg=COLOR_1, font=FONT_M)
        rad_budget = tk.Radiobutton(self, text="Budget", justify="left",
                                    variable=var_radio, value=6,
                                    bg=COLOR_3, fg=COLOR_1, font=FONT_M)

        rad_expense.grid(row=2, column=0, sticky="w",
            padx=(30,0), pady=(15,0))
        rad_subscription.grid(row=3, column=0, sticky="w",
            padx=(30,0), pady=(5,0))
        rad_income.grid(row=4, column=0, sticky="w",
            padx=(30,0), pady=(5,0))
        rad_saving.grid(row=5, column=0, sticky="w",
            padx=(30,0), pady=(5,0))
        rad_invest.grid(row=6, column=0, sticky="w",
            padx=(30,0), pady=(5,0))
        rad_budget.grid(row=7, column=0, sticky="w",
            padx=(30,0), pady=(5,0))



if __name__ == '__main__':
    root = MoneyApp()
    root.mainloop()