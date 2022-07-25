#!C:\Users\DOGUKAN\AppData\Local\Programs\Python\Python39\python

import http.cookies as Cookie
import sqlite3
import os

# charset=ISO-8859-9

# Printing header
def printHeader(title):
    print("Content-type: text/html; charset=\"UTF-8\"")
    print("")
    print("<html><head><title>{}</title>".format(title))
    print("<link rel='stylesheet' type='text/css' href='tabularformstyle.css'/></head><body style='background-color: gainsboro;'>")

# Printing footer
def printFooter():
    print("</body></html>")


# Printing header with title
printHeader("List Advertisements")


# Checking if there is cookie or not
if("HTTP_COOKIE" in os.environ):

    cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])     # Getting cookie

    if "session" in cookie.keys():                              # Checking if user has session (logged in)

        conn = sqlite3.connect("application.db")                # Creating db connection
        c = conn.cursor()                                       # Creating db connection cursor

        # Getting asked advertisements from database
        c.execute(
            "SELECT h.street, c.cname, h.noOfBedrooms, h.monthlyfee FROM HOUSE h, CITY c WHERE c.cid = h.cid")
        rows = c.fetchall()

        # print(row[3][1])
        print("<div style = 'float: right;'><a href='logout.py'><h3>Logout</h3></a></div>")
        print("<div style = 'float: left;'><a href='applicationpage.html'><h3>Previous Page</h3></a></div>")
        print("<table>")
        print("<tr><th>Street</th><th>City</th><th>Number of Bedrooms</th><th>Monthly Fee</th><th>Delete?</th>")

        deleteid = 0

        # Printing the data in table format
        for row in rows:
            print("<tr>")
            print("<td>{}</td>".format(row[0]))
            print("<td>{}</td>".format(row[1]))
            print("<td>{}</td>".format(row[2]))
            print("<td>{}</td>".format(row[3]))
            print("<td><form action='deletead.py' method='POST'><br><input type='text' name='deletead' value='{}' style='display: none; cursor:pointer;'>".format(
                deleteid+1))
            print("<input type='submit' value='Delete'></form></td>")
            print("</tr>")
            deleteid += 1

        print("</table>")
        conn.close()


printFooter()
