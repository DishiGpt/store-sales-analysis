from tkinter import *
from PIL import Image,ImageTk #pip intall pillow
from tkinter import ttk
from tkinter import messagebox
import sqlite3
class categoryClass:
    def __init__(self,root):
        self.root=root #this is to define that this object is of the class itself & ca be used in functions to modify
        self.root.geometry("1000x500+220+130")
        self.root.title("Inventroy management system | Developed by Dishi")
        self.root.config(bg="white")
        self.root.focus_force()

        #variables
        self.var_cat_id=StringVar()
        self.var_name=StringVar()

        #title
        lbl_title=Label(self.root,text="Manage Product Category",font=(15),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X,padx=10,pady=20)
        lbl_name=Label(self.root,text="Enter Category Name",font=(15),bg="white").place(x=50,y=100)

        txt_name=Entry(self.root,textvariable=self.var_name,font=(15),bg="white").place(x=50,y=150,width=300)

        btn_add=Button(self.root,text="Add",command=self.add,bg="#F5F5DC",bd=2,relief=RIDGE,cursor="hand2",fg="green",font=("bold)",10)).place(x=50,y=200,height=30,width=110)
        btn_delete=Button(self.root,text="Delete",command=self.delete,bg="#F5F5DC",bd=2,relief=RIDGE,cursor="hand2",fg="green",font=("bold)",10)).place(x=200,y=200,height=30,width=110)  
        btn_clear=Button(self.root,text="Clear",command=self.clear,bg="#F5F5DC",bd=2,relief=RIDGE,cursor="hand2",fg="green",font=("bold)",10)).place(x=350,y=200,width=110,height=30)  

         #Category details

        cat_frame=Frame(self.root,bd=3,relief=RIDGE)  
        cat_frame.place(x=0,y=300,relwidth=1,height=250)

        scrolly=Scrollbar(cat_frame,orient=VERTICAL)
        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)

        self.CategoryTable=ttk.Treeview(cat_frame,columns=("cid","name"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CategoryTable.xview)
        scrolly.config(command=self.CategoryTable.yview)

        self.CategoryTable.heading("cid",text="Category ID")
        self.CategoryTable.heading("name",text="Name")
        
        self.CategoryTable["show"]="headings"

        self.CategoryTable.column("cid",width=70)
        self.CategoryTable.column("name",width=70)
        
        self.CategoryTable.pack(fill=BOTH,expand=1)
        self.CategoryTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()    

    #functions

    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","Category Name is required",parent=self.root)
            else :
                cur.execute("Select * from category where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Category already exists, try a different one",parent=self.root)
                else:
                    cur.execute("Insert into  category(name) values(?)",(
                                        self.var_name.get(),
                                        
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Category added successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from category")
            rows=cur.fetchall()
            self.CategoryTable.delete(*self.CategoryTable.get_children())
            for row in rows:
                self.CategoryTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        
    def  get_data(self,ev):
        f=self.CategoryTable.focus()
        content=(self.CategoryTable.item(f))
        row=content['values']
        #print(row)
        self.var_cat_id.set(row[0]),
        self.var_name.set(row[1]),
        

    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cat_id.get()=="":
                messagebox.showerror("Error","Please select category from the list",parent=self.root)
            else :
                cur.execute("Select * from category where cid=?",(self.var_cat_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Category ID.",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from category where cid=?",(self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete ","Category Deleted Successfully",parent=self.root)
                        self.clear()
                        self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

        
    def clear(self):
        f=self.CategoryTable.focus()
        content=(self.CategoryTable.item(f))
        row=content['values']
        #print(row)
        self.var_cat_id.set(""),
        self.var_name.set(""),
        self.show()




if __name__=="__main__":
    root=Tk()
    obj=categoryClass(root)
    root.mainloop()