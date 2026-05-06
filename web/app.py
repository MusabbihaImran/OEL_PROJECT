import os
import sys
from unittest.mock import MagicMock

# --- Mock Tkinter for headless execution in Docker ---
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()

# --- Add project root to sys.path to allow importing from tkinter_app ---
# The web app is at /app/web/app.py in docker, or ProjectRoot/web/app.py locally
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# We also need to add tkinter_app to sys.path because some imports in tkinter_app 
# assume `app` is the root package (e.g. `from app.utils.db import get_connection`)
tkinter_app_root = os.path.join(project_root, 'tkinter_app')
if tkinter_app_root not in sys.path:
    sys.path.insert(0, tkinter_app_root)

from flask import Flask, render_template, jsonify

# Now we can safely import models
from app.models.room import RoomModel
from app.models.booking import BookingModel
from app.models.billing_model import BillingModel
from app.models.feedback_model import FeedbackModel

class HotelWebApp:
    def __init__(self):
        self.app = Flask(__name__)
        self._register_routes()

    def _register_routes(self):
        self.app.add_url_rule('/', 'dashboard', self.dashboard)
        self.app.add_url_rule('/rooms', 'rooms', self.rooms)
        self.app.add_url_rule('/bookings', 'bookings', self.bookings)
        self.app.add_url_rule('/billing', 'billing', self.billing)
        self.app.add_url_rule('/feedback', 'feedback', self.feedback)
        self.app.add_url_rule('/health', 'health', self.health)

    def dashboard(self):
        rooms = RoomModel.get_all_rooms()
        bookings = BookingModel.get_all_bookings()
        bills = BillingModel.get_all_bills()

        total_rooms = len(rooms)
        available_rooms = sum(1 for r in rooms if r['status'] == 'available')
        total_bookings = len(bookings)
        pending_payments = sum(1 for b in bills if b['payment_status'] == 'pending')

        return render_template('dashboard.html', 
                               total_rooms=total_rooms,
                               available_rooms=available_rooms,
                               total_bookings=total_bookings,
                               pending_payments=pending_payments)

    def rooms(self):
        rooms = RoomModel.get_all_rooms()
        return render_template('rooms.html', rooms=rooms)

    def bookings(self):
        bookings = BookingModel.get_all_bookings()
        return render_template('bookings.html', bookings=bookings)

    def billing(self):
        bills = BillingModel.get_all_bills()
        return render_template('billing.html', bills=bills)

    def feedback(self):
        feedbacks = FeedbackModel.get_all_feedback()
        return render_template('feedback.html', feedbacks=feedbacks)

    def health(self):
        return jsonify({"status": "healthy", "app": "Hotel Booking System"})

if __name__ == '__main__':
    hotel_web = HotelWebApp()
    hotel_web.app.run(host='0.0.0.0', port=5000, debug=True)
