#!C:\Users\DOGUKAN\AppData\Local\Programs\Python\Python39\python

import http.cookies as Cookie
import random
import sqlite3
import cgi

# Printing header
def printHeader(title):
    print("Content-type: text/html")
    print("")
    print("<html><head><title>{}</title></head><body>".format(title))

# Printing footer
def printFooter():
    print("</body></html>")

# Printing header with title
printHeader("Login")

form = cgi.FieldStorage()                                               # Creating form

conn = sqlite3.connect("application.db")                                # Creating db connection
c = conn.cursor()                                                       # Creating db connection cursor

c.execute("SELECT * FROM USER WHERE username = ? AND password = ?",     # Trying to get users with given uname nad pwd
          (form["uname"].value, form["pwd"].value))

row = c.fetchone()

# If database returns none it means no user existing with that username and password
# Else it is a hit
if(row != None):

    print("<script>window.alert('Login Successful');</script>")         # Printing login successful

    cookie = Cookie.SimpleCookie()                                      # Creating a cookie
    cookie["session"] = random.randint(1, 1000000)
    cookie["session"]["domain"] = "localhost"
    cookie["session"]["path"] = "/"

    c.execute("UPDATE USER SET sessionid = ? Where username = ?",       # Updating user's session in db
              (cookie["session"].value, form["uname"].value))

    conn.commit()

    print("<script>")
    print("document.cookie = '{}'; ".format(
        cookie.output().replace("Set-Cookie: ", "")))                   # Updating cookie
    print("window.location = 'applicationpage.html';")
    print("</script>")

# If there is no user with that username and password
# We print error
else:
    print("<script>")
    print("window.alert('Incorrect Username or Password');")
    print("window.location = 'loginpage.html';")
    print("</script>")

conn.close()

printFooter()
