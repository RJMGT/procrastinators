# Sprint 2 Review

## Sprint Goal
Deploy a functional prototype of the application with working onboarding and authentication, connected to a PostgreSQL database, and accessible on a live staging environment.

## Completed User Stories

| # | User Story / Task                             | Demo Notes                                                                 | Story Points | Status |
|---|------------------------------------------------|----------------------------------------------------------------------------|--------------|--------|
| 1 | User registration and login                   | User can sign up and log in using Django authentication. Login tested with a real account. | 5 | Done |
| 2 | Onboarding prompt (“What are you avoiding…”)  | User sees onboarding question after sign‑up. Response is stored in database. | 3 | Done |
| 3 | PostgreSQL database setup                      | Connected Django ORM to Render PostgreSQL instance. Verified schema + persistence. | 5 | Done |
| 4 | Deployment to Render                           | App deployed at https://procrastinators.onrender.com/. Auto‑deploy on push to main configured. | 5 | Done |
| 5 | Conduct first user test                        | Test user logged in using `user2/class123!` and onboarding flow worked. | 3 | Done |

### Demo Evidence
- **Staging app:** https://procrastinators.onrender.com/  
- **Test account:** `user2 / class123!`  
- **GitHub repo:** https://github.com/RJMGT/procrastinators/
- The app loads successfully, allows login, saves onboarding data, and shows persistence across refresh.

---

## Incomplete User Stories

| User Story | Reason Not Completed | Disposition |
|------------|-----------------------|-------------|
| None from Sprint 2 | All committed stories were completed. | N/A |

(Note: Some stories originally considered for Sprint 2 were intentionally deferred to Sprint 3 during planning.)

---

## Metrics

| Metric                     | Value |
|----------------------------|-------|
| Planned Story Points       | 26    |
| Completed Story Points     | 21    |
| Velocity                   | 21    |
| Completion Rate            | 81%   |

Team capacity was 30 points (3 devs × 10 pts).

---

## Lessons Learned

1. **Early deployment matters.**  
   Deploying earlier would have revealed the SQLite → PostgreSQL issue sooner. This reinforced the importance of validating infrastructure early.

2. **Local-only development caused delays.**  
   The initial localhost-only setup prevented team-wide testing. Moving to Render allowed collaboration and testing from all team members.

3. **Environment configuration takes longer than expected.**  
   Environment variables, allowed hosts, and database credentials required multiple rounds of debugging.

4. **PostgreSQL migration required extra learning.**  
   Render not supporting SQLite led to a quick but necessary switch to PostgreSQL, which required updated settings and migrations.

---

## Product Backlog Updates

Based on Sprint 2 learnings, the following updates were made:

- Added new technical tasks for Sprint 3:
  - Improve error handling on login failures  
  - Add basic logging for debugging leaderboard updates  
  - Set up automated tests for authentication  
- Raised priority of features requiring database writes due to new understanding of Render DB latency.
- Added a backlog item for **regular migration checks** to avoid version drift between dev and staging.
- Added new story: **Implement seed data script** to assist future testing.

---

## Summary

Sprint 2 successfully validated the end‑to‑end infrastructure of the project. The team delivered a functioning, deployed Django application with authentication and onboarding flows backed by a PostgreSQL database. The foundation is now in place for the core features of Sprint 3, including logging, leaderboard logic, and community engagement functionality.

