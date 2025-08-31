CREATE DATABASE IF NOT EXISTS studentdb;
USE studentdb;
DROP TABLE IF EXISTS students;
CREATE TABLE students (
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
);
SELECT * FROM students;
