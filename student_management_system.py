from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
import tkinter as tk
import winsound
root=Tk()
root.title("Student Management System")
root.geometry("550x700+450+5")
root.resizable(False,False)

'''call from root-->Add frame'''
def f1():
	addst.deiconify()
	root.withdraw()

'''call from root-->View frame'''
def f2():
	import cx_Oracle
	viewst.deiconify()
	root.withdraw()
	con=None
	cursor=None
	try:
		stdata.delete('1.0',END)
		con=cx_Oracle.connect("system/abc123")
		cursor=con.cursor()
		sql="select * from stud"
		cursor.execute(sql)
		data=cursor.fetchall()
		msg=""
		if cursor.rowcount==0:
			msg="Database is Empty"
			messagebox.showwarning("Alert",msg)
			viewst.withdraw()
			root.deiconify()
		else:
			for d in data:
				msg+="roll no-->"+str(d[0])+" name-->"+d[1]+" marks-->"+str(d[2])+"\n"
			stdata.insert(INSERT,msg)
	except cx_Oracle.DatabaseError as e:
		messagebox.showerror("query error ",e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()

'''call from root-->Update frame'''
def f3():
	updatest.deiconify()
	root.withdraw()

'''call from root-->Delete frame'''
def f4():
	deletest.deiconify()
	root.withdraw()

'''call from root-->Graph frame'''
def f5():
	graphst.deiconify()
	root.withdraw()

nmarks=[]
nname=[]
'''call from graph-->show'''
def f17():
	import cx_Oracle
	import matplotlib.pyplot as plt
	con=None
	cursor=None
	try:
		marks=[]
		name=[]
		#nmarks=[]
		#nname=[]
		con=cx_Oracle.connect("system/abc123")
		cursor=con.cursor()
		sql="select * from stud"
		cursor.execute(sql)
		data=cursor.fetchall()
		for d in data:
			marks.append(d[2])
			name.append(d[1])
			print("roll no-->",d[0]," name-->",d[1]," marks-->",d[2])
		print(marks)
		print(name)
		for i in range(len(marks)):
			if i==5:
				break
			else:
				nmarks.append(marks[i])
				nname.append(name[i])
		print(nmarks,nname)
		plt.bar(nname,nmarks)
		plt.title("Marks Analysis")
		plt.xlabel('Names')
		plt.ylabel('Marks')
		plt.grid()
		plt.show()
	except cx_Oracle.DatabaseError as e:
		print("query error ",e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()
		print("disconnected ")

'''call from graph-save'''
def f18():
	import matplotlib.pyplot as plt
	plt.bar(nname,nmarks)
	plt.title("Marks Analysis")
	plt.xlabel('Names')
	plt.ylabel('Marks')
	plt.grid()
	plt.savefig("student_analysis.png")
	messagebox.showinfo("Success","graph downloaded successfully")
	graphst.deiconify()

'''call from graph-back-->root'''
def f19():
	root.deiconify()
	graphst.withdraw()

'''add-->save'''
def f6():
	import cx_Oracle
	con=None
	cursor=None
	try:
		con=cx_Oracle.connect("system/abc123")
		rno=entAddRno.get()
		#messagebox.showerror("error","invalid Roll number")
		marks=entAddMarks.get()
		name=entAddName.get()
		cursor=con.cursor()
		'''sql="insert into stud values ('%d','%s','%d')"
		args=(rno,name,marks)
		cursor.execute(sql % args)
		con.commit()
		msg=str(cursor.rowcount)+" records inserted "
		messagebox.showinfo("Results ",msg)
		entAddRno.delete(0,END)
		entAddName.delete(0,END)
		entAddMarks.delete(0,END)
		entAddRno.focus()'''
		if str(rno).isdigit():
			if name.isalpha() and len(name)>=2 and name!="":
				if str(marks).isdigit() and (int(marks)>0 and int(marks)<=100) and marks!="":
					rno=int(rno)
					marks=int(marks)
					sql="insert into stud values ('%d','%s','%d')"
					args=(rno,name,marks)
					cursor.execute(sql % args)
					con.commit()
					winsound.PlaySound('positive.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
					msg=str(cursor.rowcount)+" records inserted "
					messagebox.showinfo("Results ",msg)
					entAddRno.delete(0,END)
					entAddName.delete(0,END)
					entAddMarks.delete(0,END)
					entAddRno.focus()
				else:
					msg=str(marks)+" invalid marks"
					winsound.PlaySound('negative.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
					messagebox.showerror("Error",msg)
					entAddMarks.delete(0,END)
					entAddMarks.focus()
			else:
				msg=name+" name must have atleast 2 characters"
				winsound.PlaySound('negative.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
				messagebox.showerror("Error",msg)
				entAddName.delete(0,END)
				entAddName.focus()
		else:
			msg=str(rno)+" should be integer"
			winsound.PlaySound('negative.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
			messagebox.showerror("Error",msg)
			entAddRno.delete(0,END)
			entAddRno.focus()
				
	except cx_Oracle.DatabaseError as e:
		winsound.PlaySound('tryAgain.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
		messagebox.showerror("wrong query ","Roll number already exists")
		con.rollback()
		entAddRno.delete(0,END)
		entAddName.delete(0,END)
		entAddMarks.delete(0,END)
		entAddRno.focus()
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()

'''add-->back'''
def f7():
	root.deiconify()
	addst.withdraw()

'''view-->back'''
def f8():
	root.deiconify()
	viewst.withdraw()

'''update-->save'''
def f9():
	import cx_Oracle
	con=None
	cursor=None
	try:
		con=cx_Oracle.connect("system/abc123")
		cursor=con.cursor()
		rno=entUpdateRno.get()
		name=entUpdateName.get()
		marks=entUpdateMarks.get()
		if str(rno).isdigit() and rno!="":
			if str(name).isalpha() and len(name)>=2 and name!="":
				if str(marks).isdigit() and (int(marks)>0 and int(marks)<=100) and marks!="":
					rno=int(rno)
					marks=int(marks)
					sql="update stud set name='%s',marks='%d' where rno='%d'"
					args=(name,marks,rno)
					cursor.execute(sql % args)
					con.commit()
					if cursor.rowcount>0:
						msg=str(cursor.rowcount)+" rows updated"
						messagebox.showinfo("Results",msg)
						entUpdateRno.delete(0,END)
						entUpdateName.delete(0,END)
						entUpdateMarks.delete(0,END)
						entUpdateRno.focus()
					else:
						winsound.PlaySound('tryAgain.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
						messagebox.showwarning("Alert","Record does not Exist")
						entUpdateRno.delete(0,END)
						entUpdateName.delete(0,END)
						entUpdateMarks.delete(0,END)
						entUpdateRno.focus()
				else:
					winsound.PlaySound('negative.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
					messagebox.showerror("Error","Invalid marks")
					entUpdateMarks.delete(0,END)
					entUpdateMarks.focus()
			else:
				winsound.PlaySound('negative.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
				messagebox.showerror("Error","Invalid name")
				entUpdateName.delete(0,END)
				entUpdateName.focus()
		else:
			winsound.PlaySound('negative.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
			messagebox.showerror("Error","Invalid rollno")
			entUpdateRno.delete(0,END)
			entUpdateRno.focus()
	except cx_Oracle.DatabaseError as e:
		messagebox.showerror("query error ",e)
		con.rollback()
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()

'''update-->back'''
def f10():
	root.deiconify()
	updatest.withdraw()

'''delete-->save'''
def f11():
	import cx_Oracle
	con=None
	cursor=None
	try:
		con=cx_Oracle.connect("system/abc123")
		cursor=con.cursor()
		rno=entDeleteRno.get()
		if str(rno).isdigit() and rno!="":
			rno=int(rno)
			sql="delete from stud where rno='%d'"
			args=(rno)
			cursor.execute(sql % args)
			if cursor.rowcount>0:
				msg=str(cursor.rowcount)+" rows deleted"
				winsound.PlaySound('positive.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
				messagebox.showinfo("Results",msg)
				con.commit()
				entDeleteRno.delete(0,END)
				entDeleteRno.focus()
			else:
				winsound.PlaySound('tryAgain.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
				messagebox.showwarning("Alert","Record does not exist")
				entDeleteRno.delete(0,END)
				entDeleteRno.focus()
		else:
			winsound.PlaySound('negative.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
			messagebox.showerror("Error","Invalid rollno")
			entDeleteRno.delete(0,END)
			entDeleteRno.focus()
	except cx_Oracle.DatabaseError as e:
		messagebox.showerror("query error ",e)
		con.rollback()
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()

'''delete-->back'''
def f12():
	root.deiconify()
	deletest.withdraw()

'''login-->root'''
def f13():
	import cx_Oracle
	con=None
	cursor=None
	try:
		username=entLoginUser.get()
		password=entLoginPass.get()
		if username=="" or password=="":
			msg="please enter the fields"
			winsound.PlaySound('login.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
			messagebox.showwarning("Invalid credentials",msg) 
			return
		else:
			con=cx_Oracle.connect("system/abc123")
			print("connected")
			cursor=con.cursor()
			sql="select * from u1 where (username='%s' and password='%s') or (email='%s' and password='%s')"
			args=(username,password,username,password)
			cursor.execute(sql % args)
			data=cursor.fetchall()
			print(data)
			if cursor.rowcount==0:
				msg="invalid username or password"
				winsound.PlaySound('login.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
				messagebox.showerror("Invalid",msg)
				entLoginUser.delete(0,END)
				entLoginPass.delete(0,END)
				entLoginUser.focus()
				return
			else:
				winsound.PlaySound('positive.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
				msg="login successful"
				messagebox.showinfo("Success","Login successfully")
				temp=entLoginUser.get()
				entLoginUser.delete(0,END)
				entLoginPass.delete(0,END)
				entLoginUser.focus()
				root.title("Welcome"+" "+temp)
				root.deiconify()
				login.withdraw()
	except cx_Oracle.DatabaseError as e:
		print("some issue",e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()
		print("disconnected")

'''login-->sign up'''
def f14():
	login.withdraw()
	signup.deiconify()

'''register-->login'''
def f15():
	import cx_Oracle
	con=None
	cursor=None
	try:
		username=entSignUser.get()
		password=entSignPass.get()
		email=entSignEmail.get()
		phoneno=entSignPhone.get()
		if username =="" or password=="" or email=="":
			winsound.PlaySound('login.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
			msg="please enter the required fields"
			messagebox.showwarning("Invalid form",msg)
			return
		else:
			if username.isalnum() and len(username)>2 and not(str(username).isdigit()):
				if len(password)>5:
					count=0
					for i in email:
						if i in ['@','.']:
							count+=1
					if count==2:
						if len(phoneno)==10 or phoneno=="":	
							con=cx_Oracle.connect("system/abc123")
							cursor=con.cursor()
							query="select * from u1 where (username='%s' and password='%s') or (email='%s' and password='%s') or username='%s' or email='%s'"
							args=(username,password,email,password,username,email)
							cursor.execute(query % args)
							data=cursor.fetchall()
							print(data)
							print(cursor.rowcount)
							if cursor.rowcount ==0:
								con=None
								cursor=None
								con=cx_Oracle.connect("system/abc123")
								cursor=con.cursor()
								sql="insert into u1 values('%s','%s','%s','%s')"
								args=(username,password,email,phoneno)
								cursor.execute(sql % args)
								con.commit()
								winsound.PlaySound('positive.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
								msg=str(cursor.rowcount)+" records inserted "
								messagebox.showinfo("Success",msg)
								entSignUser.delete(0,END)
								entSignPass.delete(0,END)
								entSignEmail.delete(0,END)
								entSignPhone.delete(0,END)
								signup.withdraw()
								login.deiconify()
							else:
								msg="user already exists"
								winsound.PlaySound('tryAgain.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
								messagebox.showwarning("Warning",msg)
								entSignUser.delete(0,END)
								entSignPass.delete(0,END)
								entSignEmail.delete(0,END)
								entSignUser.focus()
						else:
							winsound.PlaySound('login.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
							msg="Invalid Phone number"
							messagebox.showerror('Invalid credentials',msg)
							entSignPhone.delete(0,END)
							entSignPhone.focus()
							return
					else:
						winsound.PlaySound('login.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
						msg="Invalid Email Id"
						messagebox.showerror('Invalid credentials',msg)
						entSignEmail.delete(0,END)
						entSignEmail.focus()
						return
				else:
					winsound.PlaySound('login.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
					msg="Password length must be greater than 5"
					messagebox.showerror('Invalid credentials',msg)
					entSignPass.delete(0,END)
					entSignPass.focus()
					return
			else:
				winsound.PlaySound('login.wav', winsound.SND_ALIAS| winsound.SND_ASYNC)
				msg="Invalid username, length must be greater than 1"
				messagebox.showerror('Invalid credentials',msg)
				entSignUser.delete(0,END)
				entSignUser.focus()
				return
	except cx_Oracle.DatabaseError as e:
		print("some issue ",e)
		con.rollback()
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()

'''signup-login-->login'''
def f16():
	signup.withdraw()
	login.deiconify()

'''exit root'''
def quit():
	if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
		root.destroy()

'''root frame'''
root.withdraw()
btnAdd= Button(root,text="Add",font=("arial",18,"bold"),width=10,command=f1)
btnView= Button(root,text="View",font=("arial",18,"bold"),width=10,command=f2)
btnUpdate= Button(root,text="Update",font=("arial",18,"bold"),width=10,command=f3)
btnDelete= Button(root,text="Delete",font=("arial",18,"bold"),width=10,command=f4)
btnGraph= Button(root,text="Graph",font=("arial",18,"bold"),width=10,command=f5)
btnClose=Button(root,text="Close",font=("arial",18,"bold"),width=10,command=quit)
lblTemp=Label(root,text='Temperature',width=20)
lblQuote=Label(root,text='Quote of the Day',width=20)
txt1 = tk.Text(root,height=2,width=30)
txt2 = tk.Text(root,height=4,width=30)
btnAdd.pack(pady=10)
btnView.pack(pady=10)
btnUpdate.pack(pady=10)
btnDelete.pack(pady=10)
btnGraph.pack(pady=10)
btnClose.pack(pady=10)
lblTemp.pack(pady=5)
txt1.pack(pady=5)
lblQuote.pack(pady=5)
txt2.pack(pady=5)

'''temp'''
import requests
import socket

try:
	socket.create_connection(("www.google.com",80))
	a1="https://api.openweathermap.org/data/2.5/weather?units=metric"
	a2="&q=" + "mumbai"
	a3="&appid=c6e315d09197cec231495138183954bd"
	api_address = a1+a2+a3
	res1 = requests.get(api_address)
	print(res1)
	data=res1.json()
	#print(data)
	main=data['main']
	print(main)
	temp=main['temp']
except OsError as e:
	print("not connected",e)

#lblTempVal=Label(root,text=temp,width=10)
#lblTempVal.place(x=150,y=435)
txt1.tag_configure("center",justify='center')
txt1.insert("1.0",temp)
txt1.tag_add("center","1.0","end")
txt1.config(state=DISABLED)

'''Quote of the day'''
import bs4

res = requests.get("https://www.brainyquote.com/quotes_of_the_day.html")
print(res)

soup=bs4.BeautifulSoup(res.text,'lxml')
text=soup.find('img',{"class":"p-qotd"})
print(text)
quote=text['alt']
	
'''lblQuoteVal=Label(root,text=quote)
lblQuoteVal.place(x=160,y=460)'''
txt2.insert(tk.END,quote)
txt2.config(state=DISABLED)

'''add frame'''
addst=Toplevel(root)
addst.title("ADD Student")
addst.geometry("350x450+450+100")
addst.withdraw()
lblAddRno=Label(addst,text="Enter Roll No")
entAddRno=Entry(addst,bd=5)
lblAddName=Label(addst,text="Enter Name")
entAddName=Entry(addst,bd=5)
lblAddMarks=Label(addst,text="Enter Marks")
entAddMarks=Entry(addst,bd=5)
btnAddSave=Button(addst,text="Save",font=("arial",18,"bold"),width=10,command=f6)
btnAddBack=Button(addst,text="Back",font=("arial",18,"bold"),width=10,command=f7)
lblAddRno.pack(pady=5)
entAddRno.pack(pady=5)
lblAddName.pack(pady=5)
entAddName.pack(pady=5)
lblAddMarks.pack(pady=5)
entAddMarks.pack(pady=5)
btnAddSave.pack(pady=5)
btnAddBack.pack(pady=5)

'''view frame'''
viewst=Toplevel(root)
viewst.title("VIEW Student")
viewst.geometry("350x450+450+100")
viewst.withdraw()
stdata=scrolledtext.ScrolledText(viewst,width=30,height=20)
btnViewBack=Button(viewst,text="Back",font=("arial",18,"bold"),width=10,command=f8)
stdata.pack(pady=5)
btnViewBack.pack(pady=5)

'''update frame'''
updatest=Toplevel(root)
updatest.title("UPDATE Student")
updatest.geometry("350x450+450+100")
updatest.withdraw()
lblUpdateRno=Label(updatest,text="Enter Roll No")
entUpdateRno=Entry(updatest,bd=5)
lblUpdateName=Label(updatest,text="Enter Name")
entUpdateName=Entry(updatest,bd=5)
lblUpdateMarks=Label(updatest,text="Enter Marks")
entUpdateMarks=Entry(updatest,bd=5)
btnUpdateSave=Button(updatest,text="Save",font=("arial",18,"bold"),width=10,command=f9)
btnUpdateBack=Button(updatest,text="Back",font=("arial",18,"bold"),width=10,command=f10)
lblUpdateRno.pack(pady=5)
entUpdateRno.pack(pady=5)
lblUpdateName.pack(pady=5)
entUpdateName.pack(pady=5)
lblUpdateMarks.pack(pady=5)
entUpdateMarks.pack(pady=5)
btnUpdateSave.pack(pady=5)
btnUpdateBack.pack(pady=5)

'''delete frame'''
deletest=Toplevel(root)
deletest.title("DELETE Student")
deletest.geometry("350x450+450+100")
deletest.withdraw()
lblDeleteRno=Label(deletest,text="Enter Roll No")
entDeleteRno=Entry(deletest,bd=5)
btnDeleteSave=Button(deletest,text="Save",font=("arial",18,"bold"),width=10,command=f11)
btnDeleteBack=Button(deletest,text="Back",font=("arial",18,"bold"),width=10,command=f12)
lblDeleteRno.pack(pady=5)
entDeleteRno.pack(pady=5)
btnDeleteSave.pack(pady=5)
btnDeleteBack.pack(pady=5)

'''graph frame'''
graphst=Toplevel(root)
graphst.title("Student GRAPH")
graphst.geometry("350x450+450+100")
graphst.withdraw()
btnGraphShow=Button(graphst,text="Show Graph",font=("arial",20,"bold"),command=f17)
btnGraphSave=Button(graphst,text="Save Graph",font=("arial",20,"bold"),command=f18)
btnGraphBack=Button(graphst,text="Back",font=("arial",20,"bold"),command=f19)
btnGraphShow.pack(pady=10)
btnGraphSave.pack(pady=10)
btnGraphBack.pack(pady=10)

'''login frame'''
login=Toplevel(root)
login.geometry("500x300+400+200")
login.title("LOGIN")
login.withdraw()
login.resizable(False,False)
lblLoginUser=Label(login,text="Username/Email",font=("arial",18,"bold"))
lblLoginPass=Label(login,text="Password",font=("arial",18,"bold"))
entLoginUser=Entry(login,bd=5)
entLoginPass=Entry(login,bd=5,show="*")
btnLogin=Button(login,text="Login",font=("arial",20,"bold"),command=f13)
btnSignup=Button(login,text="Sign Up",font=("arial",20,"bold"),command=f14)
lblLoginUser.place(x=20,y=20)
lblLoginPass.place(x=20,y=100)
entLoginUser.place(x=250,y=20)
entLoginPass.place(x=200,y=100)
btnLogin.place(x=20,y=200)
btnSignup.place(x=200,y=200)

'''sign up frame'''
signup=Toplevel()
signup.title("Sign Up")
signup.geometry("400x500+400+100")
signup.resizable(False,False)
signup.withdraw()
lblSignUser=Label(signup,text="Username",font=("arial",18,"bold"))
lblSignPass=Label(signup,text="Password",font=("arial",18,"bold"))
lblSignEmail=Label(signup,text="Email id",font=("arial",18,"bold"))
lblSignPhone=Label(signup,text="Phone no",font=("arial",18,"bold"))
lblSignUserV=Label(signup,text="required*",fg='red')
lblSignPassV=Label(signup,text="required*",fg='red')
lblSignEmailV=Label(signup,text="required*",fg='red')
entSignUser=Entry(signup,bd=5)
entSignPass=Entry(signup,show="*",bd=5)
entSignEmail=Entry(signup,bd=5)
entSignPhone=Entry(signup,bd=5)
btnSignRegister=Button(signup,text="Register",font=("arial",20,"bold"),command=f15)
btnSignLogin=Button(signup,text="Login",font=("arial",20,"bold"),command=f16)
lblSignUser.place(x=20,y=20)
lblSignPass.place(x=20,y=100)
entSignUser.place(x=200,y=20)
entSignPass.place(x=200,y=100)
lblSignEmail.place(x=20,y=200)
entSignEmail.place(x=200,y=200)
lblSignPhone.place(x=20,y=300)
entSignPhone.place(x=200,y=300)
btnSignRegister.place(x=50,y=400)
btnSignLogin.place(x=200,y=400)
lblSignUserV.place(x=20,y=60)
lblSignEmailV.place(x=20,y=240)
lblSignPassV.place(x=20,y=140)
def fn():
	win.destroy()
	login.deiconify()
win=Toplevel(root)
def strt():
	#win=Toplevel(root)
	win.title("Student Management System")
	win.geometry("350x270+450+100")
	win.resizable(False,False)
	canvas = tk.Canvas(win)
	canvas.configure(background='blue')
	canvas.pack()
	win.tk.call('encoding', 'system', 'utf-8')
	canvas_text = canvas.create_text(70, 100, font=("Purisa",30), text='', anchor=tk.NW)
	#for emoji -> use surrogates+utf-8
	test_string = "Welcome \uD83D\uDE01"
	#Time delay between chars, in milliseconds
	delta = 300 
	delay = 0
	for i in range(len(test_string) + 1):
    		s = test_string[:i]
    		update_text = lambda s=s: canvas.itemconfigure(canvas_text, text=s)
    		canvas.after(delay, update_text)
    		delay += delta
	#canvas.after(7000, lambda: win.destroy())
	canvas.after(7000, lambda: fn())
	#fn()
strt()
root.mainloop() 









