# AttendAI

AttendAI is a production-oriented college attendance platform combining face recognition, practical liveness checks, campus geofencing, network and timetable policy, JWT access control, live activity, analytics, student administration, security alerts, and report export.

## Architecture

- **Web:** React/TanStack Start, TypeScript, Chart.js, React Webcam, responsive CSS
- **API:** typed Netlify Functions under `/api/*`, JWT access/refresh rotation, bcrypt account protection
- **Data:** Netlify Database (managed Postgres) with Drizzle ORM and deploy-time migrations
- **Vision:** Flask, OpenCV, `face_recognition`/dlib, NumPy and SciPy; persistent numerical encodings
- **Operations:** Netlify deployment plus Docker Compose for the web/database/AI stack

The requested MongoDB-shaped domain is represented relationally for Netlify Database. Students, attendance, users, alerts, and pending verifications retain the requested concepts and history-safe soft deletion.

## Local setup

Prerequisites: Node 22+, pnpm, Python 3.9–3.11, a C++ toolchain/CMake for dlib, and Netlify CLI.

```bash
cp .env.example .env
pnpm install
python -m venv ai-module/venv
source ai-module/venv/bin/activate
pip install -r ai-module/requirements.txt
python ai-module/app.py
netlify dev --port 8889
```

On Windows use `ai-module\venv\Scripts\activate`. Netlify Database is provisioned on first connection and applies `netlify/database/migrations` automatically. Configure strong JWT secrets, campus coordinates, allowed networks, sessions, and the Flask URL in Netlify. Empty `ALLOWED_WIFI_IPS` disables network enforcement.

## AI, Docker, and access

Enrollment accepts 5–10 images, requires exactly one face per accepted image, removes encoding outliers, and persists the aggregate encoding. Recognition combines face distance with texture, Laplacian sharpness, face size, and landmark geometry. These are practical basic anti-spoofing checks; high-risk installations should add depth/IR hardware.

Run the self-hosted stack with `docker compose up --build`. It exposes web `3000`, Flask `5001`, and Postgres `5432`. Netlify production uses managed Postgres.

The development bootstrap is `admin` / `Admin@123`. It is created lazily only with `ALLOW_DEFAULT_ADMIN=true`; set `DEFAULT_ADMIN_PASSWORD` and disable bootstrap after provisioning production.

## Workflow

Create a student, open **Face**, capture five or more angles, then open `/kiosk`. The browser sends a frame and coordinates. The API verifies campus, network, and session rules; Flask derives identity from liveness-tested face encoding; the API validates the active student and writes attendance. Identity is never accepted from the client. Records, analytics, alerts, and CSV/XLSX export appear in the staff workspace.

## API

- Auth: `/api/auth/login|register|refresh|logout|me`
- Students: `/api/students`, `/api/students/:id`, `/api/students/:id/register-face`
- Attendance: `/api/attendance/mark|exit|manual`, `/api/attendance`, `/api/attendance/today`
- Alerts: `/api/attendance/alerts`, `/api/attendance/alerts/:id/resolve`
- Analytics: `/api/dashboard/summary|attendance-trend|department-stats|low-attendance|recent-activity`
- Session: `/api/session/status|live-feed|verify-random`
- Export: `/api/export/attendance?format=xlsx|csv`
- AI: `/train`, `/recognize`, `/delete-encoding/:id`, `/health`, `/stats`

## Verification and troubleshooting

Test login lockout and refresh, roles, soft deletion, multi-angle enrollment, no/multiple-face rejection, unknown/liveness alerts, geofence and network rejection, session timing, duplicate check-in, checkout duration, verification mismatch, analytics, alert resolution, and both exports. Camera and location require HTTPS outside localhost. For dlib failures install CMake, a compiler, BLAS/LAPACK and Python headers. For scan failures check Flask `/health`, `FLASK_URL`, encoding volume permissions, UTC sessions, coordinates, proxy client IP, and browser permissions.
