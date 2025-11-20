## Sprint Goal

Deliver an end-to-end user journey that supports basic user-generated content. This includes creating a post, updating the home feed in real time, enabling simple engagement actions (like/dislike), and presenting user and post leaderboards to highlight participation patterns.

## Selected User Stories from Backlog

| Task               | Description                                                                                                                                                          | Story Points |
|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|
| Create a post      | As a user, I want to submit a Procrastination Story using a form with title, description, and hours. It should update the home feed and leaderboards.               | 8            |
| Home Feed          | As a user, I want to see recent stories and be able to like or dislike them on the home feed.                                                                       | 5            |
| User Leaderboard   | As a user, I want to see users ranked by total procrastination hours to encourage friendly competition.                                                             | 5            |
| Post Leaderboard   | As a user, I want to sort posts by likes, dislikes, or time to find the most engaging or latest content.                                                            | 3            |

## Story Points Committed

**Total**: 21  
**Team Capacity**: 30 (3 members × 10 points each)

## Team Assignments

- Rohan Johar: Sign-up/login, create post, feed with engagement buttons, leaderboards, UI fixes  
- Aniket Aggrawal: Assist with front-end integration, bug fixes  
- Aditi Jain: Sprint planning, coordination, documentation  
- Gerald Velasquez: UI assistance, sprint QA

## Dependencies and Risks

- Local environment setup issues due to missing `.env` variables can delay development.
- Authentication and AI-generated form logic may introduce debugging delays.
- Frontend-backend sync issues (e.g., like/dislike toggle state) may reduce feature usability.
- Unclear task ownership could lead to duplicated or delayed efforts.
