import sqlite3
import json
class JobDatabase:
    def __init__(self, db_name='jobs.db'):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self._create_table()
    def _create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS jobs (
                          title TEXT,
                          location TEXT,
                          skills TEXT
                          )''')
        self.conn.commit()
    def insert_job(self, job):
        self.c.execute("INSERT OR IGNORE INTO jobs VALUES (?, ?, ?)", (job["title"], job["location"], json.dumps(job["skills"])))
        self.conn.commit()
    def get_jobs(self):
        self.c.execute("SELECT * FROM jobs")
        return self.c.fetchall()