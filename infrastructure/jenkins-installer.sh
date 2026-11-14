# Установка Docker для сборки образов
sudo apt-get update -y
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
# Даем Дженкинсу права на использование Docker
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins