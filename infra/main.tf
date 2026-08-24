locals {
  image_name = "ghcr.io/fareed-wq/securepipe-lite:${var.app_version}"
}

resource "docker_image" "securepipe" {
  name         = local.image_name
  keep_locally = true
}

resource "docker_container" "securepipe" {
  name  = "securepipe-tofu"
  image = docker_image.securepipe.image_id

  restart = "unless-stopped"

  env = [
    "APP_ENV=${var.app_environment}"
  ]

  ports {
    internal = 8000
    external = var.host_port
  }
}