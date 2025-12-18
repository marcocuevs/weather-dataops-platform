# Fase 1: Cimientos de Infraestructura

## 🎯 Objetivo

Preparar el "escenario" donde correrá nuestro código. Esta fase establece la infraestructura base usando principios de Infraestructura como Código (IaC).

## 📊 Estado: 🟡 En Progreso (~30%)

### Completado
- [x] Estructura monorepo creada
- [x] Configuración de Git (.gitignore)
- [x] CI básico con GitHub Actions (Ruff + validación Terraform)

### Pendiente
- [ ] Configuración de Terraform para clúster Kind
- [ ] Despliegue de PostgreSQL en Kubernetes
- [ ] Configuración de gestión de secretos
- [ ] Documentación del entorno de desarrollo local

## 🛠️ Herramientas Utilizadas

| Herramienta | Propósito |
|-------------|-----------|
| **Terraform** | Infraestructura como Código |
| **Kind** | Clúster Kubernetes local |
| **Docker** | Runtime de contenedores |
| **GitHub Actions** | Pipeline CI/CD |

## 📁 Archivos Relevantes

```
weather-dataops-platform/
├── infra/
│   ├── main.tf           # Configuración principal de Terraform
│   └── variables.tf      # Variables de Terraform
├── .github/
│   └── workflows/
│       └── ci.yaml       # Pipeline CI
└── Makefile              # Automatización de tareas
```

## 📝 Pasos de Implementación

### Paso 1: Instalar Prerequisitos

**Windows (con Chocolatey o Scoop)**:
```powershell
# Instalar Docker Desktop
# Descargar de: https://www.docker.com/products/docker-desktop/

# Instalar Terraform
choco install terraform
# o
scoop install terraform

# Instalar Kind
choco install kind
# o
scoop install kind

# Instalar kubectl
choco install kubernetes-cli
# o
scoop install kubectl
```

### Paso 2: Configurar Terraform para Kind

Crear la configuración del clúster Kind en `infra/main.tf`:

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

### Paso 3: Desplegar PostgreSQL

Añadir despliegue de PostgreSQL a Terraform o usar manifiestos de Kubernetes:

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
  # ... spec del deployment
}
```

### Paso 4: Validar Infraestructura

```bash
cd infra
terraform init
terraform plan
terraform apply
```

## ✅ Checklist de Completado

- [ ] Clúster Kind ejecutándose localmente
- [ ] PostgreSQL accesible dentro del clúster
- [ ] kubectl configurado para acceder al clúster
- [ ] Pipeline CI valida Terraform
- [ ] Documentación actualizada

## 🔗 Recursos Relacionados

- [Terraform Kind Provider](https://registry.terraform.io/providers/tehcyx/kind/latest/docs)
- [Documentación de Kind](https://kind.sigs.k8s.io/)
- [PostgreSQL en Kubernetes](https://kubernetes.io/docs/tutorials/stateful-application/basic-stateful-set/)

## ➡️ Siguiente Fase

Una vez la infraestructura esté lista, proceder a [Fase 2: Ingestión](./fase-2-ingestion.md)
