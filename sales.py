from tkinter import *
from PIL import Image,ImageTk #pip intall pillow
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import os
class salesClass:
    def __init__(self,root):
        self.root=root #this is to define that this object is of the class itself & ca be used in functions to modify
        self.root.geometry("1000x500+220+130")
        self.root.title("Inventroy management system | Developed by Dishi")
        self.root.config(bg="white")
        self.root.focus_force()

        self.bill_list=[]
        self.var_invoice=StringVar()

        #title
        lbl_title=Label(self.root,text="View Customer Bills",font=(15),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X,padx=10,pady=20)

        lbl_invoice=Label(self.root,text="Invoice No.",font=(15),bg="white").place(x=50,y=100)
        txt_invoice=Entry(self.root,textvariable=self.var_invoice,font=(15),bg="white",bd=2).place(x=160,y=100,width=180,height=28)

        btn_search=Button(self.root,text="Search",command=self.search,bg="#F5F5DC",bd=2,relief=RIDGE,cursor="hand2",fg="green",font=("bold)",10)).place(x=360,y=100,width=120,height=28)
        btn_clear=Button(self.root,text="Clear",command=self.clear,bg="#F5F5DC",bd=2,relief=RIDGE,cursor="hand2",fg="green",font=("bold)",10)).place(x=490,y=100,width=120,height=28)

        #bill list
        sales_Frame=Frame(self.root,bd=3,relief=RIDGE,bg="white")
        sales_Frame.place(x=50,y=140,width=200,height=330)

        scrolly=Scrollbar(sales_Frame,orient=VERTICAL)
        self.sales_list=Listbox(sales_Frame,font=(15),bg="white",yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.sales_list.yview)
        self.sales_list.pack(fill=BOTH,expand=1)
        self.sales_list.bind("<ButtonRelease-1>",self.get_data)

        # bill area
        bill_Frame=Frame(self.root,bd=3,relief=RIDGE,bg="white")
        bill_Frame.place(x=280,y=140,width=330,height=330)

        lbl_title2=Label(bill_Frame,text="Customer Bills Area",font=(15),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)

        scrolly2=Scrollbar(bill_Frame,orient=VERTICAL)
        self.bill_area=Text(bill_Frame,bg="white",yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH,expand=1)

        self.show()
        
        #function

    def show(self):
        del self.bill_list[:]
        self.sales_list.delete(0,END)
        for i in os.listdir('bill'):
            if i.split('.')[-1]=='txt':
                self.sales_list.insert(END,i)
                self.bill_list.append(i.split('.')[0])

    def get_data(self,ev):
        index=self.sales_list.curselection()
        file_name=self.sales_list.get(index)
        self.bill_area.delete('1.0',END)
        fp=open(f'bill/{file_name}','r')
        for i in fp:
            self.bill_area.insert(END,i)
        fp.close()

    def search(self):
        if self.var_invoice.get()=="":
            messagebox.showerror("Error","Invoice no. is required",parent=self.root)
        else:
            if self.var_invoice.get() in self.bill_list:
                fp=open(f'bill/{self.var_invoice.get()}.txt','r')
                self.bill_area.delete('1.0',END)
                for i in fp:
                    self.bill_area.insert(END,i)
                fp.close()
            else:
                messagebox.showerror("Error","Invoice no. is invalid",parent=self.root)

    def clear(self):
        self.show()
        self.var_invoice.set("")
        self.bill_area.delete('1.0',END)


if __name__=="__main__":
    root=Tk()
    obj=salesClass(root)
    root.mainloop()