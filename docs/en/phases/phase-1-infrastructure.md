# Phase 1: Infrastructure Foundation

## 🎯 Objective

Prepare the "stage" where our code will run. This phase establishes the foundational infrastructure using Infrastructure as Code (IaC) principles.

## 📊 Status: 🟡 In Progress (~30%)

### Completed
- [x] Monorepo structure created
- [x] Git configuration (.gitignore)
- [x] Basic CI with GitHub Actions (Ruff + Terraform validation)

### Pending
- [ ] Terraform configuration for Kind cluster
- [ ] PostgreSQL deployment in Kubernetes
- [ ] Secrets management setup
- [ ] Local development environment documentation

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| **Terraform** | Infrastructure as Code |
| **Kind** | Local Kubernetes cluster |
| **Docker** | Container runtime |
| **GitHub Actions** | CI/CD pipeline |

## 📁 Relevant Files

```
weather-dataops-platform/
├── infra/
│   ├── main.tf           # Main Terraform configuration
│   └── variables.tf      # Terraform variables
├── .github/
│   └── workflows/
│       └── ci.yaml       # CI pipeline
└── Makefile              # Task automation
```

## 📝 Implementation Steps

### Step 1: Install Prerequisites

**Windows (with Chocolatey or Scoop)**:
```powershell
# Install Docker Desktop
# Download from: https://www.docker.com/products/docker-desktop/

# Install Terraform
choco install terraform
# or
scoop install terraform

# Install Kind
choco install kind
# or
scoop install kind

# Install kubectl
choco install kubernetes-cli
# or
scoop install kubectl
```

### Step 2: Configure Terraform for Kind

Create the Kind cluster configuration in `infra/main.tf`:

```hcl
terraform {
  required_providers {
    kind = {
      source  = "tehcyx/kind"
      version = "~> 0.2"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
  }
}

provider "kind" {}

resource "kind_cluster" "weather_platform" {
  name           = "weather-dataops"
  wait_for_ready = true

  kind_config {
    kind        = "Cluster"
    api_version = "kind.x-k8s.io/v1alpha4"

    node {
      role = "control-plane"
      extra_port_mappings {
        container_port = 30000
        host_port      = 30000
      }
    }
  }
}
```

### Step 3: Deploy PostgreSQL

Add PostgreSQL deployment to Terraform or use Kubernetes manifests:

```hcl
resource "kubernetes_namespace" "database" {
  metadata {
    name = "database"
  }
}

resource "kubernetes_deployment" "postgres" {
  metadata {
    name      = "postgres"
    namespace = kubernetes_namespace.database.metadata[0].name
  }
  # ... deployment spec
}
```

### Step 4: Validate Infrastructure

```bash
cd infra
terraform init
terraform plan
terraform apply
```

## ✅ Completion Checklist

- [ ] Kind cluster running locally
- [ ] PostgreSQL accessible within cluster
- [ ] kubectl configured to access cluster
- [ ] CI pipeline validates Terraform
- [ ] Documentation updated

## 🔗 Related Resources

- [Terraform Kind Provider](https://registry.terraform.io/providers/tehcyx/kind/latest/docs)
- [Kind Documentation](https://kind.sigs.k8s.io/)
- [PostgreSQL on Kubernetes](https://kubernetes.io/docs/tutorials/stateful-application/basic-stateful-set/)

## ➡️ Next Phase

Once infrastructure is ready, proceed to [Phase 2: Ingestion](./phase-2-ingestion.md)
