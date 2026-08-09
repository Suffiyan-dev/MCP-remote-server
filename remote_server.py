from unicodedata import category
from dns.e164 import query
from fastmcp import FastMCP
import os 
import sqlite3

DB_path = os.path.join(os.path.dirname(__file__),"expenses.db")
mcp = FastMCP(name="Expense Tracker")

CATEGORIES_PATH = os.path.join(os.path.dirname(__file__),"categories.json")


def init_db():
    with sqlite3.connect(DB_path) as c:
        c.execute("""
        CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        subcatagory TEXT DEFAULT '',
        note text default '')
        """)

init_db()


@mcp.tool()                               
def add_expense(date,amount,category,subcategory="",note=""):
    '''Add anew expense entry to the database'''
    with sqlite3.connect(DB_path) as c:
        cur=c.execute(
            "INSERT INTO expenses(date,amount,category,subcatagory,note) VALUES (?,?,?,?,?)",
            (date,amount,category,subcategory,note)
        )
        return {"status":"ok","id":cur.lastrowid}


@mcp.tool()
def list_expense(start_date,end_date):
    with sqlite3.connect(DB_path)as c:
        c.row_factory=sqlite3.Row
        cur=c.execute("SELECT * FROM expenses WHERE date BETWEEN ? AND ? ORDER BY id ASC",(start_date,end_date))
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols,r)) for r in cur.fetchall()]


def summarize(start_date,end_date,category=None):
    '''summarize expenses by catagory withan inclusive date range'''
    with sqlite3.connect(DB_path)as c:
        query = (
            "SELECT category,SUM(amount) AS total FROM expenses "
            "WHERE date BETWEEN ? AND ?"
        )
        params=(start_date,end_date)
        if category:
            query += " AND category = ?"
            params += (category)
        query += "GROUP BY category ORDER BY total DESC",params
        
        cur = c.execute(query,params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols,r)) for r in cur.fetchall()]


@mcp.resource("expense://categories",mime_type="application/json")
def expense_categories():
    """List all available expense categories and subcategories."""
    with open(CATEGORIES_PATH, "r",encoding="utf-8") as f:
        return f.read()


#this is how we run the mcp server
if __name__ == "__main__":
    mcp.run(transport="http",host="0.0.0.0",port=8000)
