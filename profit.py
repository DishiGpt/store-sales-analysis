from tkinter import *
from tkinter import ttk
import pandas as pd
import sqlite3
from PIL import Image,ImageTk
import plotly.express as px
import plotly.io as pio
import io

pio.renderers.default = 'browser'

from tkinter import messagebox
class profitClass:
    def __init__(self,root):
        self.root=root #this is to define that this object is of the class itself & ca be used in functions to modify
        self.root.geometry("600x400+220+130")
        self.root.title("Inventroy management system | Developed by Dishi")
        self.root.config(bg="white")
        self.root.focus_force()
    
         #title
        lbl_title=Label(self.root,text="View Profit & sales Analysis",font=(15),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X,padx=10,pady=20)

        btn_salm=Button(self.root,text="Sales by month",command=self.show_sales_by_month,bg="white",bd=2,relief=RIDGE,cursor="hand2",fg="green",font=("bold)",12)).place(x=250,y=100,width=150,height=40)
        btn_salc=Button(self.root,text="Sales by category",command=self.show_sales_by_category,bg="white",bd=2,relief=RIDGE,cursor="hand2",fg="green",font=("bold)",12)).place(x=250,y=160,width=150,height=40)
        btn_prom=Button(self.root,text="Profit by month",command=self.show_profit_by_month,bg="white",bd=2,relief=RIDGE,cursor="hand2",fg="green",font=("bold)",12)).place(x=250,y=220,width=150,height=40)
        btn_proc=Button(self.root,text="Profit by category",command=self.show_profit_by_category,bg="white",bd=2,relief=RIDGE,cursor="hand2",fg="green",font=("bold)",12)).place(x=250,y=280,width=150,height=40)


    def fetch_data(self):
        """Fetch sales and product data from the database."""
        con = sqlite3.connect('ims.db')
        query = """
        SELECT 
            s.date,
            s.price * s.qty AS total_sales,
            (p.sp - p.cp) * s.qty - s.discount AS profit,
            p.Category AS category
        FROM 
            sales s
        JOIN 
            product p ON s.pid = p.pid
        """
        data = pd.read_sql(query, con)
        #data['date'] = pd.to_datetime(data['date'])
        try:
            data['date'] = pd.to_datetime(data['date'], format="%d/%m/%Y", errors='coerce')
        except Exception as e:
            print(f"Error converting date: {e}")
            return pd.DataFrame()  # Return an empty DataFrame if conversion fails
        data['month'] = data['date'].dt.month
        data['year'] = data['date'].dt.year
        con.close()
        return data

    def show_sales_by_month(self):
        """Show a Plotly line chart for sales by month."""
        data = self.fetch_data()
        sales_by_month = data.groupby('month')['total_sales'].sum().reset_index()
        fig = px.line(sales_by_month, x='month', y='total_sales', title='Sales by Month', labels={'month': 'Month', 'total_sales': 'Total Sales'})
        fig.show()

    def show_sales_by_category(self):
        """Show a Plotly bar chart for sales by category."""
        data = self.fetch_data()
        sales_by_category = data.groupby('category')['total_sales'].sum().reset_index()
        fig = px.bar(sales_by_category, x='category', y='total_sales', title='Sales by Category', labels={'category': 'Category', 'total_sales': 'Total Sales'})
        fig.show()

    def show_profit_by_month(self):
        """Show a Plotly line chart for profit by month."""
        data = self.fetch_data()
        profit_by_month = data.groupby('month')['profit'].sum().reset_index()
        fig = px.line(profit_by_month, x='month', y='profit', title='Profit by Month', labels={'month': 'Month', 'profit': 'Total Profit'})
        fig.show()

    def show_profit_by_category(self):
        """Show a Plotly bar chart for profit by category."""
        data = self.fetch_data()
        profit_by_category = data.groupby('category')['profit'].sum().reset_index()
        fig = px.bar(profit_by_category, x='category', y='profit', title='Profit by Category', labels={'category': 'Category', 'profit': 'Total Profit'})
        fig.show()



if __name__=="__main__":
    root=Tk()
    obj=profitClass(root)
    root.mainloop()