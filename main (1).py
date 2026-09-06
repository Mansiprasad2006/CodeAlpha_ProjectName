"""
=====================================================================
 STOCK PORTFOLIO TRACKER
=====================================================================
 A desktop application (built with Python + Tkinter) that lets a
 user build a simple stock portfolio, calculate investment values
 based on a predefined price list, and save/load that portfolio
 to/from disk (.txt or .csv).

 Concepts demonstrated:
   - Dictionaries (stock price lookup table)
   - Object-Oriented Programming (Stock + Portfolio classes)
   - Functions
   - Loops & conditional statements
   - Input validation
   - Exception handling
   - File handling (.txt and .csv)
   - A modern Tkinter GUI (dashboard style)

 Author : (Your Name Here)
 Purpose: Internship Project
=====================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv
import os
from datetime import datetime


# =====================================================================
# 1. HARDCODED STOCK PRICE DATABASE
# =====================================================================
# In a real-world application this would come from a live stock API.
# For this project we use a fixed dictionary as required.
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
# 2. COLOUR PALETTE  (kept subtle, warm, professional)
# =====================================================================
COLORS = {
    "dark_brown": "#4A332D",
    "brown": "#795548",
    "brown_hover": "#8D6E63",
    "beige": "#F5EFE6",
    "cream": "#FFF8ED",
    "light_tan": "#E8D8C3",
    "muted_green": "#8FA998",
    "muted_green_hover": "#7C9885",
    "soft_red": "#C98276",
    "soft_red_hover": "#B76B5E",
    "text_dark": "#2F2523",
    "text_light": "#FFF8ED",
}

FONT_FAMILY = "Segoe UI"


# =====================================================================
# 3. DATA CLASSES (Object-Oriented Programming)
# =====================================================================
class Stock:
    """Represents a single stock holding inside the portfolio."""

    def __init__(self, symbol, price, quantity):
        self.symbol = symbol.upper()
        self.price = price
        self.quantity = quantity

    @property
    def investment_value(self):
        """Return price * quantity for this holding."""
        return self.price * self.quantity

    def to_row(self):
        """Return a tuple used for saving / displaying this stock."""
        return (self.symbol, self.price, self.quantity, self.investment_value)


class Portfolio:
    """Holds a collection of Stock objects and provides operations
    for adding, updating, removing, searching and persisting them."""

    def __init__(self, price_lookup):
        self.price_lookup = price_lookup
        self.holdings = {}  # symbol -> Stock

    # ---------------- Validation helpers ----------------
    def is_valid_symbol(self, symbol):
        return symbol.upper() in self.price_lookup

    @staticmethod
    def is_valid_quantity(value):
        """Quantity must be a positive whole number."""
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
            # Stock already exists -> add to the existing quantity
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
        symbol = symbol.upper().strip()
        return self.holdings.get(symbol)

    # ---------------- Statistics ----------------
    def total_stocks(self):
        """Number of different stock symbols held."""
        return len(self.holdings)

    def total_shares(self):
        return sum(s.quantity for s in self.holdings.values())

    def total_investment(self):
        return sum(s.investment_value for s in self.holdings.values())

    # ---------------- File handling ----------------
    def save_to_txt(self, filepath):
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("STOCK PORTFOLIO REPORT\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n")
                f.write(f"{'Symbol':<10}{'Price':<10}{'Qty':<10}{'Value':<12}\n")
                f.write("-" * 50 + "\n")
                for stock in self.holdings.values():
                    f.write(
                        f"{stock.symbol:<10}{stock.price:<10}"
                        f"{stock.quantity:<10}{stock.investment_value:<12}\n"
                    )
                f.write("-" * 50 + "\n")
                f.write(f"Total Stocks     : {self.total_stocks()}\n")
                f.write(f"Total Shares     : {self.total_shares()}\n")
                f.write(f"Total Investment : {self.total_investment()}\n")
        except OSError as e:
            raise IOError(f"Could not save the file: {e}")

    def save_to_csv(self, filepath):
        try:
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Symbol", "Price", "Quantity", "InvestmentValue"])
                for stock in self.holdings.values():
                    writer.writerow(stock.to_row())
        except OSError as e:
            raise IOError(f"Could not save the file: {e}")

    def load_from_csv(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        loaded = {}
        try:
            with open(filepath, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    symbol = row["Symbol"].upper()
                    price = float(row["Price"])
                    quantity = int(row["Quantity"])
                    loaded[symbol] = Stock(symbol, price, quantity)
        except (KeyError, ValueError) as e:
            raise ValueError(f"The CSV file is not in the expected format: {e}")

        self.holdings = loaded


# =====================================================================
# 4. GUI APPLICATION
# =====================================================================
class PortfolioApp:
    def __init__(self, root):
        self.root = root
        self.portfolio = Portfolio(STOCK_PRICES)

        self.root.title("Stock Portfolio Tracker")
        self.root.geometry("980x640")
        self.root.minsize(900, 600)
        self.root.configure(bg=COLORS["beige"])

        self._build_header()
        self._build_dashboard_cards()
        self._build_action_buttons()
        self._build_table()
        self._build_status_bar()

        self.refresh_table()

    # -----------------------------------------------------------------
    # HEADER
    # -----------------------------------------------------------------
    def _build_header(self):
        header = tk.Frame(self.root, bg=COLORS["dark_brown"], height=90)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="\U0001F4C8  Stock Portfolio Tracker",
            font=(FONT_FAMILY, 22, "bold"),
            bg=COLORS["dark_brown"],
            fg=COLORS["text_light"],
        )
        title.pack(anchor="w", padx=30, pady=(14, 0))

        subtitle = tk.Label(
            header,
            text="Track your investments with confidence",
            font=(FONT_FAMILY, 11),
            bg=COLORS["dark_brown"],
            fg=COLORS["light_tan"],
        )
        subtitle.pack(anchor="w", padx=30, pady=(0, 12))

    # -----------------------------------------------------------------
    # DASHBOARD SUMMARY CARDS
    # -----------------------------------------------------------------
    def _build_dashboard_cards(self):
        card_frame = tk.Frame(self.root, bg=COLORS["beige"])
        card_frame.pack(fill="x", padx=25, pady=(18, 8))

        self.card_total_stocks = self._make_card(
            card_frame, "\U0001F4BC  Total Stocks", "0"
        )
        self.card_total_shares = self._make_card(
            card_frame, "\U0001F4CA  Total Shares", "0"
        )
        self.card_total_investment = self._make_card(
            card_frame, "\U0001F4B0  Total Investment", "$0.00"
        )

        for i in range(3):
            card_frame.columnconfigure(i, weight=1)

    def _make_card(self, parent, label_text, value_text):
        card = tk.Frame(parent, bg=COLORS["light_tan"], bd=0)
        card.grid(
            row=0,
            column=len(parent.grid_slaves()),
            sticky="nsew",
            padx=8,
            ipady=10,
        )

        label = tk.Label(
            card,
            text=label_text,
            font=(FONT_FAMILY, 10, "bold"),
            bg=COLORS["light_tan"],
            fg=COLORS["text_dark"],
        )
        label.pack(anchor="w", padx=16, pady=(8, 0))

        value = tk.Label(
            card,
            text=value_text,
            font=(FONT_FAMILY, 20, "bold"),
            bg=COLORS["light_tan"],
            fg=COLORS["dark_brown"],
        )
        value.pack(anchor="w", padx=16, pady=(0, 8))

        return value  # return label so we can update its text later

    # -----------------------------------------------------------------
    # ACTION BUTTONS
    # -----------------------------------------------------------------
    def _build_action_buttons(self):
        btn_frame = tk.Frame(self.root, bg=COLORS["beige"])
        btn_frame.pack(fill="x", padx=25, pady=(4, 10))

        self._make_button(btn_frame, "\u2795 Add Stock", COLORS["brown"],
                           COLORS["brown_hover"], self.add_stock_dialog)
        self._make_button(btn_frame, "\u270F Update", COLORS["brown"],
                           COLORS["brown_hover"], self.update_stock_dialog)
        self._make_button(btn_frame, "\U0001F5D1 Remove", COLORS["soft_red"],
                           COLORS["soft_red_hover"], self.remove_stock_dialog)
        self._make_button(btn_frame, "\U0001F50D Search", COLORS["brown"],
                           COLORS["brown_hover"], self.search_stock_dialog)
        self._make_button(btn_frame, "\U0001F4BE Save", COLORS["muted_green"],
                           COLORS["muted_green_hover"], self.save_portfolio_dialog)
        self._make_button(btn_frame, "\U0001F4C2 Load", COLORS["muted_green"],
                           COLORS["muted_green_hover"], self.load_portfolio_dialog)
        self._make_button(btn_frame, "\U0001F504 Refresh", COLORS["brown"],
                           COLORS["brown_hover"], self.refresh_table)

    def _make_button(self, parent, text, bg, hover_bg, command):
        btn = tk.Button(
            parent,
            text=text,
            font=(FONT_FAMILY, 10, "bold"),
            bg=bg,
            fg=COLORS["text_light"],
            activebackground=hover_bg,
            activeforeground=COLORS["text_light"],
            relief="flat",
            bd=0,
            padx=14,
            pady=8,
            cursor="hand2",
            command=command,
        )
        btn.pack(side="left", padx=6)

        # Hover effect
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn

    # -----------------------------------------------------------------
    # TABLE (Treeview)
    # -----------------------------------------------------------------
    def _build_table(self):
        table_frame = tk.Frame(self.root, bg=COLORS["cream"])
        table_frame.pack(fill="both", expand=True, padx=25, pady=(0, 10))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background=COLORS["cream"],
            fieldbackground=COLORS["cream"],
            foreground=COLORS["text_dark"],
            rowheight=28,
            font=(FONT_FAMILY, 10),
        )
        style.configure(
            "Treeview.Heading",
            background=COLORS["brown"],
            foreground=COLORS["text_light"],
            font=(FONT_FAMILY, 10, "bold"),
            relief="flat",
        )
        style.map("Treeview", background=[("selected", COLORS["light_tan"])],
                  foreground=[("selected", COLORS["text_dark"])])

        columns = ("symbol", "price", "quantity", "value")
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", style="Treeview"
        )
        self.tree.heading("symbol", text="Stock Symbol")
        self.tree.heading("price", text="Price ($)")
        self.tree.heading("quantity", text="Quantity")
        self.tree.heading("value", text="Investment Value ($)")

        self.tree.column("symbol", anchor="center", width=150)
        self.tree.column("price", anchor="center", width=150)
        self.tree.column("quantity", anchor="center", width=150)
        self.tree.column("value", anchor="center", width=200)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # -----------------------------------------------------------------
    # STATUS BAR
    # -----------------------------------------------------------------
    def _build_status_bar(self):
        self.status_var = tk.StringVar(value="Ready.")
        status = tk.Label(
            self.root,
            textvariable=self.status_var,
            bg=COLORS["dark_brown"],
            fg=COLORS["light_tan"],
            font=(FONT_FAMILY, 9),
            anchor="w",
            padx=12,
        )
        status.pack(fill="x", side="bottom")

    def set_status(self, message):
        self.status_var.set(message)

    # -----------------------------------------------------------------
    # REFRESH / DISPLAY LOGIC
    # -----------------------------------------------------------------
    def refresh_table(self):
        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Re-insert current holdings, sorted alphabetically
        for stock in sorted(self.portfolio.holdings.values(), key=lambda s: s.symbol):
            self.tree.insert(
                "",
                "end",
                values=(stock.symbol, f"{stock.price:.2f}",
                        stock.quantity, f"{stock.investment_value:.2f}"),
            )

        # Update dashboard cards
        self.card_total_stocks.config(text=str(self.portfolio.total_stocks()))
        self.card_total_shares.config(text=str(self.portfolio.total_shares()))
        self.card_total_investment.config(
            text=f"${self.portfolio.total_investment():,.2f}"
        )
        self.set_status("Portfolio refreshed.")

    def get_selected_symbol(self):
        selection = self.tree.selection()
        if not selection:
            return None
        values = self.tree.item(selection[0], "values")
        return values[0] if values else None

    # -----------------------------------------------------------------
    # DIALOG ACTIONS
    # -----------------------------------------------------------------
    def add_stock_dialog(self):
        symbol = simpledialog.askstring(
            "Add Stock",
            "Enter stock symbol:\n\nAvailable: " + ", ".join(STOCK_PRICES.keys()),
            parent=self.root,
        )
        if symbol is None:
            return  # user cancelled

        quantity = simpledialog.askstring(
            "Add Stock", f"Enter quantity for {symbol.upper()}:", parent=self.root
        )
        if quantity is None:
            return

        try:
            stock = self.portfolio.add_stock(symbol, quantity)
            self.refresh_table()
            messagebox.showinfo(
                "Success",
                f"Added {stock.quantity} share(s) of {stock.symbol} "
                f"(Value: ${stock.investment_value:,.2f})",
            )
            self.set_status(f"Added {stock.symbol}.")
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            self.set_status("Add stock failed: invalid input.")

    def update_stock_dialog(self):
        symbol = self.get_selected_symbol()
        if symbol is None:
            symbol = simpledialog.askstring(
                "Update Stock", "Enter stock symbol to update:", parent=self.root
            )
            if symbol is None:
                return

        new_qty = simpledialog.askstring(
            "Update Stock", f"Enter new quantity for {symbol.upper()}:", parent=self.root
        )
        if new_qty is None:
            return

        try:
            stock = self.portfolio.update_quantity(symbol, new_qty)
            self.refresh_table()
            messagebox.showinfo(
                "Success", f"{stock.symbol} quantity updated to {stock.quantity}."
            )
            self.set_status(f"Updated {stock.symbol}.")
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            self.set_status("Update failed: invalid input.")

    def remove_stock_dialog(self):
        symbol = self.get_selected_symbol()
        if symbol is None:
            symbol = simpledialog.askstring(
                "Remove Stock", "Enter stock symbol to remove:", parent=self.root
            )
            if symbol is None:
                return

        confirm = messagebox.askyesno(
            "Confirm Removal", f"Are you sure you want to remove {symbol.upper()}?"
        )
        if not confirm:
            return

        try:
            self.portfolio.remove_stock(symbol)
            self.refresh_table()
            messagebox.showinfo("Removed", f"{symbol.upper()} was removed from your portfolio.")
            self.set_status(f"Removed {symbol.upper()}.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.set_status("Remove failed.")

    def search_stock_dialog(self):
        symbol = simpledialog.askstring(
            "Search Stock", "Enter stock symbol to search:", parent=self.root
        )
        if symbol is None:
            return

        stock = self.portfolio.search_stock(symbol)
        if stock is None:
            messagebox.showwarning("Not Found", f"'{symbol.upper()}' is not in your portfolio.")
            self.set_status("Search: not found.")
            return

        messagebox.showinfo(
            "Stock Found",
            f"Symbol: {stock.symbol}\n"
            f"Price: ${stock.price:.2f}\n"
            f"Quantity: {stock.quantity}\n"
            f"Investment Value: ${stock.investment_value:,.2f}",
        )
        self.set_status(f"Found {stock.symbol}.")

    def save_portfolio_dialog(self):
        if not self.portfolio.holdings:
            messagebox.showwarning("Empty Portfolio", "There is nothing to save yet.")
            return

        choice = simpledialog.askstring(
            "Save Portfolio",
            "Save as which format?\nType 'txt' or 'csv':",
            parent=self.root,
        )
        if choice is None:
            return

        choice = choice.strip().lower()
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "portfolio_data")

        try:
            if choice == "txt":
                filepath += ".txt"
                self.portfolio.save_to_txt(filepath)
            elif choice == "csv":
                filepath += ".csv"
                self.portfolio.save_to_csv(filepath)
            else:
                messagebox.showerror("Invalid Choice", "Please type 'txt' or 'csv'.")
                return

            messagebox.showinfo("Saved", f"Portfolio saved successfully to:\n{filepath}")
            self.set_status(f"Saved portfolio to {os.path.basename(filepath)}.")
        except IOError as e:
            messagebox.showerror("Save Failed", str(e))
            self.set_status("Save failed.")

    def load_portfolio_dialog(self):
        default_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "portfolio_data.csv"
        )
        filepath = simpledialog.askstring(
            "Load Portfolio",
            "Enter path to CSV file to load:",
            initialvalue=default_path,
            parent=self.root,
        )
        if filepath is None:
            return

        try:
            self.portfolio.load_from_csv(filepath)
            self.refresh_table()
            messagebox.showinfo("Loaded", "Portfolio loaded successfully.")
            self.set_status(f"Loaded portfolio from {os.path.basename(filepath)}.")
        except (FileNotFoundError, ValueError) as e:
            messagebox.showerror("Load Failed", str(e))
            self.set_status("Load failed.")


# =====================================================================
# 5. APPLICATION ENTRY POINT
# =====================================================================
def main():
    root = tk.Tk()
    app = PortfolioApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
