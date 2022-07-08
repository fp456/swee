import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('intern_roles.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS saved_jobs
                        (ID INTEGER PRIMARY KEY,
                        TITLE TEXT NOT NULL,
                        COMPANY TEXT NOT NULL,
                        DESCRIPTION  TEXT NOT NULL,
                        LOCATION TEXT,
                        LINK TEXT );''')

    def save_job(self, job):
        id = job.get('id')
        title = job.get("title")
        company = job.get("company")
        location = job.get("location")
        description = job.get("description")
        link = job.get("link")
        self.cur.execute(f'''insert or replace into saved_jobs
                          (ID,TITLE,COMPANY,DESCRIPTION,LOCATION,LINK)
                          VALUES
                          ("{id}",
                          "{title}",
                          "{company}",
                          "{description}",
                          "{location}",
                          "{link}")''')
        self.conn.commit()

    def delete_job(self, id):
          """
          Delete a job by job id
          :param conn:  Connection to the SQLite database
          :param id: id of the job
          :return:
          """
          sql = 'DELETE FROM saved_jobs WHERE id=?'
          self.cur.execute(sql, (id,))
          self.conn.commit()

    def get_saved_jobs(self):
        jobs = []
        for row in self.cur.execute('SELECT * FROM saved_jobs'):
            job = {
                'id': row[0],
                'title': row[1],
                'company': row[2],
                'location': row[3],
                'description': row[4],
                'link': row[5]
            }
            jobs.append(job)
        return jobs

    def get_job(self, id):
        sql = 'SELECT * FROM saved_jobs WHERE id=?'
        for row in self.cur.execute(sql, (id,)):
            job = {
                  'id': row[0],
                  'title': row[1],
                  'company': row[2],
                  'location': row[3],
                  'description': row[4],
                  'link': row[5]
            }
        return job
