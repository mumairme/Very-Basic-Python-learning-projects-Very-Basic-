import tkinter as tk
from tkinter import messagebox
import subprocess

# -----------------------------
# Calculator Logic
# -----------------------------
def press(key):
    """Handle button presses and update the display."""
    if key == "C":
        display_var.set("")
        return

    if key == "⌫":
        display_var.set(display_var.get()[:-1])
        return

    if key == "=":
        evaluate_expression()
        return

    # Map UI symbols to Python operators
    mapped = key
    if key == "×":
        mapped = "*"
    elif key == "÷":
        mapped = "/"

    display_var.set(display_var.get() + mapped)

def evaluate_expression():
    expr = display_var.get().strip()
    if not expr:
        return

    try:
        # Basic safe eval: no builtins, no access to Python internals
        result = eval(expr, {"__builtins__": None}, {})
        display_var.set(str(result))
    except ZeroDivisionError:
        messagebox.showerror("Math Error", "Division by zero is not allowed.")
    except Exception:
        messagebox.showerror("Error", "Invalid expression.")

def open_calculator():
    try:
        subprocess.Popen(["calc.exe"])  # Windows default calculator
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open calculator: {str(e)}")

# -----------------------------
# UI Setup
# -----------------------------
root = tk.Tk()
root.title("Full Calculator")

display_var = tk.StringVar()

display = tk.Entry(
    root,
    textvariable=display_var,
    font=("Arial", 18),
    bd=8,
    relief="ridge",
    justify="right"
)
display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

# Buttons layout
buttons = [
    ["C", "⌫", "(", ")"],
    ["7", "8", "9", "÷"],
    ["4", "5", "6", "×"],
    ["1", "2", "3", "-"],
    ["0", ".", "%", "+"],
    ["Open", "=", "", ""]
]

for r, row in enumerate(buttons, start=1):
    for c, key in enumerate(row):
        if key == "":
            continue

        if key == "Open":
            btn = tk.Button(
                root, text="Open Calculator",
                font=("Arial", 12),
                command=open_calculator
            )
            btn.grid(row=r, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
            continue

        btn = tk.Button(
            root,
            text=key,
            font=("Arial", 14),
            command=lambda k=key: press(k)
        )
        btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")

# Make the grid responsive
for i in range(4):
    root.grid_columnconfigure(i, weight=1)
for i in range(len(buttons) + 1):
    root.grid_rowconfigure(i, weight=1)

root.mainloop()