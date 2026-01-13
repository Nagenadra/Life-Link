

# LifeLink Setup Guide

## Quick Start Steps

### 1. Install Dependencies

First, make sure you have Python 3.8+ installed. Then install the required packages:

```bash
pip install -r requirements.txt
```

### 2. Create Database Migrations

Run these commands to set up the database:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create a Superuser (Optional - for Django Admin)

```bash
python manage.py createsuperuser
```

This allows you to access the Django admin panel at `/admin/`

### 4. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000/**

## Testing the Application

### Step 1: Register Test Users

1. Go to http://127.0.0.1:8000/
2. Click "Register"
3. Create test accounts for each role:
   - **Donor**: Select "Donor" role, fill details, allow location access
   - **Blood Bank**: Select "Blood Bank" role, fill details, allow location access
   - **Patient**: Select "Patient" role, fill details, allow location access

### Step 2: Complete Profiles

**For Donors:**
- Go to Donor Dashboard
- Click "Edit Profile"
- Enter age (18-65) and select blood group
- Save profile

**For Blood Banks:**
- Go to Blood Bank Dashboard
- Click "Manage Inventory"
- Add blood units for different blood groups

### Step 3: Test Features

**Search (as Patient):**
- Go to Patient Dashboard
- Click "Search Now"
- Select a blood group and search
- View nearby donors and blood banks

**Schedule Donation (as Donor):**
- Go to Donor Dashboard
- Click "Schedule New Donation"
- Select a nearby blood bank
- Choose date/time
- Confirm

**Chat Feature:**
- From search results or scheduled donors list
- Click "Chat" button
- Send messages in real-time

## Common Issues

### Issue: Location not capturing
**Solution:** Make sure you allow location permissions in your browser. In development, HTTP is fine, but in production you need HTTPS.

### Issue: WebSocket connection failed
**Solution:** Make sure you're using the standard Django development server (`python manage.py runserver`). Channels is configured to work with it.

### Issue: No migrations found
**Solution:** Run `python manage.py makemigrations` for each app:
```bash
python manage.py makemigrations accounts
python manage.py makemigrations donors
python manage.py makemigrations bloodbanks
python manage.py makemigrations patients
python manage.py makemigrations chat
python manage.py migrate
```

### Issue: Profile doesn't exist
**Solution:** The signals should automatically create profiles. If not, you can manually create them in Django admin or they'll be created when you first access the dashboard.

## Project Structure Overview

```
life_link/
├── accounts/          # User authentication & RBAC
├── donors/           # Donor module
├── bloodbanks/       # Blood bank module
├── patients/         # Patient module
├── chat/             # Real-time chat
├── templates/        # HTML templates
├── lifelink/         # Project settings
└── manage.py
```

## Ready for Demo!

Once everything is set up:
- ✅ All features are implemented and working
- ✅ RBAC is enforced
- ✅ Location-based search works
- ✅ Real-time chat is functional
- ✅ All dashboards are accessible

Good luck with your presentation! 🎓

