import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk

def load_data(filepath):
    # Load a CSV file into a pandas DataFrame
    return pd.read_csv(filepath)

def handle_missing_values(df, strategy='median'):
    # Impute missing values in numerical columns or fill categorical ones with the mode
    imputer = SimpleImputer(strategy=strategy)
    for column in df.columns:
        if df[column].dtype in ['float64', 'int64']:
            df[column] = imputer.fit_transform(df[[column]])
        else:
            df[column].fillna(df[column].mode()[0], inplace=True)
    return df

def encode_categorical(df):
    # Encode categorical variables using LabelEncoder
    label_encoders = {}
    for column in df.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        label_encoders[column] = le
    return df, label_encoders

def scale_numerical(df):
    # Scale numerical features using StandardScaler
    scaler = StandardScaler()
    numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
    df[numerical_columns] = scaler.fit_transform(df[numerical_columns])
    return df, scaler

def process_data(file_path, handle_missing, encode_cat, scale_num, save_cleaned_data=False):
    # Full data cleaning pipeline
    df = load_data(file_path)
    
    if handle_missing:
        df = handle_missing_values(df)
    if encode_cat:
        df, label_encoders = encode_categorical(df)
    if scale_num:
        df, scaler = scale_numerical(df)
    
    if save_cleaned_data:
        df.to_csv(file_path.replace('.csv', '_cleaned.csv'), index=False)
        return file_path.replace('.csv', '_cleaned.csv')
    return df

def browse_file(entry):
    # Open a file dialog to select a file, and update the entry with the file path
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    entry.delete(0, tk.END)
    entry.insert(0, filepath)

def clean_and_save():
    file_path = entry.get()
    handle_missing = missing_var.get()
    encode_cat = encode_var.get()
    scale_num = scale_var.get()

    if not file_path:
        messagebox.showwarning("Input error", "Please provide a dataset path.")
        return
    
    try:
        log_text.insert(tk.END, "Processing...\n")
        cleaned_file = process_data(file_path, handle_missing, encode_cat, scale_num, save_cleaned_data=True)
        log_text.insert(tk.END, f"Data cleaning completed. Cleaned data saved as '{cleaned_file}'.\n")
        log_text.yview(tk.END)
    except Exception as e:
        log_text.insert(tk.END, f"An error occurred: {e}\n")
        log_text.yview(tk.END)

# Set up the GUI
root = tk.Tk()
root.title("Advanced Data Cleaning Tool")

frame = ttk.Frame(root, padding="10 10 10 10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# File selection
label = ttk.Label(frame, text="Dataset")
label.grid(row=0, column=0, sticky=tk.W)

entry = ttk.Entry(frame, width=50)
entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

browse_button = ttk.Button(frame, text="Browse", command=lambda: browse_file(entry))
browse_button.grid(row=0, column=2, sticky=tk.W)

# Checkboxes for data processing options
missing_var = tk.BooleanVar(value=True)
missing_cb = ttk.Checkbutton(frame, text="Handle Missing Values", variable=missing_var)
missing_cb.grid(row=1, column=0, columnspan=3, sticky=tk.W)

encode_var = tk.BooleanVar(value=True)
encode_cb = ttk.Checkbutton(frame, text="Encode Categorical Variables", variable=encode_var)
encode_cb.grid(row=2, column=0, columnspan=3, sticky=tk.W)

scale_var = tk.BooleanVar(value=True)
scale_cb = ttk.Checkbutton(frame, text="Scale Numerical Features", variable=scale_var)
scale_cb.grid(row=3, column=0, columnspan=3, sticky=tk.W)

# Buttons
clean_button = ttk.Button(frame, text="Clean and Save", command=clean_and_save)
clean_button.grid(row=4, column=0, columnspan=3)

# Log output
log_text = scrolledtext.ScrolledText(frame, width=60, height=15, wrap=tk.WORD)
log_text.grid(row=5, column=0, columnspan=3, padx=10, pady=10)
log_text.config(state=tk.NORMAL)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

root.mainloop()
