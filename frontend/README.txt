TASKFLOW FRONTEND PROJECT-OWNERSHIP FIX

Replace these three files in your project:
  frontend/index.html
  frontend/script.js
  frontend/style.css

This fix loads projects belonging to the logged-in user. If the user has no projects, it creates a default project using the authenticated user ID. Task creation then uses the selected owned project ID instead of hard-coding project ID 1. Backend ownership checks remain enabled.

Keep your backend and database files unchanged.
After replacing the files, refresh http://127.0.0.1:5500 with Ctrl+Shift+R.
