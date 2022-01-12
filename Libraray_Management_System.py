from tabulate import tabulate
import mysql.connector as sqltor
mycon = sqltor.connect(host="localhost",user="root",passwd="demo")#Enter the passwd of your database in place of demo
cursor = mycon.cursor()

cursor.execute("create database IF NOT EXISTS Lib_Management_system")
cursor.close
mycon1= sqltor.connect(host="localhost",user="root",passwd="demo", database= "Lib_Management_system")#Enter the passwd of your database in place of demo
cursor1= mycon1.cursor()
table1= "Create table IF NOT EXISTS Student\
            (Stu_Id char(10) primary key,\
             Stu_Name char(25) NOT NULL,\
             Stu_Class varchar(4) NOT NUll,\
             Stu_section varchar(3) NOT NULL,\
             Password char(12) NOT NULL)"
cursor1.execute(table1)#Student table creating command
table2 = "Create table IF NOT EXISTS Teacher\
            (Teach_Id char(10) Primary key,\
        	Teach_Name char(25) NOT NULL,\
        	Password char(12) NOT NULL)"
cursor1.execute(table2)#Teacher table creating command
table3 = "Create table IF NOT EXISTS Books\
          	(Book_ID  int primary key,\
        	Book_Name varchar(20) NOT NULL ,\
            Author varchar(20) NOT NULL,\
        	Cost int NOT NULL)"
            
cursor1.execute(table3)#Books table creating command

table4 = "Create table IF NOT EXISTS Issuing\
           (ID char(10),\
        	Book_ID int primary key,\
        	Transaction_ID int,\
        	Date_issued Date Default(sysdate()),\
            Due_date Date,\
            Fine int default(0),\
        	Status char(10))"
cursor1.execute(table4)#Issuing table creating command
table5 = "Create table IF NOT EXISTS Issuing_History\
           (ID char(10),\
        	Book_ID int,\
        	Transaction_ID int primary key,\
        	Date_issued Date Default(sysdate()),\
            Return_Date date,\
            Fine int default(0),\
        	Status char(10))"
cursor1.execute(table5)#Issuing table creating command
table6 = "Create table IF NOT EXISTS Credits\
            (ID char(10),\
             Credits int Default(0),\
             Class char(4))"
cursor1.execute(table6)

def Fine():
    data = "Select Book_ID,Transaction_ID,Due_Date,Status\
            From Issuing"
    cursor1.execute(data)
    data2 = cursor1.fetchall()
    for a1 in data2:
        if a1[3] == "Issued":
            data3 = "Select Datediff(sysdate(),(Select Due_Date from Issuing where Book_ID={})) from issuing".format(a1[0])
            cursor1.execute(data3)
            data4 = cursor1.fetchall()
            if data4[0][0] > 0:
                fine = 100+ 10*(data4[0][0]-1)
                fine1 = "Update Issuing\
                        Set Fine = {}\
                        Where Book_ID = {}".format(fine,a1[0])
                fine2 = "Update Issuing_History\
                        Set Fine = {}\
                        Where Transaction_ID= {}".format(fine,a1[1])
                cursor1.execute(fine1)
                cursor1.execute(fine2)
                mycon1.commit()
def credit1(ID):
    if ID[0]=="S":
        credit01 = "Update Credits\
                    Set credits = credits + 100\
                    where ID = '{}'".format(ID)
        cursor1.execute(credit01)
        mycon1.commit()
def credit2(ID,Trans):
    if ID[0]=="S":
        credit02 = "Select Fine  \
                    from Issuing_History\
                    where Transaction_ID= {}".format(Trans)
        cursor1.execute(credit02)
        credit03=cursor1.fetchall()
        credit04 = (credit03[0][0]-100)*2
        credit05 = "Update Credits\
                    Set credits = credits- {}\
                    where ID = '{}'".format(credit04,ID)
    cursor1.execute(credit05)
