# LifeLink: Online Blood Donation Platform

A comprehensive Django-based web application for connecting blood donors, blood banks, and patients. Built as a final-year academic project with real-time chat functionality and location-aware features.

## Features

### 🔐 Role-Based Access Control (RBAC)
- **Three distinct roles**: Donor, Blood Bank, Patient
- Separate dashboards for each role
- Role-specific access restrictions using decorators

### 📍 Location-Aware System
- Real-time geolocation capture using Browser Geolocation API
- Stores latitude, longitude, and location name
- Distance-based search using Haversine formula
- No static text-only location fields

### 🩸 Donor Module
- Donor profile with blood group, age, availability status
- Eligibility checking (90-day rule, age restrictions)
- Availability toggle (ON/OFF)
- Donation scheduling with nearby blood banks
- Donation history tracking

### 🏥 Blood Bank Module
- Blood inventory management (add, remove, update units)
- Low stock alerts
- View scheduled donors
- Mark donations as completed
- Automatic inventory updates on completion

### 🧑‍🦱 Patient Module
- Search donors by blood group and distance
- Search blood banks with available units
- Filter by availability status
- Distance-based results

### 💬 Real-Time Chat System
- One-to-one WebSocket-based chat
- Patient ↔ Donor
- Patient ↔ Blood Bank
- Donor ↔ Blood Bank
- Real-time message delivery
- Chat history stored in database

## Tech Stack

### Backend
- Django 4.2.7
- Django Channels (WebSocket support)
- SQLite database
- Django ORM

### Frontend
- HTML5, CSS3
- Bootstrap 5
- JavaScript
- WebSockets (for real-time chat)

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd life_link
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create a superuser (optional)**
```bash
python manage.py createsuperuser
```

6. **Run the development server**
```bash
python manage.py runserver
```

7. **Run Daphne for WebSocket support** (in a separate terminal)
```bash
daphne -b 0.0.0.0 -p 8000 lifelink.asgi:application
```

Or use the standard runserver with Channels configured:
```bash
python manage.py runserver
```

## Usage

### Registration
1. Navigate to the home page
2. Click "Register"
3. Select your role (Donor, Blood Bank, or Patient)
4. Fill in your details
5. **Allow location access** when prompted (required)
6. Complete registration

### Login
1. Click "Login"
2. Select your role from the dropdown
3. Enter email and password
4. Access your role-specific dashboard

### For Donors
- Complete your profile (age, blood group)
- Toggle availability ON/OFF
- Schedule donations with nearby blood banks
- View donation history

### For Blood Banks
- Manage blood inventory (add/remove/update units)
- View scheduled donors
- Mark donations as completed
- Monitor low stock alerts

### For Patients
- Search for donors by blood group and distance
- Search for blood banks with available units
- Chat with donors or blood banks
- View availability status

## Project Structure

```
life_link/
├── accounts/          # Authentication and user management
├── donors/           # Donor module
├── bloodbanks/       # Blood bank module
├── patients/         # Patient module
├── chat/             # Real-time chat system
├── templates/        # HTML templates
├── static/           # Static files
├── lifelink/         # Main project settings
└── manage.py
```

## Key Files

- `accounts/models.py` - Custom User model with role and location
- `accounts/decorators.py` - RBAC decorators
- `accounts/utils.py` - Distance calculation utilities
- `chat/consumers.py` - WebSocket consumer for real-time chat
- `donors/models.py` - Donor profile and donation scheduling
- `bloodbanks/models.py` - Blood bank and inventory models

## Academic Features Demonstrated

✅ Clean, modular code structure
✅ RBAC implementation with decorators
✅ Real-time features (WebSocket chat)
✅ Location-aware search with distance calculation
✅ Django ORM and models
✅ Bootstrap 5 UI
✅ Django Channels integration
✅ Donor eligibility logic
✅ Inventory management
✅ Audit trails (created_at, updated_at fields)

## Important Notes

- This is an academic project, not for production use
- Location capture requires HTTPS in production (HTTP works in development)
- Chat uses InMemoryChannelLayer (use Redis for production)
- SQLite is used for simplicity (use PostgreSQL for production)

## Future Enhancements (Out of Scope)

- AI recommendations
- Payment integration
- Google Maps UI integration
- Mobile app
- SMS/Email notifications
- Advanced analytics

## License

This project is developed for academic purposes.

## Author

Developed as a final-year academic project demonstrating Django full-stack development capabilities.

