resource "aws_key_pair" "jenkins_key" {
  key_name   = "vika-terraform-key"
  public_key = var.public_key
}

resource "aws_instance" "jenkins_server" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = var.sg_for_jenkins
  key_name                    = aws_key_pair.jenkins_key.key_name
  associate_public_ip_address = var.enable_public_ip_address
  user_data                   = var.user_data_install_jenkins
  tags                        = { Name = var.tag_name }
}
