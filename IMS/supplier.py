from tkinter import *
from PIL import Image,ImageTk #pip intall pillow
from tkinter import ttk
from tkinter import messagebox
import sqlite3
class supplierClass:
    def __init__(self,root):
        self.root=root #this is to define that this object is of the class itself & ca be used in functions to modify
        self.root.geometry("1000x500+220+130")
        self.root.title("Inventroy management system | Developed by Dishi")
        self.root.config(bg="white")
        self.root.focus_force()
        
        #all variables
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        self.var_sup_invoice=StringVar()
        self.var_contact=StringVar()
        self.var_name=StringVar()
        self.var_email=StringVar()


        #search
        #self.root=LabelFrame(self.root,text="Search Supplier",font=("times new roman",15,"bold"),bd=2,relief=RIDGE,bg="white")
        #self.root.place(x=250,y=20,width=600,height=70)

        #option
        lbl_search=Label(self.root,text="Search by Invoice No.",bg="white",font=(15)) #justify=CENTER
        lbl_search.place(x=500,y=70)

        txt_search=Entry(self.root,textvariable=self.var_searchtxt,bd=2,relief=RIDGE).place(x=700,y=70,width=200)   #for single row Entry for multiple Text
        btn_search=Button(self.root,text="Search",command=self.search,bg="#F5F5DC",bd=2,relief=RIDGE,cursor="hand2",fg="green",font=("bold)",10)).place(x=950,y=69,width=150,height=22)

        #title
        title=Label(self.root,text="Supplier Details",font=(15),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X,padx=10,pady=20)

        #content
        #row 1
        lbl_supplier_invoice=Label(self.root,text="Invoice No.",font=(15),bg="white").place(x=50,y=70)
        txt_supplier_invoice=Entry(self.root,textvariable=self.var_sup_invoice,font=(15),bg="white",bd=2).place(x=180,y=70,width=180)
        

        #row 2
        lbl_name=Label(self.root,text="Name",font=(15),bg="white").place(x=50,y=120)
        txt_name=Entry(self.root,textvariable=self.var_name,font=(15),bg="white",bd=2).place(x=180,y=120,width=180)
        
        #row 3
        lbl_contact=Label(self.root,text="Contact",font=(15),bg="white").place(x=50,y=170)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=(15),bg="white",bd=2).place(x=180,y=170,width=180)

        #row 4
        lbl_email=Label(self.root,text="Email",font=(15),bg="white").place(x=50,y=220)
        txt_email=Entry(self.root,textvariable=self.var_email,font=(15),bg="white",bd=2).place(x=180,y=220,width=180)
        

        #row 4
        lbl_desc=Label(self.root,text="Description",font=(15),bg="white").place(x=50,y=270) 
        self.txt_desc=Text(self.root,font=(15),bg="white",bd=2)
        self.txt_desc.place(x=180,y=270,width=300,height=60)
        
        #buttons
        btn_add=Button(self.root,text="Save",command=self.add,bg="#F5F5DC",bd=2,relief=RIDGE,cursor="hand2",fg="green",font=("bold)",10)).place(x=180,y=370,width=110,height=28)
        btn_update=Button(self.root,text="Update",command=self.update,bg="#F5F5DC",bd=2,relief=RIDGE,cursor="hand2",fg="green",font=("bold)",10)).place(x=300,y=370,width=110,height=28)
        btn_delete=Button(self.root,text="Delete",command=self.delete,bg="#F5F5DC",bd=2,relief=RIDGE,cursor="hand2",fg="green",font=("bold)",10)).place(x=420,y=370,width=110,height=28)
        btn_clear=Button(self.root,text="Clear",command=self.clear,bg="#F5F5DC",bd=2,relief=RIDGE,cursor="hand2",fg="green",font=("bold)",10)).place(x=540,y=370,width=110,height=28)

        #Supplier details

        emp_frame=Frame(self.root,bd=3,relief=RIDGE)  
        emp_frame.place(x=0,y=410,relwidth=1,height=150)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.SupplierTable=ttk.Treeview(emp_frame,columns=("invoice","name","contact","email","desc"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.SupplierTable.xview)
        scrolly.config(command=self.SupplierTable.yview)
        self.SupplierTable.heading("invoice",text="Invoice No.")
        self.SupplierTable.heading("name",text="Name")
        self.SupplierTable.heading("contact",text="Contact")
        self.SupplierTable.heading("email",text="Email")
        self.SupplierTable.heading("desc",text="Description")
        self.SupplierTable["show"]="headings"

        self.SupplierTable.column("invoice",width=100)
        self.SupplierTable.column("name",width=100)
        self.SupplierTable.column("contact",width=100)
        self.SupplierTable.column("email",width=100)
        self.SupplierTable.column("desc",width=100)
        self.SupplierTable.pack(fill=BOTH,expand=1)
        self.SupplierTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()
 
    #functions
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice No. is required",parent=self.root)
            else :
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Invoice No. is already assigned, try a different one",parent=self.root)
                else:
                    cur.execute("Insert into supplier (invoice,name,contact,email,desc) values(?,?,?,?,?)",(
                                        self.var_sup_invoice.get(),
                                        self.var_name.get(),
                                        self.var_contact.get(),
                                        self.var_email.get(),
                                        self.txt_desc.get('1.0',END),
                                        
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier added successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        
    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from supplier")
            rows=cur.fetchall()
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                self.SupplierTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        
    def  get_data(self,ev):
        f=self.SupplierTable.focus()
        content=(self.SupplierTable.item(f))
        row=content['values']
        #print(row)
        self.var_sup_invoice.set(row[0]),
        self.var_name.set(row[1]),
        self.var_contact.set(row[2]),
        self.var_email.set(row[3]),
        self.txt_desc.delete('1.0',END),
        self.txt_desc.insert(END,row[4])

    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice No. is required",parent=self.root)
            else :
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice No.",parent=self.root)
                else:
                    cur.execute("Update supplier set name=?,contact=?,email=?,desc=? where invoice=?",(
                                        self.var_name.get(),
                                        self.var_contact.get(),
                                        self.var_email.get(),
                                        self.txt_desc.get('1.0',END),
                                        self.var_sup_invoice.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier updated successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice No. is required",parent=self.root)
            else :
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice No.",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from supplier where invoice=?",(self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete ","Supplier Deleted Successfully",parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def clear(self):
        f=self.SupplierTable.focus()
        content=(self.SupplierTable.item(f))
        row=content['values']
        #print(row)
        self.var_sup_invoice.set(""),
        self.var_name.set(""),
        self.var_contact.set(""),
        self.var_email.set(""),
        self.txt_desc.delete('1.0',END),
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:       
            if self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Invoice No. is required",parent=self.root)
            else:
                cur.execute("select * from supplier where invoice=?",(self.var_searchtxt.get(),))
                row=cur.fetchone()
                if row!=None:
                    self.SupplierTable.delete(*self.SupplierTable.get_children())
                    self.SupplierTable.insert('',END,values=row)
                else :
                    messagebox.showerror("Error","No record found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)



if __name__=="__main__":
    root=Tk()
    obj=supplierClass(root)
    root.mainloop()