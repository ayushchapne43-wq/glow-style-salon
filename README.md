# Glow & Style Salon

A static salon website with a small Python backend for appointment requests.

## Run locally

Requires Python 3.10 or newer.

```powershell
py python.py
```

While the server is running, open `http://127.0.0.1:8000` in your browser. This is a local-only address, so it works on your computer but not from the GitHub README. Booking requests are validated and stored locally in `data/appointments.json` (the file is ignored by Git).

## Deploy publicly

GitHub stores the source code, but it does not run the Python backend. To publish the working full-stack site, create a free Web Service on [Render](https://render.com), connect this GitHub repository, and use the included `render.yaml` configuration. Render will provide a public `onrender.com` URL that you can share in your portfolio.

The appointment demo stores requests in a local JSON file. This is suitable for a portfolio demonstration; use a hosted database before using it for real customers.

## API

`POST /api/appointments` accepts JSON with `name`, `phone`, `service`, `date`, and an optional `message`. The same endpoint powers the booking form in the browser.
