# Hotel Management System

checkout button(generate billl)
LOGIN TO ADIM PAGE 

internal error 
oops concept 
raw sql
only shoq available ones in public home page 
place order error 


## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Setup and Installation](#setup-and-installation)
5. [Database Configuration](#database-configuration)
6. [Usage Instructions](#usage-instructions)
7. [Project Structure](#project-structure)
8. [Screenshots](#screenshots)
9. [Future Enhancements](#future-enhancements)
10. [Contributors](#contributors)
11. [License](#license)

---

## Project Overview
The **Hotel Management System** is a full-stack web application designed to manage hotel operations, such as room bookings, food ordering, and billing. This project helps streamline the management of hotel resources and provides a user-friendly interface for both staff and guests.

---

## Features
- **Room Booking**: Select and book rooms based on availability.
- **Food Ordering**: Choose dishes from a predefined menu.
- **Billing System**: Generate detailed bills for rooms and ordered food.
- **User Authentication**: Secure login for administrators and users.
- **Dashboard**: View room availability, food orders, and customer details.
- **Search Functionality**: Filter rooms and orders easily.

---

## Technologies Used
### Backend:
- **Python** (Django Framework)
- **MySQL** (Database Management System)

### Frontend:
- **HTML5**, **CSS3**, **JavaScript**
- **Bootstrap** (Responsive UI Framework)

### Tools:
- **MySQL Workbench** (Database Management)
- **Git** (Version Control)

---

## Setup and Installation
Follow the steps below to set up and run the project on your local machine:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/hotel-management-system.git
   cd hotel-management-system
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**:
   - Install MySQL and create a database named `hotelmanagementsystem`.
   - Update the credentials in `settings.py`:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.mysql',
             'NAME': 'hotelmanagementsystem',
             'USER': 'root',
             'PASSWORD': 'password123',
             'HOST': '127.0.0.1',
             'PORT': '3306',
         }
     }
     ```
   - Apply migrations:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

5. **Run the Server**:
   ```bash
   python manage.py runserver
   ```
   Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## Database Configuration
- **Database**: MySQL
- **Name**: `hotelmanagementsystem`
- **Tables**:
   - `Rooms`: Stores room details (room number, type, price, status).
   - `Dishes`: Contains menu items (name, price).
   - `Orders`: Stores food orders.
   - `Bookings`: Contains room bookings and customer information.

---

## Usage Instructions
1. **Login**: Access the admin dashboard via `/admin`.
2. **Room Booking**:
   - Navigate to the "Rooms" section.
   - Select available rooms to book.
3. **Food Ordering**:
   - Browse through the menu and add dishes.
   - Place an order and generate a bill.
4. **Billing**: View and print invoices for room bookings and food orders.

---

## Project Structure
```
myhotel_project/
|-- manage.py
|-- myhotel_project/
|   |-- settings.py
|   |-- urls.py
|   |-- wsgi.py
|-- hotel_app/
|   |-- templates/
|   |-- static/
|   |-- migrations/
|   |-- views.py
|   |-- models.py
|   |-- urls.py
|-- static/
|-- templates/
|-- requirements.txt
```


## Future Enhancements
- Add user roles (admin, receptionist, guest).
- Integrate online payment gateways.
- Include room check-in/check-out reminders.
- Add advanced reporting and analytics.

---


## License
This project is licensed under the SRH License - see the [LICENSE]file for details.
