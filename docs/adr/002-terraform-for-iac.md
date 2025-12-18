# ADR-002: Terraform for Infrastructure as Code

## Status
Accepted

## Date
2024-12-18

## Context
We need to provision and manage infrastructure for our data platform, including a local Kubernetes cluster (Kind) and PostgreSQL database. We need a tool that:
- Is declarative and version-controlled
- Supports local development environments
- Is widely used in the industry (good for learning)
- Can scale to cloud providers in the future

## Decision
We will use **Terraform** as our Infrastructure as Code (IaC) tool.

Key providers:
- `tehcyx/kind` - For local Kubernetes cluster
- `hashicorp/kubernetes` - For K8s resources
- `hashicorp/helm` - For Helm chart deployments

## Consequences

### Positive
- **Industry standard**: Most requested IaC skill in job market
- **Cloud agnostic**: Same tool works for AWS, GCP, Azure
- **Declarative**: Define desired state, Terraform handles the rest
- **State management**: Tracks what's deployed
- **Large ecosystem**: Many providers and modules available
- **Good documentation**: Extensive learning resources

### Negative
- **Learning curve**: HCL syntax takes time to learn
- **State file management**: Need to handle state carefully
- **Provider limitations**: Some providers lag behind API changes

### Neutral
- Requires Terraform CLI installation
- State can be local (dev) or remote (team/prod)

## Alternatives Considered

### Pulumi
- **Pros**: Use real programming languages (Python, TypeScript)
- **Cons**: Smaller community, less job market demand
- **Why rejected**: Terraform is more widely adopted for learning purposes

### Ansible
- **Pros**: Good for configuration management, agentless
- **Cons**: Procedural (not declarative), less suited for cloud infra
- **Why rejected**: Better for config management than infrastructure provisioning

### kubectl + YAML manifests
- **Pros**: Native K8s, no extra tools
- **Cons**: No state management, harder to manage dependencies
- **Why rejected**: Terraform provides better lifecycle management

### Docker Compose only
- **Pros**: Simple, familiar
- **Cons**: Not suitable for K8s, limited to local Docker
- **Why rejected**: Want to learn Kubernetes patterns

## References
- [Terraform Documentation](https://developer.hashicorp.com/terraform/docs)
- [Kind Terraform Provider](https://registry.terraform.io/providers/tehcyx/kind/latest/docs)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
