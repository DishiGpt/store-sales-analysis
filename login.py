from tkinter import *
import sqlite3
import os
from tkinter import messagebox
import email_pass
import time
import smtplib
class Login_system:
    def __init__(self,root):
        self.root=root
        self.root.title("Inventory Management system | Login page")
        self.root.geometry("1350x700+0+0")

        self.otp=''

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

        btn_forget=Button(login_frame,text="Forget Password",command=self.forget_window,font=("times new roman",13,"bold"),bd=0,bg="white",fg="#00759E",activebackground="white",activeforeground="#00759E",cursor="hand2").place(x=113,y=350)

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
            cur.execute("select utype from employee where eid=? AND password=?",(self.employee_id.get(),self.password.get()))
            user=cur.fetchone()
            if user==None:
                messagebox.showerror("Error","invalid Username or Password",parent=self.root)
            else:
                if user[0]=="Admin":
                    self.root.destroy()
                    os.system("python dashboard.py")
                else:
                    self.root.destroy()
                    os.system("python billing.py")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def forget_window(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.employee_id.get()=="":
                messagebox.showerror("Error","Employee ID is required",parent=self.root)
            else:
                cur.execute("select email from employee where eid=? ",(self.employee_id.get(),))
                email=cur.fetchone()
                if email==None:
                    messagebox.showerror("Error","invalid Employee ID",parent=self.root)
                else:
                    #forget window
                    self.var_otp=StringVar()
                    self.var_new_pass=StringVar()
                    self.var_conf_pass=StringVar()
                    """chk=self.send_email_(email[0])
                    if chk!='s':
                        messagebox.showerror("Error","Connection failed,parent=self.root)
                    else:
                        put rest part in else   """
                    self.forget_win=Toplevel(self.root,bg="white")
                    self.forget_win.title('Reset Password')
                    self.forget_win.geometry('400x350+500+100')
                    self.forget_win.focus_force()

                    titlef=Label(self.forget_win,text="Reset Password",font=("times new roman",15,"bold"),bg="white").pack(side=TOP,fill=X)
                    lbl_reset=Label(self.forget_win,text="Enter OTP sent on registered Email",font=("times new roman",15),bg="white").place(x=20,y=60)
                    txt_reset=Entry(self.forget_win,textvariable=self.var_otp,font=("times new roman",15),bg="white").place(x=20,y=100,width=250,height=30)

                    self.btn_reset=Button(self.forget_win,text="Submit",font=("times new roman",10),bg="lightgray")#command=self.validate
                    self.btn_reset.place(x=280,y=100,width=100,height=30)

                    lbl_new_pass=Label(self.forget_win,text="New Password",font=("times new roman",15),bg="white").place(x=20,y=160)
                    txt_new_pass=Entry(self.forget_win,textvariable=self.var_new_pass,font=("times new roman",15),bg="white").place(x=20,y=190,width=250,height=30)

                    lbl_c_pass=Label(self.forget_win,text="Confirm Password",font=("times new roman",15),bg="white").place(x=20,y=225)
                    txt_c_pass=Entry(self.forget_win,textvariable=self.var_conf_pass,font=("times new roman",15),bg="white").place(x=20,y=255,width=250,height=30)

                    self.btn_update=Button(self.forget_win,text="Update",state="disabled",font=("times new roman",10),bg="lightgray")#command=self.update_password()
                    self.btn_update.place(x=150,y=300,width=100,height=30)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    """

    def update_password(self):
        if self.var_new_pass.get()=="" or self.var_conf_pass=="":
            messagebox.showerror("Error","Password is required".parent=self.forget_win)
        elif self.var_new_pass.get()!= self.var_conf_pass:
            messagebox.showerror("Error","Password must be same".parent=self.forget_win)
        else:
            con=sqlite3.connect(database=r'ims.db')
            cur=con.cursor()
            try:
                cur.execute("Update employee  SET password=? where eid=?",(self.var_new_pass.get(),self.employee_id.get()))
                con.commit()
                messagebox.showinfo("Success","Password updated",parent=slef.forget_win)
                self.forget_win.destroy()
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def validate(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.btn_update.config(state=NORMAL)
            self.btn_reset.config(state=DISABLED)
        else:
            messagebox.showerror("Error","invalid OTP \ntry again",parent=self.forget_win)
    
    
    def send_email_(self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_=email_pass.email_
        pass_=email_pass.pass_

        s.login(email_,pass_)

        self.otp=str(time.strftime("%H%M%S"))+str(time.strftime("%S"))
        subj='IMS-Reset Password OTP'  
        msg='OTP for password reset is {str(self.otp)}'
        msg="Subject:{}\n\n{}".format(subj,msg)
        s.sendmail(email,to_,msg)
        chk=s.ehlo()  
        if chk[0]==250:
            return 's' 
        else:
            return 'f'     
        """


root=Tk()
obj=Login_system(root)
root.mainloop()