🧮 BMI Calculator — OIBSIP Task 2



A professional BMI (Body Mass Index) Calculator developed in Python as part of the Oasis Infobyte Python Internship (OIBSIP) — Task 2.



The application provides a user-friendly graphical interface, BMI calculation, input validation, database storage, BMI history, and a Matplotlib-based BMI graph.



✨ Features



\- Calculate BMI using weight and height

\- BMI category detection:

&#x20; - Underweight

&#x20; - Normal Weight

&#x20; - Overweight

&#x20; - Obese

\- Male/Female selection

\- Input validation and error handling

\- Clear input fields

\- Save BMI records using SQLite database

\- View the latest 10 BMI records

\- Clear complete BMI history

\- BMI graph using Matplotlib

\- Separate BMI Graph button

\- Professional and colourful Tkinter GUI

\- BMI result displayed with category-based colours

\- Successfully saved status message



🛠️ Technologies Used



\- Python

\- Tkinter — Graphical User Interface

\- SQLite3 — Database management

\- Matplotlib — BMI graph visualization



📁 Project Structure



Task 2 - BMI Calculator/

│

├── bmi\_gui.py

├── bmi\_records.db

└── README.md



📐 BMI Formula



BMI is calculated using:



BMI = Weight (kg) / Height² (m)



Height entered in centimetres is converted into metres before calculation.



BMI Categories



BMI Range| Category

Below 18.5| Underweight

18.5 – 24.9| Normal Weight

25 – 29.9| Overweight

30 and above| Obese



⚙️ Installation



Make sure Python is installed on your system.



Install Matplotlib:



pip install matplotlib



Tkinter and SQLite3 are included with standard Python installations on most systems.



▶️ How to Run



Open the project folder in Command Prompt or Terminal and run:



python bmi\_gui.py



The BMI Calculator GUI will open.



Steps



1\. Enter your name.

2\. Select Male or Female.

3\. Enter your weight in kilograms.

4\. Enter your height in centimetres.

5\. Click Calculate BMI.

6\. View your BMI and category.

7\. Use BMI Graph to view the graphical representation.

8\. Use History to view saved BMI records.



📊 BMI Graph



The application uses Matplotlib to display BMI ranges and highlight the user's current BMI.



The graph provides a visual representation of:



\- Underweight range

\- Normal Weight range

\- Overweight range

\- Obese range

\- Current BMI value



🗄️ Database



The application uses SQLite3 to store BMI records.



Each record contains:



\- Name

\- Gender

\- Weight

\- Height

\- BMI

\- BMI Category



The History section displays the latest 10 saved records.



🎨 GUI



The application uses Tkinter to provide a clean and professional graphical interface with:



\- Modern input section

\- Colour-coded fields

\- Clear buttons

\- Result card

\- BMI graph

\- History window



📸 Screenshots



Main BMI Calculator



Add your main GUI screenshot here.



BMI Result



Add your BMI result screenshot here.



BMI Graph



Add your Matplotlib graph screenshot here.



BMI History



Add your BMI History screenshot here.



🎥 Demo



Add your project demo video link here.



👨‍💻 Internship



Oasis Infobyte — OIBSIP Python Internship



Task: 2 — BMI Calculator



Technology: Python



📌 Author



Adarsh Tiwari



\---



⭐ If you find this project useful, consider giving it a star!

