resource "aws_lb_target_group" "main" {
  name     = var.lb_target_group_name
  port     = var.lb_target_group_port
  protocol = var.lb_target_group_protocol
  vpc_id   = var.vpc_id

  health_check {
    path    = "/login"
    port    = "8080"
    matcher = "200"
  }
}

resource "aws_lb_target_group_attachment" "main" {
  target_group_arn = aws_lb_target_group.main.arn
  target_id        = var.ec2_instance_id
  port             = 8080
}
