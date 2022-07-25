import socket
from tkinter import *
from tkinter import messagebox
import tkinter


class ApartmentApp(Frame):

    # ApartmentApp Frame Class constructor with client
    def __init__(self, client):

        # Calling Frame Class constructor
        # Assigning self's client with input client
        Frame.__init__(self)
        self.client = client

        # Calling Tkinter pack() Method
        # Naming the title of frame as "Login"
        self.pack()
        self.master.title("Login")

        # Creating a frame for user name
        # Packing user name frame with paddings
        self.userNameFrame = Frame(self)
        self.userNameFrame.pack(padx=5,pady=5)

        # Creating a label for user name frame
        # Packing the user name label
        # with left alignment and paddings
        self.userNameLabel = Label(self.userNameFrame,text="Username: ")
        self.userNameLabel.pack(side=LEFT,padx=5,pady=5)

        # Creating an Entry for user name
        # Packing the user name
        self.userName = Entry(self.userNameFrame, name="username")
        self.userName.pack(side=LEFT,padx=5,pady=5)

        # Creating a password frame with paddings
        self.passwordFrame = Frame(self)
        self.passwordFrame.pack(padx=5,pady=5)

        # Creating a label for password with left alignment and paddings
        self.passwordLabel = Label(self.passwordFrame, text="Password: ")
        self.passwordLabel.pack(side=LEFT,padx=5,pady=5)

        # Creating an Entry for password with showing **** for security
        # Packing with left alignment and paddings
        self.password = Entry(self.passwordFrame, name="password",show="*")
        self.password.pack(side=LEFT,padx=5,pady=5)

        # Creating an login frame which will be basic login button
        # Packing it with paddings
        self.LoginFrame = Frame(self)
        self.LoginFrame.pack(padx=5,pady=5)

        # Creating a "Button" with name Login and giving a functionality (can be called listener)
        # When it is pressed it will call loginButtonPressed
        # Packing it with left alignment and paddings
        self.login = Button(self.LoginFrame, text="Login",command=self.loginButtonPressed)
        self.login.pack(side=LEFT,padx=5,pady=5)


    # When the Login button is pressed this method is executed
    def loginButtonPressed(self):

        # Using the global variable to hold employeeName
        global employeeName

        # Getting the userName and assigning it to global variable employeeName
        employeeName=self.userName.get()

        # Creating client message in format of username;userpassword
        clientMsg=self.userName.get()+";"+self.password.get()

        # Sending message in format of login;username;userpassword with encoding
        self.client.send(("login;"+clientMsg).encode())

        # Getting the server's reply and decoding it
        # Naming the reply as server message and splitting the message by semicolon
        # After splitting printing the server message
        serverMsg = self.client.recv(1024).decode()
        serverMsgList=serverMsg.split(";")
        print(serverMsg)

        # If server replies a login success then we will call employee frame or manager frame depends on the message
        # If server replies a login failure then we will show error and user will try again to login
        if serverMsgList[0]=="loginsuccess" and serverMsgList[-1]=="employee":
            self.employeeFrame()
        elif serverMsgList[0]=="loginsuccess" and serverMsgList[-1]=="manager":
            self.managerFrame()
        elif serverMsgList[0]=="loginfailure":
            messagebox.showerror("Message","Invalid Credentials...")

    def employeeFrame(self):

        # Destroying LoginFrame totally to generate new frame for employee
        self.userNameFrame.destroy()
        self.passwordFrame.destroy()
        self.LoginFrame.destroy()

        # Naming the title of the frame as Employee
        self.master.title("Employee")

        # The creating a frame for apartment code and packing it with paddings
        self.apartmentCodeFrame = Frame(self)
        self.apartmentCodeFrame.pack(padx=5,pady=5)

        # Creating a label for apartment code and packing it with left alignment and paddings
        self.apartmentCodeLabel = Label(self.apartmentCodeFrame, text="Apartment Code: ")
        self.apartmentCodeLabel.pack(side=LEFT,padx=5,pady=5)

        # Creating an Entry for apartment code and packing it with left alignment and paddings
        self.apartmentCode = Entry(self.apartmentCodeFrame, name="apartmentcode")
        self.apartmentCode.pack(side=LEFT,padx=5,pady=5)

        # Creating a Frame named start date and packing it with paddings
        self.startDateFrame = Frame(self)
        self.startDateFrame.pack(padx=5,pady=5)

        # Creating a label for start date and packing it with left alignment and paddings
        self.startDateLabel = Label(self.startDateFrame, text="Start Date: ")
        self.startDateLabel.pack(side=LEFT,padx=5,pady=5)

        # Creating an Entry for start date and packing it with left alignment and paddings
        self.startDate = Entry(self.startDateFrame, name="startdate")
        self.startDate.pack(side=LEFT,padx=5,pady=5)

        # Creating an frame named EndDate and packing it with paddings
        self.endDateFrame = Frame(self)
        self.endDateFrame.pack(padx=5,pady=5)

        # Creating an label for end date and packing it with left alignment and paddings
        self.endDateLabel = Label(self.endDateFrame, text="End Date: ")
        self.endDateLabel.pack(side=LEFT,padx=5,pady=5)

        # Creating an entry for end date and packing it with left alignment and paddings
        self.endDate = Entry(self.endDateFrame, name="enddate")
        self.endDate.pack(side=LEFT,padx=5,pady=5)

        # Creating a frame named customer name and packing it with left and right paddings
        self.customerNameFrame = Frame(self)
        self.customerNameFrame.pack(padx=5,pady=5)

        # Creating an label for customer name frame and packing it with left alignment and paddings
        self.customerNameLabel = Label(self.customerNameFrame, text="Customer Name: ")
        self.customerNameLabel.pack(side=LEFT,padx=5,pady=5)

        # Creating an entry for customer name and packing it with left alignment and paddings
        self.customerName = Entry(self.customerNameFrame, name="customername")
        self.customerName.pack(side=LEFT,padx=5,pady=5)

        # Creating an Frame named button frame and packing it with left and right paddings
        self.buttonFrame = Frame(self)
        self.buttonFrame.pack(padx=5,pady=5)

        # Creating an button named show with functionality named showButtonPressed
        # Packing it with left alignment and paddings
        self.show = Button(self.buttonFrame, text="Show",command=self.showButtonPressed)
        self.show.pack(side=LEFT,padx=5,pady=5)

        # Creating an button named reserve with functionality named reserveButtonPressed
        # Packing it with left alignment and paddings
        self.reserve = Button(self.buttonFrame, text="Reserve",command=self.reserveButtonPressed)
        self.reserve.pack(side=LEFT,padx=5,pady=5)

        # Creating an button named reserve with functionality named reserveButtonPressed
        # Packing it with left alignment and paddings
        self.employeeClose = Button(self.buttonFrame, text="Close",command=self.closeButtonPressed)
        self.employeeClose.pack(side=LEFT,padx=5,pady=5)


    def showButtonPressed(self):

        # Creating a message in the format of apartmentCode;startDate;endDate
        clientMsg=self.apartmentCode.get()+";"+self.startDate.get()+";"+self.endDate.get()

        # Sending that message to server as apartment;apartmentCode;startDate;endDate as encoded
        self.client.send(("apartment;"+clientMsg).encode())

        # Receiving an reply from server and decoding it
        serverMsg=self.client.recv(1024).decode()

        # Splitting the server's reply by semicolon
        serverMsgList=serverMsg.split(";")

        # Adding a space to the beginning of the split server reply message
        aptMsg=" ".join(serverMsgList)

        # Printing the server msg
        print(serverMsg)

        # Printing the server's reply to the user
        if serverMsgList[0]!="invalidapartmentcode":
            if serverMsgList[-1]=="True":
                messagebox.showinfo("Message",aptMsg)
            elif serverMsgList[-1] == "False":
                messagebox.showinfo("Message",aptMsg)
        else:
            messagebox.showerror("Message","Invalid Apartment Code...")

    def reserveButtonPressed(self):

        # Using the global variable employee name
        global employeeName

        # Creating client message in format of apartmentCode;customerName;startDate;endDate;employeeName
        clientMsg=self.apartmentCode.get()+";"+self.customerName.get()+";"+self.startDate.get()+";"+self.endDate.get()+";"+employeeName

        # Sending the client message in format of reservation;apartmentCode;customerName;startDate;endDate;employeeName
        # To server in encoded version
        self.client.send(("reservation;"+clientMsg).encode())

        # Receiving server's reply
        serverMsg=self.client.recv(1024).decode()

        # Showing the server's reply
        if serverMsg=="successfulreservation":
            messagebox.showinfo("Message",serverMsg)
        elif serverMsg=="invalidapartmentcode":
            messagebox.showerror("Message",serverMsg)
        elif serverMsg=="notavailable":
            messagebox.showerror("Message",serverMsg)


    def managerFrame(self):

        # Destroying LoginFrame to create managerFrame in the next steps
        self.userNameFrame.destroy()
        self.passwordFrame.destroy()
        self.LoginFrame.destroy()

        # Creating manager label and packing it with paddings
        self.managerlabel= Label(self,text="Select your report:")
        self.managerlabel.pack(padx=5,pady=5)

        # Creating a radio button frame and packing with default
        # Each radio button will correspond a different report
        self.frameradiobtn1 = Frame(self)
        self.frameradiobtn1.pack()

        # Creating report selections and report titles list
        reportSelections=["1","2","3","4"]
        reportTitles=["(1) Which employee makes the highest number of reservations?","(2) Which apartment is the most popular?"
                        ,"(3) How mant apartments are currently available?","(4) How many apartments have not been reserved yet?"]

        # Creating a StringVar
        self.chosenReport=StringVar()

        # Setting StringVar with first String in ReportSelection list which is "1"
        self.chosenReport.set(reportSelections[0])

        # Creating a counter variable which will act as index in for loop
        counter=0

        # Creating a for loop for every element in reportSelections list
        # Value of report will be 1 2 3 4 and 5
        # Each turn we will create a radio button and titles will come from reportTitles
        for report in reportSelections:
                rBtn = Radiobutton(self.frameradiobtn1,text=reportTitles[counter],variable=self.chosenReport,value=report)
                rBtn.pack(padx=5,pady=5)
                counter+=1

        # Creating a frame for managing buttons
        # Buttons will be request button and close button and packing with default
        self.managerBtnFrame = Frame(self)
        self.managerBtnFrame.pack()

        # Creating a button named requestBtn and packing it with left alignment and paddings
        # When this button is pressed requestButtonPressed method will be executed
        # In that method we will generate reports in short
        self.requestBtn = Button(self.managerBtnFrame, text="Request",command=self.requestButtonPressed)
        self.requestBtn.pack(side=LEFT,padx=5,pady=5)

        # Creating a button named closeBtn and packing it with left alignment and paddings
        # When this button is pressed closeButtonPressed method will be executed
        # In that method we will send terminate message to server and Print server's response
        # Then destroy the current client thread
        self.closeBtn = Button(self.managerBtnFrame, text="Close",command=self.closeButtonPressed)
        self.closeBtn.pack(side=LEFT,padx=5,pady=5)

    def requestButtonPressed(self):

        # If the first radio button is chosen
        if self.chosenReport.get() == "1":

            # Sending server a message "report1" as encoded
            self.client.send(("report1").encode())

            # Receiving server reply
            serverMsg=self.client.recv(1024).decode()

            # Splitting the message with semicolons
            serverMsgList=serverMsg.split(";")

            # Adding ", " to the beginning of the server's reply
            msg=", ".join(serverMsgList[1::])

            # Printing the ", " added and split version of server reply
            print(serverMsg)

            # Showing the message to the user
            messagebox.showinfo("Message","Employee(s) that make highest reservations: {}".format(msg))

        # If the second radio button is chosen
        elif self.chosenReport.get() == "2":

            # Sending server a message "report2" as encoded
            self.client.send(("report2").encode())

            # Receiving server reply
            serverMsg=self.client.recv(1024).decode()

            # Splitting the message with semicolons
            serverMsgList=serverMsg.split(";")

            # Adding ", " to the beginning of the server's reply
            msg=", ".join(serverMsgList[1::])

            # Printing the ", " added and split version of server reply
            print(serverMsg)

            # Showing the message to the user
            messagebox.showinfo("Message","Most popular Apartement(s): {}".format(msg))

        # If the third radio button is chosen
        elif self.chosenReport.get() == "3":

            # Sending server a message "report3" as encoded
            self.client.send(("report3").encode())

            # Receiving server reply
            serverMsg=self.client.recv(1024).decode()

            # Splitting the message with semicolons
            serverMsgList=serverMsg.split(";")

            # Adding ", " to the beginning of the server's reply
            msg=", ".join(serverMsgList[1::])

            # Printing the ", " added and split version of server reply
            print(serverMsg)

            # Showing the message to the user
            messagebox.showinfo("Message","Currently {} available apartment(s)!".format(msg))

        # If the fourth radio button is chosen
        elif self.chosenReport.get() == "4":

            # Sending server a message "report3" as encoded
            self.client.send(("report4").encode())

            # Receiving server reply
            serverMsg=self.client.recv(1024).decode()

            # Splitting the message with semicolons
            serverMsgList=serverMsg.split(";")

            # Adding ", " to the beginning of the server's reply
            msg=", ".join(serverMsgList[1::])

            # Printing the ", " added and split version of server reply
            print(serverMsg)

            # Showing the message to the user
            messagebox.showinfo("Message","{} apartment(s) not reserved yet!".format(msg))

    def closeButtonPressed(self):

        # In this method we will send terminate message to server and Print server's response
        self.client.send(("terminate").encode())

        serverMsg=self.client.recv(1024).decode()

        print(serverMsg)

        # Then destroy the current client frame
        # Which means return to main and in main we will close the socket to kill connection
        self.master.destroy()

#global employee name to keep track of the employee who just logged in
employeeName=""

if __name__ == "__main__":

    # HOST ip is 127.0.0.1
    HOST = "127.0.0.1"

    # PORT is 5000
    PORT = 5000

    # Creating a socket
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        # Trying to create connection with HOST and PORT values
        client.connect((HOST,PORT))
    except:
        print("Failed to connect to the server")
        exit(1)

    # Creating windows as ApartmentApp frame class with
    # sending client which is a created socket with connection
    window=ApartmentApp(client)

    # Calling window's tkinter "event loop" until this window is called on close
    window.mainloop()

    # closing the socket
    client.close()