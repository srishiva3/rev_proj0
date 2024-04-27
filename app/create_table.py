import sqlite3
con = sqlite3.connect("/mnt/c/Computer_science/devops/revature/srip0/db.db")
cur = con.cursor()

cur.execute("""CREATE TABLE jobseeker (
            jobseeker_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            jobseeker_name TEXT, email_id TEXT,
            pass_wd TEXT,
            contact_no INTEGER, 
            js_resume BLOB,
            work_exp TEXT,
            qualification TEXT,
            skill_set TEXT)""")



cur.execute("""CREATE TABLE employer (
            employer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT, 
            email_id TEXT,
            pass_wd TEXT,
            contact_person TEXT,
            location TEXT)""")


cur.execute("""CREATE TABLE job_posting (
            job_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            descriptions TEXT,
            location TEXT,
            experience_required INTEGER,
            employer_id INTEGER,
            job_type TEXT,
            salary_range TEXT,
            skills_required TEXT, 
            date_posted TEXT)""")

cur.execute("""CREATE TABLE application (
            application_id INTEGER PRIMARY KEY AUTOINCREMENT,

            job_seeker_id INTEGER,
            job_posting_id INTEGER,
            cover_letter TEXT,
            application_date TEXT,
            status TEXT)""")




jobseeker=con.execute('''select * from jobseeker''').fetchall()
employer=con.execute('''select * from employer''').fetchall()
jobs=con.execute('''select * from job_posting''').fetchall()
applications = con.execute('''SELECT * FROM application''').fetchall()


print(jobseeker)
print(employer)
print(jobs)
print(applications)


con.commit()

con.close()
