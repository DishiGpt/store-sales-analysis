import sqlite3
def create_db():
    con=sqlite3.connect(database=r'ims.db')
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT,name text,email text,gender text,contact text,dob text,doj text,password text ,utype text,address text,salary text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS supplier(invoice INTEGER PRIMARY KEY AUTOINCREMENT,name text,contact text,email text,desc text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY AUTOINCREMENT,name text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS product(pid INTEGER PRIMARY KEY AUTOINCREMENT,Category text,Supplier text,name text,qty text,status text,cp text,sp text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS sales(sid INTEGER PRIMARY KEY , cname text,contact text,pid text,pname text,qty INTEGER,price REAL,date text,discount REAL)")
    con.commit()


create_db()