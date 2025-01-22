from tkinter import *
from PIL import Image,ImageTk
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
from tkinter import messagebox
import time
import os
import sqlite3
class IMS:
    def __init__(self,root):
        self.root=root #this is to define that this object is of the class itself & ca be used in functions to modify
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventroy management system | Developed by Dishi")
        self.root.config(bg="white")

        #title
        self.icon_title=PhotoImage(file="images/icon.png")
        title=Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#4a68b3",fg="#F0F0F0",anchor="w",padx=20,pady=20).place(x=0,y=0,relwidth=1,height=70)
        
        #button
        btn_logout=Button(self.root,text="logout",font=("times new roman",15,"bold"),bg="red",cursor="hand2").place(x=1200,y=20,height=30,width=70)

        #clock
        self.lbl_clock=Label(self.root,text="Welcome to Inventory management system\t\t Date: DD/MM/YYYY\t\t Time:  HH/MM/SS",font=("times new roman",15,),bg="#333333",fg="#F0F0F0")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #left menu
        self.MenuLogo=Image.open("images/menu.png")
        self.MenuLogo=self.MenuLogo.resize((200,200),Image.Resampling.LANCZOS)
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)

        LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=102,width=200,height=565)

        lbl_menuLogo=Label(LeftMenu,image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP,fill=X)       #self define

        self.icon_side=PhotoImage(file="images/bullet.png")

        lbl_menu=Label(LeftMenu,text="Menu",font=("times new roman",20),bg="#009688").pack(side=TOP,fill=X)


        btn_employee=Button(LeftMenu,text="Employee",command=self.employee,font=("times new roman",15),bg="white",bd=2,cursor="hand2").pack(side=TOP,fill=X)
        btn_supplier=Button(LeftMenu,text="Supplier",command=self.supplier,font=("times new roman",15),bg="white",bd=2,cursor="hand2").pack(side=TOP,fill=X)
        btn_category=Button(LeftMenu,text="Category",command=self.category,font=("times new roman",15),bg="white",bd=2,cursor="hand2").pack(side=TOP,fill=X)
        btn_product=Button(LeftMenu,text="Product",command=self.product,font=("times new roman",15),bg="white",bd=2,cursor="hand2").pack(side=TOP,fill=X)
        btn_sales=Button(LeftMenu,text="Sales",command=self.sales,font=("times new roman",15),bg="white",bd=2,cursor="hand2").pack(side=TOP,fill=X)
        btn_exit=Button(LeftMenu,text="Exit",font=("times new roman",15),bg="white",bd=2,cursor="hand2").pack(side=TOP,fill=X)

        #content
        self.lbl_employee=Label(self.root,text="Total employees\n\n0",bd=5,relief=RIDGE,bg="#6495ED",fg="white",font=("times new roman",20,"bold"))
        self.lbl_employee.place(x=300,y=120,height=150,width=250)

        self.lbl_supplier=Label(self.root,text="Total suppliers\n\n0",bd=5,relief=RIDGE,bg="#6495ED",fg="white",font=("times new roman",20,"bold"))
        self.lbl_supplier.place(x=650,y=120,height=150,width=250)

        self.lbl_category=Label(self.root,text="Total categories\n\n0",bd=5,relief=RIDGE,bg="#6495ED",fg="white",font=("times new roman",20,"bold"),)
        self.lbl_category.place(x=1000,y=120,height=150,width=250)

        self.lbl_product=Label(self.root,text="Total products\n\n0",bd=5,relief=RIDGE,bg="#6495ED",fg="white",font=("times new roman",20,"bold"))
        self.lbl_product.place(x=300,y=300,height=150,width=250)

        self.lbl_sales=Label(self.root,text="Total sales\n\n0",bd=5,relief=RIDGE,bg="#6495ED",fg="white",font=("times new roman",20,"bold"))
        self.lbl_sales.place(x=650,y=300,height=150,width=250)

        #footer
        lbl_footer=Label(self.root,text="IMS : Inventroy management system | Developed by Dishi\nFor any technical issue Contact : 987xxxxxx1",font=("times new roman",12),bg="#333333",fg="#F0F0F0").pack(side=BOTTOM,fill=X)

        self.update_content()

    def employee(self):   #self to use members of IMS,root
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeClass(self.new_win)

    def supplier(self):   #self to use members of IMS,root
        self.new_win=Toplevel(self.root)
        self.new_obj=supplierClass(self.new_win)

    def category(self):   #self to use members of IMS,root
        self.new_win=Toplevel(self.root)
        self.new_obj=categoryClass(self.new_win)

    def product(self):   #self to use members of IMS,root
        self.new_win=Toplevel(self.root)
        self.new_obj=productClass(self.new_win)

    def sales(self):   #self to use members of IMS,root
        self.new_win=Toplevel(self.root)
        self.new_obj=salesClass(self.new_win)

    def update_content(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            product=cur.fetchall()
            self.lbl_product.config(text=f'Total products\n\n{str(len(product))}')

            cur.execute("select * from supplier")
            supplier=cur.fetchall()
            self.lbl_supplier.config(text=f'Total suppliers\n\n{str(len(supplier))}')

            cur.execute("select * from category")
            category=cur.fetchall()
            self.lbl_category.config(text=f'Total categories\n\n{str(len(category))}')

            cur.execute("select * from employee")
            employee=cur.fetchall()
            self.lbl_employee.config(text=f'Total employees\n\n{str(len(employee))}')
            bill=len(os.listdir('bill'))
            self.lbl_sales.config(text=f'Total sales\n\n{str(bill)}')

            time_stmp=time.strftime("%H:%M:%S")
            date_stmp=time.strftime("%d/%m/%Y")
            self.lbl_clock.config(text=f"Welcome to Inventory management system\t\t Date: {str(date_stmp)}\t\t Time:  {str(time_stmp)}")
            self.lbl_clock.after(200,self.update_content)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    

if __name__=="__main__":
    root=Tk()
    obj=IMS(root)
    root.mainloop()  #this is so the program doen't run & exit but stays


