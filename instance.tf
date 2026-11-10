resource "aws_instance" "my_instance" {
  ami                    = data.aws_ami.amazon-linux-2.image_id
  instance_type          = var.aws_instance_type
  subnet_id              = aws_subnet.public_subnet.id
  vpc_security_group_ids = [aws_security_group.my_sg.id]

  user_data = file("user_data.sh")

  tags = {
    Name     = var.aws_instance_name
    owner    = var.owner
  }
}
