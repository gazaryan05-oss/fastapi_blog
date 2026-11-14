#!/bin/bash
# Установка Java и Jenkins
sudo apt-get update -y
sudo apt-get install -y openjdk-11-jdk-headless wget net-tools docker.io

# Включаем Docker
sudo systemctl start docker
sudo systemctl enable docker

# Установка Jenkins (напрямую через .deb, чтобы избежать ошибок с ключами)
wget https://get.jenkins.io/debian-stable/jenkins_2.452.1_all.deb
sudo dpkg -i jenkins_2.452.1_all.deb
sudo apt-get install -f -y
sudo systemctl start jenkins
sudo systemctl enable jenkins

# Даем Дженкинсу права на Docker
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins