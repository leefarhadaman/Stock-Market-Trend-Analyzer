import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to fetch and plot stock data
def fetch_data():
    stock_symbol = stock_entry.get()
    if not stock_symbol:
        messagebox.showerror("Input Error", "Please enter a stock symbol.")
        return

    try:
        data = yf.download(stock_symbol, start="2020-01-01", end="2024-12-31")
        if data.empty:
            messagebox.showerror("Data Error", "No data found for the stock symbol.")
            return

        # Plot stock price trend
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(data['Close'], label='Closing Price', color='blue')
        ax.set_title(f"{stock_symbol.upper()} Stock Price Trend")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (USD)")
        ax.legend()

        # Embed the plot into the GUI
        for widget in plot_frame.winfo_children():
            widget.destroy()  # Clear previous plot
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.get_tk_widget().grid(row=0, column=0)
        canvas.draw()

        # Display statistics
        min_price = float(data['Close'].min())
        max_price = float(data['Close'].max())
        avg_price = float(data['Close'].mean())

        stats.set(f"Min Price: ${min_price:.2f}\nMax Price: ${max_price:.2f}\nAverage Price: ${avg_price:.2f}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main application window
root = tk.Tk()
root.title("Stock Market Trend Analyzer")
root.geometry("800x600")

# Stock symbol input
input_frame = tk.Frame(root, padx=10, pady=10)
input_frame.pack()

tk.Label(input_frame, text="Enter Stock Symbol:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
stock_entry = ttk.Entry(input_frame, font=("Arial", 12))
stock_entry.grid(row=0, column=1, padx=5, pady=5)

fetch_button = ttk.Button(input_frame, text="Fetch Data", command=fetch_data)
fetch_button.grid(row=0, column=2, padx=5, pady=5)

# Plotting area
plot_frame = tk.Frame(root, padx=10, pady=10)
plot_frame.pack()

# Statistics display
stats = tk.StringVar()
stats.set("Min Price: \nMax Price: \nAverage Price: ")
stats_label = tk.Label(root, textvariable=stats, font=("Arial", 12), justify=tk.LEFT)
stats_label.pack(pady=10)

# Run the application
root.mainloop()
