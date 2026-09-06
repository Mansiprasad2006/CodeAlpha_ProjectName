# 📈 Stock Portfolio Tracker

Two versions of the same app, sharing the same core logic (dictionaries,
OOP, validation, exception handling, file/CSV handling):

- **`main.py`** — Desktop app (Tkinter). Runs locally on one machine.
- **`streamlit_app.py`** — Web app (Streamlit). Runs in a browser and can be
  deployed for free so you (or anyone with the link) can use it from
  anywhere — phone, laptop, tablet, no install required.

Built as an internship project to demonstrate core Python skills.

---

## 🌐 Web Version (Streamlit) — Run Globally

### Option A: Run it locally first
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Launch the app:
   ```bash
   streamlit run streamlit_app.py
   ```
3. Your browser opens automatically at `http://localhost:8501`. Anyone on
   your same network can also reach it via the "Network URL" Streamlit prints
   in the terminal.

### Option B: Deploy it for free so it's reachable from anywhere
The easiest option is **Streamlit Community Cloud** (free, made by the
Streamlit team):

1. Create a free GitHub account if you don't have one, and push this project
   folder to a new GitHub repository (must include `streamlit_app.py` and
   `requirements.txt`).
2. Go to **https://share.streamlit.io** and sign in with GitHub.
3. Click **"New app"**, select your repository and branch, and set the
   main file path to `streamlit_app.py`.
4. Click **Deploy**. In about a minute you'll get a public URL like
   `https://your-app-name.streamlit.app` that works on any device, globally,
   with no installation needed on the visitor's end.

Other free/low-cost options that work the same way: **Render**, **Railway**,
or **Hugging Face Spaces** (Streamlit is a supported Space type there too).

### How the web version differs from the desktop version
- Instead of writing files to disk, **Save** gives you a **Download** button
  (CSV or TXT) — the browser saves it to your computer's Downloads folder.
- Instead of a "load from path" dialog, **Load** uses a file **uploader** —
  drag and drop a previously downloaded `portfolio_data.csv`.
- Your portfolio lives in the browser session's memory (`st.session_state`)
  while the tab is open. Download your data if you want to keep it — a
  refresh or new browser session starts with an empty portfolio, same as
  restarting the desktop app without loading a file.

---

## 🖥️ Desktop Version (Tkinter)

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
├── main.py               # Desktop application (Tkinter GUI + logic)
├── streamlit_app.py       # Web application (Streamlit GUI + same logic)
├── portfolio_data.csv    # Sample portfolio data you can load
├── README.md             # This file
└── requirements.txt      # Dependency notes (streamlit + pandas for web version)
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
