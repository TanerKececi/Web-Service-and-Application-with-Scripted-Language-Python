#!C:\Users\DOGUKAN\AppData\Local\Programs\Python\Python39\python

import http.cookies as Cookie
import sqlite3
import cgi
import os

# Printing header
def printHeader(title):
    print("Content-type: text/html")
    print("")
    print("<html><head><title>{}</title></head><body>".format(title))

# Printing footer
def printFooter():
    print("</body></html>")

# Printing header with title
printHeader("Delete Advertisement")

if("HTTP_COOKIE" in os.environ):                                # Checking if there is any cookie

    cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])     # Getting cookie

    if "session" in cookie.keys():                              # If user has session (logged in)

        form = cgi.FieldStorage()                               # Creating a form

        conn = sqlite3.connect("application.db")                # Creating a connection with data base
        c = conn.cursor()                                       # Creating a database cursor

        print(form["deletead"].value)                           # Printing the form

        c.execute("DELETE FROM HOUSE WHERE houseid = ?",        # Deleting the advertisement by given house id
                  (form["deletead"].value,))

        conn.commit()                                           # Committing the changes to db
        conn.close()                                            # Closing the db connection

        # Printing alert message that deletion is successful
        print("<script>")
        print("window.alert('Row deletion is successful');")
        print("window.location='listad.py';")
        print("</script>")
