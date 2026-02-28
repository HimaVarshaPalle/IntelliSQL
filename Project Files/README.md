**IntelliSQL**
# Intelligent SQL Querying with Large Language Models

IntelliSQL lets you interact with a database using plain English. It converts your natural language questions into SQL using Google's Gemini Pro model and displays the results in an interactive Streamlit web interface.

---

# Project Overview

Most people who work with databases don't have strong SQL skills. IntelliSQL solves this by letting anyone — students, analysts, or business users — simply type a question like *"show all customers from Hyderabad"* and get instant results, without writing a single line of SQL.

---

# Features

-  Ask questions in plain English
-  Gemini Pro converts them to SQL automatically
-  Results displayed as a clean interactive table
-  Query history with timestamps
-  API key input directly in the browser sidebar
-  One-click example questions to get started

---

# Project Structure

```
IntelliSQL/
├── app.py                  # Main Streamlit web application
├── setup_database.py       # Creates the SQLite database and inserts sample data
├── requirements.txt        # Python dependencies
├── sales.db                # SQLite database (created after running setup)
└── README.md
```

---

# How to Run

# Step 1 — Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/IntelliSQL.git
cd IntelliSQL
```

# Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

# Step 3 — Set up the database
```bash
python setup_database.py
```
This creates `sales.db` with a `customers` table and sample records.

# Step 4 — Add your Google API Key
Open `app.py` and replace line 4:
```python
client = genai.Client(api_key="YOUR_API_KEY_HERE")
```
Get a free API key at: https://aistudio.google.com/app/apikey

# Step 5 — Run the app
```bash
streamlit run app.py
```
The app will open at **http://localhost:8501**

---

# Database Schema

```
customers(id, name, city, purchase_amount)
```

**Sample data:**
| ID | Name   | City      | Purchase Amount |
|----|--------|-----------|----------------|
| 1  | Neerja | Kadapa    | 2500           |
| 2  | Nikhil | Tirupati  | 5000           |
| 3  | Rehman | Hyderabad | 7568           |

---

# Tech Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| Frontend   | Streamlit                           |
| AI / LLM   | Google Gemini Pro (via google-genai) |
| Database   | SQLite3                             |
| Language   | Python 3.12                         |

---

# Requirements

```
google-genai
streamlit
python-dotenv
pandas
```

---

# Example Questions to Try

- Show all customers
- Who is from Hyderabad?
- Show the customer with the highest purchase amount
- Count total customers
- Sort customers by purchase amount

---

# Note

This project uses the **Google Gemini API (Free Tier)**. Make sure to use your own API key. Get one for free at https://aistudio.google.com/app/apikey

---

# Submission

This project was built as part of the **IntelliSQL** submission covering:
- Ideation Phase
- Requirement Analysis
- Project Design
- Project Planning
- Project Development
- Project Documentation
- Project Demonstration
