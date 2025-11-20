## Sprint 3 Retrospective

### What Went Well
- The new sign-up workflow (email, username, password) worked end-to-end, including validation and PostgreSQL data storage.
- The app continued running smoothly on Render with no downtime during the sprint.
- Core Sprint 3 features (logging procrastination updates, leaderboard categories, and UI enhancements) made measurable progress.
- The AI-assisted workflow (Cursor) accelerated UI development and reduced manual boilerplate.
- Improvements to the onboarding and login screens enhanced the user experience.

### What Didn’t Go Well
- Environment variable confusion during local testing caused the app to connect to the production database on Render, leading to unintended writes.
- The like/dislike interaction was buggy: buttons showed delayed toggle, and UI often failed to update immediately despite backend state changing.
- Communication dropped compared to Sprint 2, with unclear division of backend vs frontend responsibilities, leading to duplicated or untouched tasks.
- The authentication flow revisions took longer than expected due to edge case validation errors and buggy AI-generated redirect logic.

### What to Improve
- **Standardize development environments**: Use a shared `.env.example` file and clear onboarding steps for all team members to avoid misconfiguration.
- **Clarify ownership and increase check-ins**: Implement daily check-ins or brief async updates and assign explicit owners to user stories during sprint planning.

### Action Items
| Action Item | Owner | Deadline |
|------------|--------|----------|
| Create and maintain a shared `.env.example` file | Aniket | Start of Sprint 4 |
| Assign clear owners during sprint planning and track updates in GitHub project board | Aditi | Sprint 4 Planning |
| Schedule async check-ins via Slack | Gerald | Ongoing during Sprint 4 |
| Investigate and fix like/dislike UI refresh issue | Rohan | Mid-Sprint 4 |

### Team Dynamics Reflection
The team continues to make strong progress toward core features, but Sprint 3 surfaced challenges in cross-functional communication and clarity around responsibilities. With clear task ownership, shared environment setup, and slightly tighter coordination, the team is well-positioned to increase velocity and reduce duplicated effort going forward.
