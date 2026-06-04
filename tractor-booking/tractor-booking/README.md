# 🚜 KisanShakti — Tractor Booking Website

A complete Flask + MySQL tractor booking website with WhatsApp integration.

---

## 📁 Project Structure

```
tractor-booking/
├── app.py                  ← Flask application (main file)
├── requirements.txt        ← Python packages to install
├── setup_database.sql      ← MySQL database setup script
├── templates/
│   ├── base.html           ← Navbar + Footer (shared layout)
│   ├── index.html          ← Home page
│   ├── services.html       ← Services page
│   ├── booking.html        ← Booking form page
│   ├── gallery.html        ← Photo gallery
│   ├── contact.html        ← Contact page
│   └── admin.html          ← Admin dashboard
└── static/
    ├── css/
    │   └── style.css       ← All styles (dark green + amber theme)
    ├── js/
    │   └── main.js         ← Booking form + animations
    └── images/             ← Put your tractor photos here
```

---

## ⚙️ Setup Instructions

### Step 1 — Install Python packages
```bash
pip install -r requirements.txt
```

### Step 2 — Setup MySQL Database
Open MySQL and run:
```bash
mysql -u root -p < setup_database.sql
```
Or open MySQL Workbench and paste the contents of `setup_database.sql` and run it.

### Step 3 — Configure Database + WhatsApp Number
Open `app.py` and edit these values:

```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'tractor_booking',
    'user': 'root',
    'password': 'YOUR_MYSQL_PASSWORD'   # ← Change this
}

WHATSAPP_NUMBER = "919876543210"   # ← Your father's number (91 + 10-digit)
```

### Step 4 — Run the Website
```bash
python app.py
```

Open your browser: **http://localhost:5000**

---

## 📄 Pages

| Page | URL | Description |
|------|-----|-------------|
| Home | `/` | Hero, services, testimonials, CTA |
| Services | `/services` | Detailed service list with pricing |
| Booking | `/booking` | Customer booking form |
| Gallery | `/gallery` | Tractor photo gallery |
| Contact | `/contact` | Phone, WhatsApp, quick messages |
| Admin | `/admin` | View all bookings, WhatsApp customer, delete |

---

## 🚀 How Booking Works

1. Customer fills the booking form at `/booking`
2. Form data is saved to MySQL database
3. A WhatsApp message opens automatically with booking details
4. Customer sends the WhatsApp message to your father
5. Your father calls the customer to confirm

---

## 📲 WhatsApp Message Format

```
🚜 New Tractor Booking

👤 Name: Raju Yadav
📞 Mobile: 9876543210
🏘️ Village: Dongarkhed
⚙️ Service: Land Ploughing
🌾 Acres: 3.5
📅 Date: 20 May 2025

Please contact the customer to confirm. 🙏
```

---

## 🗄️ Database Table: `bookings`

| Column | Type | Description |
|--------|------|-------------|
| id | INT AUTO_INCREMENT | Unique booking ID |
| name | VARCHAR(100) | Customer full name |
| mobile | VARCHAR(15) | 10-digit mobile number |
| village | VARCHAR(100) | Village/location name |
| service | VARCHAR(100) | Type of tractor service |
| acres | DECIMAL(5,2) | Number of acres |
| booking_date | DATE | Requested service date |
| status | ENUM | pending/confirmed/completed/cancelled |
| notes | TEXT | Optional extra notes |
| created_at | TIMESTAMP | Auto-set when record created |

---

## 🎨 Customization

### Change Colors
Edit CSS variables in `static/css/style.css`:
```css
:root {
  --green-dark: #0d3320;   /* Main dark green */
  --amber:      #f5a623;   /* Accent yellow */
}
```

### Add Real Photos
1. Copy your tractor photos to `static/images/`
2. In `templates/gallery.html`, replace the placeholder divs with:
```html
<img src="{{ url_for('static', filename='images/your-photo.jpg') }}" class="gallery-img">
```

### Change Business Name
Search and replace `KisanShakti` in all template files with your actual business name.

### Change Pricing
Edit pricing in `templates/services.html`, `templates/booking.html`, and `static/css/style.css`.

---

## 🌐 Hosting on Render (Free)

1. Push code to GitHub
2. Go to https://render.com
3. New → Web Service → Connect GitHub repo
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app`
6. Add environment variables for DB_CONFIG
7. Use PlanetScale or Railway for MySQL hosting

---

## 🌐 Hosting on Hostinger

1. Upload files via File Manager or FTP
2. Create MySQL database in Hostinger control panel
3. Update `DB_CONFIG` in `app.py` with Hostinger DB credentials
4. Set up Python app in Hostinger (Passenger WSGI)

---

## 📞 Admin Panel

Visit `/admin` to:
- View all customer bookings
- Search by name, village, or service
- WhatsApp individual customers directly
- Delete bookings
- See total bookings, acres, and villages stats

---

## 🛡️ Security Notes

- Add login protection to `/admin` before going live
- Use HTTPS in production
- Store DB password in environment variables, not in code
- Add CSRF protection for forms in production

---

Built with ❤️ for Indian farmers using Flask + MySQL + Bootstrap + WhatsApp
