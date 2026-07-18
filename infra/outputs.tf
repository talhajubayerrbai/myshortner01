output "ec2_public_ip" {
  description = "Public IP of the app EC2 instance."
  value       = aws_instance.app.public_ip
}

output "rds_endpoint" {
  description = "RDS Postgres endpoint (host:port)."
  value       = aws_db_instance.postgres.endpoint
}

output "rds_host" {
  description = "RDS Postgres hostname."
  value       = aws_db_instance.postgres.address
}
