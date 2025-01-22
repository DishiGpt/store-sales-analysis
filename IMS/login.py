from tkinter import *
import sqlite3
import os
from tkinter import messagebox
class Login_system:
    def __init__(self,root):
        self.root=root
        self.root.title("Inventory Management system | Login page")
        self.root.geometry("1350x700+0+0")

        self.employee_id=StringVar()
        self.password=StringVar()

        #login frame
        login_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        login_frame.place(x=500,y=90,width=350,height=460)

        title=Label(login_frame,text="Login System",font=("times new roman",20,"bold"),bg="white").place(x=0,y=30,relwidth=1)

        lbl_user=Label(login_frame,text="Employee ID",font=("times new roman",15),bg="white").place(x=40,y=100)
        txt_user=Entry(login_frame,textvariable=self.employee_id,font=("times new roman",15),bg="#ECECEC").place(x=40,y=140,width=250)

        lbl_pass=Label(login_frame,text="Password",font=("times new roman",15),bg="white").place(x=40,y=180)
        txt_pass=Entry(login_frame,textvariable=self.password,show="*",font=("times new roman",15),bg="#ECECEC").place(x=40,y=220,width=250)

        btn_login=Button(login_frame,text="Log In",command=self.login,font=("times new roman",15),bg="#00B0F0",fg="white",cursor="hand2",activebackground="#00B0F0",activeforeground="white").place(x=125,y=270,width=100,height=35)

        hr=Label(login_frame,bg="lightgray").place(x=40,y=325,width=250,height=2)
        or_=Label(login_frame,text="OR",fg="lightgray",font=("times new roman",),bg="white").place(x=150,y=312)

        btn_forget=Button(login_frame,text="Forget Password",font=("times new roman",13,"bold"),bd=0,bg="white",fg="#00759E",activebackground="white",activeforeground="#00759E",cursor="hand2").place(x=113,y=350)

        # register frame
        register_frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        register_frame.place(x=500,y=570,width=350,height=60)

        lbl_register=Label(register_frame,text="Quit as an admin ",font=("times new roman",13),bg="white").place(x=0,y=15,relwidth=1)
        
    def login(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="" or self.password.get()=="":
                messagebox.showerror("Error","all fields are required",parent=self.root)
            cur.execute("select * from employee where eid=? AND password=?",(self.employee_id.get(),self.password.get()))
            user=cur.fetchone()
            if user==None:
                messagebox.showerror("Error","invalid Username or Password",parent=self.root)
            else:
                self.root.destroy()
                os.system("python dashboard.py")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


        

root=Tk()
obj=Login_system(root)
root.mainloop()