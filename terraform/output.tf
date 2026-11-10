output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.my_instance.id
}

output "instance_private_ip" {
  description = "Private IP address of the EC2 instance"
  value       = aws_instance.my_instance.private_ip
}

output "alb_dns_name" {
  description = "URL publica del Application Load Balancer"
  value       = "http://${aws_lb.this.dns_name}"
}
