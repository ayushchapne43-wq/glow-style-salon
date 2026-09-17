import json
import os
import re
from datetime import date
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).parent.resolve()
DATA_FILE = ROOT / "data" / "appointments.json"
ALLOWED_SERVICES = {
    "Hair styling",
    "Haircut & grooming",
    "Hair colour",
    "Nail care",
    "Facial & skincare",
    "Bridal services",
}


def read_appointments():
    DATA_FILE.parent.mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def save_appointment(appointment):
    appointments = read_appointments()
    appointments.append(appointment)
    DATA_FILE.write_text(json.dumps(appointments, indent=2), encoding="utf-8")


def validate_appointment(payload):
    if not isinstance(payload, dict):
        return "Please send a valid appointment request."

    name = str(payload.get("name", "")).strip()
    phone = str(payload.get("phone", "")).strip()
    service = str(payload.get("service", "")).strip()
    preferred_date = str(payload.get("date", "")).strip()

    if not name or len(name) > 100:
        return "Please enter your name."
    if not re.fullmatch(r"[+()\d\s.-]{7,30}", phone):
        return "Please enter a valid phone number."
    if service not in ALLOWED_SERVICES:
        return "Please choose a service from the menu."
    try:
        requested_date = date.fromisoformat(preferred_date)
    except ValueError:
        return "Please choose a valid appointment date."
    if requested_date < date.today():
        return "Please choose a date from today onward."

    return None


class SalonRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        if urlparse(self.path).path == "/health":
            self.send_json({"status": "ok"}, HTTPStatus.OK)
            return
        super().do_GET()

    def do_POST(self):
        if urlparse(self.path).path != "/api/appointments":
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        content_length = int(self.headers.get("Content-Length", 0))
        if content_length > 10_000:
            self.send_json({"error": "Request is too large."}, HTTPStatus.REQUEST_ENTITY_TOO_LARGE)
            return

        try:
            payload = json.loads(self.rfile.read(content_length))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self.send_json({"error": "Please send valid JSON."}, HTTPStatus.BAD_REQUEST)
            return

        error = validate_appointment(payload)
        if error:
            self.send_json({"error": error}, HTTPStatus.BAD_REQUEST)
            return

        appointment = {
            "name": payload["name"].strip(),
            "phone": payload["phone"].strip(),
            "service": payload["service"].strip(),
            "date": payload["date"].strip(),
            "message": str(payload.get("message", "")).strip()[:1000],
        }
        save_appointment(appointment)
        self.send_json(
            {"message": f"Thanks, {appointment['name'].split()[0]}! Your request has been received."},
            HTTPStatus.CREATED,
        )

    def send_json(self, payload, status):
        response = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    os.chdir(ROOT)
    server = ThreadingHTTPServer(("0.0.0.0", port), SalonRequestHandler)
    print(f"Glow & Style is running on port {port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()