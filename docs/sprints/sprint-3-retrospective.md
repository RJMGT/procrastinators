# Sprint 3 Retrospective

**Date:** Nov-24  

## Attendees
- Rohan Johar  
- Aniket Aggrawal  
- Aditi Jain  
- Gerald Velasquez  

---

## ✅ What Went Well
- The newly implemented sign-up workflow (email, username, password) works end-to-end, including validation and PostgreSQL data storage.
- The app continued running smoothly on Render with no downtime during the sprint.
- Core Sprint 3 features (logging procrastination updates, leaderboard categories, and UI enhancements) made measurable progress.
- The AI-assisted workflow (Cursor) accelerated UI development and reduced manual boilerplate.
- Improvements to the onboarding and login screens enhanced the user experience.

---

## ❌ What Didn’t Go Well

### 1. Environment Variable Confusion (Recurring Issue)
- Team members repeatedly forgot to configure required environment variables during local testing.
- Django defaulted to the production PostgreSQL database on Render, causing accidental writes to the live DB.
- Resulted in slower development and inconsistent test results.

### 2. Like/Dislike Interaction Bug
- The like/dislike buttons were expected to toggle after one click, but:
  - They switch states with noticeable delay.  
  - The UI does not always update immediately.  
  - Backend updates occur, but the frontend sometimes fails to refresh the state.

### 3. Reduced Communication + Unclear Responsibilities
- Lower team communication compared to Sprint 2.
- Unclear division of responsibilities between backend and UI tasks.
- Some work was duplicated, while other tickets remained untouched longer than planned.

### 4. Authentication Workflow Revisions Took Longer Than Expected
- AI-generated signup/login components required multiple debugging cycles.
- Issues encountered:
  - Form validation edge cases.
  - Incorrect redirects during testing.
- The effort to refine AI-generated code was underestimated.

---

