module "networking" {
  source               = "./modules/networking"
  vpc_cidr             = var.vpc_cidr
  vpc_name             = var.vpc_name
  cidr_public_subnet   = var.cidr_public_subnet
  eu_availability_zone = var.eu_availability_zone
}

module "security_group" {
  source              = "./modules/security-groups"
  ec2_sg_name         = "SG for EC2 to enable SSH(22) and HTTP(80)"
  vpc_id              = module.networking.vpc_id
  ec2_jenkins_sg_name = "Allow port 8080 for jenkins"
}

module "jenkins" {
  source                    = "./modules/jenkins"
  ami_id                    = var.ec2_ami_id
  instance_type             = "t3.small"
  tag_name                  = "Vika-Jenkins-Server"
  public_key                = var.public_key
  subnet_id                 = module.networking.public_subnets[0]
  sg_for_jenkins            = [module.security_group.sg_ssh_http_id, module.security_group.sg_jenkins_8080_id]
  enable_public_ip_address  = true
  user_data_install_jenkins = file("./jenkins-installer.sh")
}

module "lb_target_group" {
  source                   = "./modules/lb-target-group"
  lb_target_group_name     = "vika-jenkins-tg"
  lb_target_group_port     = 8080
  lb_target_group_protocol = "HTTP"
  vpc_id                   = module.networking.vpc_id
  ec2_instance_id          = module.jenkins.jenkins_id
}

module "alb" {
  source              = "./modules/alb"
  lb_name             = "vika-jenkins-alb"
  is_external         = true
  lb_type             = "application"
  sg_enable_ssh_https = module.security_group.sg_ssh_http_id
  subnet_ids          = module.networking.public_subnets
  lb_target_group_arn = module.lb_target_group.target_group_arn
  lb_listner_port     = 80
}
