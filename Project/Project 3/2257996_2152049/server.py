import socket, threading
from datetime import *

class ClientThread(threading.Thread):

    #contructor for the ClientThread class.
    def __init__(self,clientAddress,clientSocket):

        threading.Thread.__init__(self)
        self.clientAddress=clientAddress
        self.clientSocket=clientSocket
        self.lock=threading.RLock()

    #This run function is the main method for threading and in this function message format is checked which is received by client
    def run(self):

        print("Hi - ",self.clientAddress)

        clientMsg=self.clientSocket.recv(1024).decode()
        #turn the message sent by client into a list
        clientMsgList=clientMsg.split(";")

        #global employee name to keep track of the logged employee
        global employeeName

        #while message's first element sent by the client is not terminate keep looping
        while clientMsgList[0]!="terminate":

            if clientMsgList[0]=="login":

                username=clientMsgList[1]
                password=clientMsgList[2]
                self.login(username,password)
                employeeName=username
            
            elif clientMsgList[0]=="apartment":

                apartmentCode=clientMsgList[1]
                startDate=clientMsgList[2]
                endDate=clientMsgList[3]

                self.apartment(apartmentCode,startDate,endDate)

            elif clientMsgList[0]=="reservation":

                apartmentCode=clientMsgList[1]
                customerName=clientMsgList[2]
                startDate=clientMsgList[3]
                endDate=clientMsgList[4]
                
                self.reservation(apartmentCode,customerName,startDate,endDate,employeeName)

            elif clientMsgList[0]=="report1":
                
                self.report1()

            elif clientMsgList[0]=="report2":
                
                aptDict=self.getAptDict()
                self.report2(aptDict)

            elif clientMsgList[0]=="report3":
                
                aptDict=self.getAptDict()
                self.report3(aptDict)

            elif clientMsgList[0]=="report4":
                
                aptDict=self.getAptDict()
                self.report4(aptDict)

            clientMsg=self.clientSocket.recv(1024).decode()
            clientMsgList=clientMsg.split(";")


        print(clientMsg)
        
        msg = "SERVER >>> TERMINATE".encode()
        self.clientSocket.send(msg)
        print("Connection from ", self.clientAddress," is terminated")
        self.clientSocket.close()

    #This function is used to check if the user who tries to log in is an employee or a manager
    def login(self,username,password):
        
        self.lock.acquire()

        try:
            file=open("users.txt","r")
        except:
            print("User file could not be opened...")

        isUser,role=self.readUser(file,username,password)
        file.close()

        if isUser==True:

            if role=="manager":
                #send message to the server
                msg=("loginsuccess;"+username+";"+role).encode()
                self.clientSocket.send(msg)

            elif role=="employee":
                #send message to the server
                msg=("loginsuccess;"+username+";"+role).encode()
                self.clientSocket.send(msg)

        else:
            #send message to the server
            msg="loginfailure".encode()
            self.clientSocket.send(msg)

        self.lock.release()

    #This function is used to see if that user is in the user.txt. Returns boolean and role
    def readUser(self,file,username,password):
        
        self.lock.acquire()

        for line in file:
            contents=line.strip().split(';')
            if (contents[0]==username) and (contents[1]==password):
                self.lock.release()
                return True,contents[2]
        
        self.lock.release()
        return False,contents[2]
    
    #This function checks whether the apartment is available or not when the show button is clicked
    def apartment(self,ac,startdate,enddate):
        
        self.lock.acquire()

        d1,m1,y1=[int(i) for i in startdate.split("/")]
        sd = date(y1,m1,d1)
        d2,m2,y2=[int(i) for i in enddate.split("/")]
        ed = date(y2,m2,d2)

        availability=0
        isThereReservation=0

        try:
            reservedfile=open("reservations.txt","r")
            apartmentfile=open("apartments.txt","r")
        except:
            print("Reservations file could not be opened...")
        
        validApt=[""]

        #if an aptcode is matched and apartments date is available in reservations.txt, availability and isThereReservation becomes 1 otherwise 0
        for line in reservedfile:
                contents=line.strip().split(";")
                if contents[0]==ac and ac!="":
                    isThereReservation=1
                    d1,m1,y1=[int(i) for i in contents[2].split("/")]
                    sd2 = date(y1,m1,d1)
                    d2,m2,y2=[int(i) for i in contents[3].split("/")]
                    ed2 = date(y2,m2,d2)
                    if sd>ed2:
                        availability=1
                    elif ed<sd2:
                        availability=1
                    else:
                        availability=0
                        break
        
        #keep list of all apartments in the apartments.txt
        for line in apartmentfile:
            aptContents=line.strip().split(";")
            validApt.append(aptContents[0])
        
        reservedfile.close()
        apartmentfile.seek(0)

        #If aptcode is in validapts, it is checked whether it has reservation or not. If it has an reservation, its availability is chechked.
        #After all is done, message is sent to the client in an appropriate format.  
        if ac in validApt:
            for line in apartmentfile:
                aptContents=line.strip().split(";")
                if aptContents[0] == ac and ac!="":
                    aptContentsMsg=";".join(aptContents)
                    if isThereReservation==1:
                        if availability==1:
                            msg=("apartment;"+aptContentsMsg+";"+"True").encode()
                            #send message to the server
                            self.clientSocket.send(msg)
                            apartmentfile.close()
                            self.lock.release()
                            return True
                        else:
                            msg=("apartment;"+aptContentsMsg+";"+"False").encode()
                            #send message to the server
                            self.clientSocket.send(msg)
                            apartmentfile.close()
                            self.lock.release()
                            return False
                    else:
                            msg=("apartment;"+aptContentsMsg+";"+"True").encode()
                            #send message to the server
                            self.clientSocket.send(msg)
                            apartmentfile.close()
                            self.lock.release()
                            return True
        
        #if aptcod eis not valid then appropriate message is sent to the client.
        else:
            apartmentfile.close()
            msg=(("invalidapartmentcode").encode())
            self.clientSocket.send(msg)
            self.lock.release()
           
    #This function checks if the desired apt has an reservation or not on those dates.
    #If there is no reservation for those dates and for that aptcode, then make a reservation into the reservations.txt.
    def reservation(self,ac,cn,startdate,enddate,en):

        self.lock.acquire()

        d1,m1,y1=[int(i) for i in startdate.split("/")]
        sd = date(y1,m1,d1)
        d2,m2,y2=[int(i) for i in enddate.split("/")]
        ed = date(y2,m2,d2)

        availability=0
        isThereReservation=0

        try:
            reservedfile=open("reservations.txt","r")
            apartmentfile=open("apartments.txt","r")
        except:
            print("Reservations file could not be opened...")
        
        validApt=[""]

        #checks whether the apartment is available in those dates.
        for line in reservedfile:
                contents=line.strip().split(";")
                if contents[0]==ac and ac!="":
                    isThereReservation=1
                    d1,m1,y1=[int(i) for i in contents[2].split("/")]
                    sd2 = date(y1,m1,d1)
                    d2,m2,y2=[int(i) for i in contents[3].split("/")]
                    ed2 = date(y2,m2,d2)
                    if sd>ed2:
                        availability=1
                    elif ed<sd2:
                        availability=1
                    else:
                        availability=0
                        break
        
        #keep a list of all apartments
        for line in apartmentfile:
            aptContents=line.strip().split(";")
            validApt.append(aptContents[0])
        
        apartmentfile.close()
        reservedfile.close()

        #try to open reservations.txt again but in appendable format.
        try:
            reservedfile=open("reservations.txt","a")
        except:
            print("Reservations files could not be opened...")

        #If reservation can be made, this is the format to be written in reservations.txt.
        textList=[str(ac),str(cn),str(startdate),str(enddate),str(en)]

        #If there is an apartment with that code, its reservation and if there is an reservation, its availability is checked.
        # If it is available to be reserved, then reservation is done by appending the reservation into the reservations.txt.
        # After all done, message is sent to the client in an appropriate format. 
        if ac in validApt:
            if isThereReservation==1:
                if availability==1:
                    for line in textList:
                        
                        reservedfile.write(line)
                        if line != textList[-1]:
                            reservedfile.write(";")

                    reservedfile.write("\n")
                    reservedfile.close()
                    self.clientSocket.send(("successfulreservation").encode())

                elif availability==0:
                    
                    reservedfile.close()
                    self.clientSocket.send(("notavailable").encode())
            
            else:
            
                for line in textList:
                        
                    reservedfile.write(line)
                    if line != textList[-1]:
                        reservedfile.write(";")

                reservedfile.write("\n")
                reservedfile.close()
                self.clientSocket.send(("successfullreservation").encode())
        else:
            reservedfile.close()
            self.clientSocket.send(("invalidapartmentcode").encode())

        self.lock.release()

    #This function keeps a dictionary of all apartments and returns that dictionary.
    def getAptDict(self):

        self.lock.acquire()

        try:
            aptfile=open("apartments.txt","r")
        except:
            print("Apartments file could not be opened...")

        aptDict={}

        for line in aptfile:
            contents=line.strip().split(";")
            if contents[0] not in aptDict:
                aptDict[contents[0]]=1

        aptfile.close()
        return aptDict

    #This function is used to find the employee who made highest number of reservations and sends the result to the client in an appropriate format.
    def report1(self):

        self.lock.acquire()

        try:
            userfile=open("users.txt","r")
            reservationfile=open("reservations.txt","r")
        except:
            print("Users file could not be opened...")

        highestReserveDict={}
        userDict={}

        #keep a dictionary of all employees
        for line in userfile:
            contents=line.strip().split(";")
            if contents[-1] == "employee" and contents[0] not in userDict:
                userDict[contents[0]]=1

        #keep a dictionary of all reservations(value) made by each employee(employee)
        for line in reservationfile:
            contents=line.strip().split(";")
            if contents[-1] in userDict:
                if contents[-1] not in highestReserveDict:
                    highestReserveDict[contents[-1]]=1
                else:
                    highestReserveDict[contents[-1]]+=1

        ansList=[" "]
        ans=0

        #find the employee(key) with the highest number of value(reservation)
        while highestReserveDict:
            key,value=highestReserveDict.popitem()
            if value > ans:
                ans=value
                ansList=[key]
            elif value == ans:
                ansList.append(key)

        userfile.close()
        reservationfile.close()

        ansMsg=";".join(ansList)
        msg=("report1;"+ansMsg).encode()
        
        #send result to the client with appropriate format.
        self.clientSocket.send(msg)

        self.lock.release()
        
    #This function is used to find which apartment is the most popular.
    def report2(self,aD):

        self.lock.acquire()

        try:
            file=open("Reservations.txt","r")
        except:
            print("Reservations file could not be opened...")

        mostPopularDict={}

        #for each time an aptcode is seen in the reservations.txt its value is added to the new dictionary.
        for line in file:
            contents=line.strip().split(";")
            if contents[0] in aD:
                if contents[0] not in mostPopularDict:
                    mostPopularDict[contents[0]]=1
                else:
                    mostPopularDict[contents[0]]+=1

        file.close()

        ansList=[" "]
        ans=0
        
        #Find the most popular(value) apartment(key)
        while mostPopularDict:
            key,value=mostPopularDict.popitem()
            if value > ans:
                ans=value
                ansList=[key]
            elif value == ans:
                ansList.append(key)
        
        ansMsg=";".join(ansList)
        msg=("report2;"+ansMsg).encode()
        
        #send result to the client in an appropriate format.
        self.clientSocket.send(msg)
        
        self.lock.release()

    #This function finds the number of apartments which are currently(right now) available
    def report3(self,aD):

        self.lock.acquire()

        #get today's date
        today=date.today()

        try:
            file=open("Reservations.txt","r")
        except:
            print("Reservations file could not be opened...")

        curAvailable=0
        notAvailabe=[" "]

        #If today's date is within start and end dates then add the apartment to notAvailable list.
        for line in file:
            contents=line.strip().split(";")
                
            d1,m1,y1 = [int(i) for i in contents[2].split("/")]
            sd2=date(y1,m1,d1)
            d2,m2,y2 = [int(i) for i in contents[3].split("/")]
            ed2=date(y2,m2,d2)

            if today>=sd2 and today<=ed2:
                notAvailabe.append(contents[0])

        file.close()

        #for each apartment in apartments dictionary, increase the curAvailable
        for i in aD:
            curAvailable+=1
        
        #for each i in notavaible list, if that i is in apartment dictionary then decrease the curAvailable.
        for i in notAvailabe:
            if i in aD:
                curAvailable-=1
        
        msg=("report3;"+str(curAvailable)).encode()

        #send result to the client in an appropriate format.
        self.clientSocket.send(msg)
        
        self.lock.release()

    #This function is used to find the number of apartments that has not been reserved yet.
    def report4(self,aD):
        
        self.lock.acquire()

        try:
            file=open("Reservations.txt","r")
        except:
            print("Reservations file could not be opened")
        
        notAvailable=[" "]
        notReserved=0

        #if aptcode in reservations.txt is in apartment dictionary and not in notAvailable, it is added to the notAvailable list.
        for line in file:
            contents=line.strip().split(";")
            if contents[0] in aD and contents[0] not in notAvailable:
                notAvailable.append(contents[0])

        file.close()

        #for each aptcode in apartment dictionary, if that aptcode is not in notAvailable list then increase the notReserved.
        for i in aD:
            if i not in notAvailable:
                notReserved+=1
        
        msg=("report3;"+str(notReserved)).encode()

        #send result to the client in an appropriate format.
        self.clientSocket.send(msg)
       
        self.lock.release()

#global employee name to keep track of the employee who just logged in.
employeeName=""

if __name__=="__main__":

    HOST = "127.0.0.1"
    PORT = 5000

    counter=0

    #create a socket in TCP 
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #socket_SO_REUSEADDR is not known so code crashes
    #mySocket.setsockopt(socket.SOL_SOCKET, socket_SO_REUSEADDR, 1)

    try:
        mySocket.bind((HOST,PORT))
    except:
        print("Call to bind failed")
        exit(1)

    print("Waiting for Connection...")
    while True:

        mySocket.listen()
        connection, address=mySocket.accept()
        counter +=1
        print("Connection ",counter," is received from ", address[0])
        
        #create a new client thread with address and connection.
        newthread = ClientThread(address,connection)
        #invoke ClientThread's run function.
        newthread.start()
    
    
    