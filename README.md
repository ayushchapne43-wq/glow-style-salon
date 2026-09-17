# Glow & Style Salon

A static salon website with a small Python backend for appointment requests.

## Run locally

Requires Python 3.10 or newer.

```powershell
py python.py
```

While the server is running, open `http://127.0.0.1:8000` in your browser. This is a local-only address, so it works on your computer but not from the GitHub README. Booking requests are validated and stored locally in `data/appointments.json` (the file is ignored by Git).

## API

`POST /api/appointments` accepts JSON with `name`, `phone`, `service`, `date`, and an optional `message`. The same endpoint powers the booking form in the browser.