def menu1():#menu for user type
    print("\n\n\n---------------------------------------\
           \n\tCHOOSE FROM MENU BELOW:\
           \n---------------------------------------")
    print("\n1. Librarin '1'")
    print("2. student as '2'")
    print("3. Teacher as '3'")
    print("4. exit as '4'")
    user =int(input("ENTER YOUR CHOICE :"))
    return user
def menu2():# menu for librarian 
    print("\n---------------------------------------\
           \n\tCHOOSE FROM MENU BELOW:\
           \n---------------------------------------")
    print("\n1.LIST OF BOOKS AS '1'")
    print("2.REGISTER BOOKS AS '2'")
    print("3.STUDENT USERS OF LIBRARY AS '3'")
    print("4.TEACHER USERS OF LIBRARY AS '4'")
    print("5.BOOKS IN TRANSACTION AS '5'")
    print("6.TO ADD NEW STUDENT AS '6'")
    print("7.To ADD NEW TEACHER AS '7'")
    print("8.BEST READER OF THE MONTH AS'8'")
    print("9.EXIT AS '9'")
    choice = int(input("ENTER YOUR CHOICE :"))
    return choice
def menu3():#Menu for students and teachers
    print("\n---------------------------------------\
           \n\tCHOOSE FROM MENU BELOW:\
           \n---------------------------------------")
    print("1.TO ISSUE BOOK ENTER '1'")
    print("2.TO RETURN BOOK ENTER '2'")
    print("3.TO SEE YOUR ISSUING HISTORY ENTER '3'")
    print("4.TO EXIT ENTER '4'")
    choice= int(input("ENTER YOUR CHOICE : "))
    return choice
def login1():
    loop1 =1
    while loop1==1:
        password = str(input("Password:"))
        if password == "lib234556#":
            loop1=2
            return True
        else:
            print("\nPASSWORD WAS INCORRECT !!!")
            print("\n1.TO TRY AGAIN ENTER 1")
            print("2.TO EXIT ENTER 2")
            e = int(input("ENTER YOUR CHOICE: "))
            if e == 1:
                pass
            elif e== 2:
                loop1 = 2
                return False
def login2(a):#lgin for teacher and student
    if a == 2:
        loop1=0
        while loop1==0:
            print("---------------------------------------------------------\
        \n    \t\tSTUDENT LOGIN\t\t\
        \n---------------------------------------------------------")
            Id = str(input("ENTER YOUR ID : "))
            Pass = str(input("ENTER YOUR PASSWORD: "))
            Search ="Select Stu_Id\
                    From Student\
                    where Stu_Id like '{}'\
                    And Password like '{}'".format(Id,Pass)
            cursor1.execute(Search)
            Search1= cursor1.fetchall()
            try:
                if Id in Search1[0]:
                   return [True,2,Id]
                   loop1 = 1
                else:
                  print("INVALID LOGIN!!!!!")
                  print(" WHAT WOUL YOU LIKE TO DO NEXT\
                        \n1. TO TRY AGAIN ENTER '1'\
                        \n2. TO EXIT STUDENT LOGIN ENTER '2'")
                  Choice = int(input("ENTER YOUR CHOICE : "))
                  if Choice == 1:
                      pass
                  else:
                      loop1=1
                      return [False,0]
            except IndexError:
                print("INVALID LOGIN!!!!!")
                print("\nWHAT WOUL YOU LIKE TO DO NEXT\
                        \n1. TO TRY AGAIN ENTER '1'\
                        2. TO EXIT STUDENT LOGIN ENTER '2'")
                Choice = int(input("ENTER YOUR CHOICE : "))
                if Choice == 1:
                    pass
                else:
                    loop1=1
                    return [False,0]
                
                 
    else:
        loop1=0
        while loop1==0:
            print("---------------------------------------------------------\
        \n    \t\tTEACHER LOGIN\t\t\
        \n---------------------------------------------------------")
            Id = str(input("ENTER YOUR ID : "))
            Pass = str(input("ENTER YOUR PASSWORD: "))
            Search ="Select Teach_Id\
                    From Teacher\
                    where Teach_Id = '{}'\
                    And Password like '{}'".format(Id,Pass)
            cursor1.execute(Search)
            Search1= cursor1.fetchall()
            try:
                if Id in Search1[0]:
                   return [True,3,Id]
                   loop1 = 1
                else:
                  print("INVALID LOGIN!!!!!")
                  print(" WHAT WOULD YOU LIKE TO DO NEXT\
                            \n1. TO TRY AGAIN ENTER '1'\
                            \n2. TO EXIT TEACHER LOGIN ENTER '2'")
                  Choice = int(input("ENTER YOUR CHOICE : "))
                  if Choice == 1:
                      pass
                  else:
                      loop1=1
                      return [False,0]
            except:
                  print("INVALID LOGIN!!!!!")
                  print(" WHAT WOULD YOU LIKE TO DO NEXT\
                            \n1. TO TRY AGAIN ENTER '1'\
                            \n2. TO EXIT TEACHER LOGIN ENTER '2'")
                  Choice = int(input("ENTER YOUR CHOICE : "))
                  if Choice == 1:
                      pass
                  else:
                      loop1=1
                      return [False,0]
                  
