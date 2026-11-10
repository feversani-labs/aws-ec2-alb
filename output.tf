output "public_ip" {
  value       = aws_instance.my_instance.public_ip
  description = "IP Public of the instances"
}
