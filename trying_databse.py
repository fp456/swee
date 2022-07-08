import sqlite3

conn = sqlite3.connect('saved_jobs.db')

#conn.execute('''CREATE TABLE COMPANY
 #        (ID INT PRIMARY KEY     NOT NULL,
  #       NAME           TEXT    NOT NULL,
   #      AGE            INT     NOT NULL,
    #     ADDRESS        CHAR(50),
     #    SALARY         REAL);''')


values = {
      'ID': 4,
      'NAME': "Alice",
      'AGE' : 20,
      'ADDRESS': "DENVER",
      'SALARY' : 20000
}

conn.execute(f"INSERT OR REPLACE INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES ({values['ID']}, '{values['NAME']}', '{values['AGE']}', '{values['ADDRESS']}', {values['SALARY']} )")

conn.commit()

cursor = conn.execute("SELECT id, name, address, salary from COMPANY")
for row in cursor:
   print ("ID = ", row[0])
   print ("NAME = ", row[1])
   print ("ADDRESS = ", row[2])
   print ("SALARY = ", row[3], "\n")

conn.close()