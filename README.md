# Health Management System (HMS) 🚑

Welcome to the Health Management System (HMS) project! This is a comprehensive clinical web application designed to streamline patient care and healthcare management. The system provides a user-friendly interface for patients, doctors, and administrators, facilitating appointment scheduling, prescription management, and more.

## Table of Contents

- Features
- Project Structure
- Database Schema
- Setup & Installation
- Usage
- API Endpoints
- Contributing
- License
- Contact

## Features 🏥

- **Patient Panel**: Patients can view appointment history and prescriptions.
- **Doctor Panel**: Doctors can manage appointments, prescribe medications, and search for patient appointments.
- **Admin Panel**: Administrators can manage doctors, patients, and view appointment details.
- **Search Functionality**: Search patients, doctors, appointments, and messages using contact details.
- **Appointment Management**: Create, view, and cancel appointments.
- **Prescription Management**: Submit and view prescriptions.
- **User Authentication**: Secure login and logout functionalities for all users.

## Project Structure 📂

- **static/**: Contains static files such as CSS and JavaScript.
- **templates/**: Contains HTML templates for different pages.
- **app.py**: The main Flask application file.
- **README.md**: This file.
- **requirements.txt**: Lists the dependencies required to run the project.
- **Schema.sql**: Contains the SQL scripts to create the database schema, including tables, views, and stored procedures.

## Database Schema 🗂️

The HMS project uses a SQL Server database with the following schema:

### Tables

- **Users**: Stores user information including `user_id`, `first_name`, `last_name`, `gender`, `email`, `contact`, `password`, `role`, and `specialization`.
- **Appointments**: Stores appointment details including `appointment_id`, `date`, `status`, `patient_id`, `doctor_id`.
- **Prescriptions**: Stores prescription details including `prescription_id`, `appointment_id`, `patient_id`, `doctor_id`, `date`, `medication`, `allergy`, `dosage`, `payment_status`.
- **ContactMessages**: Stores contact messages including `message_id`, `name`, `contact`, `email`, `message`, `date`.

### Views

- **P_Appoinment_details**: Displays appointment details for patients.
- **Prescription_Details**: Displays prescription details for patients.
- **DoctorView**: Displays a list of doctors with their full names, user IDs, gender, email, contact, password, role, and specialization.

### Stored Procedures

- `DoctorList`, `PatientList`, `AppointmentDetails`, `PrescriptionList`, `AddDoctor`, `DeleteDoctor`, etc.

  
## Setup & Installation 🛠️

### Prerequisites

- Python 3.x
- SQL Server
- Flask

### Installation

1. **Clone the repository**:
    ```bash
   git clone https://github.com/AshrafAbdelkhalek10/HMS.git
   cd HMS

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt

4. **Set up the database**:

    ```bash
   - Create the database in SQL Server.
   - Run the provided SQL script to create the tables, views, and stored procedures.

5. **Run the application**:
   ```bash
   flask run

6. **Access the application**:
   ```bash
   Open your browser and go to http://localhost:5000.

## Usage 💻

- **Login**: Users can log in based on their roles (Patient, Doctor, Admin).
- **Patient Panel**: View appointments and prescriptions.
- **Doctor Panel**: Manage patient appointments and prescriptions.
- **Admin Panel**: Manage doctors, patients, and view appointment details.

## API Endpoints 🛣️

Here are some of the key API endpoints available in the application:

- **GET** `/patient-panel.html`: Renders the patient panel.
- **POST** `/create-appointment`: Creates a new appointment.
- **POST** `/cancel-appointment/<int:appointment_id>`: Cancels an appointment.
- **GET** `/get-doctors`: Retrieves doctors based on specialization.
- **GET** `/search.html`: Search for appointments by patient contact.

## Contributing 🤝

We welcome contributions to this project! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (git checkout -b feature/your-feature-name).
3. Make your changes and commit them (git commit -m 'Add some feature').
4. Push to the branch (git push origin feature/your-feature-name).
5. Open a Pull Request.

## License 📄

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact 📧

If you have any questions or suggestions, feel free to contact us:

- **Email**: [Ashraf Abdelkhalek](mailto:abdelkhalekashraf0@gmail.com)
- **GitHub**: [Ashraf Abdelkhalek](https://github.com/AshrafAbdelkhalek10)

