import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt


DB_NAME = "bmi_records.db"

# Professional fonts
FONT = "Segoe UI"


# =========================
# DATABASE SETUP
# =========================
def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bmi_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            gender TEXT DEFAULT 'Not specified',
            weight REAL NOT NULL,
            height REAL NOT NULL,
            bmi REAL NOT NULL,
            category TEXT NOT NULL
        )
    """)

    cursor.execute("PRAGMA table_info(bmi_records)")
    columns = [column[1] for column in cursor.fetchall()]

    if "gender" not in columns:
        cursor.execute("""
            ALTER TABLE bmi_records
            ADD COLUMN gender TEXT DEFAULT 'Not specified'
        """)

    conn.commit()
    conn.close()


setup_database()


# =========================
# CALCULATE BMI
# =========================
def calculate_bmi():

    name = name_entry.get().strip()
    gender = gender_var.get()
    weight_text = weight_entry.get().strip()
    height_text = height_entry.get().strip()

    if not name:
        messagebox.showerror("Input Error", "Please enter your name.")
        return

    if not weight_text:
        messagebox.showerror("Input Error", "Please enter your weight.")
        return

    if not height_text:
        messagebox.showerror("Input Error", "Please enter your height.")
        return

    try:
        weight = float(weight_text)
        height_cm = float(height_text)

        if weight <= 0:
            messagebox.showerror(
                "Invalid Weight",
                "Weight must be greater than 0."
            )
            return

        if height_cm <= 0:
            messagebox.showerror(
                "Invalid Height",
                "Height must be greater than 0."
            )
            return

        height_m = height_cm / 100

        # BMI Formula
        bmi = weight / (height_m ** 2)
        bmi = round(bmi, 2)

        # BMI Category
        if bmi < 18.5:
            category = "Underweight"
            result_color = "#2563eb"

        elif bmi < 25:
            category = "Normal Weight"
            result_color = "#16a34a"

        elif bmi < 30:
            category = "Overweight"
            result_color = "#ea580c"

        else:
            category = "Obese"
            result_color = "#dc2626"

        result_label.config(
            text=f"BMI: {bmi:.2f}\nCategory: {category}",
            fg=result_color
        )

        # Save to database
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO bmi_records
                (name, gender, weight, height, bmi, category)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                name,
                gender,
                weight,
                height_cm,
                bmi,
                category
            ))

            conn.commit()
            conn.close()

            save_status.config(
                text="✓ Successfully saved",
                fg="#16a34a"
            )

        except sqlite3.Error as e:
            messagebox.showerror(
                "Database Error",
                f"Could not save record.\n{e}"
            )

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter valid numbers for weight and height."
        )


# =========================
# CLEAR CURRENT INPUT
# =========================
def clear_fields():

    name_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)

    gender_var.set("Male")

    result_label.config(
        text="Enter your details and click Calculate BMI",
        fg="#64748b"
    )

    save_status.config(text="")


# =========================
# ADVANCED BMI GRAPH
# =========================
def show_bmi_graph():

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT bmi, category, name
            FROM bmi_records
            ORDER BY id DESC
            LIMIT 1
        """)

        record = cursor.fetchone()
        conn.close()

        if record is None:
            messagebox.showinfo(
                "BMI Graph",
                "Please calculate BMI first."
            )
            return

        bmi, category, name = record

        # Create advanced Matplotlib graph
        fig, ax = plt.subplots(figsize=(10, 5.5))

        # BMI category ranges
        ranges = [
            ("Underweight", 0, 18.5),
            ("Normal Weight", 18.5, 25),
            ("Overweight", 25, 30),
            ("Obese", 30, 45)
        ]

        # Background category zones
        ax.axhspan(0, 18.5, alpha=0.12)
        ax.axhspan(18.5, 25, alpha=0.12)
        ax.axhspan(25, 30, alpha=0.12)
        ax.axhspan(30, 45, alpha=0.12)

        # Category boundary lines
        ax.axhline(18.5, linestyle="--", linewidth=1.5)
        ax.axhline(25, linestyle="--", linewidth=1.5)
        ax.axhline(30, linestyle="--", linewidth=1.5)

        # Category labels
        ax.text(
            0.5, 9.25,
            "Underweight\n< 18.5",
            ha="center",
            va="center",
            fontsize=11,
            fontweight="bold"
        )

        ax.text(
            0.5, 21.75,
            "Normal Weight\n18.5 – 24.9",
            ha="center",
            va="center",
            fontsize=11,
            fontweight="bold"
        )

        ax.text(
            0.5, 27.5,
            "Overweight\n25 – 29.9",
            ha="center",
            va="center",
            fontsize=11,
            fontweight="bold"
        )

        ax.text(
            0.5, 37.5,
            "Obese\n≥ 30",
            ha="center",
            va="center",
            fontsize=11,
            fontweight="bold"
        )

        # Current BMI marker
        ax.axhline(
            bmi,
            linewidth=3,
            label=f"{name}'s BMI = {bmi:.2f}"
        )

        ax.scatter(
            0.5,
            bmi,
            s=140,
            zorder=5
        )

        ax.annotate(
            f"  Your BMI: {bmi:.2f}\n  {category}",
            xy=(0.5, bmi),
            xytext=(1.2, bmi),
            fontsize=11,
            fontweight="bold",
            va="center",
            arrowprops=dict(
                arrowstyle="->",
                linewidth=1.5
            )
        )

        # Graph title and labels
        ax.set_title(
            "BMI Health Range Graph",
            fontsize=19,
            fontweight="bold",
            pad=15
        )

        ax.set_ylabel(
            "BMI Value",
            fontsize=12,
            fontweight="bold"
        )

        ax.set_xlabel(
            "BMI Categories",
            fontsize=12,
            fontweight="bold"
        )

        ax.set_ylim(0, 45)

        ax.set_xlim(0, 1)

        ax.set_xticks([0.5])
        ax.set_xticklabels(["BMI Range"])

        ax.grid(
            axis="y",
            linestyle=":",
            alpha=0.5
        )

        ax.legend(
            loc="upper right",
            fontsize=10
        )

        # Remove unnecessary borders
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        plt.tight_layout()
        plt.show()

    except sqlite3.Error as e:
        messagebox.showerror(
            "Database Error",
            f"Could not load BMI data.\n{e}"
        )


