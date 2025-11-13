# Sprint retrospective

Date: Nov-10

Attendees:
- Rohan Johar
- Aniket Aggrawal
- Aditi Jain
- Gerald Velasquez

## What didn't go well
- The local and cloud deployments went smoothly.
- The project is progressing according to the plan.
- Team collaboration and communication remained consistent throughout the sprint.
  
## What didn't go well
#### Render deployment
- The dev team initially built the app locally on localhost 127.0.0.1 to create the first interfaces and test the database connection. This setup prevented other users from accessing the app externally.

- The next step was to deploy the app and the database on Render.

- Finally, we created a Django app on Render. After configuration, the app went live and users could log into their accounts. So far, only one demo account is available.

#### Database selection
- When we tried to migrate the SQLite database to Render, we realized that Render does not support SQLite for free-tier usage. We migrated to PostgreSQL using the same schema and by updating the connection settings.

## What to improve
- Solve configuration issues to properly create GitHub branches. Action: Dev team to replicate the repo locally and tested synchronization.
- Coordinate and planne the first round of testing. Action: The whole team is to build the test plan in the next meeting.
