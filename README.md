# myshortner01 — URL Shortener

A fast, lightweight URL shortener built with **FastAPI** + **PostgreSQL** (AWS RDS), deployed on **AWS EC2** via Gunicorn + Nginx.

---

## API Reference

All requests/responses are JSON. Base URL: `http://<your-ec2-ip>`

### Health

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness + DB probe |

```json
// GET /health
{ "status": "ok", "db": "ok" }
```

---

### Shorten a URL

**POST** `/shorten`

```json
// Request body
{
  "url": "https://www.example.com/some/very/long/path?with=params",
  "custom_code": "mycode"   // optional — omit for a random 7-char code
}
```

```json
// 201 Created
{
  "short_code": "mycode",
  "short_url": "http://<host>/mycode",
  "original_url": "https://www.example.com/some/very/long/path?with=params",
  "created_at": "2024-01-01T12:00:00"
}
```

Error codes:
- `409 Conflict` — custom code already taken
- `422 Unprocessable Entity` — invalid URL

---

### Redirect

**GET** `/{code}`

Performs a **301 redirect** to the original URL and increments the click counter.

---

### Stats

**GET** `/{code}/stats`

```json
// 200 OK
{
  "short_code": "mycode",
  "original_url": "https://www.example.com/...",
  "click_count": 42,
  "created_at": "2024-01-01T12:00:00",
  "updated_at": "2024-01-01T13:00:00"
}
```

Error codes:
- `404 Not Found` — code doesn't exist

---

## Local Development

```bash
# 1. Start a local Postgres instance
docker run -d \
  -e POSTGRES_USER=shortener \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=shortener \
  -p 5432:5432 postgres:15

# 2. Set environment variables
export DB_HOST=localhost
export DB_PASSWORD=secret
export BASE_URL=http://localhost:8000

# 3. Install dependencies
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 4. Run migrations
alembic upgrade head

# 5. Start the server
uvicorn app.main:app --reload
```

API docs available at: `http://localhost:8000/docs`

---

## Architecture

- **App server**: EC2 t3.micro (Ubuntu 22.04), Gunicorn + UvicornWorker, Nginx reverse proxy on port 80
- **Database**: RDS Postgres 15 (db.t3.micro, single-AZ), accessible only from the EC2 security group
- **CI/CD**: GitHub Actions → Terraform (provision) → Ansible (configure) → health-check (verify)
- **Migrations**: Alembic, run during the configure stage before the service starts

---

## Optional Enhancements (not included)

- HTTPS via ACM + ALB
- RDS Multi-AZ + automated backups
- CloudWatch alarms and log shipping
- Auto Scaling Group behind ALB
- ElastiCache Redis for hot-URL caching
- CloudFront CDN
