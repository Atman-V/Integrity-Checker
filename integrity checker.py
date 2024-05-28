import hashlib
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def calculate_hash(filepath, algorithm="sha256"):
    """Calculates the hash of a file."""
    try:
        hasher = hashlib.new(algorithm)
        with open(filepath, "rb") as file:
            while True:
                chunk = file.read(4096)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found.")  # More specific error message
        return None
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None

def verify_integrity():
    filepath = filepath_entry.get()
    if not filepath:
        messagebox.showwarning("Warning", "Please select a file.")
        return

    original_hash = original_hash_entry.get()
    if not original_hash:
        messagebox.showwarning("Warning", "Please enter the original hash.")
        return

    calculated_hash = calculate_hash(filepath, selected_algorithm.get())
    if calculated_hash is None:
        return

    if calculated_hash.lower() == original_hash.lower():
        result_label.config(text="Integrity Verified!", foreground="green")
    else:
        result_label.config(text="Integrity Check Failed!", foreground="red")

def browse_file():
    filepath = filedialog.askopenfilename()
    if filepath:
        filepath_entry.delete(0, tk.END)
        filepath_entry.insert(0, filepath)

def calculate_and_display_hash():
    filepath = filepath_entry.get()
    if not filepath:
        messagebox.showwarning("Warning", "Please select a file first.")
        return

    calculated_hash = calculate_hash(filepath, selected_algorithm.get())
    if calculated_hash:
        calculated_hash_label.config(text=f"Calculated Hash: {calculated_hash}")
    else:
        calculated_hash_label.config(text="Calculated Hash: ")  # Clear the label on error

def copy_hash():
    """Copies the calculated hash to the clipboard."""
    try:
        calculated_hash = calculated_hash_label.cget("text").replace("Calculated Hash: ", "")
        root.clipboard_clear()
        root.clipboard_append(calculated_hash)
        root.update()
        messagebox.showinfo("Copied", "Calculated hash copied to clipboard!")
    except tk.TclError:
        messagebox.showwarning("Warning", "No hash calculated yet.")

root = tk.Tk()
root.title("File Integrity Checker")

# File Selection
filepath_label = ttk.Label(root, text="Filepath:")
filepath_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

filepath_entry = ttk.Entry(root, width=50)
filepath_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

browse_button = ttk.Button(root, text="Browse", command=browse_file)
browse_button.grid(row=0, column=2, padx=5, pady=5)

# Hash Algorithm Selection
algorithm_label = ttk.Label(root, text="Algorithm:")
algorithm_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

algorithms = ["md5", "sha1", "sha256", "sha512"]
selected_algorithm = tk.StringVar(value="sha256")
algorithm_dropdown = ttk.Combobox(root, textvariable=selected_algorithm, values=algorithms, state="readonly")
algorithm_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="w")

# Calculate Hash Button
calculate_button = ttk.Button(root, text="Calculate Hash", command=calculate_and_display_hash)
calculate_button.grid(row=2, column=0, columnspan=3, pady=(10, 5))

# Calculated Hash Display
calculated_hash_label = ttk.Label(root, text="Calculated Hash:")
calculated_hash_label.grid(row=3, column=0, columnspan=2, padx=5, pady=(0, 10), sticky="w")  # Adjusted columnspan

# Copy Hash Button
copy_button = ttk.Button(root, text="Copy Hash", command=copy_hash)
copy_button.grid(row=3, column=2, padx=5, pady=(0, 10))

# Original Hash Input
original_hash_label = ttk.Label(root, text="Original Hash:")
original_hash_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")

original_hash_entry = ttk.Entry(root, width=50)
original_hash_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

# Verify Button
verify_button = ttk.Button(root, text="Verify Integrity", command=verify_integrity)
verify_button.grid(row=5, column=0, columnspan=3, pady=(10, 5))

# Result Label
result_label = ttk.Label(root, text="")
result_label.grid(row=6, column=0, columnspan=3, pady=(0, 10))

root.grid_columnconfigure(1, weight=1)

root.mainloop()