def reg_books():#code for registration of books
    loop1 = 0
    loop2 = 0
    while loop2 == 0:
        while loop1 == 0:#code to enter id of book
            flag1=1
            cursor1.execute("select Book_ID from Books")
            data = cursor1.fetchall()
            iD = int(input('ENTER ID OF THE BOOK: '))
            for k in data:
                if iD == k:
                    flag1 = 0
            '''if iD.isspace() :
                print("THE ID YOU ENTERED IS INVALID!")
                break'''
            if flag1 == 0:
                print("THE ID YOU ENTERED ALREADY EXISTS!")
            else:
                choice1 = int(input("TO CONFIRM ENTER '1' OR ELSE ENTER '2': "))
                if choice1 == 1: 
                    loop1=1
                else:
                    pass
        loop1 = 0
        while loop1 == 0:#code to enter name of book
            BookName = str(input('ENTER THE BOOK-NAME: '))
            if BookName.isspace() :
                print("THE BOOK- NAME YOU ENTERED IS INVALID! ")
            else:
                choice1 = int(input("TO CONFIRM ENTER '1' OR ELSE ENTER '2': "))
                if choice1 == 1: 
                    loop1=1
                else:
                    pass
        loop1 = 0       
        while loop1 == 0:#code to enter Author of the book
            BookAuthor = str(input('ENTER AUTHOR OF THE BOOK : '))
            if BookAuthor.isspace() :
                print("THE AUTHOR YOU ENTERED IS INVALID!")
            else:
                choice1 = int(input("TO CONFIRM ENTER '1' OR ELSE ENTER '2': "))
                if choice1 == 1: 
                    loop1=1
                else:
                    pass
        loop1 = 0       
        while loop1 == 0:#code to enter cost of book
            BookCost = float(input('ENTER COST OF BOOK : '))
            if BookCost== 0.0 :
                print("THE COST YOU ENTERED IS INVALID!")
            else:
                choice1 = int(input("TO CONFIRM ENTER '1' OR ELSE ENTER '2': "))
                if choice1 ==1: 
                    print("\nCONFIRM THE REGISTRATION OF BOOK TO LIBRARY BY ENTERING '1' OR ELSE PRESS ENTER")
                    choice=int(input("ENTER YOUR CHOICE : "))
                    if choice==1:
                        loop1=1
                        loop2=1
                    else:
                        loop1=1
                        loop2=1
                else:
                    pass
    if choice ==1:
        cursor1.execute("Insert into Books values({},'{}','{}',{})".format(iD,BookName,BookAuthor,BookCost))
        cursor1.execute("Insert into issuing(Book_ID,Status) values({},'Returned')".format(iD))
        print("THE BOOK IS SUCCEESSFULLY REGISTERED")
        mycon1.commit()
    else:
        print("THE BOOK IS NOT REGISTERED")
