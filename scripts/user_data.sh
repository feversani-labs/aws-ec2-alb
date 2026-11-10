#!/bin/bash
sudo yum update -y

# Instalar y arrancar Docker
sudo yum install docker -y
sudo systemctl enable docker
sudo systemctl start docker

# Agregar el usuario ec2-user al grupo docker
sudo usermod -aG docker ec2-user

# Correr el contenedor Hello World de Nginx en el puerto 80
sudo docker run -d --restart always --name web-demo -p 80:80 nginxdemos/hello
