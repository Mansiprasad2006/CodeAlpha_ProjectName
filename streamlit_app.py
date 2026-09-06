"""
=====================================================================
 STOCK PORTFOLIO TRACKER — STREAMLIT WEB VERSION
=====================================================================
 A web-based version of the desktop Tkinter app, built with Streamlit
 so it can be deployed and accessed from anywhere (Streamlit Community
 Cloud, Render, etc.) instead of running only on one machine.

 Concepts demonstrated:
   - Dictionaries (stock price lookup table)
   - Object-Oriented Programming (Stock + Portfolio classes)
   - Functions
   - Loops & conditional statements
   - Input validation
   - Exception handling
   - File handling (.txt / .csv export & CSV import)
   - A modern, styled web UI (dashboard style) with Streamlit

 Author : (Your Name Here)
 Purpose: Internship Project
=====================================================================
"""

import io
import csv
from datetime import datetime

import pandas as pd
import streamlit as st


# =====================================================================
# 1. HARDCODED STOCK PRICE DATABASE
# =====================================================================
STOCK_PRICES = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOGL": 140,
    "MSFT": 420,
    "AMZN": 190,
    "NFLX": 610,
    "META": 480,
    "NVDA": 900,
}


# =====================================================================
# 2. DATA CLASSES (Object-Oriented Programming)
# =====================================================================
class Stock:
    """Represents a single stock holding inside the portfolio."""

    def __init__(self, symbol, price, quantity):
        self.symbol = symbol.upper()
        self.price = price
        self.quantity = quantity

    @property
    def investment_value(self):
        return self.price * self.quantity

    def to_row(self):
        return (self.symbol, self.price, self.quantity, self.investment_value)


class Portfolio:
    """Holds Stock objects and provides add/update/remove/search/save/load."""

    def __init__(self, price_lookup):
        self.price_lookup = price_lookup
        self.holdings = {}  # symbol -> Stock

    # ---------------- Validation helpers ----------------
    def is_valid_symbol(self, symbol):
        return symbol.upper() in self.price_lookup

    @staticmethod
    def is_valid_quantity(value):
        try:
            qty = int(value)
            return qty > 0
        except (ValueError, TypeError):
            return False

    # ---------------- Core operations ----------------
    def add_stock(self, symbol, quantity):
        symbol = symbol.upper().strip()

        if not self.is_valid_symbol(symbol):
            raise ValueError(f"'{symbol}' is not a recognised stock symbol.")
        if not self.is_valid_quantity(quantity):
            raise ValueError("Quantity must be a positive whole number.")

        quantity = int(quantity)
        price = self.price_lookup[symbol]

        if symbol in self.holdings:
            self.holdings[symbol].quantity += quantity
        else:
            self.holdings[symbol] = Stock(symbol, price, quantity)

        return self.holdings[symbol]

    def update_quantity(self, symbol, new_quantity):
        symbol = symbol.upper().strip()
        if symbol not in self.holdings:
            raise ValueError(f"'{symbol}' is not in your portfolio.")
        if not self.is_valid_quantity(new_quantity):
            raise ValueError("Quantity must be a positive whole number.")

        self.holdings[symbol].quantity = int(new_quantity)
        return self.holdings[symbol]

    def remove_stock(self, symbol):
        symbol = symbol.upper().strip()
        if symbol not in self.holdings:
            raise ValueError(f"'{symbol}' is not in your portfolio.")
        del self.holdings[symbol]

    def search_stock(self, symbol):
        return self.holdings.get(symbol.upper().strip())

    # ---------------- Statistics ----------------
    def total_stocks(self):
        return len(self.holdings)

    def total_shares(self):
        return sum(s.quantity for s in self.holdings.values())

    def total_investment(self):
        return sum(s.investment_value for s in self.holdings.values())

    # ---------------- File handling ----------------
    def to_dataframe(self):
        rows = [s.to_row() for s in sorted(self.holdings.values(), key=lambda s: s.symbol)]
        return pd.DataFrame(rows, columns=["Symbol", "Price", "Quantity", "InvestmentValue"])

    def to_txt_bytes(self):
        buf = io.StringIO()
        buf.write("STOCK PORTFOLIO REPORT\n")
        buf.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        buf.write("=" * 50 + "\n")
        buf.write(f"{'Symbol':<10}{'Price':<10}{'Qty':<10}{'Value':<12}\n")
        buf.write("-" * 50 + "\n")
        for stock in sorted(self.holdings.values(), key=lambda s: s.symbol):
            buf.write(
                f"{stock.symbol:<10}{stock.price:<10}"
                f"{stock.quantity:<10}{stock.investment_value:<12}\n"
            )
        buf.write("-" * 50 + "\n")
        buf.write(f"Total Stocks     : {self.total_stocks()}\n")
        buf.write(f"Total Shares     : {self.total_shares()}\n")
        buf.write(f"Total Investment : {self.total_investment()}\n")
        return buf.getvalue().encode("utf-8")

    def to_csv_bytes(self):
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["Symbol", "Price", "Quantity", "InvestmentValue"])
        for stock in sorted(self.holdings.values(), key=lambda s: s.symbol):
            writer.writerow(stock.to_row())
        return buf.getvalue().encode("utf-8")

    def load_from_csv_file(self, uploaded_file):
        """Load holdings from an uploaded CSV file-like object."""
        try:
            text = uploaded_file.getvalue().decode("utf-8")
            reader = csv.DictReader(io.StringIO(text))
            loaded = {}
            for row in reader:
                symbol = row["Symbol"].upper()
                price = float(row["Price"])
                quantity = int(row["Quantity"])
                loaded[symbol] = Stock(symbol, price, quantity)
        except (KeyError, ValueError) as e:
            raise ValueError(f"The CSV file is not in the expected format: {e}")

        self.holdings = loaded