def reg_Student():#code to register student
     loop4 = 0
     loop5 = 0
     while loop5 == 0:
         while loop4 == 0:#code to enter user id
             User=0
             iD = str(input('ENTER USER ID : '))
             cursor1.execute("Select Stu_Id from Student where Stu_Id like '{}'".format(iD))
             User1 = cursor1.fetchone()
             if User1 is None:
                 User = 1
             if iD.isspace() :
                 print("THE ID YOU ENTERED IS INVALID")
                 break
             elif User == 0:
                 print("THE ID YOU ENTERED ALREADY EXISTS !")
             else:
                 choice2 = int(input("TO CONFIRM ENTER '1' OR ELSE ENTER '2': "))
                 if choice2 == 1: 
                     loop4=1
                 else:
                     pass
         loop4 = 0
         while loop4 == 0:#code to enter user name
             UserName = str(input('ENTER THE USER NAME : '))
             if UserName.isspace() :
                 print("THE USER- NAME YOU ENTERED IS INVALID !")
             else:
                 choice2 = int(input("TO CONFIRM ENTER '1' OR ELSE ENTER '2': "))
                 if choice2 == 1: 
                     loop4=1
                 else:
                     pass
         loop4 = 0
         while loop4 == 0:#code to enter class
             Class = str(input('ENTER CLASS : '))
             if Class.isspace() :
                 print("THE CLASS YOU ENTERED IS INVALID !")
             else:
                 choice2 = int(input("TO CONFIRM ENTER '1' OR ELSE ENTER '2': "))
                 if choice2 == 1: 
                     loop4=1
                 else:
                     pass
         loop4 = 0
         while loop4 == 0:#code to enter user section
             Section = str(input('ENTER SECTION : '))
             if Section.isspace() :
                 print("THE SECTION YOU ENTERED IS INVALID!")
             else:
                 choice2 = int(input("TO CONFIRM ENTER '1' OR ELSE ENTER '2': "))
                 if choice2 == 1: 
                     loop4=1
                 else:
                     pass
         loop4 = 0
         while loop4 == 0:#code to enter password
             Pass = str(input('ENTER YOUR PASSWORD:'))
             if  Pass.isspace() :
                 print("THE PASSWORD YOU ENTERED IS INVALID")
             else:
                 choice2 = int(input("TO CONFIRM ENTER '1' OR ELSE ENTER '2': "))
                 if choice2 == 1: 
                     loop4=1
                 else:
                     pass
         print("\nCONFIRM THE REGISTRATION OF USER TO LIBRARY BY ENTERING '1' OR ELSE PRESS ENTER")
         choice=str(input("ENTER YOUR CHOICE : "))
         if choice=="1":
             cursor1.execute("insert into Student VALUES('{}','{}','{}','{}','{}')".format(iD,UserName,Class,Section,Pass))
             cursor1.execute("insert into Credits(ID,Class) Values('{}','{}')".format(iD,Class))
             print("THE STUDENT IS SUCCEESSFULLY REGISTERED")
             mycon1.commit()
             loop5=1
         else:
            print("THE STUDENT IS NOT REGISTERED")
            loop5=1
