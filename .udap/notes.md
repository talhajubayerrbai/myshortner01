# myshortner01 — Working Notes

## Project Summary
URL shortener, Python/FastAPI + SQLAlchemy + Alembic, RDS Postgres 15, EC2 t3.micro Ubuntu 22.04, Gunicorn+Nginx, Ansible configure, us-east-1.

## Decisions
- FastAPI (not in scaffold catalog — files written manually)
- No tests (user explicitly opted out)
- Default VPC used (3 existing VPCs; default has 6 subnets, cleanest for Tier 1)
- RDS db.t3.micro single-AZ, skip_final_snapshot=true, deletion_protection=false (Tier 1)
- EC2 t3.micro Ubuntu 22.04 (ubuntu SSH user, apt)
- Gunicorn + UvicornWorker as systemd service, Nginx as reverse proxy
- SSH key injected via SSH_PUBLIC_KEY / SSH_PRIVATE_KEY secrets (platform standard)
- DB_PASSWORD set as pipeline secret before deploy
- Alembic migration runs in configure stage before service start
- Base URL derived from EC2 public IP at configure time (no custom domain, Tier 1)

## Status
- [x] Plan approved
- [x] Architecture written
- [x] Pipeline written (v2 — corrected TF backend init args + SSH key handling)
- [x] App code generated (app/, alembic/, requirements.txt)
- [x] Terraform written (infra/)
- [x] Ansible written (ansible/)
- [x] README written
- [ ] validate_project
- [ ] Repo created
- [ ] Secrets set
- [ ] Deployed

## Known Gotchas
- RDS takes 5-10 min to provision — Terraform apply will be slow on first run
- ansible inventory.ini uses `{{ ec2_public_ip }}` placeholder; pipeline does a sed replace before ansible-playbook
- APP_HOST in verify stage uses EC2_PUBLIC_IP env var exported from TF outputs
- Terraform backend bucket literal "TF_STATE_BUCKET" in main.tf — platform patches this at deploy time via -backend-config in the pipeline
