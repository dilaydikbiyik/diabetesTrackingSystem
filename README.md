# Diabetes Tracking System

A modular desktop application designed to simplify diabetes management for doctors and patients. It provides comprehensive infrastructure including blood sugar tracking, diet/exercise planning, alert systems, and disease diagnosis mechanisms.

---

## About the Project
The Diabetes Tracking System allows patients to perform their routine checks in daily life, while enabling doctors to manage their patients from a single panel. Thanks to its user-friendly interface, it offers easy-to-understand charts and reports.

## Key Features

### Doctor Module
- **Patient Management:** Add new patients to the system and view detailed archives of existing patients.
- **Diagnosis & Alert System:** Automatic alert assignments for critical and emergency situations, along with disease diagnosis.
- **Diet & Exercise Planning:** Customized diets (Low-Sugar, Sugar-Free, etc.) and activities (Clinical Exercise, Cycling, etc.) tailored to the patient's condition.
- **Graphical Tracking:** Analyze blood sugar fluctuations through hourly/meal-based charts.

### Patient Module
- **Data Entry:** Record regular blood sugar measurements and symptoms such as polyuria, fatigue, and blurred vision.
- **Recommendation Engine:** A personalized recommendation system that informs the patient based on entered values.
- **Tracking:** Monitor the status ("applied / not applied") of exercises and diets assigned by the doctor.

## Technologies Used
- **Programming Language:** Python 3.x
- **GUI Framework:** PyQt5
- **Database:** PostgreSQL (psycopg2)
- **Data Visualization:** Matplotlib / PyQtGraph

## Installation & Running

1. Clone the repository:
   ```bash
   git clone https://github.com/dilaydikbiyik/diabetesTrackingSystem.git
   cd diabetesTrackingSystem
   ```
2. Install required dependencies:
   ```bash
   pip install PyQt5 psycopg2 matplotlib
   ```
3. Set up the database:
   - Create a database named `diabetes_tracking_system` on PostgreSQL.
   - Import the `database.sql` and `diabetes_schema.sql` files located in the project directory.
   - Update the password/username in `database.py` to match your PostgreSQL configuration.
4. Launch the application:
   ```bash
   python app.py
   ```

## Screenshots

> 📸 Screenshots will be added soon.

## Author

**Dilay Dikbıyık** — [github.com/dilaydikbiyik](https://github.com/dilaydikbiyik)
