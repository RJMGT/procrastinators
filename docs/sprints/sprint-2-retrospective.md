Render deployment:
 The dev team initially built the app locally (localhost 127.0.0.1) to create the first interfaces and test the database connection. However, this setup prevented other users from accessing the app externally.
 Our next step was to deploy the app locally and database on Render.
Finally, we created a Django app on render. After configuration, the app went live and users could log into their accounts (so far, only one demo account).
Database selection:
We we tried to migrate the database (SQLite) to Render, we realized that Reder does not support SQLite for free tier usage. So, we migrated to PostgreSQL using the same schema and by updating the connection settings.