# =====================================================================
# 3. STREAMLIT PAGE CONFIG + STYLING (same warm brown/beige theme)
# =====================================================================
st.set_page_config(
    page_title="Stock Portfolio Tracker",
    page_icon="📈",
    layout="wide",
)

CUSTOM_CSS = """
<style>
:root {
    --dark-brown: #4A332D;
    --brown: #795548;
    --beige: #F5EFE6;
    --cream: #FFF8ED;
    --light-tan: #E8D8C3;
    --muted-green: #8FA998;
    --soft-red: #C98276;
    --text-dark: #2F2523;
    --text-light: #FFF8ED;
}

/* Overall page background */
.stApp {
    background-color: var(--beige);
}

/* Header banner */
.ptf-header {
    background-color: var(--dark-brown);
    padding: 28px 32px 22px 32px;
    border-radius: 10px;
    margin-bottom: 22px;
}
.ptf-header h1 {
    color: var(--text-light);
    margin: 0;
    font-size: 2rem;
}
.ptf-header p {
    color: var(--light-tan);
    margin: 6px 0 0 0;
    font-size: 1rem;
}

/* Dashboard summary cards */
.ptf-card {
    background-color: var(--light-tan);
    border-radius: 10px;
    padding: 16px 20px;
    text-align: left;
}
.ptf-card .label {
    color: var(--text-dark);
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 4px;
}
.ptf-card .value {
    color: var(--dark-brown);
    font-size: 1.6rem;
    font-weight: 700;
}

/* Buttons */
.stButton>button {
    background-color: var(--brown);
    color: var(--text-light);
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 0.5rem 1rem;
}
.stButton>button:hover {
    background-color: #8D6E63;
    color: var(--text-light);
}
.stDownloadButton>button {
    background-color: var(--muted-green);
    color: var(--text-light);
    border: none;
    border-radius: 8px;
    font-weight: 600;
}
.stDownloadButton>button:hover {
    background-color: #7C9885;
    color: var(--text-light);
}

/* Section headers */
h2, h3 {
    color: var(--dark-brown) !important;
}

/* Dataframe container */
[data-testid="stDataFrame"] {
    background-color: var(--cream);
    border-radius: 8px;
    padding: 4px;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# =====================================================================
# 4. SESSION STATE INITIALISATION
# =====================================================================
if "portfolio" not in st.session_state:
    st.session_state.portfolio = Portfolio(STOCK_PRICES)

portfolio: Portfolio = st.session_state.portfolio


# =====================================================================
# 5. HEADER
# =====================================================================
st.markdown(
    """
    <div class="ptf-header">
        <h1>📈 Stock Portfolio Tracker</h1>
        <p>Track your investments with confidence</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =====================================================================
# 6. DASHBOARD SUMMARY CARDS
# =====================================================================
card1, card2, card3 = st.columns(3)

