group "default" {
  targets = ["api","web"]
}

target "api" {
  dockerfile = "docker/Dockerfile"
  context = "backend"
  target = "prod"
  tags = ["docker.io/bierik/timeline-api:latest"]
}

target "web" {
  dockerfile = "docker/Dockerfile"
  context = "frontend"
  target = "prod"
  tags = ["docker.io/bierik/timeline-web:latest"]
}
