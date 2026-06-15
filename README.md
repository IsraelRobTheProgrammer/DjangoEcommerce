# Django E-Commerce Platform

A full-stack e-commerce platform built with Django and PostgreSQL, designed for dairy product sales. The application provides a complete online shopping experience including product browsing, cart management, wishlists, order processing, and secure payments through Flutterwave.

---

## Features

* User authentication and authorization
* Product catalog and category management
* Shopping cart functionality
* Wishlist management
* Secure checkout process
* Flutterwave payment integration
* Order tracking and management
* Admin dashboard for product and order administration
* Responsive web interface

---

## Tech Stack

### Backend

* Django

### Database

* PostgreSQL

### Payment Processing

* Flutterwave

### Deployment

* AWS

### Authentication

* Django Authentication System

---

## Architecture Overview

The application follows Django's MVT (Model-View-Template) architecture and is structured around core e-commerce workflows:

* Product Management
* Customer Accounts
* Cart and Wishlist Operations
* Order Processing
* Payment Handling
* Administrative Controls

---

## Getting Started

### Prerequisites

Before running the project, ensure you have the following installed:

* Python 3.10+
* PostgreSQL
* Git

---

### Installation

Clone the repository:

```bash
git clone https://github.com/IsraelRobTheProgrammer/DjangoEcommerce.git
cd project-name
```

Create and activate a virtual environment:

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

### Environment Variables

Create a `.env` file in the project root and configure the following variables:

```env
SECRET_KEY=your_secret_key

DB_NAME=your_database
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432

FLUTTERWAVE_PUBLIC_KEY=your_flutterwave_public_key
FLUTTERWAVE_SECRET_KEY=your_flutterwave_secret_key
```

---

### Database Setup

Apply migrations:

```bash
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

---

### Running the Application

Start the development server:

```bash
python manage.py runserver
```

Visit:

```text
http://127.0.0.1:8000
```

---

## Project Structure

```text
project/
├── app/
├── EcommerceApp/
├── staticfiles/
├── media/
├── manage.py
└── requirements.txt
```

---

## Challenges & Learnings

During development, key challenges included:

* Integrating Flutterwave payment services and handling payment verification workflows.
* Designing relationships between products, carts, wishlists, and orders.
* Managing order lifecycle transitions after successful payments.
* Configuring and deploying a Django application on AWS.
* Handling environment-specific settings for development and production.

This project provided practical experience with building and deploying a complete e-commerce workflow using Django and PostgreSQL.

---

## Future Improvements

* Product reviews and ratings
* Inventory management system
* Email notifications
* Sales analytics dashboard
* Product recommendation engine

---

## License

This project was created for learning and portfolio purposes.