def reg_Teacher():#code to register teacher
    loop4 = 0
    loop5 = 0
    while loop5 == 0:
        while loop4 == 0:#code to enter user id
            User=0
            iD = str(input('ENTER ID : '))
            cursor1.execute("Select Teach_Id from Teacher where Teach_Id like '{}'".format(iD))
            User1 = cursor1.fetchone()
            if User1 is None:
                 User = 1
            if iD.isspace() :
                 print("THE ID YOU ENTERED IS INVALID")
                 break
            elif User == 0:
                 print("THE ID YOU ENTERED ALREADY EXISTS !")
            else:
                 choice2 = int(input("TO CONFIRM ENTER '1' OR ELSE ENTER '2': "))
                 if choice2 == 1: 
                     loop4=1
                 else:
                     pass
        loop4 = 0
        while loop4 == 0:#code to enter user name
            UserName = str(input('ENTER THE NAME : '))
            if UserName.isspace() :
                print("THE USER- NAME YOU ENTERED IS INVALID !")
            else:
                choice2 = int(input("TO CONFIRM ENTER '1' OR ELSE ENTER '2': "))
                if choice2 == 1: 
                    loop4=1
                else:
                    pass
        loop4 = 0
        while loop4 == 0:#code to enter password
            Pass = str(input('ENTER YOUR PASSWORD:'))
            if  Pass.isspace() :
                print("THE PASSWORD YOU ENTERED IS INVALID")
            else:
                choice2 = int(input("TO CONFIRM ENTER '1' OR ELSE ENTER '2': "))
                if choice2 == 1: 
                    loop4=1
                else:
                    pass
        print("\nCONFIRM THE REGISTRATION OF USER TO LIBRARY BY ENTERING '1' OR ELSE PRESS ENTER")
        choice=str(input("ENTER YOUR CHOICE : "))
        if choice=="1":
            cursor1.execute("insert into Teacher VALUES('{}','{}','{}')".format(iD,UserName,Pass))            
            print("THE TEACHER IS SUCCEESSFULLY REGISTERED")
            mycon1.commit()
            loop5=1
        else:
            print("THE TEACHER IS NOT REGISTERED")
            loop5=1
    
def Show(n,ID):# codes to show tables
    print("\n\n")
    if n==2:
        command = "Select* from Student "
        cursor1.execute(command)
        d = cursor1.fetchall()
        print(tabulate(d,headers=("ID","NAME","CLASS","SECTION","PASSWORD")))
    elif n ==1:
        command = "Select* from Books"
        cursor1.execute(command)
        d = cursor1.fetchall()
        print(tabulate(d,headers=("BOOK_ID","BOOK_NAME","AUTHOR","COST")))
    elif n == 3:
        command = "Select* from Teacher"
        cursor1.execute(command)
        d = cursor1.fetchall()
        print(tabulate(d,headers=("ID","NAME","PASSWORD")))
    elif n== 4:
        command = "Select* from Issuing"
        cursor1.execute(command)
        d = cursor1.fetchall()
        print(tabulate(d,headers=("ID","BOOK ID","TRANSACTION ID","DATE ISSUED","DUE DATE","FINE","STATUS")))
    elif n== 5:
        command = "Select Books.Book_ID,Book_Name,Author\
                    from Books,Issuing\
                    where Books.Book_ID like Issuing.Book_ID\
                    And Issuing.Status not like \"Issued\""
        cursor1.execute(command)
        d = cursor1.fetchall()
        print(tabulate(d,headers=("ID","NAME","AUTHOR")))
    elif n == 6:
        command = "Select * From Issuing_History where ID like '{}'".format(ID)
        cursor1.execute(command)
        d = cursor1.fetchall()
        print(tabulate(d,headers=("BOOK ID","TRANSACTION ID","DATE ISSUED","RETURN DATE","FINE","STATUS")))
    else:
        pass
    
def issuing(ID):#code for issuimg of books
    print("The List of Books is as follows")
    Show(5,ID)
    print("WHICH BOOK WOULD YOU LIKE ISSUE?")
    CHOICE= int(input("Enter ID of Book: "))
    cursor1.execute("select Books.Book_ID\
                    From Books,Issuing\
                    Where Books.Book_ID like Issuing.Book_ID\
                    And Books.Book_ID = {}\
                    And Issuing.Status like 'Returned' ".format(CHOICE))
    try:
        check = cursor1.fetchall()
        if CHOICE in check[0]:
            Due=str(input("Enter Duedate (YYYY-MM-DD) : "))
            try:
                cursor1.execute("select max(Transaction_ID) from Issuing_History")
                Lasttrans = cursor1.fetchall()
                Trans_ID = Lasttrans[0][0]+1
                
            except:
                Trans_ID = 1
            
            Entry= "Insert into Issuing_History(ID,Book_ID,Transaction_ID,Status)\
                    values('{}',{},{},'Issued')".format(ID,CHOICE,Trans_ID)
            Entry2 = "UPDATE Issuing \
                    SET ID = \"{}\",\
                    Transaction_ID = {},\
                    Due_date= '{}',\
                    Status='Issued'\
                    where Book_ID = {}".format(ID,Trans_ID,Due,CHOICE)
            cursor1.execute(Entry)
            cursor1.execute(Entry2)
            print("You successfuly issued the book")
            credit1(ID)
            mycon1.commit()
        else:
            print("The book you entered cannot be issued")
    except :
        print("The book you entered cannot be issued")
                
