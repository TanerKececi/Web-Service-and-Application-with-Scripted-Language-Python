#!C:\Users\DOGUKAN\AppData\Local\Programs\Python\Python39\python

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


printHeader("Registration")                                     # Printing header with title

form = cgi.FieldStorage()                                       # Creating a form

conn = sqlite3.connect("application.db")                        # Creating a database connection
c = conn.cursor()                                               # Creating a database connection cursor

# Asking given username to database it is in database
c.execute("SELECT username FROM USER WHERE username = ? ", (form["uname"].value,))

row = c.fetchone()

if row != None:                         # Printing that given user is existing already
    print("<p>This user exists</p>")

# Otherwise inserting the user to database
else:
    c.execute("INSERT INTO USER VALUES(?,?,?,?,?,?)",
              (form["uname"].value, form["pwd"].value, form["name"].value, form["email"].value, form["pnum"].value, -1))
    conn.commit()

    # Printing the registration is successful message
    print("<script>")
    print("window.alert('Registration is successful');")
    print("window.location='homepage.html';")
    print("</script>")

# c.execute("SELECT * FROM USER")
# row = c.fetchone()
# while row != None:
#     print(row)
#     row = c.fetchone()
# conn.close()

printFooter()
