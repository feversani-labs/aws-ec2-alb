resource "aws_instance" "my_instance" {
  ami                    = data.aws_ami.amazon-linux-2.image_id
  instance_type          = var.aws_instance_type
  subnet_id              = aws_subnet.private_subnet.id
  vpc_security_group_ids = [aws_security_group.my_sg.id]

  user_data = file("${path.module}/../scripts/user_data.sh")

  iam_instance_profile = aws_iam_instance_profile.my_instance_profile.name

  tags = {
    Name     = var.aws_instance_name
    owner    = var.owner
  }
}
