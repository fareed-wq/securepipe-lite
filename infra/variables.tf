variable "app_version" {
  description = "SecurePipe Lite container version to deploy"
  type        = string
  default     = "v1.1.0"
}

variable "app_environment" {
  description = "Application runtime environment"
  type        = string
  default     = "production"
}

variable "host_port" {
  description = "Host port exposed for SecurePipe Lite"
  type        = number
  default     = 8000
}