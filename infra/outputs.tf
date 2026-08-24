output "container_name" {
  description = "Name of the deployed SecurePipe Lite container"
  value       = docker_container.securepipe.name
}

output "image" {
  description = "SecurePipe Lite image being deployed"
  value       = local.image_name
}

output "application_url" {
  description = "Local SecurePipe Lite URL"
  value       = "http://127.0.0.1:${var.host_port}"
}