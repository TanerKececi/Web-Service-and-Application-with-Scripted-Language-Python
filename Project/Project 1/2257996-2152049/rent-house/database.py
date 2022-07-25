import sqlite3

# Creating database
def createDatabase(dbfilename):

    conn = sqlite3.connect(dbfilename)                  # Creating database connection
    c = conn.cursor()                                   # Creating database connection cursor

    # Creating User table if it is not created already
    # username is integer and primary key
    # No fields can be null
    # sessionID is integer others are text
    c.execute("""CREATE TABLE IF NOT EXISTS USER(
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        fullname TEXT NOT NULL,
        email TEXT NOT NULL,
        phoneNo TEXT NOT NULL,
        sessionID INTEGER NOT NULL)""")

    # Creating city table if it is not created already
    # cid (city id) is integer and primary key
    # cname (city name) can't be null and it is text
    c.execute("""CREATE TABLE IF NOT EXISTS CITY(
        cid INTEGER PRIMARY KEY,
        cname TEXT NOT NULL)""")

    # Creating house if it is not created already
    # houseid is integer and primary key
    # No attribute can be null
    # street and username is text others are integer
    # username is foreign key to user table
    # cid is foreign key to city table
    c.execute("""CREATE TABLE IF NOT EXISTS HOUSE(
        houseid INTEGER PRIMARY KEY,
        street TEXT NOT NULL,
        noOfBedrooms INTEGER NOT NULL,
        monthlyFee INTEGER NOT NULL,
        username TEXT NOT NULL,
        cid INTEGER NOT NULL,
        FOREIGN KEY (username) REFERENCES USER(username),
        FOREIGN KEY (cid) REFERENCES CITY(cid))""")

    conn.commit()
    conn.close()

# Inserting cities to database
def insertRecords(dbfilename):

    conn = sqlite3.connect(dbfilename)
    c = conn.cursor()

    cities = [(1, "Lefkosa"), (2, "Girne"),
              (3, "Gazi Magusa"), (4, "Iskele"), (5, "Guzelyurt"), (6, "Lefke")]

    c.executemany("INSERT INTO CITY VALUES(?,?)", cities)

    conn.commit()
    conn.close()

# main function
if __name__ == "__main__":

    dbfilename = "application.db"       # creating application.db file
    createDatabase(dbfilename)          # creating database
    insertRecords(dbfilename)           # inserting cities into database

    conn = sqlite3.connect(dbfilename)  # creating file connection
    c = conn.cursor()                   # creating database cursor

    c.execute("SELECT * FROM CITY")     # Printing cities to console for testing
    row = c.fetchone()
    while row != None:
        print(row)
        row = c.fetchone()
