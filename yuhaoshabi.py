import tkinter as tk
import sqlite3
from tkinter.constants import END, INSERT, RIGHT, X, Y
from tkinter import Pack, ttk

#连接数据库
conn = sqlite3.connect('my_db.db', check_same_thread = False)
#获取游标
cursor = conn.cursor()

try:
    cursor.execute('''
    CREATE TABLE "txl" (
        "name"	TEXT,
        "phone"	TEXT,
        "address"	TEXT,
        PRIMARY KEY("name")
    );  
    '''
    )
    print('通讯录创建成功')
except:
    print('通讯录已存在')

class txl:
    def __init__(self):
        #初始化
        self.mw = tk.Tk()
        self.mw.title('txl')
        self.mw.geometry('400x650+50+50')

        #分为左右两部分
        self.lf = tk.Frame(self.mw)
        self.lf.place(x = 10, y = 10)
        self.rt = tk.Frame(self.mw)
        self.rt.place(x = 250, y = 10)

        #创建列表
        self.tree_txl = ttk.Treeview(
            self.lf,
            show = 'headings', #创建表头
            columns = ('name', 'phone', 'address'), #创建属性
            height= 30,
            )
        #属性名
        self.tree_txl.heading('name', text='name')
        self.tree_txl.heading('phone', text='phone')
        self.tree_txl.heading('address', text='address')
        #属性宽度
        self.tree_txl.column('name', width=60)
        self.tree_txl.column('phone', width=70)
        self.tree_txl.column('address', width=80)
        self.tree_txl.pack()

        #插入通讯录数据
        txl = cursor.execute('''
                SELECT * FROM "main"."txl" ;
            '''
            ).fetchall()
        for i in txl:
            self.tree_txl.insert('','end',values=i)
        
        #创建插入按钮
        self.button_insert = tk.Button(
            self.rt,
            text = 'insert',
            command = self.insert,
            width=15,
            height=5,
        ).pack(pady=10)
        
        #创建删除按钮
        self.button_delete = tk.Button(
            self.rt,
            text = 'delete',
            command = self.delete,
            width=15,
            height=5,
        ).pack(pady=10)

        #创建修改按钮
        self.button_update = tk.Button(
            self.rt,
            text = 'update',
            command = self.update,
            width=15,
            height=5,
        ).pack(pady=10)

        #创建查询按钮
        self.button_select = tk.Button(
            self.rt,
            text = 'select',
            command = self.select,
            width=15,
            height=5,
        ).pack(pady=10)

        #创建刷新按钮
        self.button_overload = tk.Button(
            self.rt,
            text = 'Overload',
            command = self.overload,
            width=15,
            height=5,
        ).pack(pady=10)
        
        tk.mainloop()

    #创建插入窗口
    def insert(self):
        self.insert_w = tk.Tk()
        self.insert_w.title('Insert')
        self.insert_w.geometry('300x200+500+50')

        self.label_name = tk.Label(self.insert_w,text='name:').pack()
        self.insert_name = tk.Entry(self.insert_w)
        self.insert_name.pack()

        self.label_phone = tk.Label(self.insert_w,text='phone:').pack()
        self.insert_phone = tk.Entry(self.insert_w)
        self.insert_phone.pack()

        self.label_address = tk.Label(self.insert_w,text='address:').pack()
        self.insert_address = tk.Entry(self.insert_w)
        self.insert_address.pack()

        self.button_insert_w = tk.Button(
            self.insert_w,
            text='insert',
            command=self.insert_achieve,
        ).pack(pady=5)
        
    #实现插入功能
    def insert_achieve(self):
        self.name = str(self.insert_name.get())
        self.phone = str(self.insert_phone.get())
        self.address = str(self.insert_address.get())
        try:
            cursor.execute('''
                INSERT INTO "main"."txl"("name","phone","address") 
                VALUES (?,?,?);
            ''',(self.name,self.phone,self.address)
            )
            conn.commit()
            self.overload()
        except:
            print('姓名为:' + self.name + '的用户已存在')

    #创建删除窗口
    def delete(self):
        self.delete_w = tk.Tk()
        self.delete_w.title('Delete')
        self.delete_w.geometry('300x100+500+300')

        self.label_name = tk.Label(self.delete_w,text='name:').pack()
        self.delete_name = tk.Entry(self.delete_w)
        self.delete_name.pack()

        self.button_delete_w = tk.Button(
            self.delete_w,
            text = 'delete',
            command = self.delete_achieve,
        ).pack(pady=5)
        
    #实现删除功能
    def delete_achieve(self):
        self.name = str(self.delete_name.get())
        try:
            cursor.execute('''
                DELETE FROM "main"."txl" 
                WHERE name = ?;
            ''',(self.name,)  #','非常重要使它成为元组
            )
            conn.commit()
            self.overload()
        except:
            print('姓名为:' + self.name + '的用户不存在')
        

    #创建修改窗口
    def update(self):
        self.update = tk.Tk()
        self.update.title('Update')
        self.update.geometry('300x230+500+450')

        self.label = tk.Label(self.update,text = 'Name to be change:').pack()
        self.update_name = tk.Entry(self.update)
        self.update_name.pack()

        self.label = tk.Label(self.update,text = 'new name:').pack()
        self.updated_name = tk.Entry(self.update)
        self.updated_name.pack()

        self.label = tk.Label(self.update,text = 'new phone:').pack()
        self.updated_phone = tk.Entry(self.update)
        self.updated_phone.pack()

        self.label = tk.Label(self.update,text = 'new address:').pack()
        self.updated_address = tk.Entry(self.update)
        self.updated_address.pack()

        self.button_update = tk.Button(
            self.update,
            text = 'Update',
            command = self.update_achieve,
        ).pack(pady=5)
    
    #实现修改功能
    def update_achieve(self):
        self.name_old = str(self.update_name.get())
        self.name_new = str(self.updated_name.get())
        self.phone_new = str(self.updated_phone.get())
        self.address_new = str(self.updated_address.get())
        try:
            cursor.execute('''
                UPDATE "main"."txl" 
                SET name = ?, phone = ?, address = ?
                WHERE name = ?;
            ''',(self.name_new,self.phone_new,self.address_new,self.name_old)
            )
            conn.commit()
            self.overload()
        except:
            print('不存在姓名为:' + self.name_old + '的用户')

    #创建查询窗口
    def select(self):
        self.select = tk.Tk()
        self.select.title('Select')
        self.select.geometry('300x100+500+730')

        self.label_name = tk.Label(self.select,text = 'name:').pack()
        self.select_name = tk.Entry(self.select)
        self.select_name.pack()
        self.button_select_name = tk.Button(
            self.select,
            text = 'Select',
            command = self.select_achieve,
        ).pack(pady=5)

    #实现查询功能
    def select_achieve(self):
        self.name = str(self.select_name.get())
        try:
            x = self.tree_txl.get_children()
            for item in x:
                self.tree_txl.delete(item)
            s = cursor.execute('''
                SELECT * FROM "main"."txl"
                WHERE name = ?
            ''',(self.name,)
            ).fetchall()
            for i in s:
                self.tree_txl.insert('','end',values=i)
            conn.commit()
        except:
            print('通讯录中没有姓名为 ' + self.name + ' 的用户')

    #更新功能
    def overload(self):
        x = self.tree_txl.get_children() #获取元组编号的列表 一个编号代表一个元组
        for item in x:
            self.tree_txl.delete(item)
        txl = cursor.execute('''
                SELECT * FROM "main"."txl" ;
            '''
            ).fetchall()
        for i in txl:
            self.tree_txl.insert('','end',values=i)

        tk.mainloop()

win = txl()