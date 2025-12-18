# =============================================================================
# VARIABLES - Configurable values used in main.tf
# Similar to parameters in a Python function
# You can override these values with a terraform.tfvars file
# =============================================================================

variable "cluster_name" {
  description = "Name of the local Kubernetes cluster"
  type        = string                      # Data type (string, number, bool, list, map)
  default     = "weather-data-cluster"      # Default value if not specified
}

variable "postgres_password" {
  description = "Password for the database"
  type        = string
  default     = "postgres123"               # In production NEVER hardcode passwords
}
