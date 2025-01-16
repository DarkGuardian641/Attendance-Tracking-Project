# IoT Attendance Tracker

## Project Overview
The **IoT Attendance Tracker** is an RFID-based attendance management system designed to automate the process of recording and storing attendance. The system uses an Arduino Uno microcontroller, RFID readers, and a MySQL database to provide an efficient and low-cost solution for attendance tracking in various settings like schools, offices, and events.

---

## Features
- **Automated Attendance**: Tracks attendance using RFID tags assigned to individuals.
- **Efficient Data Management**: Stores attendance records in a MySQL database for easy access and retrieval.
- **Scalability**: Can be implemented in multiple environments with minimal adjustments.
- **Real-time Compatibility**: Potential for real-time updates with future Wi-Fi integration.

---

## System Requirements

### Hardware
- Arduino Uno
- RFID Reader and Tags
- Connecting Wires

### Software
- Arduino IDE
- MySQL Database
- Python (optional for advanced features)

---

## Setup

1. **Hardware Setup**:
   - Connect the RFID reader to the Arduino Uno using appropriate wires.
   - Assign RFID tags to users.

2. **Software Setup**:
   - Install the Arduino IDE and upload the provided Arduino code to the Arduino Uno.
   - Configure the MySQL database with the necessary schema:
     - Table: `attendance`
     - Fields: `id` (Primary Key), `rfid_id`, `name`, `date`, `time`.

3. **Database Configuration**:
   - Use MySQL to create the database and table structure.
   - Ensure the Arduino communicates with the database to log attendance records.

---

## Modules Used

1. **Hardware Module**:
   - **RFID Reader and Tags**: Reads and identifies users based on their RFID tags.
   - **Arduino Uno**: Microcontroller to process RFID data and interface with the database.

2. **Software Module**:
   - **Arduino Code**: Handles RFID data reading and communication.
   - **MySQL Database**: Stores attendance data for easy retrieval and analysis.

---

## Test Cases

### Test Case 1
- **Description**: Verify RFID reader functionality.
- **Input**: Present an RFID tag to the reader.
- **Expected Output**: Tag ID is displayed on the serial monitor and stored in the database.
- **Result**: Pass

### Test Case 2
- **Description**: Check database storage.
- **Input**: Insert data via RFID tag interaction.
- **Expected Output**: Data is correctly stored in MySQL fields.
- **Result**: Pass

### Test Case 3
- **Description**: Test system with multiple tags.
- **Input**: Present multiple RFID tags sequentially.
- **Expected Output**: Each tag is read and logged without conflict.
- **Result**: Pass

---

## Author
This project was collaboratively developed by:
- **Atharva Baikar**
- **Akanksha Kanade**
- **Sakshi Chandekar**
- **Azlaan Khan**

For any inquiries or contributions, feel free to reach out.