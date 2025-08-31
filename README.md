Student Registration & Email Verification System
This project is a full-stack web application developed as part of my internship. It allows students to register securely, stores their details in a database, and verifies their email addresses through a token-based verification link — simulating a real-world user onboarding workflow.
🚀 Features
Responsive student registration form with Angular
Secure data handling and RESTful APIs using FastAPI (Python)
MySQL database integration for persistent storage
Token-based email verification flow
Modular architecture for scalability and maintainability
🛠️ Tech Stack
Frontend: Angular
Backend: FastAPI (Python)
Database: MySQL
📌 Use Case
This project demonstrates the fundamentals of modern full-stack application development, user authentication workflows, and integration between frontend, backend, and database systems. It is an excellent reference for students and developers looking to understand secure form handling and email verification processes in web applications.


[ User (Student) ]
         │
         ▼
[ Frontend (Angular) ]
         │
         ▼
[ Backend (FastAPI - Python) ]
     ┌───────────────┴───────────────┐
     ▼                               ▼
[ MySQL Database ]         [ Email Service (SMTP) ]
                                   │
                                   ▼
                          [ Verification Link Sent ]
                                   │
                                   ▼
                          [ User Clicks Link ]
                                   │
                                   ▼
                        [ Backend verifies token → Updates DB ]

