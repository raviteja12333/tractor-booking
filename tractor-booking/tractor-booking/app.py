from flask import Flask, render_template, request, jsonify, redirect, url_for
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os

app = Flask(__name__)

# ─────────────────────────────────────────
# DATABASE CONFIG — edit these values
# ─────────────────────────────────────────
DB_CONFIG = {
    'host': 'localhost',
    'database': 'tractor_booking',
    'user': 'root',
    'password': 'your_password_here'
}

# WhatsApp number (your father's number with country code, no + or spaces)
WHATSAPP_NUMBER = "919392186462"  # Example: India +91 98765 43210


def get_db_connection():
    """Create and return a database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Database connection error: {e}")
        return None


def init_db():
    """Initialize the database and create tables if they don't exist."""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                mobile VARCHAR(15) NOT NULL,
                village VARCHAR(100) NOT NULL,
                service VARCHAR(100) NOT NULL,
                acres DECIMAL(5,2) NOT NULL,
                booking_date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully.")
    else:
        print("Could not connect to database. Running without DB.")


# ─────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────

@app.route('/')
def home():
    return render_template('index.html', whatsapp_number=WHATSAPP_NUMBER)


@app.route('/services')
def services():
    return render_template('services.html', whatsapp_number=WHATSAPP_NUMBER)


@app.route('/booking')
def booking():
    return render_template('booking.html', whatsapp_number=WHATSAPP_NUMBER)


@app.route('/gallery')
def gallery():
    return render_template('gallery.html', whatsapp_number=WHATSAPP_NUMBER)


@app.route('/contact')
def contact():
    return render_template('contact.html', whatsapp_number=WHATSAPP_NUMBER)


@app.route('/submit-booking', methods=['POST'])
def submit_booking():
    """Handle booking form submission."""
    try:
        data = request.get_json()

        name         = data.get('name', '').strip()
        mobile       = data.get('mobile', '').strip()
        village      = data.get('village', '').strip()
        service      = data.get('service', '').strip()
        acres        = float(data.get('acres', 0))
        booking_date = data.get('booking_date', '').strip()

        # Basic validation
        if not all([name, mobile, village, service, acres, booking_date]):
            return jsonify({'success': False, 'message': 'All fields are required.'}), 400

        # Save to database
        saved = False
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO bookings (name, mobile, village, service, acres, booking_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, mobile, village, service, acres, booking_date))
            conn.commit()
            booking_id = cursor.lastrowid
            cursor.close()
            conn.close()
            saved = True
        else:
            booking_id = "N/A (DB offline)"

        # Build WhatsApp message
        formatted_date = datetime.strptime(booking_date, '%Y-%m-%d').strftime('%d %B %Y')
        whatsapp_msg = (
            f"🚜 *New Tractor Booking*\n\n"
            f"👤 *Name:* {name}\n"
            f"📞 *Mobile:* {mobile}\n"
            f"🏘️ *Village:* {village}\n"
            f"⚙️ *Service:* {service}\n"
            f"🌾 *Acres:* {acres}\n"
            f"📅 *Date:* {formatted_date}\n\n"
            f"Please contact the customer to confirm. 🙏"
        )

        import urllib.parse
        whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(whatsapp_msg)}"

        return jsonify({
            'success': True,
            'message': 'Booking saved successfully!',
            'booking_id': booking_id,
            'whatsapp_url': whatsapp_url,
            'db_saved': saved
        })

    except Exception as e:
        print(f"Booking error: {e}")
        return jsonify({'success': False, 'message': 'Server error. Please try again.'}), 500


@app.route('/admin')
def admin():
    """Admin page to view all bookings."""
    bookings = []
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM bookings ORDER BY created_at DESC")
        bookings = cursor.fetchall()
        cursor.close()
        conn.close()
    return render_template('admin.html', bookings=bookings, whatsapp_number=WHATSAPP_NUMBER)


@app.route('/admin/delete/<int:booking_id>', methods=['POST'])
def delete_booking(booking_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('admin'))


@app.route('/admin/complete/<int:booking_id>', methods=['POST'])
def complete_booking(booking_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        # Add a status column if needed; for now just flag in response
        cursor.close()
        conn.close()
    return redirect(url_for('admin'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
