from tkinter import *
from PIL import Image,ImageTk
import sqlite3
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
import time
import os
import tempfile
class billClass:
    def __init__(self,root):
        self.root=root #this is to define that this object is of the class itself & ca be used in functions to modify
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventroy management system | Developed by Dishi")
        self.root.config(bg="white")
        self.cart_list=[]
        self.var_sid=StringVar()
        self.quantity=StringVar()
        self.var_date=StringVar()
        self.discount=0
        self.chk_print=0

        #title
        self.icon_title=PhotoImage(file="images/icon.png")
        title=Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#4a68b3",fg="#F0F0F0",anchor="w",padx=20,pady=20).place(x=0,y=0,relwidth=1,height=70)
        
        #button
        btn_logout=Button(self.root,text="logout",command=self.logout,font=("times new roman",15,"bold"),bg="red",cursor="hand2").place(x=1200,y=20,height=30,width=70)

        #clock
        self.lbl_clock=Label(self.root,text="Welcome to Inventory management system\t\t Date: DD/MM/YYYY\t\t Time:  HH/MM/SS",font=("times new roman",15,),bg="#333333",fg="#F0F0F0")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #product frame
        self.var_search=StringVar()

        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        ProductFrame1.place(x=6,y=110,width=410,height=570)

        ptitle=Label(ProductFrame1,text="All Products",font=("times new roman",20,"bold"),bg="#262680",fg="white").pack(side=TOP,fill=X)

        #product search frame
        ProductFrame2=Frame(ProductFrame1,bd=4,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=42,width=398,height=90)

        lbl_search=Label(ProductFrame2,text="Search Product | By Name ",font=("times new roman",15,"bold"),bg="white").place(x=2,y=5)

        lbl_search1=Label(ProductFrame2,text="Product Name",font=("times new roman",15,"bold"),bg="white").place(x=5,y=45)
        self.txt_search1=Entry(ProductFrame2,textvariable=self.var_search,font=("times new roman",15),bg="white").place(x=133,y=47,width=130,height=22)
        btn_search=Button(ProductFrame2,text="Search",command=self.search,bg="#F5F5DC",bd=2,relief=RIDGE,cursor="hand2",fg="green",font=("bold)",10)).place(x=280,y=47,width=100,height=22)
        btn_show_all=Button(ProductFrame2,text="Show All",command=self.show,bg="#F5F5DC",bd=2,relief=RIDGE,cursor="hand2",fg="green",font=("bold)",10)).place(x=280,y=10,width=100,height=22)

        ProductFrame3=Frame(ProductFrame1,bd=3,relief=RIDGE)  
        ProductFrame3.place(x=2,y=150,width=398,height=385)

        scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)

        self.product_Table=ttk.Treeview(ProductFrame3,columns=("pid","name","sp","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)
        self.product_Table.heading("pid",text="PID")
        self.product_Table.heading("name",text="Name")
        self.product_Table.heading("sp",text="Price")
        self.product_Table.heading("qty",text="Quantity")
        self.product_Table.heading("status",text="Status")
        self.product_Table["show"]="headings"

        self.product_Table.column("pid",width=60)
        self.product_Table.column("name",width=60)
        self.product_Table.column("sp",width=60)
        self.product_Table.column("qty",width=60)
        self.product_Table.column("status",width=60)
        self.product_Table.pack(fill=BOTH,expand=1)
        self.product_Table.bind("<ButtonRelease-1>",self.get_data)

        lbl_note=Label(ProductFrame1,text="Note:'Enter 0 quantity to remove product from cart'",bg="white",fg="red",anchor="w").pack(side=BOTTOM,fill=X)

        #customer frame
 
        self.var_cname=StringVar()
        self.var_contact=StringVar()

        CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        CustomerFrame.place(x=420,y=110,width=530,height=70)

        ctitle=Label(CustomerFrame,text="Customer Details",font=("times new roman",15),bg="light gray").pack(side=TOP,fill=X)

        lbl_name=Label(CustomerFrame,text="Name",font=("times new roman",15),bg="white").place(x=5,y=35)
        txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("times new roman",13),bg="white").place(x=65,y=35,width=170)

        lbl_contact=Label(CustomerFrame,text="Contact No.",font=("times new roman",15),bg="white").place(x=245,y=35)
        txt_contact=Entry(CustomerFrame,textvariable=self.var_contact,font=("times new roman",13),bg="white").place(x=355,y=35,width=160)

        #calculator cart frame

        cal_cart_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        cal_cart_Frame.place(x=420,y=190,width=530,height=360)

        #calculator frame

        self.var_cal_input=StringVar()
        cal_Frame=Frame(cal_cart_Frame,bd=8,relief=RIDGE,bg="white")
        cal_Frame.place(x=5,y=10,width=268,height=340)

        txt_cal_input=Entry(cal_Frame,textvariable=self.var_cal_input,font=(15),width=21,bd=8,relief=GROOVE,state='readonly',justify=RIGHT)
        txt_cal_input.grid(row=0,columnspan=4)

        btn_7=Button(cal_Frame,text='7',font=('times new roman',15,'bold'),command=lambda:self.get_input(7),bd=5,width=4,pady=13,cursor="hand2").grid(row=1,column=0)
        btn_8=Button(cal_Frame,text='8',font=('times new roman',15,'bold'),command=lambda:self.get_input(8),bd=5,width=4,pady=13,cursor="hand2").grid(row=1,column=1)
        btn_9=Button(cal_Frame,text='9',font=('times new roman',15,'bold'),command=lambda:self.get_input(9),bd=5,width=4,pady=13,cursor="hand2").grid(row=1,column=2)
        btn_sum=Button(cal_Frame,text='+',font=('times new roman',15,'bold'),command=lambda:self.get_input('+'),bd=5,width=4,pady=13,cursor="hand2").grid(row=1,column=3)

        btn_4=Button(cal_Frame,text='4',font=('times new roman',15,'bold'),command=lambda:self.get_input(4),bd=5,width=4,pady=13,cursor="hand2").grid(row=2,column=0)
        btn_5=Button(cal_Frame,text='5',font=('times new roman',15,'bold'),command=lambda:self.get_input(5),bd=5,width=4,pady=13,cursor="hand2").grid(row=2,column=1)
        btn_6=Button(cal_Frame,text='6',font=('times new roman',15,'bold'),command=lambda:self.get_input(6),bd=5,width=4,pady=13,cursor="hand2").grid(row=2,column=2)
        btn_sub=Button(cal_Frame,text='-',font=('times new roman',15,'bold'),command=lambda:self.get_input('-'),bd=5,width=4,pady=13,cursor="hand2").grid(row=2,column=3)

        btn_1=Button(cal_Frame,text='1',font=('times new roman',15,'bold'),command=lambda:self.get_input(1),bd=5,width=4,pady=13,cursor="hand2").grid(row=3,column=0)
        btn_2=Button(cal_Frame,text='2',font=('times new roman',15,'bold'),command=lambda:self.get_input(2),bd=5,width=4,pady=13,cursor="hand2").grid(row=3,column=1)
        btn_3=Button(cal_Frame,text='3',font=('times new roman',15,'bold'),command=lambda:self.get_input(3),bd=5,width=4,pady=13,cursor="hand2").grid(row=3,column=2)
        btn_mul=Button(cal_Frame,text='*',font=('times new roman',15,'bold'),command=lambda:self.get_input('*'),bd=5,width=4,pady=13,cursor="hand2").grid(row=3,column=3)

        btn_0=Button(cal_Frame,text='0',font=('times new roman',15,'bold'),command=lambda:self.get_input(0),bd=5,width=4,pady=13,cursor="hand2").grid(row=4,column=0)
        btn_c=Button(cal_Frame,text='Clear',font=('times new roman',15,'bold'),command=self.clear_cal,bd=5,width=4,pady=13,cursor="hand2").grid(row=4,column=1)
        btn_eq=Button(cal_Frame,text='=',font=('times new roman',15,'bold'),command=self.perform_cal,bd=5,width=4,pady=13,cursor="hand2").grid(row=4,column=2)
        btn_div=Button(cal_Frame,text='/',font=('times new roman',15,'bold'),command=lambda:self.get_input('/'),bd=5,width=4,pady=13,cursor="hand2").grid(row=4,column=3)

        #cart frame

        cart_Frame=Frame(cal_cart_Frame,bd=3,relief=RIDGE)  
        cart_Frame.place(x=280,y=8,width=245,height=342)
        self.cartTitle=Label(cart_Frame,text="Cart \tTotal Products [0]",font=("times new roman",15),bg="light gray")
        self.cartTitle.pack(side=TOP,fill=X)


        scrolly=Scrollbar(cart_Frame,orient=VERTICAL)
        scrollx=Scrollbar(cart_Frame,orient=HORIZONTAL)

        self.cart_Table=ttk.Treeview(cart_Frame,columns=("pid","name","sp","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.cart_Table.xview)
        scrolly.config(command=self.cart_Table.yview)
        self.cart_Table.heading("pid",text="PID")
        self.cart_Table.heading("name",text="Name")
        self.cart_Table.heading("sp",text="Price")
        self.cart_Table.heading("qty",text="Quantity")
        self.cart_Table["show"]="headings"

        self.cart_Table.column("pid",width=40)
        self.cart_Table.column("name",width=100)
        self.cart_Table.column("sp",width=60)
        self.cart_Table.column("qty",width=60)
        self.cart_Table.pack(fill=BOTH,expand=1)
        self.cart_Table.bind("<ButtonRelease-1>",self.get_data_cart)
 
        #add cart widgets frame
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_qty=StringVar()
        self.var_price=StringVar()
        self.var_status=StringVar()
        self.var_stock=StringVar()

        cart_widgets_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        cart_widgets_Frame.place(x=420,y=550,width=530,height=140)

        lbl_p_name=Label(cart_widgets_Frame,text="Product Name",font=("times new roman",15),bg="white").place(x=5,y=5)
        txt_p_name=Entry(cart_widgets_Frame,textvariable=self.var_pname,font=("times new roman",15),bg="white",state="readonly").place(x=5,y=35,width=190,height=22)

        lbl_p_price=Label(cart_widgets_Frame,text="Price per quantity",font=("times new roman",15),bg="white").place(x=230,y=5)
        txt_p_price=Entry(cart_widgets_Frame,textvariable=self.var_price,font=("times new roman",15),bg="white",state="readonly").place(x=230,y=35,width=120,height=22)

        lbl_p_qty=Label(cart_widgets_Frame,text="Quantity",font=("times new roman",15),bg="white").place(x=390,y=5)
        txt_p_qty=Entry(cart_widgets_Frame,textvariable=self.var_qty,font=("times new roman",15),bg="white").place(x=390,y=35,width=120,height=22)

        self.lbl_inStock=Label(cart_widgets_Frame,text="In stock ",font=("times new roman",15),bg="white")
        self.lbl_inStock.place(x=5,y=70)

        btn_clear_cart=Button(cart_widgets_Frame,text="Clear",command=self.clear_cart,font=("times new roman",12),bg="beige",fg="green",cursor="hand2").place(x=180,y=70,width=80,height=30)
        btn_add_cart=Button(cart_widgets_Frame,text="Add | Update Cart",command=self.add_update_cart,font=("times new roman",12),bg="beige",fg="green",cursor="hand2").place(x=280,y=70,width=140,height=30)

        #billing area
        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billFrame.place(x=953,y=110,width=320,height=410)

        btitle=Label(billFrame,text="Customer Bill",font=("times new roman",20,"bold"),bg="#262680",fg="white").pack(side=TOP,fill=X)
        scrolly1=Scrollbar(billFrame,orient=VERTICAL)
        scrolly1.pack(side=RIGHT,fill=Y)
        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly1.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly1.config(command=self.txt_bill_area.yview)

 
        #billing buttons

        billmenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billmenuFrame.place(x=953,y=520,width=315,height=140)

        self.lbl_amount=Label(billmenuFrame,text="Bill Amount\n0",bg="beige",fg="green")
        self.lbl_amount.place(x=4,y=5,width=95,height=55)

        self.lbl_discount=Label(billmenuFrame,text="Discount\n%",bg="beige",fg="green")
        self.lbl_discount.place(x=106,y=5,width=95,height=55)

        self.lbl_net_pay=Label(billmenuFrame,text="Net pay\n0",bg="beige",fg="green")
        self.lbl_net_pay.place(x=208,y=5,width=95,height=55)

        btn_print=Button(billmenuFrame,text="Print",command=self.print_bill,bg="beige",fg="green",cursor="hand2")
        btn_print.place(x=4,y=70,width=90,height=40)

        btn_clear_all=Button(billmenuFrame,text="Clear All",command=self.clear_all,bg="beige",fg="green",cursor="hand2")
        btn_clear_all.place(x=106,y=70,width=90,height=40)

        btn_generate=Button(billmenuFrame,text="Generate & \nSave Bill",command=self.generate_bill,bg="beige",fg="green",cursor="hand2")
        btn_generate.place(x=208,y=70,width=95,height=40)

        #footer
        footer=Label(self.root,text="IMS - Inventory Management System ",bg="gray",fg="white").pack(side=BOTTOM,fill=X)
        self.show()
        self.update_date_time()

        #functions

    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum) 

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            #self.product_Table=ttk.Treeview(ProductFrame3,columns=("pid","Category","Supplier","name","qty","status","cp","sp"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
            cur.execute("select pid,name,sp,qty,status from product where status='Active'")
            rows=cur.fetchall()
            self.product_Table.delete(* self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("select pid,name,sp,qty,status from product where name LIKE '%"+self.var_search.get()+"%' and status='Active'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_Table.delete(* self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('',END,values=row)
                else :
                    messagebox.showerror("Error","No record found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def  get_data(self,ev):
        f= self.product_Table.focus()
        content=(self.product_Table.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"In stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')

    def  get_data_cart(self,ev):
        f= self.cart_Table.focus()
        content=(self.cart_Table.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_inStock.config(text=f"In stock [{str(row[4])}]")
        self.var_stock.set(row[4])
        

    def add_update_cart(self):
        if self.var_pid.get()=='':
             messagebox.showerror("Error","Please select product from list",parent=self.root)
        elif self.var_qty.get()=='':
            messagebox.showerror("Error","Quantity is required",parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror("Error","Quantity is out of bounds",parent=self.root)
        else:
            price_cal=self.var_price.get()
            cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]
            #update cart
            present='no'
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1
            if present=='yes':
                op=messagebox.askyesno('Confirm',"Product already in cart\nDo you want to update | Remove from cart list",parent=self.root)
                if op==True:
                    if self.var_qty.get()=='0':
                        self.cart_list.pop(index_)
                    else:
                        #self.cart_list[index_][2]=price_cal 
                        self.cart_list[index_][3]=self.var_qty.get()
            else:
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_updates()

    def bill_updates(self):
        discount_str=simpledialog.askstring("Enter discount","Enter discount number :",parent=self.root)
        discount_per=float(discount_str)
        self.bill_amt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            self.bill_amt+=(float(row[2]))*int(row[3])
        self.discount=(self.bill_amt*discount_per)/100 
        #self.discount=(self.bill_amt*5)/100
        self.net_pay=self.bill_amt-self.discount
        self.lbl_amount.config(text=f'Bill Amount(Rs.)\n{str(self.bill_amt)}')
        self.lbl_net_pay.config(text=f'Net Amount(Rs.)\n{str(self.net_pay)}')
        self.lbl_discount.config(text=f'Discount\n{str(discount_per)}%')
        self.cartTitle.config(text= f'Cart \tTotal Products [{str(len(self.cart_list))}]')


    def show_cart(self):
        try:
            self.cart_Table.delete(* self.cart_Table.get_children())
            for row in self.cart_list:
                self.cart_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


    def generate_bill(self):
        if self.var_cname.get()=='' or self.var_contact.get()=='':
            messagebox.showerror("Error","Customer details are required",parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error","Please add product(s) to the cart",parent=self.root)
        else:
            self.bill_top()
            self.bill_middle()
            self.bill_bottom()
            
            fp=open(f'bill/{str(self.invoice)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            self.add()
            messagebox.showinfo("Saved","Bill has been generated/Saved",parent=self.root)
            self.chk_print=1

    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        self.var_sid.set(self.invoice)
        bill_top_temp=f'''
\t    XYZ-Inventory
 Phone No. 98725***** , Delhi-125001
{str("="*36)}
 Customer Name: {self.var_cname.get()}
 Ph no. :{self.var_contact.get()} 
 Bill No. {str(self.invoice)}\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*36)}
 Product Name\t\tQTY\tPrice
{str("="*36)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*36)}
 Bill Amount\t\t\tRs.{self.bill_amt}
 Discount\t\t\tRs.{self.discount}
 Net Pay\t\t\tRs.{self.net_pay}
{str("="*36)}\n
        '''
        self.txt_bill_area.insert(END,bill_bottom_temp)


    def bill_middle(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            for row in self.cart_list:
                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status='Inactive'
                if int(row[3])!=int(row[4]):
                    status='Active'
                price=float(row[2])*int(row[3])
                price=str(price)
                self.txt_bill_area.insert(END,"\n "+name+"\t\t"+row[3]+"\tRs."+price)
                #update quantity in product table
                cur.execute('Update product set qty=?,status=? where pid=?',(
                    qty,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_inStock.config(text=f"In stock")
        self.var_stock.set('') 

    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0',END)
        self.var_search.set('')
        self.cartTitle.config(text= f'Cart \tTotal Products [0]')
        self.chk_print=0
        self.clear_cart()
        self.show()
        self.show_cart()

    def update_date_time(self):
        time_stmp=time.strftime("%H:%M:%S")
        date_stmp=time.strftime("%d/%m/%Y")
        self.var_date=date_stmp
        self.lbl_clock.config(text=f"Welcome to Inventory management system\t\t Date: {str(date_stmp)}\t\t Time:  {str(time_stmp)}")
        self.lbl_clock.after(200,self.update_date_time)

    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo('Print',"Please wait while printing",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')
        else:
            messagebox.showerror("Error","Please generate bill before printing",parent=self.root)

    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            for row in self.cart_list:
                cur.execute("INSERT INTO sales(sid,cname,contact,pid,pname,qty,price,date,discount) VALUES(?,?,?,?,?,?,?,?,?)",
                            (
                                self.var_sid.get(),
                                self.var_cname.get(),
                                self.var_contact.get(),
                                row[0],
                                row[1],
                                row[3],
                                row[2],
                                self.var_date,
                                self.discount
                            ))
                con.commit()
                messagebox.showinfo("Success","Order saved sccessfully",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")


if __name__=="__main__":
    root=Tk()
    obj=billClass(root)
    root.mainloop()  #this is so the program doen't run & exit but stays
