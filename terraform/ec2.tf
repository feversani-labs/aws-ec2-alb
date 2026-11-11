resource "aws_instance" "my_instance" {
  ami                    = data.aws_ami.amazon-linux-2.image_id
  instance_type          = var.aws_instance_type
  subnet_id              = aws_subnet.private_subnet_0.id
  vpc_security_group_ids = [aws_security_group.ec2.id]

  user_data                   = file("${path.module}/../scripts/user_data.sh")
  user_data_replace_on_change = true

  iam_instance_profile = aws_iam_instance_profile.my_instance_profile.name

  metadata_options {
    http_tokens                 = "required"
    http_endpoint               = "enabled"
    http_put_response_hop_limit = 2
  }

  tags = {
    Name  = var.aws_instance_name
    owner = var.owner
  }
}
