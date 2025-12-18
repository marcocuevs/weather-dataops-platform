# =============================================================================
# PROVIDERS - "Connectors" that allow Terraform to talk to different platforms
# Similar to importing libraries in Python to connect to different sources
# =============================================================================
terraform {
  required_providers {
    # Provider to create local Kubernetes clusters with Kind
    # Kind = "Kubernetes IN Docker" - like having AKS on your PC
    kind = {
      source  = "tehcyx/kind"
      version = "0.2.1"
    }
    # Provider to create resources INSIDE the cluster (pods, deployments, etc.)
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "2.23.0"
    }
  }
}

provider "kind" {}

# =============================================================================
# RESOURCE 1: Local Kubernetes Cluster
# This creates a complete Kubernetes inside Docker on your PC
# Azure equivalent: Like creating an AKS but free and local
# =============================================================================
resource "kind_cluster" "weather_platform" {
  name           = var.cluster_name        # Cluster name (comes from variables.tf)
  node_image     = "kindest/node:v1.27.3"  # Kubernetes version to use
  wait_for_ready = true                    # Wait until ready before continuing

  kind_config {
    kind        = "Cluster"
    api_version = "kind.x-k8s.io/v1alpha4"

    node {
      role = "control-plane"  # This node will be the cluster's "brain"

      # IMPORTANT: Port mapping
      # Exposes port 30001 from the cluster to port 5432 on Windows
      # This way you can connect to Postgres from your PC as localhost:5432
      extra_port_mappings {
        container_port = 30001  # Port inside the cluster
        host_port      = 5432   # Port on your Windows
      }
    }
  }
}

# =============================================================================
# RESOURCE 2: PostgreSQL Deployment
# A Deployment says "I want X replicas of this container always running"
# Azure equivalent: Like an Azure SQL Database but in a container
# =============================================================================
resource "kubernetes_deployment" "postgres" {
  # Don't create this until the cluster exists
  depends_on = [kind_cluster.weather_platform]

  metadata {
    name = "postgres-db"  # Deployment name in Kubernetes
  }

  spec {
    replicas = 1  # Only 1 Postgres instance (fine for dev)

    # Selector: how Kubernetes identifies which pods belong to this deployment
    # It's like a "tag" to group resources
    selector {
      match_labels = {
        app = "postgres"
      }
    }

    # Template: defines what each pod (container) will look like
    template {
      metadata {
        labels = {
          app = "postgres"  # Must match the selector above
        }
      }

      spec {
        container {
          name  = "postgres"
          image = "postgres:15"  # Official image from Docker Hub

          # Environment variables (like App Settings in Azure Functions)
          env {
            name  = "POSTGRES_PASSWORD"
            value = var.postgres_password  # Comes from variables.tf
          }

          # Port exposed by the container
          port {
            container_port = 5432
          }
        }
      }
    }
  }
}
