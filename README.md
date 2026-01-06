# Library-QR-Code-Management-System

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25-orange?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Firebase](https://img.shields.io/badge/Firebase-FFCA28?logo=firebase&logoColor=black)](https://firebase.google.com/)

A **Streamlit-based Library Management System** built with Python and Firebase, using QR code technology for secure authentication, efficient book issue/return, transaction tracking, and automated overdue penalty management.

---

## Table of Contents

1. [Overview](#overview)  
2. [Problem Statement](#problem-statement)  
3. [Data Storage](#data-storage)  
4. [Tools & Technologies](#tools--technologies)  
5. [Project Structure](#project-structure)  
6. [System Workflow](#system-workflow)  
7. [Key Insights](#key-insights)  
8. [Use Cases](#use-cases)  
9. [Future Enhancements](#future-enhancements)  
10. [How to Run This Project](#how-to-run-this-project)  
11. [Author](#author)  

---

## Overview

Traditional libraries often rely on manual processes for managing books, student records, and transactions, which can be time-consuming and error-prone. This system automates library operations using **QR code technology**, enabling:

- Faster and more accurate book issue and return processes  
- Reliable tracking of overdue books and penalty calculations  
- Efficient digital management of books and student records  
- Secure authentication and complete transaction logging  

---

## Problem Statement

Manual library management systems are **time-consuming and prone to human error**, which often results in:

- Misplaced or lost books  
- Difficulty in tracking issued and returned books  
- Incorrect calculation of overdue fines  
- Inefficient management of student and book records  

To address these challenges, the **Library QR Code Management System** introduces a **digital, QR-based approach** that automates library operations and improves accuracy, efficiency, and reliability.

---

## Data Storage

All application data is stored and managed using **Firebase Realtime Database**, ensuring real-time synchronization and secure data handling:

- **Books:** Book ID, Title, Author, QR Code, Availability Status, Issued Status  
- **Students:** Student ID, Name
- **Transactions:** Book issue and return records, due dates, and overdue penalty details  
> All data is created and maintained within Firebase; no external sources are needed.

---

## Tools & Technologies

- **Frontend:** Streamlit 
- **Backend:** Python  
- **Database:** Firebase Realtime Database  
- **QR Code generation & Scanning:** `qrcode`, OpenCV  
- **Authentication:** Firebase Authentication  
- **Version Control:** Git & GitHub  

---

## Project Structure
```md
Library-QR-Code-Management-System/
│
├── Home.py
│
├── pages/
│   ├── 1_Manage_Books.py
│   ├── 2_Manage_Students.py
│   ├── 3_Issue_Book.py
│   ├── 4_Return_Book.py
│   ├── 5_Overdue.py
│   └── 6_Transaction_History.py
│
├── helpers/
│   └── firebase_helpers.py
│
├── firebase_config_example.py
├── requirements.txt
├── .gitignore
└── README.md
```
---

## System Workflow

1. **User Authentication** – Secure login using **Firebase Authentication** with email and password, ensuring that only authorized librarians or admins can access the system.  

2. **Book Management** – Add, update, or remove books from the library database, and automatically generate QR codes for each book for fast scanning.  

3. **Student Management** – Maintain student records by adding, updating, or removing student information efficiently.  

4. **Book Issue & Return** – Scan book QR codes to issue or return books. The system enforces a **maximum book issue limit per student**, tracks due dates, and updates the status of each book automatically.  

5. **Overdue Tracking** – Automatically calculate overdue fines based on due dates, ensuring accurate penalties for late returns.  

6. **Transaction History** – Maintain a complete log of all book issue and return transactions for easy auditing and reporting.

---

## Key Insights

- **QR-based workflows** streamline book issue and return processes, enhancing speed and accuracy.  
- **Firebase Realtime Database** ensures instant data synchronization across the system.  
- **Streamlit** allows rapid development of interactive, data-driven dashboards for library management.  
- **Automation of core tasks**, such as overdue calculations and transaction logging, reduces manual errors and improves efficiency.  
- **Role-based authentication and structured workflows** provide secure and organized management of books and student records.

---

## Use Cases

- College and school libraries  
- Small private libraries  
- Digital book tracking systems  
- QR-based inventory management  

---

## Future Enhancements

- Role-based access control (Admin / Librarian)  
- Book reservation system  
- Email notifications for due and overdue books  
- Support for multiple library branches  

---

## How to Run This Project

**1. Clone the repository**
```bash
git clone https://github.com/rashmi-devadiga/Library-QR-Code-Management-System.git
cd Library-QR-Code-Management-System
```
**2. Create a virtual environment (optional but recommended)**
```bash
#Create virtual environment
python -m venv venv

#Activate on Windows
venv\Scripts\activate

#Activate on macOS/Linux
source venv/bin/activate
```
**3. Install dependencies**
```bash
pip install -r requirements.txt
```
**4. Configure Firebase**
- Go to [Firebase Console](https://console.firebase.google.com/) and create a new project.
- Enable Email/Password Authentication.
- Enable Realtime Database.
- Rename firebase_config_example.py → firebase_config.py.

- Add your Firebase credentials in firebase_config.py:
```python
firebase_config = {
    "apiKey": "YOUR_API_KEY",
    "authDomain": "YOUR_PROJECT_ID.firebaseapp.com",
    "databaseURL": "https://YOUR_PROJECT_ID.firebaseio.com",
    "projectId": "YOUR_PROJECT_ID",
    "storageBucket": "YOUR_PROJECT_ID.appspot.com",
    "messagingSenderId": "YOUR_SENDER_ID",
    "appId": "YOUR_APP_ID"
}
```
**5. Run the Streamlit app**
```bash
streamlit run Home.py
```

---

## Author
**Rashmi Devadiga**  
Bachelor of Computer Applications Graduate  
[LinkedIn](https://www.linkedin.com/in/your-link) | [GitHub](https://github.com/your-username)

---
