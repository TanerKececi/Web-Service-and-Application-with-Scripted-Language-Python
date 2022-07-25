#!C:\Users\DOGUKAN\AppData\Local\Programs\Python\Python39\python

import sqlite3
import cgi

# Printing header
def printHeader(title):
    print("Content-type: text/html")
    print("")
    print("<html><head><title>{}</title>".format(title))
    print("<link rel='stylesheet' type='text/css' href='tabularformstyle.css'/>")
    print("</head><body style='background-color:gainsboro;'>")

# Printing footer
def printFooter():
    print("</body></html>")


printHeader("Most Recent Advertisements")           # Printing header with title

conn = sqlite3.connect("application.db")            # Creating database connection
c = conn.cursor()                                   # Creating database connection cursor

# Printing previous page button and form for criterias
print("<div><a href='homepage.html'><h3>Previous Page</h3></a></div>")
print("<div style = 'text-align: center;'><h3>List criteria</h3>")
print("<p>(Fill the desired blank to get the list by criteria. To see all list leave fields empty and click submit)</p>")
print("<form action='listallad.py' method='post' name='adcriteria'>")
print("<p>No of Bedrooms: <input type='text' name='bed'></p>")
print("<p>Monthly Fee Range: <input type='text' name='fee1'> , <input type='text' name='fee2'></p>")
print("<p>City: <input type='text' name='cname'></p>")
print("<input type='submit' style='cursor:pointer;' ><br></br></form></div>")

form = cgi.FieldStorage()       # Getting criteria

try:
    bed = form["bed"].value     # Getting bed criteria if there is any
except:
    bed = ""

try:
    fee1 = form["fee1"].value     # Getting fee criteria if there is any
    fee2 = form["fee2"].value
except:
    fee1 = ""
    fee2 = ""

try:
    cname = form["cname"].value     # Getting cname criteria if there is any
except:
    cname = ""

# Creating base query string
# We will concatenate the filters at the end of this string
query = "SELECT h.street, c.cname, h.noOfBedrooms, h.monthlyfee, u.email, u.phoneNo FROM HOUSE h, CITY c, USER u WHERE c.cid = h.cid AND h.username = u.username "
val = ()

if bed != "":                                       # If there is bed criteria
    query = query+"AND h.noOfBedrooms = ? "         # Add criteria in the end of query
    val = val + (bed,)

if cname != "":                                     # If there is city criteria
    query = query + "AND c.cname = ? "              # Add criteria in the end of query
    val = val + (cname,)

if fee1 != "" and fee2 != "":                               # If there is fee criteria
    query = query + "AND h.monthlyfee BETWEEN ? AND ? "     # Add criteria in the end of query
    val = val + (fee1, fee2)

c.execute(query, val)                   # Executing the query

row = c.fetchone()                      # To check if there is any result we get first row

if row == None:                         # If there is no row we print error
    print("<h3 style='text-align: center;'>No Advertisement found</h3>")

else:                                   # If there is a row we print table
    print("<table>")
    print("<tr><th>Street</th><th>City</th><th>Number of Bedrooms</th><th>Monthly Fee</th><th>Contact Email</th><th>Contact Phone</th>")

    while row != None:
        print("<tr>")
        print("<td>{}</td>".format(row[0]))
        print("<td>{}</td>".format(row[1]))
        print("<td>{}</td>".format(row[2]))
        print("<td>{}</td>".format(row[3]))
        print("<td>{}</td>".format(row[4]))
        print("<td>{}</td>".format(row[5]))
        print("</tr>")
        row = c.fetchone()

conn.close()

printFooter()
