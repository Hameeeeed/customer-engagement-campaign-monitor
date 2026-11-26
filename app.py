"""
Customer Engagement Campaign Monitoring System
A Flask REST API that simulates campaign delivery monitoring.
Database: SQLite
"""

import logging
import sqlite3
from contextlib import contextmanager
from pathlib import Path

from flask import Flask, jsonify

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "campaign_monitor.db"
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "application.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True,
)
logger = logging.getLogger("CampaignMonitor")
app = Flask(__name__)

SAMPLE_CAMPAIGNS = [
    (101, "C101", "Rahul", "Email", "Welcome Campaign", "Delivered", None),
    (102, "C102", "Amit", "Push", "Offer Campaign", "Failed", "Device token invalid"),
    (103, "C103", "Priya", "SMS", "Reminder Campaign", "Delivered", None),
    (104, "C104", "Neha", "Email", "Welcome Campaign", "Failed", "Invalid email address"),
    (105, "C105", "Arjun", "Push", "Offer Campaign", "Delivered", None),
    (106, "C106", "Sara", "SMS", "Reminder Campaign", "Failed", "Network timeout"),
    (107, "C107", "Karan", "Email", "Offer Campaign", "Delivered", None),
    (108, "C108", "Ananya", "Push", "Welcome Campaign", "Failed", "Device token expired"),
]


@contextmanager
def get_db_connection():
    """Open a SQLite connection and always close it after use."""
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    finally:
        connection.close()


def initialize_database():
    """Create the table and insert sample records only when it is empty."""
    with get_db_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS campaigns (
                campaign_id INTEGER PRIMARY KEY,
                customer_id TEXT NOT NULL,
                customer_name TEXT NOT NULL,
                channel TEXT NOT NULL,
                campaign_name TEXT NOT NULL,
                delivery_status TEXT NOT NULL,
                error_reason TEXT
            )
            """
        )

        count = connection.execute(
            "SELECT COUNT(*) FROM campaigns"
        ).fetchone()[0]

        if count == 0:
            connection.executemany(
                """
                INSERT INTO campaigns
                (campaign_id, customer_id, customer_name, channel,
                 campaign_name, delivery_status, error_reason)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                SAMPLE_CAMPAIGNS,
            )
            connection.commit()

        failed_rows = connection.execute(
            """
            SELECT campaign_id, channel, error_reason
            FROM campaigns
            WHERE delivery_status = 'Failed'
            ORDER BY campaign_id
            """
        ).fetchall()

    logger.info("Campaign Monitoring Application initialized.")
    logger.info("SQLite database ready: %s", DATABASE)

    for row in failed_rows:
        logger.warning(
            "Campaign failure - ID: %s | Channel: %s | Reason: %s",
            row["campaign_id"],
            row["channel"],
            row["error_reason"],
        )


@app.route("/", methods=["GET"])
def home():
    """API health check."""
    return jsonify({
        "message": "Customer Engagement Campaign Monitoring API",
        "status": "Running",
    })


@app.route("/campaigns", methods=["GET"])
def get_campaigns():
    """Return all campaign records."""
    with get_db_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM campaigns ORDER BY campaign_id"
        ).fetchall()
    return jsonify([dict(row) for row in rows])


@app.route("/campaigns/<int:campaign_id>", methods=["GET"])
def get_campaign(campaign_id):
    """Return one campaign; reject zero and report missing IDs."""
    if campaign_id <= 0:
        return jsonify({"error": "Campaign ID must be positive"}), 400

    with get_db_connection() as connection:
        row = connection.execute(
            "SELECT * FROM campaigns WHERE campaign_id = ?",
            (campaign_id,),
        ).fetchone()

    if row is None:
        return jsonify({"error": "Campaign not found"}), 404
    return jsonify(dict(row))


@app.route("/campaigns/failed", methods=["GET"])
def get_failed_campaigns():
    """Return failed campaign records."""
    with get_db_connection() as connection:
        rows = connection.execute(
            """
            SELECT * FROM campaigns
            WHERE delivery_status = 'Failed'
            ORDER BY campaign_id
            """
        ).fetchall()
    return jsonify([dict(row) for row in rows])


@app.route("/reports/summary", methods=["GET"])
def campaign_summary():
    """Return overall delivery counts and success rate."""
    with get_db_connection() as connection:
        row = connection.execute(
            """
            SELECT
                COUNT(*) AS total,
                SUM(CASE WHEN delivery_status = 'Delivered'
                    THEN 1 ELSE 0 END) AS delivered,
                SUM(CASE WHEN delivery_status = 'Failed'
                    THEN 1 ELSE 0 END) AS failed
            FROM campaigns
            """
        ).fetchone()

    total = row["total"] or 0
    delivered = row["delivered"] or 0
    failed = row["failed"] or 0
    success_rate = (delivered / total * 100) if total else 0

    return jsonify({
        "total_campaigns": total,
        "delivered": delivered,
        "failed": failed,
        "success_rate": round(success_rate, 2),
    })


@app.route("/reports/channel", methods=["GET"])
def channel_report():
    """Return campaign counts grouped by channel."""
    with get_db_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                channel,
                COUNT(*) AS total,
                SUM(CASE WHEN delivery_status = 'Delivered'
                    THEN 1 ELSE 0 END) AS delivered,
                SUM(CASE WHEN delivery_status = 'Failed'
                    THEN 1 ELSE 0 END) AS failed
            FROM campaigns
            GROUP BY channel
            ORDER BY channel
            """
        ).fetchall()
    return jsonify([dict(row) for row in rows])


if __name__ == "__main__":
    initialize_database()
    print("Database initialized. Starting Flask development server...")
    print("API base URL: http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
