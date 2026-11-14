output "sg_ssh_http_id" { value = aws_security_group.ec2_sg_ssh_http.id }
output "sg_jenkins_8080_id" { value = aws_security_group.ec2_jenkins_port_8080.id }
