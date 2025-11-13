# Sprint 2 Review

## Sprint Summary

**Goal:**  
Deliver a functional prototype with working onboarding and authentication, deployed on a live environment.

**Did we achieve it?**  
Yes. We built and deployed a working Django app with PostgreSQL integration on Render. Authentication and user onboarding are functional, and we successfully completed our first round of user testing.

## Key Outcomes

- Users can now register, log in, and complete an onboarding prompt.
- Admin can add/remove users.
- User data is stored persistently in a PostgreSQL database.
- Deployment pipeline is configured to auto-update on each push to the main branch.

**Staging App:**  
https://procrastinators.onrender.com/  
Test credentials: `user2 / class123!`

**GitHub Repo:**  
https://github.com/RJMGT/procrastinators/

## Deployment Details

| Component        | Tech Stack               |
|------------------|--------------------------|
| Backend          | Django 5.0               |
| Database         | PostgreSQL (Render DB)   |
| Hosting          | Render                   |
| Version Control  | GitHub                   |

## Completed Work

| # | Task                                | Description                                               | Story Points | Status |
|---|-------------------------------------|-----------------------------------------------------------|--------------|--------|
| 1 | User registration and login         | Implemented Django authentication                         | 5            | ✅ Done |
| 2 | Onboarding prompt                   | Added “What are you avoiding today?” user field           | 3            | ✅ Done |
| 3 | PostgreSQL DB setup                 | Configured on Render and connected with Django ORM        | 5            | ✅ Done |
| 4 | App deployment                      | Deployed backend + DB to Render                           | 5            | ✅ Done |
| 5 | User testing (first test)           | Verified onboarding and login with 1 real user            | 3            | ✅ Done |

## Metrics

| Metric                   | Value  |
|--------------------------|--------|
| Story Points Planned     | 26     |
| Story Points Completed   | 21     |
| Velocity (SP / Sprint)   | ≈ 21   |
| Completion Rate          | 81%    |
| Team Capacity            | 30 pts (3 members × 10 pts) |

## Retrospective Notes

**Render Deployment**  
- Initially, we developed on localhost which made external access difficult.  
- We switched to Render and configured the app for public deployment.  
- After resolving environment variables and database connections, the live app was functional and accessible.

**Database Migration**  
- We initially used SQLite but Render doesn’t support it on the free tier.  
- We migrated the app to PostgreSQL and updated the connection settings accordingly.

## Looking Ahead: Sprint 3 Preview

Goal: Deliver the Logging & Leaderboard MVP — allowing users to log fake progress and view a community leaderboard.

| Feature                                | Story Points | Priority |
|----------------------------------------|--------------|----------|
| Submit “fake progress” update          | 5            | High     |
| View daily log history                 | 3            | High     |
| Leaderboard ranked by “Hours Wasted”   | 5            | High     |
| Leaderboard ranked by “Creative Excuse”| 5            | High     |
| Upvotes/comments (basic version)       | 3            | Medium   |
| Unit tests for new endpoints           | 2            | Medium   |
