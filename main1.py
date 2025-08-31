from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import uuid
import re
import smtplib
from email.message import EmailMessage
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  
    allow_headers=["*"],
)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Yokesh@123",      
    database="studentdb"
)
cursor = db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    email_verified BOOLEAN DEFAULT FALSE,
    verify_token VARCHAR(64),
    mobile VARCHAR(20) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    current_location VARCHAR(200) NOT NULL,
    permanent_address VARCHAR(300) NOT NULL,
    college_name VARCHAR(200) NOT NULL,
    school_name VARCHAR(200) NOT NULL,
    photo LONGBLOB,
    resume LONGBLOB,
    INDEX idx_email(email)
)
""")
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "yokeshvenkadachalam@gmail.com"
SMTP_PASSWORD = "dkvs aktz dfxs tfzm"  
def validate_email_simple(email: str):
    regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(regex, email):
        raise ValueError("Invalid email format")
def send_verification_email(to_email: str, token: str):
    msg = EmailMessage()
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = "Verify Your Email"
    msg.set_content(f"Click the link to verify your email: http://localhost:4200/verify?token={token}")

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
@app.post("/students")
async def add_student(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    mobile: str = Form(...),
    gender: str = Form(...),
    current_location: str = Form(...),
    permanent_address: str = Form(...),
    college_name: str = Form(...),
    school_name: str = Form(...),
    photo: UploadFile = File(...),
    resume: UploadFile = File(...)
):
    try:
        validate_email_simple(email)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    token = str(uuid.uuid4())
    photo_data = await photo.read()
    resume_data = await resume.read()
    try:
        cursor.execute("""
            INSERT INTO students
            (first_name, last_name, email, verify_token, mobile, gender, current_location,
             permanent_address, college_name, school_name, photo, resume)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            first_name, last_name, email, token, mobile, gender,
            current_location, permanent_address, college_name,
            school_name, photo_data, resume_data
        ))
        db.commit()
    except mysql.connector.Error as e:
        if e.errno == 1062:  
            raise HTTPException(status_code=400, detail="This email is already registered.")
        raise HTTPException(status_code=400, detail=f"MySQL error: {e}")
    try:
        send_verification_email(email, token)
    except Exception:
        pass

    return {"message": "Student added successfully! Please check your email to verify."}
@app.get("/verify-email")
async def verify_email(token: str):
    cursor.execute("SELECT id FROM students WHERE verify_token=%s", (token,))
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=400, detail="Invalid or expired token.")

    cursor.execute(
        "UPDATE students SET email_verified=TRUE, verify_token=NULL WHERE verify_token=%s",
        (token,)
    )
    db.commit()
    return {"message": "Email verified successfully!"}
