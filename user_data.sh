#!/bin/bash
sudo yum update -y
sudo amazon-linux-extras install nginx1 -y  
sudo systemctl enable nginx
sudo systemctl start nginx

sudo yum install docker -y
sudo systemctl enable docker
sudo systemctl start docker