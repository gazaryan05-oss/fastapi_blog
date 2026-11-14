resource "aws_lb" "main" {
  name               = var.lb_name
  internal           = var.is_external
  load_balancer_type = var.lb_type
  security_groups    = [var.sg_enable_ssh_https]
  subnets            = var.subnet_ids
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = var.lb_listner_port
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = var.lb_target_group_arn
  }
}
