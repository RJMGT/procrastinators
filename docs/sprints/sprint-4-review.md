## Sprint 4 Review

## Sprint Goal and Whether Achieved
The goal of Sprint 4 was to finalize backend compliance and documentation, ensure linting and 12-factor application adherence, and prepare the application for production readiness. This included updating README files, validating Render YAML configurations, and enforcing code quality standards.

The sprint goal was achieved. The application met production-readiness criteria, with successful deployments, strong linting scores, and finalized documentation supporting maintainability and evaluation.

## Completed User Stories

### Backend Compliance and 12-Factor Alignment
The application was reviewed against 12-factor principles, including configuration via environment variables, separation of staging and production environments, and deployment portability. Configuration assumptions and environment dependencies were documented.

### Linting and Code Quality
The codebase was reviewed and cleaned to comply with linting standards. A Pylint score of **9.53/10** was achieved, indicating high code quality and consistency. Minor issues such as unused imports and long lines were identified and addressed where feasible.

### Documentation Updates
README files were updated to clearly explain:
- Project purpose and scope
- Local setup and deployment steps
- Environment variable requirements
- Staging and production URLs

Render YAML files were updated and validated to reflect correct deployment configuration, even though some of these changes were not redeployed to production due to timing.

## Incomplete User Stories
None. All Sprint 4 tasks related to compliance, documentation, and quality assurance were completed.

## Demo Notes
Sprint 4 focused on system readiness rather than new user-facing features. The following were demonstrated:

- Successful production deployment on Render (`/d92e206/` endpoint)
- Stable staging environment
- Verified environment-based configuration
- Linting compliance and code quality metrics
- Updated documentation walkthrough

Live Demo: https://procrastinators-prod.onrender.com/

## Metrics

**Planned vs Completed Story Points**
- Planned: 21 pts  
- Completed: 21 pts  

**Velocity**
- Sprint 4: 21 story points  

**Cumulative Velocity**
- Sprint 2: 18 pts  
- Sprint 3: 21 pts  
- Sprint 4: 21 pts  
- Total: 60 story points  

Internal feedback highlighted:
- Strong production stability
- High code quality relative to project scope
- Clear documentation and handoff readiness
- Need for earlier automation of testing in future projects