# =========================
# HISTORY WINDOW
# =========================
def show_history():

    history_window = tk.Toplevel(window)

    history_window.title("BMI History")
    history_window.geometry("950x600")
    history_window.configure(bg="#eef4fb")

    tk.Label(
        history_window,
        text="BMI History",
        font=(FONT, 24, "bold"),
        bg="#eef4fb",
        fg="#2563eb"
    ).pack(pady=(20, 5))

    tk.Label(
        history_window,
        text="Your saved BMI records",
        font=(FONT, 12),
        bg="#eef4fb",
        fg="#64748b"
    ).pack(pady=(0, 10))

    tk.Button(
        history_window,
        text="Clear History",
        command=lambda: clear_history(history_window),
        font=(FONT, 11, "bold"),
        bg="#dc2626",
        fg="white",
        padx=18,
        pady=7,
        relief="flat",
        cursor="hand2"
    ).pack(pady=(0, 10))

    table_frame = tk.Frame(
        history_window,
        bg="white"
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=10
    )

    scrollbar = tk.Scrollbar(table_frame)
    scrollbar.pack(side="right", fill="y")

    history_canvas = tk.Canvas(
        table_frame,
        bg="white",
        highlightthickness=0,
        yscrollcommand=scrollbar.set
    )

    history_canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.config(
        command=history_canvas.yview
    )

    history_content = tk.Frame(
        history_canvas,
        bg="white"
    )

    history_canvas.create_window(
        (0, 0),
        window=history_content,
        anchor="nw"
    )

    history_content.bind(
        "<Configure>",
        lambda e: history_canvas.configure(
            scrollregion=history_canvas.bbox("all")
        )
    )

    headers = [
        "No.",
        "Name",
        "Gender",
        "Weight",
        "Height",
        "BMI",
        "Category"
    ]

    for col, header in enumerate(headers):

        tk.Label(
            history_content,
            text=header,
            font=(FONT, 11, "bold"),
            bg="#2563eb",
            fg="white",
            padx=14,
            pady=10
        ).grid(
            row=0,
            column=col,
            sticky="nsew"
        )

    load_history_records(history_content)


