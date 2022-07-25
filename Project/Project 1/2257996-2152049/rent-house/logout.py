#!C:\Users\DOGUKAN\AppData\Local\Programs\Python\Python39\python
import http.cookies as Cookie
import random
import sqlite3
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
printHeader("Logout process")

if "HTTP_COOKIE" in os.environ:                                                  # Checking if there is any cookie

    cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])                      # Getting cookie

    if "session" in cookie.keys():                                      # If there is a session we enter this if

        conn = sqlite3.connect("application.db")                        # Creating database connection
        c = conn.cursor()                                               # Creating database connection cursor

        # Getting session id
        c.execute("SELECT * FROM USER WHERE sessionid= ?",
                  (cookie["session"].value,))
        row = c.fetchone()


        if row != None:

            # Updating the session id with -1 instead of deleting it
            c.execute("UPDATE USER SET sessionid = -1 WHERE username = ?", (row[0],))

            conn.commit()

            # Printing the logout successful message
            print("<script>")
            print("document.cookie = 'session=; expires=Thu, 01 Jan 1970 00:00:00 UTF; path=/;';")
            print("window.alert('Logout is successful!');")
            print("window.location='homepage.html';")
            print("</script>")

        else:
            print("<p>No matching user!</p>")
        conn.close()
    else:
        print("<p>Login required!</p>")
else:
    print("<p>Login required!</p>")

printFooter()
