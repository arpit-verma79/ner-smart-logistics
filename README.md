# NER Logistics Intelligence

Government-style Streamlit portal for smart logistics, accessibility monitoring, weather, route planning, incident reporting, and disruption-risk review across the North Eastern Region.

## Requirements

- Python 3.10 or newer
- Internet access for weather, elevation, and route APIs
- Local branding reference: `public/assets/govt-header-reference.png`

## Windows setup

Open PowerShell in this folder and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py -m streamlit run anti.py
```

Then open `http://localhost:8501`.

## Demo login

- User: `user` / `user2026`
- Admin: `admin` / `admin2026`

Credentials can be overridden with environment variables before launch. Do not use the demo credentials in production.

## Optional weather API key

Set `OPENWEATHER_API_KEY` before starting the app. Without it, the weather panel will show as unavailable while the rest of the dashboard can run.

```powershell
$env:OPENWEATHER_API_KEY = "your-api-key"
```

## Portal workflow

- Field officials can submit state, district, category, description, GPS coordinates, images, and optional supporting documents through the Field Reports tab.
- The SQLite database stores the submitter, state, district, category, coordinates, image/document paths, review status, reviewer, and review time.
- Field submissions start as `Pending`; authorized administrators can search, filter by status/state/district/category, edit, approve, reject, download documents, or delete records from the Admin Operations tab.
- Only approved submissions appear in the public incident archive. Published notices are stored in the `announcements` table and rendered dynamically.
- Administrators can publish portal announcements from the Admin Operations tab. The portal search checks published announcements and field submissions.
- Demo credentials can be overridden before launch with `NER_USER_USERNAME`, `NER_USER_PASSWORD`, `NER_ADMIN_USERNAME`, and `NER_ADMIN_PASSWORD`.

## Portal design

- Premium near-black operations interface with ivory text and restrained saffron, green, and bronze accents.
- Separate Field Official and Administrator login routes with local government branding.
- Responsive government-style header, navigation, latest-updates strip, opening gateway animation, and official-style footer.

For production deployment, replace the demo login with an identity provider or server-side password hashing, add CSRF/session protection, place the database and uploaded files behind a protected service, validate file content and size, and serve the app behind HTTPS with restricted API credentials.
