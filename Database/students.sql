CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rfid_uid VARCHAR(50),
    student_name VARCHAR(100)
);

INSERT INTO students (rfid_uid, student_name) VALUES
('B3C7F30', 'John Doe'),
('31B4DF5', 'David Smith');

SELECT * FROM students;
