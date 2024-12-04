import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

# Function to create the model, perform predictions, and display results
def run_model():
    # Get user input for start date
    start_date = start_date_entry.get_date()

    # Sample data based on user-selected start date
    data = {
        'Date': pd.date_range(start=start_date, periods=10, freq='D'),
        'Sales': [200, 220, 210, 250, 240, 230, 260, 270, 280, 290]
    }

    # Create DataFrame and set 'Date' as the index
    df = pd.DataFrame(data).set_index('Date')

    # Feature engineering
    df['Month'] = df.index.month
    df['Day_of_Week'] = df.index.dayofweek
    df['Lagged_Sales'] = df['Sales'].shift(1).fillna(df['Sales'].mean())  # Fill NaN with mean instead of dropping rows

    # Define features and target variable
    X = df[['Month', 'Day_of_Week', 'Lagged_Sales']]
    y = df['Sales']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Initialize and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate Mean Squared Error
    mse = mean_squared_error(y_test, y_pred)
    mse_label.config(text=f'Mean Squared Error: {mse:.2f}')

    # Plot Actual vs Predicted Sales
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(y_test.index, y_test, label='Actual Sales', marker='o')
    ax.plot(y_test.index, y_pred, label='Predicted Sales', linestyle='--', marker='x')
    ax.set_xlabel('Date')
    ax.set_ylabel('Sales')
    ax.set_title('Actual vs Predicted Sales')
    ax.legend()

    # Clear previous plot
    for widget in plot_frame.winfo_children():
        widget.destroy()

    # Display the plot in the tkinter window
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Create the main tkinter window
root = tk.Tk()
root.title("Sales Prediction Model")

# Add a frame for the Mean Squared Error
mse_frame = ttk.Frame(root, padding="10")
mse_frame.pack(side=tk.TOP, fill=tk.X)
mse_label = ttk.Label(mse_frame, text="Mean Squared Error: N/A")
mse_label.pack()

# Add a frame for date selection
date_frame = ttk.Frame(root, padding="10")
date_frame.pack(side=tk.TOP, fill=tk.X)
ttk.Label(date_frame, text="Select Start Date:").pack(side=tk.LEFT)
start_date_entry = DateEntry(date_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
start_date_entry.pack(side=tk.LEFT, padx=10)

# Add a frame for the plot
plot_frame = ttk.Frame(root, padding="10")
plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Add a button to run the model
button_frame = ttk.Frame(root, padding="10")
button_frame.pack(side=tk.BOTTOM, fill=tk.X)
run_button = ttk.Button(button_frame, text="Run Model", command=run_model)
run_button.pack()

# Run the tkinter main loop
root.mainloop()
