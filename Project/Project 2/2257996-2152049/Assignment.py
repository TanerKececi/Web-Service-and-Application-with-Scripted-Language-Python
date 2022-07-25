import sys
import matplotlib.pyplot as plt

#this function creates dictionary and calculates the TimeViewed,Fixations and Revisits
def create_dict(myDict,PageName,ElementName,UserGroup,TimeViewed,Fixations,Revisits):
    #if there is no any key with that pagename, create a nested dictionary
    if PageName not in myDict.keys():
        myDict[PageName]={}
    ##if there is no any key with that elementname in that pagename, create a nested dictionary
    if ElementName not in myDict[PageName].keys():
        myDict[PageName][ElementName]={}
    #if there is no any key with that usergroup in [pagename][elementname], load TimeViewed,Fixations,Revisits as a list value
    #then return to get the second line
    if UserGroup not in myDict[PageName][ElementName].keys():
        myDict[PageName][ElementName][UserGroup]=[TimeViewed,Fixations,Revisits]
        return
    #if the last if condition doesnt hold then these 6 lines below sums every totalview, totalfixation and totalrevisit
    #for each same pagename element usergroup in the dictionary
    totalview = float(myDict[PageName][ElementName][UserGroup][0])
    totalfixation = float(myDict[PageName][ElementName][UserGroup][1])
    totalrevisit = float(myDict[PageName][ElementName][UserGroup][2]) 

    totalview = totalview + float(TimeViewed)
    totalfixation = totalfixation + float(Fixations)
    totalrevisit = totalrevisit + float(Revisits)

    #overwrite the totalview,totalfixation,totalrevisit
    myDict[PageName][ElementName][UserGroup] = [totalview,totalfixation,totalrevisit]

#this function works after the user selects 1st option from menu
#in this function users are asked for selecting desired total number, page and element
def selection1(myDict):
    print("\n1. Total time viewed\n2. Total number of fixations\n3. Total number of revisits")
    choice = int(input("\nEnter you choice: "))
    if choice == 1:
        total='Total time viewed'
    elif choice == 2:
        total='Total number of fixations'
    elif choice==3:
        total='Total number of revisits'
    else:
        print("Invalid parameter...")

    element = input("\nChoose a particular element (A,B,C,D) : ")
    page = input("\nChoose a specific web page (Apple,Babylon,AVG,BBC,GoDaddy,Yahoo) : ")

    groups=["People with Autism","People Without Autism"]
    #In values variable desired page, element and one of the (TimeViewed,Fixations,Revisits) is put
    #one of the values is for Autism other one is for none-Autism
    values=[myDict[page][element]["ASD"][choice-1],myDict[page][element]["CONTROL"][choice-1]]
    plt.bar(groups, values)
    plt.xlabel('Groups')
    plt.ylabel(total)
    plt.title('Comparison Between People With & Without Autism\nfor Element {} on Page {}'.format(element,page))
    plt.show()

    #return to the main menu
    return

#this function works after the user selects 2nd option from menu
#in this function users are asked for selecting desired total number and page
def selection2(myDict):
    print("\n1. Total time viewed\n2. Total number of fixations\n3. Total number of revisits")
    choice = int(input("Enter you choice: "))
    if choice == 1:
        total='Total time viewed'
    elif choice == 2:
        total='Total number of fixations'
    elif choice==3:
        total='Total number of revisits'
    else:
        print("Invalid parameter...")

    page = input("\nChoose a specific web page (Apple,Babylon,AVG,BBC,GoDaddy,Yahoo) : ")

    #sum1 and sum2 are the desired page and desired total number by adding every element together
    sum1=myDict[page]['A']['CONTROL'][choice-1]+myDict[page]['B']['CONTROL'][choice-1]+myDict[page]['C']['CONTROL'][choice-1]+myDict[page]['D']['CONTROL'][choice-1]
    sum2=myDict[page]['A']['ASD'][choice-1]+myDict[page]['B']['ASD'][choice-1]+myDict[page]['C']['ASD'][choice-1]+myDict[page]['D']['ASD'][choice-1]

    groups=["People with Autism","People Without Autism"]
    values=[sum2,sum1]
    plt.bar(groups, values)
    plt.xlabel('Groups')
    plt.ylabel(total)
    plt.title('Comparison Between People With & Without Autism\non Page {}'.format(page))
    plt.show()

    #return to the main menu
    return

#This is the menu function with a loop as long as user doesnt press 3 this menu keeps appearing
def menu(myDict):
    loop=1
    while loop: 
        print("------------------------------------------------------------------------------------------------")
        print("\nWELCOME TO A SIMPLE EYE-TRACKING DATA ANALYSER FOR WITH AUTISM\n")
        print("1. Compare the total time viewed, the total number of fixations or the total number of revisits\nfor people with and without autism for a particular element on a specific web page\n")
        print("2. Compare the total time viewed, the total number of fixations or the total number of revisits\nfor people with and without autism on a specific web page\n")
        print("3. Exit\n")
        print("4. See the nested dictionary\n")
        print("------------------------------------------------------------------------------------------------")
        choice = int(input("\nEnter your choice: "))
        print("\n")
        if(choice == 1):
            selection1(myDict)
        elif(choice == 2):
            selection2(myDict)
        elif(choice == 3):
            print("BYEEEE!!!!")
            break
        elif(choice == 4):
            for i in myDict:
                print(i,myDict[i])
                print("\n")
        else:
            print("Unknown menu choice is selected please try again!")

#This function reads every line of the file and sends each line to create_dict function. Afterwards it calls menu function.
def read_line(file):
    myDict={}
    for line in file:
        #this line removes every ; from the read file and that line is loaded in to contents as a list
        contents=line.strip().split(';')
        #send the dictionary, PageName, ElementName, UserGroup, TimeViewed, Fixations, Revisits to the create_dict function
        create_dict(myDict,contents[0],contents[1],contents[4],contents[5],contents[6],contents[7])
    menu(myDict)


#Below helps to get the text file from command line and we used exception handler for reading the file
if len(sys.argv)!=2:
    print("Invalid Parameter")

try:
    file=open(sys.argv[1],'r')
except:
    print("File could not be opened...")
else:
    #first line of the text file is read because we dont need it
    line=file.readline()
    read_line(file)
