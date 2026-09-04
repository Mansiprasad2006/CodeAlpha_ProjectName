# 📈 Stock Portfolio Tracker

A desktop application built with **Python + Tkinter** that lets you manage a
simple stock portfolio, automatically calculate investment values from a
predefined price list, and save/load your data to and from disk.

Built as an internship project to demonstrate core Python skills: dictionaries,
functions, OOP, loops, conditionals, input validation, exception handling, and
file/CSV handling — wrapped in a clean, modern GUI.

---

## ✨ Features

- **Add / Update / Remove** stocks in your portfolio
- **Search** for a specific stock
- **Live dashboard cards**: Total Stocks, Total Shares, Total Investment
- **Portfolio table** showing symbol, price, quantity, and investment value
- **Save** your portfolio as `.txt` or `.csv`
- **Load** a previously saved `.csv` portfolio
- Input validation with friendly pop-up error messages
- Warm, professional colour theme (browns, beige, cream)

---

## 🗂️ Project Structure

```
StockPortfolioTracker/
│
├── main.py               # Complete application (GUI + logic)
├── portfolio_data.csv    # Sample portfolio data you can load
├── README.md             # This file
└── requirements.txt      # Dependency notes (standard library only)
```

---

## 🧠 Supported Stocks

The app uses a hardcoded price dictionary. You can add more symbols by
editing the `STOCK_PRICES` dictionary near the top of `main.py`.

| Symbol | Price ($) |
|--------|-----------|
| AAPL   | 180       |
| TSLA   | 250       |
| GOOGL  | 140       |
| MSFT   | 420       |
| AMZN   | 190       |
| NFLX   | 610       |
| META   | 480       |
| NVDA   | 900       |

---

## ▶️ How to Run in VS Code

1. **Install Python 3.8 or newer**
   Download from [python.org](https://www.python.org/downloads/) if you don't
   already have it. During installation on Windows, make sure "Add Python to
   PATH" is checked.

2. **Open the project folder in VS Code**
   `File → Open Folder…` and select the `StockPortfolioTracker` folder.

3. **Check that tkinter is available** (it ships with Python by default).
   If you're on Linux and get a `tkinter` import error, install it with:
   ```bash
   sudo apt-get install python3-tk
   ```

4. **Run the app**
   Open `main.py` in VS Code, then either:
   - Click the ▶️ "Run" button in the top-right corner, **or**
   - Open a terminal (`` Ctrl+` ``) and run:
     ```bash
     python main.py
     ```

5. **Use the app!**
   - Click **➕ Add Stock** to add a symbol and quantity.
   - Select a row in the table, then click **✏️ Update** or **🗑️ Remove**.
   - Click **🔍 Search** to look up a specific holding.
   - Click **💾 Save** and type `csv` or `txt` to export your portfolio.
   - Click **📂 Load** to load `portfolio_data.csv` (the sample file included,
     or one you've saved yourself).

No extra installation steps or `pip install` commands are required — the
whole project runs on Python's standard library.

---

## 🛠️ Python Concepts Demonstrated

- **Dictionaries** – `STOCK_PRICES` lookup table
- **Classes / OOP** – `Stock` and `Portfolio` classes
- **Functions** – small, single-purpose methods for each action
- **Loops** – iterating over holdings to build tables/reports
- **Conditionals & validation** – symbol and quantity checks
- **Exception handling** – `try/except` around file I/O and user input
- **File handling** – writing/reading `.txt` and `.csv` files
- **GUI programming** – Tkinter widgets, `ttk.Treeview`, hover effects

---

## 📌 Notes

- Portfolio data is kept in memory while the app is running. Use **Save** to
  persist it, and **Load** to bring it back in a future session.
- The sample `portfolio_data.csv` file is provided so you can try **Load**
  immediately without first adding stocks manually.
