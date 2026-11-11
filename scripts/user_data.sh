#!/bin/bash
# 1. Instalar Docker en Amazon Linux 2
if command -v amazon-linux-extras &> /dev/null; then
    sudo amazon-linux-extras install docker -y
else
    sudo yum install -y docker
fi

# 2. Iniciar y habilitar el servicio de Docker
sudo systemctl enable --now docker
sudo usermod -aG docker ec2-user

# 3. Descargar y correr el contenedor Hello World de NGINX en el puerto 80
sudo docker run -d --restart always --name web-demo -p 80:80 nginxdemos/hello
