# Week 3 Labs: Flet User Login Application

This folder contains a simple Flet-based Login application connected to MySQL, following the lab instructions.

## Prerequisites
- Python 3.x
- MySQL Server
- Replace the password in `userlogin/src/db_connection.py` with your actual MySQL root password.

## Setup
```sql
-- Create database and table in MySQL
CREATE DATABASE fletapp;
USE fletapp;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);
INSERT INTO users (username, password) VALUES ("testuser", "password123");
```

## Install dependencies
```bash
pip install -r requirements.txt
```

## Run the app
```bash
cd userlogin
flet run
```

Expected behavior matches the lab spec (success, failure, input error, and DB error dialogs).
