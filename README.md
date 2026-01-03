# Library-QR-Code-Management-System

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25-orange?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Firebase](https://img.shields.io/badge/Firebase-FFCA28?logo=firebase&logoColor=black)](https://firebase.google.com/)

A **Streamlit-based Library Management System** using **Python** and **Firebase** that leverages **QR code technology** to manage books, students, and library transactions efficiently. The system enables **secure authentication, QR-based book issue/return, transaction history tracking, and overdue penalty management**, allowing librarians to manage library operations digitally with improved accuracy and efficiency.

---

## Table of Contents

1. [Overview](#overview)  
2. [Problem Statement](#problem-statement)  
3. [Data Storage](#data-storage)  
4. [Tools & Technologies](#tools--technologies)  
5. [Project Structure](#project-structure)  
6. [Methods](#methods)  
7. [Key Insights](#key-insights)  
8. [Use Cases](#use-cases)  
9. [Future Enhancements](#future-enhancements)  
10. [How to Run This Project](#how-to-run-this-project)  
11. [Author](#author)  

---

## Overview

Traditional libraries often rely on manual processes for book management, student records, and transaction tracking. This system automates library operations using **QR code technology**, enabling:

- Faster book issue and return processes
- Accurate tracking of overdue books and penalties  
- Efficient digital management of books and students  
- Secure authentication and transaction logging  

---

## Problem Statement

Manual library management is **time-consuming and error-prone**, leading to:

- Misplaced or lost books  
- Difficulty tracking borrowed and returned books  
- Errors in calculating overdue fines  
- Inefficient student and book management  

The **Library QR Code Management System** provides a **digital, QR-based solution** to handle these challenges efficiently.

---

## Data Storage

All data is stored in **Firebase Realtime Database**:

- **Books:** Book ID, Title, Author, QR Code, Availability  
- **Students:** Student ID, Name 
- **Transactions:** Book issued, returned, due dates, overdue penalties  

> No external dataset is required; all data is managed in Firebase.

---

## Tools & Technologies

- **Frontend:** Streamlit  
- **Backend:** Python  
- **Database:** Firebase Realtime Database  
- **QR Code:** `qrcode`, OpenCV  
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

## Methods

1. **User Authentication** – Secure login via Firebase Authentication.  
2. **Book Management** – Add, update, delete books; generate QR codes.  
3. **Student Management** – Add, update, remove student records.  
4. **Book Issue & Return** – Scan QR codes to issue/return books; track due dates.  
5. **Overdue Tracking** – Automatic penalty calculation based on due dates.  
6. **Transaction History** – Complete log of issued and returned books.

---

## Key Insights

- QR-based workflows significantly improve accuracy and speed.
- Firebase Realtime Database enables instant data synchronization.
- Streamlit allows rapid development of data-driven dashboards.
- Automation reduces manual errors in book tracking and fine calculation.  

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
BCA Graduate | Python Developer | Streamlit & Firebase Applications   
[LinkedIn](https://linkedin.com/in/rashmidevadiga) |
[GitHub](https://github.com/rashmi-devadiga)

---
