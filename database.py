#!/usr/bin/python

import sqlite3


conn = sqlite3.connect('intern_roles.db')

conn.execute('''CREATE TABLE saved_jobs
             (ID INTEGER PRIMARY KEY  AUTOINCREMENT,
              TITLE TEXT NOT NULL,
              COMPANY TEXT NOT NULL,
              DESCRIPTION  TEXT NOT NULL,
              LOCATION TEXT,
              LINK TEXT );''')

def save_job(job):
      title=job.get("title")
      company=job.get("company")
      location=job.get("location")
      description=job.get("description")
      link=job.get("link")
      conn=sqlite3.connect("intern_roles.db")
      conn.execute(f"insert into saved_jobs (TITLE,COMPANY,DESCRIPTION,LOCATION,LINK) VALUES ('{title}','{company}','{description}','{location}','{link}')")
      conn.commit()
 
for row in conn.execute("SELECT* FROM saved_jobs ORDER BY title"):
      print(row)

def delete_job(id):
    """
    Delete a job by job id
    :param conn:  Connection to the SQLite database
    :param id: id of the job
    :return:
    """
    conn=sqlite3.connect("intern_roles.db")
    sql = 'DELETE FROM saved_jobs WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()
    cur.execute("SELECT * FROM saved_jobs")
    conn.commit()

cur=conn.cursor()
cur.execute("SELECT * FROM saved_jobs")
print(cur.fetchall())
  
conn.commit()

conn.close()