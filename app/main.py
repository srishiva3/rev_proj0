from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import sqlite3
from typing import Optional, List


# FastAPI app setup
app = FastAPI()

# Database connection setup
conn = sqlite3.connect(r"C:\Users\HP\Desktop\srip0\db.db")
cursor = conn.cursor()

# Pydantic model for JobSeeker registration
class JobSeekerRegistration(BaseModel):
    jobseeker_name: str
    email_id: str
    pass_wd: str
    contact_no: int
    js_resume: bytes
    work_exp: str
    qualification: str
    skill_set: str

# Pydantic model for JobSeeker login
class JobSeekerLogin(BaseModel):
    email_id: str
    pass_wd: str


# Endpoint for job seeker registration
@app.post("/job-seekers/register")
async def register_job_seeker(job_seeker: JobSeekerRegistration):
    try:
        query = """
            INSERT INTO jobseeker (jobseeker_name, email_id, pass_wd, contact_no, js_resume, work_exp, qualification, skill_set)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
            job_seeker.jobseeker_name, job_seeker.email_id, job_seeker.pass_wd,
            job_seeker.contact_no, job_seeker.js_resume, job_seeker.work_exp,
            job_seeker.qualification, job_seeker.skill_set
        ))
        conn.commit()
        return {"message": "Job seeker registered successfully"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()


# Endpoint for job seeker login
@app.post("/job-seekers/login")
async def login_job_seeker(job_seeker: JobSeekerLogin):
    try:
        conn = sqlite3.connect(r"C:\Users\HP\Desktop\srip0\db.db")
        cursor = conn.cursor()
        
        query = "SELECT * FROM jobseeker WHERE email_id = ? AND pass_wd = ?"
        cursor.execute(query, (job_seeker.email_id, job_seeker.pass_wd))
        job_seeker_data = cursor.fetchone()

        if job_seeker_data:
            return {
                "message": "Login successful",
                "job_seeker_data": job_seeker_data,
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()


# Pydantic model for Employer registration
class EmployerRegistration(BaseModel):
    company_name: str
    email_id: str
    pass_wd: str
    contact_person: str
    location: str

# Pydantic model for Employer login
class EmployerLogin(BaseModel):
    email_id: str
    pass_wd: str


# Endpoint for employer registration
@app.post("/employers/register")
async def register_employer(employer: EmployerRegistration):
    try:
        query = """
            INSERT INTO employer (company_name, email_id, pass_wd, contact_person, location)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
            employer.company_name, employer.email_id, employer.pass_wd,
            employer.contact_person, employer.location
        ))
        conn.commit()
        return {"message": "Employer registered successfully"}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()


# Endpoint for employer login
@app.post("/employers/login")
async def login_employer(employer: EmployerLogin):
    try:
        conn = sqlite3.connect(r"C:\Users\HP\Desktop\srip0/db.db")
        cursor = conn.cursor()
        
        query = "SELECT * FROM employer WHERE email_id = ? AND pass_wd = ?"
        cursor.execute(query, (employer.email_id, employer.pass_wd))
        employer_data = cursor.fetchone()

        if employer_data:
            return {
                "message": "Login successful",
                "employer_data": employer_data,
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()


# Define the data model for a job posting
class JobPosting(BaseModel):
    title: str
    descriptions: str
    location: str
    experience_required: int
    employer_id: int
    job_type: str
    salary_range: str
    skills_required: str  # Comma-separated list of skills
    date_posted: str  # Expected date in string format like "YYYY-MM-DD"


# Endpoint to create a new job posting
@app.post("/job_posting", status_code=status.HTTP_201_CREATED)
def create_job_posting(job_posting: JobPosting):
    try:
        conn = sqlite3.connect(r"C:\Users\HP\Desktop\srip0/db.db")
        cursor = conn.cursor()
        
        query = """
            INSERT INTO job_posting (title, descriptions, location, experience_required, employer_id, job_type, salary_range, skills_required, date_posted)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(
            query,
            (
                job_posting.title,
                job_posting.descriptions,
                job_posting.location,
                job_posting.experience_required,
                job_posting.employer_id,
                job_posting.job_type,
                job_posting.salary_range,
                job_posting.skills_required,
                job_posting.date_posted,
            ),
        )
        
        conn.commit()
        return {"message": "Job posting created successfully"}
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        conn.close()


# Pydantic model for job application
class JobApplication(BaseModel):
    job_seeker_id: int
    cover_letter: str


# Endpoint to apply for a job
@app.post("/jobs/{job_id}/apply", status_code=status.HTTP_200_OK)
async def apply_for_job(job_id: int, application: JobApplication):
    conn = None
    try:
        conn = sqlite3.connect(r"C:\Users\HP\Desktop\srip0/db.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM job_posting WHERE job_id = ?", (job_id,))
        job_posting = cursor.fetchone()

        if not job_posting:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job posting not found")

        query = """
            INSERT INTO application (job_seeker_id, job_posting_id, cover_letter, application_date, status)
            VALUES (?, ?, ?, datetime('now'), 'Applied')
        """
        cursor.execute(query, (application.job_seeker_id, job_id, application.cover_letter))
        conn.commit()

        return {"message": "Application submitted successfully"}

    except sqlite3.Error as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")
    finally:
        if conn:
            conn.close()


# Define the data model for job application status update
class ApplicationStatusUpdate(BaseModel):
    status: str  # Possible values: "shortlisted", "rejected"


# Endpoint to view applicants for a specific job posting
@app.get("/jobs/{job_id}/applicants/", response_model=List[JobApplication], status_code=status.HTTP_200_OK)
async def view_applicants(job_id: int):
    try:
        conn = sqlite3.connect(r"C:\Users\HP\Desktop\srip0/db.db")
        cursor = conn.cursor()
        
        query = """
            SELECT * FROM application WHERE job_posting_id = ?
        """
        cursor.execute(query, (job_id,))
        applications = cursor.fetchall()

        if not applications:
            raise HTTPException(status_code=404, detail="No applicants found for this job posting")
        
        columns = [col[0] for col in cursor.description]

        application_list = [
            {columns[i]: app[i] for i in range(len(columns))}
            for app in applications
        ]

        return [
            JobSeekerApplication(
                application_id=app["application_id"],
                job_seeker_id=app["job_seeker_id"],
                job_posting_id=app["job_posting_id"],
                status=app["status"],
                cover_letter=app.get("cover_letter", None),
            )
            for app in application_list
        ]

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        if conn:
            conn.close()


# Endpoint to update the status of a job application
@app.patch("/jobs/{job_id}/applicants/{application_id}", status_code=status.HTTP_200_OK)
async def update_application_status(job_id: int, application_id: int, status_update: ApplicationStatusUpdate):
    if status_update.status not in ["shortlisted", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    try:
        conn = sqlite3.connect(r"C:\Users\HP\Desktop\srip0/db.db")
        cursor = conn.cursor()
        
        query = """
            SELECT * FROM application 
            WHERE job_posting_id = ? AND application_id = ?
        """
        cursor.execute(query, (job_id, application_id))
        application = cursor.fetchone()

        if not application:
            raise HTTPException(status_code=404, detail="Application not found")

        query = """
            UPDATE application 
            SET status = ? 
            WHERE job_posting_id = ? AND application_id = ?
        """
        cursor.execute(query, (status_update.status, job_id, application_id))
        conn.commit()

        return {"message": "Application status updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        conn.close()
