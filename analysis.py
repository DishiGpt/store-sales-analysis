import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class salesClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1300x700+220+130")
        self.root.title("Inventory Management System | Sales Analysis")
        self.root.config(bg="white")
        self.root.focus_force()

        # Database connection
        self.conn = sqlite3.connect('ims.db')

        # Create main frame layout
        self.create_main_layout()

        # Load sales data
        self.load_sales_data()

    def create_main_layout(self):
        # Main Frame
        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left Side - Bill List and Buttons
        left_frame = tk.Frame(main_frame, bg="white", width=250)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Analysis Buttons Frame
        btn_frame = tk.Frame(left_frame, bg="white")
        btn_frame.pack(fill=tk.X, pady=10)

        # Analysis Buttons
        analysis_buttons = [
            ("Monthly Sales", self.show_monthly_sales),
            ("Monthly Profit", self.show_monthly_profit),
            ("Sales by Category", self.show_category_sales),
            ("Profit by Category", self.show_category_profit)
        ]

        for text, command in analysis_buttons:
            btn = tk.Button(btn_frame, text=text, command=command, 
                            bg="#0f4d7d", fg="white", font=("Arial", 10))
            btn.pack(fill=tk.X, pady=5)

        # Bill List Section (from original code)
        sales_Frame = tk.Frame(left_frame, bd=3, relief=tk.RIDGE, bg="white")
        sales_Frame.pack(fill=tk.BOTH, expand=True, pady=10)

        scrolly = tk.Scrollbar(sales_Frame, orient=tk.VERTICAL)
        self.sales_list = tk.Listbox(sales_Frame, font=(15), bg="white", yscrollcommand=scrolly.set)
        scrolly.pack(side=tk.RIGHT, fill=tk.Y)
        scrolly.config(command=self.sales_list.yview)
        self.sales_list.pack(fill=tk.BOTH, expand=1)
        self.sales_list.bind("<ButtonRelease-1>", self.get_data)

        # Right Side - Analysis Display
        self.analysis_frame = tk.Frame(main_frame, bg="white")
        self.analysis_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Bill Area (from original code)
        bill_Frame = tk.Frame(self.analysis_frame, bd=3, relief=tk.RIDGE, bg="white")
        bill_Frame.pack(fill=tk.BOTH, expand=True)

        lbl_title2 = tk.Label(bill_Frame, text="Customer Bills Area", font=(15), bg="#0f4d7d", fg="white")
        lbl_title2.pack(side=tk.TOP, fill=tk.X)

        scrolly2 = tk.Scrollbar(bill_Frame, orient=tk.VERTICAL)
        self.bill_area = tk.Text(bill_Frame, bg="white", yscrollcommand=scrolly2.set)
        scrolly2.pack(side=tk.RIGHT, fill=tk.Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=tk.BOTH, expand=1)

        # Invoice Search Section
        search_frame = tk.Frame(left_frame, bg="white")
        search_frame.pack(fill=tk.X, pady=10)

        self.var_invoice = tk.StringVar()
        lbl_invoice = tk.Label(search_frame, text="Invoice No.", font=(15), bg="white")
        lbl_invoice.pack(side=tk.LEFT)
        txt_invoice = tk.Entry(search_frame, textvariable=self.var_invoice, font=(15), bg="white", bd=2)
        txt_invoice.pack(side=tk.LEFT, padx=5)

        btn_search = tk.Button(search_frame, text="Search", command=self.search, 
                                bg="#F5F5DC", bd=2, relief=tk.RIDGE, 
                                cursor="hand2", fg="green", font=("bold", 10))
        btn_search.pack(side=tk.LEFT, padx=5)
        btn_clear = tk.Button(search_frame, text="Clear", command=self.clear, 
                               bg="#F5F5DC", bd=2, relief=tk.RIDGE, 
                               cursor="hand2", fg="green", font=("bold", 10))
        btn_clear.pack(side=tk.LEFT)

        # Show initial bill list
        self.show()

    def load_sales_data(self):
        """Load sales data from SQLite database"""
        try:
            # Read sales data
            self.sales_df = pd.read_sql_query("SELECT * FROM sales", self.conn)
            
            # Convert date column to datetime
            self.sales_df['date'] = pd.to_datetime(self.sales_df['date'])
            
            # Calculate total sale amount and profit
            self.sales_df['total_sale'] = self.sales_df['qty'].astype(float) * self.sales_df['price'].astype(float)
            self.sales_df['profit'] = self.sales_df['total_sale'] * 0.2  # Assuming 20% profit margin
        except Exception as e:
            messagebox.showerror("Data Load Error", str(e))

    def create_analysis_chart(self, data, title, chart_type='bar'):
        """
        Create a chart in the analysis frame
        
        :param data: Pandas Series with data to plot
        :param title: Chart title
        :param chart_type: Type of chart (bar or pie)
        """
        # Clear previous chart
        for widget in self.analysis_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget != self.bill_area.master:
                widget.destroy()

        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if chart_type == 'bar':
            data.plot(kind='bar', ax=ax)
            ax.set_xlabel('Category')
            ax.tick_params(axis='x', rotation=45)
        elif chart_type == 'pie':
            data.plot(kind='pie', ax=ax, autopct='%1.1f%%')
        
        ax.set_title(title)
        
        # Embed in Tkinter
        chart_frame = tk.Frame(self.analysis_frame)
        chart_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

    def show_monthly_sales(self):
        """Display monthly sales chart"""
        monthly_sales = self.sales_df.groupby(self.sales_df['date'].dt.to_period('M'))['total_sale'].sum()
        self.create_analysis_chart(monthly_sales, 'Monthly Sales')

    def show_monthly_profit(self):
        """Display monthly profit chart"""
        monthly_profit = self.sales_df.groupby(self.sales_df['date'].dt.to_period('M'))['profit'].sum()
        self.create_analysis_chart(monthly_profit, 'Monthly Profit')

    def show_category_sales(self):
        """Display sales by product category"""
        category_sales = self.sales_df.groupby('pname')['total_sale'].sum()
        self.create_analysis_chart(category_sales, 'Sales by Product Category', chart_type='pie')

    def show_category_profit(self):
        """Display profit by product category"""
        category_profit = self.sales_df.groupby('pname')['profit'].sum()
        self.create_analysis_chart(category_profit, 'Profit by Product Category', chart_type='pie')

    # Existing methods from the original salesClass
    def show(self):
        del self.bill_list[:]
        self.sales_list.delete(0, tk.END)
        for i in os.listdir('bill'):
            if i.split('.')[-1] == 'txt':
                self.sales_list.insert(tk.END, i)
                self.bill_list.append(i.split('.')[0])

    def get_data(self, ev):
        index = self.sales_list.curselection()
        file_name = self.sales_list.get(index)
        self.bill_area.delete('1.0', tk.END)
        with open(f'bill/{file_name}', 'r') as fp:
            for i in fp:
                self.bill_area.insert(tk.END, i)

    def search(self):
        if self.var_invoice.get() == "":
            messagebox.showerror("Error", "Invoice no. is required", parent=self.root)
        else:
            if self.var_invoice.get() in self.bill_list:
                with open(f'bill/{self.var_invoice.get()}.txt', 'r') as fp:
                    self.bill_area.delete('1.0', tk.END)
                    for i in fp:
                        self.bill_area.insert(tk.END, i)
            else:
                messagebox.showerror("Error", "Invoice no. is invalid", parent=self.root)

    def clear(self):
        self.show()
        self.var_invoice.set("")
        self.bill_area.delete('1.0', tk.END)

    def __del__(self):
        """Close database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    obj = salesClass(root)
    root.mainloop()