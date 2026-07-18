# Automated Income Tax & Client Management System

A modern, responsive full-stack web application designed for tax professionals to compute dynamic income tax liabilities and manage client financial ledgers cleanly. Built as an independent capstone prototype during my technical placement training.

## 🚀 Features
- **Interactive UI Dashboard:** Built using semantic HTML5 and modern CSS Grid/Flexbox layouts.
- **Dynamic Tax Calculation Engine:** Implements the progressive slab-based tax calculation model with safe client-side validation checks.
- **Robust Flask REST API Backend:** Server-side computational validation built with Python Flask.
- **Relational SQL Database Layer:** Implements a schema mapping a `Clients` master table to a `TaxRecords` ledger table via transactional Foreign Keys (`ON DELETE CASCADE`).

---

## 🛠️ Tech Stack
- **Frontend:** HTML5, CSS3, JavaScript (ES6+ Asynchronous Fetch)
- **Backend Framework:** Python Flask
- **Database Engine:** SQLite (Relational SQL)

---

## 💻 Installation & Setup Guide

Ensure you have **Python 3.x** installed on your machine before starting.

### 🍏 Option A: Running on macOS

1. **Open Terminal** and navigate to the project directory:
   ```bash
   cd ~/Documents/tax-management-system
   Set up a clean Virtual Environment:

Bash
python3 -m venv env
Activate the environment:

Bash
source env/bin/activate
Install necessary project dependencies:

Bash
pip install --upgrade pip
pip install Flask
Start the web application server:

Bash
python app.py
🪟 Option B: Running on Windows
Open Command Prompt (cmd) or PowerShell and navigate to your project workspace folder:

DOS
cd C:\Users\YourUsername\Documents\tax-management-system
Create a Virtual Environment:

DOS
python -m venv env
Activate the environment:

If using Command Prompt:

DOS
env\Scripts\activate.bat
If using PowerShell:

PowerShell
.\env\Scripts\Activate.ps1
Install dependencies:

DOS
pip install --upgrade pip
pip install Flask
Start the application:

DOS
python app.py
