import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import date, timedelta
import requests
import os
from tkinter import messagebox
import ml

# Constants
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
BG_COLOR = "#f0f0f0"
HEADER_COLOR = "#2c3e50"
TEXT_COLOR = "#34495e"
ACCENT_COLOR = "#3498db"

# API Endpoints and Keys
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = os.getenv("STOCK_API_KEY", " ")
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = os.getenv("NEWS_API_KEY", " ")

# Train the model and make predictions
model, df = ml.train_model(stock_symbol=STOCK, api_key=STOCK_API_KEY)

if model:
    next_day_price = ml.predict_next_day(model, df)
    print(f"Predicted Stock Price for Tomorrow: ${next_day_price:.2f}")


class StockTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Stock Insights")
        self.root.geometry("900x700")
        self.root.configure(bg=BG_COLOR)

        self.setup_ui()
        self.fetch_data()

    def setup_ui(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg=HEADER_COLOR, padx=10, pady=10)
        header_frame.pack(fill="x")

        tk.Label(
            header_frame,
            text="Real-Time Stock Insights",
            font=("Helvetica", 16, "bold"),
            fg="white",
            bg=HEADER_COLOR
        ).pack(side="left")

        # Stock Info Frame
        stock_frame = tk.LabelFrame(
            self.root,
            text="Stock Information",
            font=("Helvetica", 10, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            padx=10,
            pady=10
        )
        stock_frame.pack(fill="x", padx=10, pady=5)

        self.stock_info_text = tk.Text(
            stock_frame,
            height=5,
            width=80,
            wrap=tk.WORD,
            font=("Helvetica", 9),
            bg="white",
            fg=TEXT_COLOR,
            padx=5,
            pady=5
        )
        self.stock_info_text.pack(fill="x")

        # News Frame
        news_frame = tk.LabelFrame(
            self.root,
            text="Latest News",
            font=("Helvetica", 10, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            padx=10,
            pady=10
        )
        news_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.news_canvas = tk.Canvas(news_frame, bg="white")
        self.news_scrollbar = ttk.Scrollbar(news_frame, orient="vertical", command=self.news_canvas.yview)
        self.news_scrollable_frame = tk.Frame(self.news_canvas, bg="white")

        self.news_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.news_canvas.configure(
                scrollregion=self.news_canvas.bbox("all")
            )
        )

        self.news_canvas.create_window((0, 0), window=self.news_scrollable_frame, anchor="nw")
        self.news_canvas.configure(yscrollcommand=self.news_scrollbar.set)

        self.news_canvas.pack(side="left", fill="both", expand=True)
        self.news_scrollbar.pack(side="right", fill="y")

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        tk.Label(
            self.root,
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(fill="x", side=tk.BOTTOM)

    def fetch_data(self):
        self.status_var.set("Fetching data...")
        self.root.update()

        try:
            # Fetch stock data
            stock_params = {
                "function": "TIME_SERIES_DAILY",
                "symbol": STOCK,
                "apikey": STOCK_API_KEY
            }

            response_stock = requests.get(STOCK_ENDPOINT, params=stock_params)
            response_stock.raise_for_status()
            stock_data = response_stock.json()

            # Get today's date
            today_date = date.today()

            # Function to find the most recent valid trading day
            def get_valid_trading_day(data, target_date):
                for i in range(10):
                    current_date = target_date - timedelta(days=i)
                    current_date_str = current_date.strftime("%Y-%m-%d")
                    if current_date_str in data.get("Time Series (Daily)", {}):
                        return current_date_str
                return None

            # Get valid trading days
            yesterday_date_str = get_valid_trading_day(stock_data, today_date - timedelta(days=1))
            day_before_date_str = get_valid_trading_day(stock_data, today_date - timedelta(days=2))

            if not yesterday_date_str or not day_before_date_str:
                messagebox.showerror("Error", "Could not find valid trading days.")
                return

            # Get metadata
            meta_data = stock_data.get("Meta Data", {})
            last_refreshed = meta_data.get("3. Last Refreshed", "N/A")
            time_zone = meta_data.get("5. Time Zone", "N/A")

            # Get stock prices
            yesterday_data = stock_data["Time Series (Daily)"][yesterday_date_str]
            day_before_data = stock_data["Time Series (Daily)"][day_before_date_str]

            yesterday_close = float(yesterday_data["4. close"])
            day_before_open = float(day_before_data["1. open"])

            # Calculate percentage change
            difference = abs(yesterday_close - day_before_open)
            percentage = round((difference / yesterday_close) * 100, 2)
            direction = "up" if yesterday_close > day_before_open else "down"

            # Display stock info
            stock_info = (
                f"Stock: {STOCK} ({COMPANY_NAME})\n"
                f"Last Refreshed: {last_refreshed} ({time_zone})\n"
                f"Current Price: ${yesterday_close:.2f} ({direction} {percentage}%)\n"
                f"Previous Open: ${day_before_open:.2f}\n"
                f"Date Range: {day_before_date_str} to {yesterday_date_str}"
            )

            self.stock_info_text.config(state=tk.NORMAL)
            self.stock_info_text.delete(1.0, tk.END)
            self.stock_info_text.insert(tk.END, stock_info)
            self.stock_info_text.config(state=tk.DISABLED)

            # Always fetch news (not just when percentage > 1)
            news_params = {
                "apiKey": NEWS_API_KEY,
                "qInTitle": COMPANY_NAME,
                "sortBy": "publishedAt",
                "pageSize": 100  # Increased from default to get more articles
            }

            response_news = requests.get(NEWS_ENDPOINT, params=news_params)
            response_news.raise_for_status()
            news_data = response_news.json()
            articles = news_data.get("articles", [])

            # Clear previous news
            for widget in self.news_scrollable_frame.winfo_children():
                widget.destroy()

            if not articles:
                no_news_label = tk.Label(
                    self.news_scrollable_frame,
                    text="No news articles found",
                    font=("Helvetica", 10),
                    bg="white",
                    fg=TEXT_COLOR
                )
                no_news_label.pack(pady=20)
            else:
                # Display each news article
                for i, article in enumerate(articles):
                    self.create_news_card(
                        article.get("title", "No title"),
                        article.get("description", "No description available"),
                        article.get("url", "#"),
                        article.get("publishedAt", "N/A"),
                        article.get("content", "No content available"),
                        i
                    )

            self.status_var.set(f"Data fetched successfully - {len(articles)} news articles found")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch data: {str(e)}")
            self.status_var.set("Error fetching data")

    def create_news_card(self, title, description, url, published_at, content, index):
        card_frame = tk.Frame(
            self.news_scrollable_frame,
            bg="white",
            bd=1,
            relief=tk.RAISED,
            padx=10,
            pady=10
        )
        card_frame.pack(fill="x", padx=5, pady=5)

        # Title
        title_label = tk.Label(
            card_frame,
            text=title,
            font=("Helvetica", 10, "bold"),
            bg="white",
            fg=ACCENT_COLOR,
            anchor="w",
            wraplength=800
        )
        title_label.pack(fill="x")

        # Published At
        published_label = tk.Label(
            card_frame,
            text=f"Published: {published_at}",
            font=("Helvetica", 8),
            bg="white",
            fg="gray",
            anchor="w"
        )
        published_label.pack(fill="x")

        # Description
        desc_label = tk.Label(
            card_frame,
            text=description,
            font=("Helvetica", 9),
            bg="white",
            fg=TEXT_COLOR,
            anchor="w",
            wraplength=800
        )
        desc_label.pack(fill="x", pady=(5, 0))

        # URL Button
        def open_url():
            import webbrowser
            webbrowser.open_new(url)

        url_button = tk.Button(
            card_frame,
            text="Read Full Article",
            command=open_url,
            bg=ACCENT_COLOR,
            fg="white",
            relief=tk.FLAT,
            font=("Helvetica", 8, "bold")
        )
        url_button.pack(side="left", pady=(10, 0))

        # Content (truncated)
        content_text = tk.Text(
            card_frame,
            height=4,
            width=80,
            wrap=tk.WORD,
            font=("Helvetica", 8),
            bg="#f9f9f9",
            fg=TEXT_COLOR,
            padx=5,
            pady=5
        )
        content_text.insert(tk.END, content[:500] + ("..." if len(content) > 500 else ""))
        content_text.config(state=tk.DISABLED)
        content_text.pack(fill="x", pady=(5, 0))


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = StockTrackerApp(root)
    root.mainloop()