with card1:
    st.markdown(
        f"""
        <div class="ptf-card">
            <div class="label">💼 TOTAL STOCKS</div>
            <div class="value">{portfolio.total_stocks()}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with card2:
    st.markdown(
        f"""
        <div class="ptf-card">
            <div class="label">📊 TOTAL SHARES</div>
            <div class="value">{portfolio.total_shares()}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with card3:
    st.markdown(
        f"""
        <div class="ptf-card">
            <div class="label">💰 TOTAL INVESTMENT</div>
            <div class="value">${portfolio.total_investment():,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")  # spacer


# =====================================================================
# 7. SIDEBAR — ALL PORTFOLIO ACTIONS
# =====================================================================
st.sidebar.header("Portfolio Actions")

available_symbols = ", ".join(STOCK_PRICES.keys())
st.sidebar.caption(f"Available symbols: {available_symbols}")

# ---- Add Stock ----
with st.sidebar.expander("➕ Add Stock", expanded=True):
    with st.form("add_stock_form", clear_on_submit=True):
        add_symbol = st.selectbox("Stock symbol", options=list(STOCK_PRICES.keys()), key="add_symbol")
        add_qty = st.text_input("Quantity", key="add_qty")
        add_submitted = st.form_submit_button("Add to Portfolio")

    if add_submitted:
        try:
            stock = portfolio.add_stock(add_symbol, add_qty)
            st.sidebar.success(
                f"Added {stock.quantity} share(s) of {stock.symbol} "
                f"(Value: ${stock.investment_value:,.2f})"
            )
        except ValueError as e:
            st.sidebar.error(str(e))

# ---- Update Stock ----
with st.sidebar.expander("✏️ Update Quantity"):
    if portfolio.holdings:
        with st.form("update_stock_form", clear_on_submit=True):
            upd_symbol = st.selectbox(
                "Stock to update", options=list(portfolio.holdings.keys()), key="upd_symbol"
            )
            upd_qty = st.text_input("New quantity", key="upd_qty")
            upd_submitted = st.form_submit_button("Update")

        if upd_submitted:
            try:
                stock = portfolio.update_quantity(upd_symbol, upd_qty)
                st.sidebar.success(f"{stock.symbol} quantity updated to {stock.quantity}.")
            except ValueError as e:
                st.sidebar.error(str(e))
    else:
        st.sidebar.info("Your portfolio is empty — add a stock first.")

# ---- Remove Stock ----
with st.sidebar.expander("🗑️ Remove Stock"):
    if portfolio.holdings:
        with st.form("remove_stock_form", clear_on_submit=True):
            rem_symbol = st.selectbox(
                "Stock to remove", options=list(portfolio.holdings.keys()), key="rem_symbol"
            )
            rem_submitted = st.form_submit_button("Remove")

        if rem_submitted:
            try:
                portfolio.remove_stock(rem_symbol)
                st.sidebar.success(f"{rem_symbol} removed from your portfolio.")
            except ValueError as e:
                st.sidebar.error(str(e))
    else:
        st.sidebar.info("Your portfolio is empty — add a stock first.")

# ---- Search Stock ----
with st.sidebar.expander("🔍 Search Stock"):
    search_symbol = st.text_input("Symbol to search", key="search_symbol")
    if st.button("Search", key="search_button"):
        if search_symbol:
            found = portfolio.search_stock(search_symbol)
            if found:
                st.sidebar.success(
                    f"**{found.symbol}**\n\n"
                    f"Price: ${found.price:.2f}\n\n"
                    f"Quantity: {found.quantity}\n\n"
                    f"Investment Value: ${found.investment_value:,.2f}"
                )
            else:
                st.sidebar.warning(f"'{search_symbol.upper()}' is not in your portfolio.")
        else:
            st.sidebar.warning("Please enter a symbol to search.")

# ---- Save Portfolio (download) ----
with st.sidebar.expander("💾 Save Portfolio"):
    if portfolio.holdings:
        st.download_button(
            "Download as CSV",
            data=portfolio.to_csv_bytes(),
            file_name="portfolio_data.csv",
            mime="text/csv",
        )
        st.download_button(
            "Download as TXT",
            data=portfolio.to_txt_bytes(),
            file_name="portfolio_data.txt",
            mime="text/plain",
        )
    else:
        st.info("Add stocks to your portfolio before saving.")

# ---- Load Portfolio (upload) ----
with st.sidebar.expander("📂 Load Portfolio"):
    uploaded = st.file_uploader("Upload a portfolio CSV", type=["csv"], key="uploader")
    if uploaded is not None:
        if st.button("Load Uploaded File", key="load_button"):
            try:
                portfolio.load_from_csv_file(uploaded)
                st.sidebar.success("Portfolio loaded successfully.")
                st.rerun()
            except ValueError as e:
                st.sidebar.error(str(e))

# ---- Refresh ----
if st.sidebar.button("🔄 Refresh Dashboard"):
    st.rerun()


# =====================================================================
# 8. MAIN PORTFOLIO TABLE
# =====================================================================
st.subheader("Portfolio Overview")

if portfolio.holdings:
    df = portfolio.to_dataframe()
    df_display = df.rename(
        columns={
            "Symbol": "Stock Symbol",
            "Price": "Price ($)",
            "Quantity": "Quantity",
            "InvestmentValue": "Investment Value ($)",
        }
    )
    st.dataframe(df_display, use_container_width=True, hide_index=True)
else:
    st.info(
        "Your portfolio is empty. Use **➕ Add Stock** in the sidebar to get started, "
        "or **📂 Load Portfolio** to import a saved CSV."
    )

st.caption(
    "Built with Streamlit • Prices are a fixed demo dataset, not live market data."
)