# =========================
# LOAD HISTORY RECORDS
# =========================
def load_history_records(history_content):

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name, gender, weight, height, bmi, category
            FROM bmi_records
            ORDER BY id DESC
            LIMIT 10
        """)

        records = cursor.fetchall()
        conn.close()

        records.reverse()

        for i, record in enumerate(records, start=1):

            name, gender, weight, height, bmi, category = record

            values = [
                i,
                name,
                gender,
                f"{weight} kg",
                f"{height} cm",
                f"{bmi:.2f}",
                category
            ]

            for col, value in enumerate(values):

                if category == "Normal Weight":
                    text_color = "#16a34a"

                elif category == "Underweight":
                    text_color = "#2563eb"

                elif category == "Overweight":
                    text_color = "#ea580c"

                else:
                    text_color = "#dc2626"

                tk.Label(
                    history_content,
                    text=value,
                    font=(FONT, 10),
                    bg="white",
                    fg=text_color if col == 6 else "#1e293b",
                    padx=12,
                    pady=9
                ).grid(
                    row=i,
                    column=col,
                    sticky="nsew"
                )

    except sqlite3.Error as e:
        messagebox.showerror(
            "Database Error",
            f"Could not load history.\n{e}"
        )


# =========================
# CLEAR HISTORY
# =========================
def clear_history(history_window):

    answer = messagebox.askyesno(
        "Clear History",
        "Are you sure you want to delete all BMI history?"
    )

    if not answer:
        return

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM bmi_records")

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "History Cleared",
            "BMI history has been cleared successfully."
        )

        history_window.destroy()
        show_history()

    except sqlite3.Error as e:
        messagebox.showerror(
            "Database Error",
            f"Could not clear history.\n{e}"
        )


# =========================
# MAIN WINDOW
# =========================
window = tk.Tk()

window.title("BMI Calculator - OIBSIP Task 2")
window.configure(bg="#eef4fb")

try:
    window.state("zoomed")
except:
    window.geometry("1100x750")

window.resizable(True, True)


# =========================
# HEADER
# =========================
header = tk.Frame(
    window,
    bg="#2563eb",
    height=85
)

header.pack(fill="x")
header.pack_propagate(False)


tk.Label(
    header,
    text="BMI CALCULATOR",
    font=(FONT, 28, "bold"),
    bg="#2563eb",
    fg="white"
).pack(pady=(12, 0))


tk.Label(
    header,
    text="OIBSIP Python Internship • Task 2",
    font=(FONT, 12),
    bg="#2563eb",
    fg="#dbeafe"
).pack()


# =========================
# CONTENT
# =========================
content = tk.Frame(
    window,
    bg="#eef4fb"
)

content.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=15
)

# =========================
# INPUT CARD
# =========================
input_card = tk.Frame(
    content,
    bg="#f5f3ff",
    highlightthickness=1,
    highlightbackground="#c4b5fd"
)

input_card.pack(
    fill="x",
    pady=(0, 10)
)


# Input card title
tk.Label(
    input_card,
    text="Enter Your Details",
    font=(FONT, 19, "bold"),
    bg="#f5f3ff",
    fg="#5b21b6"
).grid(
    row=0,
    column=0,
    columnspan=2,
    pady=(15, 12)
)


# -------------------------
# Name
# -------------------------
tk.Label(
    input_card,
    text="Name",
    font=(FONT, 12, "bold"),
    bg="#f5f3ff",
    fg="#4c1d95"
).grid(
    row=1,
    column=0,
    sticky="e",
    padx=(35, 15),
    pady=8
)

name_entry = tk.Entry(
    input_card,
    font=(FONT, 12),
    width=32,
    bg="#ffffff",
    fg="#1e293b",
    insertbackground="#5b21b6",
    relief="solid",
    bd=1
)

name_entry.grid(
    row=1,
    column=1,
    sticky="w",
    padx=(5, 35),
    pady=8,
    ipady=6
)


# -------------------------
# Gender
# -------------------------
tk.Label(
    input_card,
    text="Gender",
    font=(FONT, 12, "bold"),
    bg="#f5f3ff",
    fg="#4c1d95"
).grid(
    row=2,
    column=0,
    sticky="e",
    padx=(35, 15),
    pady=8
)

gender_var = tk.StringVar(value="Male")

gender_frame = tk.Frame(
    input_card,
    bg="#fce7f3",
    highlightthickness=1,
    highlightbackground="#f9a8d4"
)

gender_frame.grid(
    row=2,
    column=1,
    sticky="w",
    padx=(5, 35),
    pady=8
)


tk.Radiobutton(
    gender_frame,
    text="  Male",
    variable=gender_var,
    value="Male",
    bg="#fce7f3",
    fg="#9d174d",
    activebackground="#fbcfe8",
    activeforeground="#9d174d",
    selectcolor="#ffffff",
    font=(FONT, 11, "bold"),
    padx=10,
    pady=5
).pack(side="left")


tk.Radiobutton(
    gender_frame,
    text="  Female",
    variable=gender_var,
    value="Female",
    bg="#fce7f3",
    fg="#9d174d",
    activebackground="#fbcfe8",
    activeforeground="#9d174d",
    selectcolor="#ffffff",
    font=(FONT, 11, "bold"),
    padx=10,
    pady=5
).pack(side="left", padx=(5, 10))


# -------------------------
# Weight
# -------------------------
tk.Label(
    input_card,
    text="Weight (kg)",
    font=(FONT, 12, "bold"),
    bg="#f5f3ff",
    fg="#166534"
).grid(
    row=3,
    column=0,
    sticky="e",
    padx=(35, 15),
    pady=8
)

weight_entry = tk.Entry(
    input_card,
    font=(FONT, 12),
    width=32,
    bg="#f0fdf4",
    fg="#14532d",
    insertbackground="#16a34a",
    relief="solid",
    bd=1
)

weight_entry.grid(
    row=3,
    column=1,
    sticky="w",
    padx=(5, 35),
    pady=8,
    ipady=6
)


# -------------------------
# Height
# -------------------------
tk.Label(
    input_card,
    text="Height (cm)",
    font=(FONT, 12, "bold"),
    bg="#f5f3ff",
    fg="#9a3412"
).grid(
    row=4,
    column=0,
    sticky="e",
    padx=(35, 15),
    pady=8
)

height_entry = tk.Entry(
    input_card,
    font=(FONT, 12),
    width=32,
    bg="#fff7ed",
    fg="#7c2d12",
    insertbackground="#ea580c",
    relief="solid",
    bd=1
)

height_entry.grid(
    row=4,
    column=1,
    sticky="w",
    padx=(5, 35),
    pady=8,
    ipady=6
)



# =========================
# BUTTONS
# =========================
button_frame = tk.Frame(
    input_card,
    bg="white"
)

button_frame.grid(
    row=5,
    column=0,
    columnspan=2,
    pady=(8, 12)
)


tk.Button(
    button_frame,
    text="Calculate BMI",
    command=calculate_bmi,
    font=(FONT, 11, "bold"),
    bg="#2563eb",
    fg="white",
    padx=18,
    pady=7,
    relief="flat",
    cursor="hand2"
).pack(side="left", padx=4)


tk.Button(
    button_frame,
    text="Clear",
    command=clear_fields,
    font=(FONT, 11, "bold"),
    bg="#64748b",
    fg="white",
    padx=18,
    pady=7,
    relief="flat",
    cursor="hand2"
).pack(side="left", padx=4)


tk.Button(
    button_frame,
    text="BMI Graph",
    command=show_bmi_graph,
    font=(FONT, 11, "bold"),
    bg="#16a34a",
    fg="white",
    padx=18,
    pady=7,
    relief="flat",
    cursor="hand2"
).pack(side="left", padx=4)


tk.Button(
    button_frame,
    text="History",
    command=show_history,
    font=(FONT, 11, "bold"),
    bg="#7c3aed",
    fg="white",
    padx=18,
    pady=7,
    relief="flat",
    cursor="hand2"
).pack(side="left", padx=4)


# =========================
# RESULT CARD
# =========================
result_card = tk.Frame(
    content,
    bg="white",
    highlightthickness=1,
    highlightbackground="#dbe3ef"
)

result_card.pack(
    fill="x",
    pady=(0, 8)
)


tk.Label(
    result_card,
    text="Your Result",
    font=(FONT, 16, "bold"),
    bg="white",
    fg="#1e293b"
).pack(pady=(7, 1))


result_label = tk.Label(
    result_card,
    text="Enter your details and click Calculate BMI",
    font=(FONT, 16, "bold"),
    bg="white",
    fg="#64748b",
    justify="center",
    wraplength=900,
    pady=8
)

result_label.pack(
    fill="x",
    padx=20
)


# Successfully saved message
save_status = tk.Label(
    result_card,
    text="",
    font=(FONT, 11, "bold"),
    bg="white",
    fg="#16a34a"
)

save_status.pack(
    pady=(0, 8)
)


# =========================
# FOOTER
# =========================
tk.Label(
    window,
    text="BMI Calculator • OIBSIP Python Internship Task 2",
    font=(FONT, 9),
    bg="#eef4fb",
    fg="#64748b"
).pack(pady=(0, 5))


# =========================
# RUN
# =========================
window.mainloop()