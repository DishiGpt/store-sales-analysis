from tkinter import *
from PIL import Image,ImageTk #pip intall pillow
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import os
class orderClass:
    def __init__(self,root):
        self.root=root #this is to define that this object is of the class itself & ca be used in functions to modify
        self.root.geometry("1000x500+220+130")
        self.root.title("Inventroy management system | Developed by Dishi")
        self.root.config(bg="white")
        self.root.focus_force()

        self.bill_list=[]
        self.var_invoice=StringVar() 
        self.sid=StringVar()
        self.cname=StringVar()
        self.contact=StringVar()
        self.pid=StringVar()
        self.pname=StringVar()
        self.qty=StringVar()
        self.price=StringVar()
        self.date=StringVar()
        self.discount=StringVar()

        #title
        lbl_title=Label(self.root,text="View Order Details",font=(15),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X,padx=10,pady=20)

        lbl_invoice=Label(self.root,text="Invoice No.",font=(15),bg="white").place(x=50,y=100)
        txt_invoice=Entry(self.root,textvariable=self.var_invoice,font=(15),bg="white",bd=2).place(x=160,y=100,width=180,height=28)

        btn_search=Button(self.root,text="Search",command=self.search,bg="#F5F5DC",bd=2,relief=RIDGE,cursor="hand2",fg="green",font=("bold)",10)).place(x=360,y=100,width=120,height=28)
        btn_clear=Button(self.root,text="Clear",command=self.clear,bg="#F5F5DC",bd=2,relief=RIDGE,cursor="hand2",fg="green",font=("bold)",10)).place(x=490,y=100,width=120,height=28)


        # bill area
        bill_Frame=Frame(self.root,bd=3,relief=RIDGE,bg="white")
        bill_Frame.place(x=50,y=160,width=600,height=500)

        scrolly1=Scrollbar(bill_Frame,orient=VERTICAL)
        scrollx1=Scrollbar(bill_Frame,orient=HORIZONTAL)

        self.order_detail=ttk.Treeview(bill_Frame,columns=("sid","cname","contact","pid","pname","qty","price","date","discount"),yscrollcommand=scrolly1.set,xscrollcommand=scrollx1.set)
        scrollx1.pack(side=BOTTOM,fill=X)
        scrolly1.pack(side=RIGHT,fill=Y)
        scrollx1.config(command=self.order_detail.xview)
        scrolly1.config(command=self.order_detail.yview)
        self.order_detail.heading("sid",text="SID")
        self.order_detail.heading("cname",text="Customer Name")
        self.order_detail.heading("contact",text="Contact No.")
        self.order_detail.heading("pid",text="PID")
        self.order_detail.heading("pname",text="Product Name")
        self.order_detail.heading("qty",text="Quantity")
        self.order_detail.heading("price",text="Price")
        self.order_detail.heading("date",text="Date")
        self.order_detail.heading("discount",text="Discount")
        self.order_detail["show"]="headings"

        self.order_detail.column("sid",width=60)
        self.order_detail.column("cname",width=100)
        self.order_detail.column("contact",width=90)
        self.order_detail.column("pid",width=60)
        self.order_detail.column("pname",width=90)
        self.order_detail.column("qty",width=60)
        self.order_detail.column("price",width=80)
        self.order_detail.column("date",width=90)
        self.order_detail.column("discount",width=90)
        self.order_detail.pack(fill=BOTH,expand=1)
        self.order_detail.bind("<ButtonRelease-1>",self.get_data)

        self.show()

    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_invoice.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("select * from sales where sid LIKE '%"+self.var_invoice.get()+"%' ")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.order_detail.delete(* self.order_detail.get_children())
                    for row in rows:
                        self.order_detail.insert('',END,values=row)
                else :
                    messagebox.showerror("Error","No record found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


    def clear(self):
        self.show()
        self.var_invoice.set("")
        self.bill_area.delete('1.0',END)

    def  get_data(self,ev):
        f= self.order_detail.focus()
        content=(self.order_detail.item(f))
        row=content['values']
        self.var_invoice.set(row[0]) 
        self.sid.set(row[1])
        self.cname.set(row[2])
        self.contact.set(row[3])
        self.pid.set(row[4])
        self.pname.set(row[5])
        self.qty.set(row[6])
        self.price.set(row[7])
        self.date.set(row[8])
        self.discount.set(row[9])

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from sales")
            rows=cur.fetchall()
            self.order_detail.delete(*self.order_detail.get_children())
            for row in rows:
                self.order_detail.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


if __name__=="__main__":
    root=Tk()
    obj=orderClass(root)
    root.mainloop()