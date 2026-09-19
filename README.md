# NER Logistics Intelligence

A government-style logistics and field operations portal for the North Eastern Region, built with Streamlit. The application combines official branding, weather intelligence, route-awareness, incident reporting, and admin review workflows in a single dark premium dashboard.

## Overview

This project is designed for:

- Field officials to log operational issues, incidents, and accessibility updates
- Administrators to review submissions, publish updates, and approve or reject reports
- Public-facing information access through a clean government portal experience
- Local, secure-first usage with SQLite-backed data handling and project-based branding assets

## Features

- Secure login with separate Field Official and Administrator roles
- Field report submission with district, state, category, GPS information, notes, image uploads, and document attachments
- Review workflow with pending, approved, rejected, and archived states
- Admin operations for filtering, searching, editing, downloading, and deleting records
- Public announcement feed and search-through-portal experience
- Dark premium government interface with official-style colour palette and branding
- Weather-ready dashboard with optional API support
- Local static assets for ministry and portal branding

## Tech stack

- Python 3.10+
- Streamlit
- SQLite
- Pandas, NumPy
- scikit-learn
- XGBoost
- Folium and streamlit-folium
- Requests

## Project structure

```text
NER_Logistics_Intelligence/
├── anti.py                  # Main Streamlit application
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
├── public/
│   └── assets/
│       ├── govt-header-reference.png
│       ├── ministry-of-education.png
│       ├── ner-smart-logistics-icon.png
│       └── ...
├── field_report_images/     # Uploaded field evidence images
├── data/                    # Optional local database or supporting files
└── .venv/                   # Virtual environment (when created locally)
```

## Requirements

- Python 3.10 or newer
- Internet access for weather, route, and map-related integrations
- A local environment with access to the project assets in `public/assets`

## Quick start

### Windows

Open PowerShell in the project folder and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py -m streamlit run anti.py
```

Then open the app in the browser at:

```text
http://localhost:8501
```

> Important: launch the app with `py -m streamlit run anti.py` rather than running the file directly with Python in bare mode.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run anti.py
```

## Demo credentials

The application ships with the following demo accounts:

- Field Official
  - Username: `user`
  - Password: `user2026`

- Administrator
  - Username: `admin`
  - Password: `admin2026`

These values can be overridden using environment variables before launch:

```powershell
$env:NER_USER_USERNAME = "user"
$env:NER_USER_PASSWORD = "user2026"
$env:NER_ADMIN_USERNAME = "admin"
$env:NER_ADMIN_PASSWORD = "admin2026"
```

## Optional configuration

### Weather API

The app can use an OpenWeather API key for weather intelligence. Without it, the weather section may display as unavailable while the rest of the dashboard remains functional.

```powershell
$env:OPENWEATHER_API_KEY = "your-api-key"
```

## Application workflow

1. A field official logs in and submits a report.
2. The report is stored in the SQLite database with metadata such as state, district, category, coordinates, and file references.
3. The admin dashboard reviews all incoming submissions.
4. Admins can approve, reject, edit, filter, or delete the report records.
5. Approved records appear in the public-facing operational information layer.
6. Announcements and updates can be published from the admin side and displayed dynamically in the portal.

## Admin and operations notes

- Submissions start in a pending state.
- Only approved records are treated as public-facing operational content.
- Admin searches can filter by status, state, district, and category.
- Uploaded documents and media are stored locally as part of the project workflow.
- Local branding files in `public/assets` are used to keep the portal aligned with the official government-style look.

## Security and deployment guidance

This project is intended for local or controlled environment use. For production deployment, it is recommended to:

- replace demo credentials with a proper identity provider
- hash passwords server-side instead of relying on stored plaintext demo values
- restrict database and upload access behind protected infrastructure
- validate uploaded file types and sizes
- enable HTTPS and secure session management
- use environment-based secrets for API credentials and admin configuration

## Notes

- The app is intended to run through the Streamlit launcher using `py -m streamlit run anti.py`.
- The portal styling emphasizes a premium near-black operational palette with restrained saffron, green, and bronze highlights.
- The project uses local government-branding assets rather than external image URLs so it remains portable and consistent.

## License and usage

This project is intended for internal demonstration, operations support, and regional logistics intelligence workflows. Please ensure that any deployment follows the relevant institutional, data, and security policies for your environment.
