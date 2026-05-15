# Contributing Guide

## Setup

1. Fork the repository
2. Create feature branch: `git checkout -b feat/your-feature`
3. Make changes
4. Run tests: `cd backend && pytest` and `cd viewer && npm test`
5. Commit: `git commit -m "feat(scope): description"`
6. Push and open PR

## Coding Standards

- Python: PEP 8, type hints required
- TypeScript: Strict mode, no `any`
- Commits: Conventional commits format
- Tests: Required for new features

## PR Process

1. Open PR with clear description
2. CI must pass (tests + build)
3. Code review by maintainer
4. Merge to main
