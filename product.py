from tkinter import *
from PIL import Image,ImageTk #pip intall pillow
from tkinter import ttk
from tkinter import messagebox
import sqlite3
class productClass:
    def __init__(self,root):
        self.root=root #this is to define that this object is of the class itself & ca be used in functions to modify
        self.root.geometry("1000x500+220+130")
        self.root.title("Inventroy management system | Developed by Dishi")
        self.root.config(bg="white")
        self.root.focus_force()

        #all variables
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_pid=StringVar()
        self.var_cat=StringVar()
        self.cat_list=[]
        self.sup_list=[]
        self.fetch_cat_sup()
        self.var_sup=StringVar()
        self.var_name=StringVar()
        self.var_cost_price=StringVar()
        self.var_sell_price=StringVar()
        self.var_qty=StringVar()
        self.var_status=StringVar()

        #Frame
        product_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        product_Frame.place(x=10,y=10,width=450,height=600)

        #title
        title=Label(product_Frame,text="Manage Product Details",font=(15),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)

        lbl_pid=Label(product_Frame,text="Product ID ",font=(15),bg="white",state="disabled").place(x=30,y=60)
        lbl_category=Label(product_Frame,text="Category ",font=(15),bg="white").place(x=30,y=110)
        lbl_supplier=Label(product_Frame,text="Supplier",font=(15),bg="white").place(x=30,y=160)
        lbl_product_name=Label(product_Frame,text="Name",font=(15),bg="white").place(x=30,y=210)
        lbl_cost_price=Label(product_Frame,text="Cost Price",font=(15),bg="white").place(x=30,y=260)
        lbl_sell_price=Label(product_Frame,text="Selling Price",font=(15),bg="white").place(x=30,y=310)
        lbl_qty=Label(product_Frame,text="Quantity",font=(15),bg="white").place(x=30,y=360)
        lbl_status=Label(product_Frame,text="Status",font=(15),bg="white").place(x=30,y=410)

        #option
        cmb_cat=ttk.Combobox(product_Frame,textvariable=self.var_cat,values=self.cat_list,state="readonly") #justify=CENTER
        cmb_cat.place(x=150,y=115,width=200)
        cmb_cat.current(0)

        cmb_sup=ttk.Combobox(product_Frame,textvariable=self.var_sup,values=self.sup_list,state="readonly") #justify=CENTER
        cmb_sup.place(x=150,y=165,width=200)
        cmb_sup.current(0)

        txt_pid=Entry(product_Frame,textvariable=self.var_pid,bg="white",bd=2,state="disabled").place(x=150,y=65,width=200)
        txt_name=Entry(product_Frame,textvariable=self.var_name,bg="white",bd=2).place(x=150,y=215,width=200)
        txt_cost_price=Entry(product_Frame,textvariable=self.var_cost_price,bg="white",bd=2).place(x=150,y=265,width=200)
        txt_sell_price=Entry(product_Frame,textvariable=self.var_sell_price,bg="white",bd=2).place(x=150,y=315,width=200)
        txt_qty=Entry(product_Frame,textvariable=self.var_qty,bg="white",bd=2).place(x=150,y=365,width=200)

        cmb_status=ttk.Combobox(product_Frame,textvariable=self.var_status,values=("Active","Inactive"),state="readonly") #justify=CENTER
        cmb_status.place(x=150,y=415,width=200)
        cmb_status.current(0)

        #buttons
        btn_add=Button(product_Frame,text="Save",command=self.add,bg="#F5F5DC",bd=2,relief=RIDGE,cursor="hand2",fg="green",font=("bold)",10)).place(x=10,y=500,width=100,height=28)
        btn_update=Button(product_Frame,text="Update",command=self.update,bg="#F5F5DC",bd=2,relief=RIDGE,cursor="hand2",fg="green",font=("bold)",10)).place(x=120,y=500,width=100,height=28)
        btn_delete=Button(product_Frame,text="Delete",command=self.delete,bg="#F5F5DC",bd=2,relief=RIDGE,cursor="hand2",fg="green",font=("bold)",10)).place(x=230,y=500,width=100,height=28)
        btn_clear=Button(product_Frame,text="Clear",command=self.clear,bg="#F5F5DC",bd=2,relief=RIDGE,cursor="hand2",fg="green",font=("bold)",10)).place(x=340,y=500,width=100,height=28)

        #search
        SearchFrame=LabelFrame(self.root,text="Search Product",font=("times new roman",15,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=480,y=10,width=600,height=80)

        #option
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("  Select","  pid","  Category","  Supplier","  Name"),state="readonly") #justify=CENTER
        cmb_search.place(x=10,y=10,width=100)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,bd=2,relief=RIDGE).place(x=200,y=10,width=200)   #for single row Entry for multiple Text
        btn_search=Button(SearchFrame,text="Search",command=self.search,bg="#F5F5DC",bd=2,relief=RIDGE,cursor="hand2",fg="green",font=("bold)",10)).place(x=410,y=9,width=150,height=22)

        #product details

        pro_frame=Frame(self.root,bd=3,relief=RIDGE)  
        pro_frame.place(x=480,y=100,width=600,height=390)

        scrolly=Scrollbar(pro_frame,orient=VERTICAL)
        scrollx=Scrollbar(pro_frame,orient=HORIZONTAL)

        self.productTable=ttk.Treeview(pro_frame,columns=("pid","Category","Supplier","name","qty","status","cp","sp"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command= self.productTable.xview)
        scrolly.config(command= self.productTable.yview)
        self.productTable.heading("pid",text="Product ID")
        self.productTable.heading("Category",text="category")
        self.productTable.heading("Supplier",text="Supplier")
        self.productTable.heading("name",text="Name")
        self.productTable.heading("qty",text="Quantity")
        self.productTable.heading("status",text="Status")
        self.productTable.heading("cp",text="Cost Price")
        self.productTable.heading("sp",text="Selling Price")
        self.productTable["show"]="headings"

        self.productTable.column("pid",width=100)
        self.productTable.column("Category",width=100)
        self.productTable.column("Supplier",width=100)
        self.productTable.column("name",width=100)
        self.productTable.column("qty",width=100)
        self.productTable.column("status",width=100)
        self.productTable.column("cp",width=100)
        self.productTable.column("sp",width=100)
        self.productTable.pack(fill=BOTH,expand=1)
        self.productTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()
        

        #functions

    def fetch_cat_sup(self):
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select name from category")
            cat=cur.fetchall()
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])

            cur.execute("Select name from supplier")
            sup=cur.fetchall()
            if len(sup)>0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cat.get()=="Select" or self.var_cat.get()=="Empty" or self.var_sup.get()=="Select" or self.var_name.get()=="":
                messagebox.showerror("Error","All fields are required",parent=self.root)
            else :
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This product ID is already assigned, try a different one",parent=self.root)
                else:
                    cur.execute("Insert into product (Category,Supplier,name,qty,status,cp,sp) values(?,?,?,?,?,?,?)",(
                                        self.var_cat.get(),
                                        self.var_sup.get(),
                                        self.var_name.get(),
                                        self.var_qty.get(),
                                        self.var_status.get(),
                                        self.var_cost_price.get(),
                                        self.var_sell_price.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Product added successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        
    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            rows=cur.fetchall()
            self.productTable.delete(* self.productTable.get_children())
            for row in rows:
                self.productTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        
    def  get_data(self,ev):
        f= self.productTable.focus()
        content=( self.productTable.item(f))
        row=content['values']
        self.var_pid.set(row[0]),
        self.var_cat.set(row[1]),
        self.var_sup.set(row[2]),
        self.var_name.set(row[3]),
        self.var_qty.set(row[4]),
        self.var_status.set(row[5]),
        self.var_cost_price.set(row[6]),
        self.var_sell_price.set(row[7]),
        

    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","product ID is required",parent=self.root)
            else :
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid product ID",parent=self.root)
                else:
                    cur.execute("Update product set Category=?,Supplier=?,name=?,qty=?,status=?,cp=?,sp=? where pid=?",(
                                        self.var_cat.get(),
                                        self.var_sup.get(),
                                        self.var_name.get(),
                                        self.var_qty.get(),
                                        self.var_status.get(),
                                        self.var_cost_price.get(),
                                        self.var_sell_price.get(),
                                        self.var_pid.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success","product updated successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","product ID is required",parent=self.root)
            else :
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid product ID",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from product where pid=?",(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete ","product Deleted Successfully",parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def clear(self):
        f= self.productTable.focus()
        content=( self.productTable.item(f))
        row=content['values']
        self.var_pid.set(""),
        self.var_cat.set("Select"),
        self.var_sup.set("Select"),
        self.var_name.set(""),
        self.var_qty.set(""),
        self.var_status.set("Active"),
        self.var_cost_price.set(""),
        self.var_sell_price.set(""),
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()


    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if(self.var_searchby.get()=="Select"):
                messagebox.showerror("Error","Select search by option",parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("select * from product where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.productTable.delete(* self.productTable.get_children())
                    for row in rows:
                        self.productTable.insert('',END,values=row)
                else :
                    messagebox.showerror("Error","No record found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


if __name__=="__main__":
    root=Tk()
    obj=productClass(root)
    root.mainloop()