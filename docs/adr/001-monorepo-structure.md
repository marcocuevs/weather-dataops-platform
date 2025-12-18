# ADR-001: Monorepo Structure

## Status
Accepted

## Date
2024-12-18

## Context
We need to organize the codebase for a data platform that includes multiple components: infrastructure code, data ingestion, orchestration, transformations, and documentation. The question is whether to use a monorepo (single repository) or polyrepo (multiple repositories) approach.

## Decision
We will use a **monorepo structure** with clear separation of concerns through directories:

```
weather-dataops-platform/
├── .github/workflows/    # CI/CD pipelines
├── docs/                 # Documentation (EN/ES)
├── infra/                # Terraform IaC
├── ingestion/            # Python data ingestion
├── orchestration/        # Dagster pipelines
├── transformations/      # dbt models
└── scripts/              # Utility scripts
```

## Consequences

### Positive
- **Single source of truth**: All code in one place, easier to understand the full system
- **Atomic changes**: Can update infrastructure and code together in one PR
- **Simplified CI/CD**: One pipeline can validate all components
- **Easier refactoring**: Cross-component changes are straightforward
- **Better for learning**: See how all pieces connect

### Negative
- **Larger repository**: Clone size grows over time
- **CI complexity**: Need to handle selective builds/tests
- **Access control**: Harder to restrict access to specific components

### Neutral
- Requires clear directory structure conventions
- Need good documentation to navigate

## Alternatives Considered

### Polyrepo (Multiple Repositories)
- **Pros**: Smaller repos, independent versioning, clearer ownership
- **Cons**: Harder to make cross-repo changes, dependency management complexity
- **Why rejected**: For a learning project, seeing all components together is more valuable

### Monorepo with Git Submodules
- **Pros**: Logical separation with linked repos
- **Cons**: Complex Git workflows, submodule sync issues
- **Why rejected**: Adds unnecessary complexity for this project size

## References
- [Monorepo vs Polyrepo](https://www.atlassian.com/git/tutorials/monorepos)
- [dbt Monorepo Best Practices](https://docs.getdbt.com/guides/best-practices/how-we-structure/1-guide-overview)
