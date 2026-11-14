output "jenkins_public_ip" {
  description = "Public IP of the Jenkins server"
  value       = module.jenkins.jenkins_public_ip
}

output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  value       = module.alb.alb_dns_name
}
