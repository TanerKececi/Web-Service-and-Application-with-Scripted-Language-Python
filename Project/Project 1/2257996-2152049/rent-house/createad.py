#!C:\Users\DOGUKAN\AppData\Local\Programs\Python\Python39\python

import http.cookies as Cookie
import sqlite3
import cgi
import os

# This function prints header
# Takes the page title as input
# Things we will write to the page will come after this function


def printHeader(title):
    print("Content-type: text/html; charset=\"UTF-8\"")
    print("")
    print("<html><head><title>{}</title></head><body>".format(title))

# This function prints footer
# Things we will write to the page will come before this function


def printFooter():
    print("</body></html>")


# Printing the header with title
printHeader("Create Advertisement")

if("HTTP_COOKIE" in os.environ):                                    # Checking if there is any cookie
    cookie = Cookie.SimpleCookie(
        os.environ["HTTP_COOKIE"])         # Getting the cookie
    if "session" in cookie.keys():                                  # Checking if the user is logged in

        form = cgi.FieldStorage()                                   # Creating a form

        # Creating a database connection
        conn = sqlite3.connect("application.db")
        # Creating database cursor to write into database
        c = conn.cursor()

        c.execute("SELECT username FROM USER WHERE sessionid = ?",  # Getting username by session id to the DB cursor
                  (cookie["session"].value,))
        # Setting user name from DB cursor
        uname = c.fetchone()

        c.execute("SELECT cid FROM CITY WHERE cname = ?",           # Getting city name ro the DB cursor
                  (form["cname"].value,))
        # Setting city name from DB cursor
        cid = c.fetchone()

        # Checking if there is any house in DB
        c.execute("SELECT count(*) FROM HOUSE")
        isThere = c.fetchone()

        # If there is no advertisement in DB
        if(isThere[0] == 0):

            c.execute("INSERT INTO HOUSE VALUES(?,?,?,?,?,?)",      # Insert the advertisement to DB
                      (1, form["sname"].value, form["noOfbedrooms"].value, form["mfee"].value, uname[0], cid[0]))

            print("<p>Creating the advertisement was successful</p>")
            print("<script>")
            print("window.alert('Creating the advertisement was successful');")
            print("window.location='applicationpage.html';")
            print("</script>")
            conn.commit()

        else:                                                   # If DB is not empty

            c.execute(                                          # Checking if DB has this advertisement already or not
                "SELECT * FROM HOUSE WHERE street = ? AND noOfBedrooms = ? AND monthlyfee = ?", (form["sname"].value, form["noOfbedrooms"].value, form["mfee"].value))

            row = c.fetchone()
            # If cursor has value this means
            # that specific advertisement already existing

            if row != None:                                         # If this advertisement is existing we print error

                print("<script>")
                print("window.alert('This Advertisement already exists');")
                print("window.location='applicationpage.html';")
                print("</script>")

            else:                                                   # If there is no advertisement we create one

                # Getting maximum house id to increment it
                c.execute("SELECT MAX(houseid) FROM HOUSE")
                houseid = c.fetchone()

                # Inserting the advertisement while incrementing the max house id
                # So that house id's will remain unique
                c.execute("INSERT INTO HOUSE VALUES(?,?,?,?,?,?)", (houseid[0]+1,
                          form["sname"].value, form["noOfbedrooms"].value, form["mfee"].value, uname[0], cid[0]))

                conn.commit()

                # Printing that advertisement is created successfully
                print("<script>")
                print("window.alert('Creating the advertisement was successful');")
                print("window.location='applicationpage.html';")
                print("</script>")

        conn.close()

    else:
        print("<p>Login required</p>")

else:
    print("<p>Login required</p>")

# c.execute("SELECT * FROM HOUSE")
# row = c.fetchall()
# while row != None:
#     print(row)
#     row = c.fetchone()
# conn.close()


printFooter()               # Printing footer