def retur(ID):#Code to return book
    print("Your issuing history:")
    Show(6,ID)
    trans_ID = int(input("Enter the transaction ID of the Book you are returning:"))
    cursor1.execute("select Status\
                    from Issuing\
                    where Transaction_ID = {} \
                    And ID like '{}'".format(trans_ID,ID))
    trans= cursor1.fetchall()
    try:
        if trans[0][0] == "Issued":
            cursor1.execute("Update Issuing\
                            Set Status= 'Returned'\
                            where Transaction_ID = {}".format(trans_ID))
            cursor1.execute("Update Issuing_History\
                            Set Status= 'Returned',\
                                return_date = sysdate()\
                                where Transaction_ID = {}".format(trans_ID))
            credit2(ID,trans_ID)
            
            print("You successfully returned the book")
            mycon1.commit()
        elif trans[0][0] == "Returned":
            print("You have returned the book in this transaction")
        else :
            print("The transaction ID you entered is invalid")
    except IndexError:
        print("The transaction ID you entered is invalid")
def BestReader():#Code to generate the best reader 
    command = "Select ID,class,max(credits) from Credits"            
    cursor1.execute(command)
    k = cursor1.fetchall()
    command2 = "Select * from Student\
                where Stu_Id like '{}'".format(k[0][0])
    cursor1.execute(command2)
    r = cursor1.fetchall()
    print("The best reader of month is ",r[0][1],"\nof class ",r[0][2]," Section ",r[0][3]," \nID :", r[0][0])
    print("\n\n\n---------------------------------------------------\
           \n\tWOULD YOU LIKE TO CLEAR THE CREDIT DATA:\
           \n---------------------------------------------------")
    print("\n1. FOR Yes ENTER '1'\
          \n2. FOR NO ENTER '2'")
    try:
        choice = int(input("ENTER YOUR CHOICE: "))
        if choice == 1:
            command3 = "Update Credits\
                        Set credits = 0"
            cursor1.execute(command3)
            mycon1.commit()
            print("All CREDIT DATA CLEARED")
        else:
            pass
    except:
        pass
Fine()
loop1=0
print("---------------------------------------------------------\
          \n    \t\tWELCOME TO THE LIBRARY\t\t\
          \n---------------------------------------------------------")
while loop1==0:
    use= menu1()
    if use==1:
        log = login1()
        if log == True:
            print("YOU LOGGED IN ")
            loop2=0
            while loop2==0:
                choice= menu2()
                if choice == 1:
                    Show(1,"lib")
                elif choice == 2:
                    reg_books()
                elif choice ==3:
                    Show(2,"lib")
                elif choice == 4:
                    Show(3,"Lib")
                elif choice == 5:
                    Show(4,"lib")
                elif choice == 6:
                    reg_Student()
                elif choice == 7:
                    reg_Teacher()
                elif choice == 8:
                    BestReader()
                else:
                    loop2 =1
    elif (use ==2) or (use == 3):
        log1 = login2(use)
        if log1[0] ==True:
            print("YOU LOGGED IN")
            loop2 =0
            while loop2 == 0:
                choice = menu3()
                if choice == 1:
                    Id = log1[2]
                    issuing(log1[2])
                elif choice == 2:
                    retur(log1[2])
                elif choice == 3:
                    Show(5,log1[2])
                else:
                    loop2 =1
    else:
        loop1=1
        print("---------------------------------------------------------\
        \n    \t\tTHANK YOU !!!!!!!!!\t\t\
        \n---------------------------------------------------------")
mycon1.close()
    
