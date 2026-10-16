
from sqlalchemy import inspect, text
from backend.database import engine

inspector = inspect(engine)
columns = [
    column["name"]
    for column in inspector.get_columns("users")
]

print("Existing columns:", columns)

if "password_hash" not in columns:
    with engine.begin() as connection:
        connection.execute(
            text("ALTER TABLE users ADD COLUMN password_hash VARCHAR")
        )
    print("password_hash column added successfully.")
else:
    print("password_hash column already exists.")

print("Database update complete.")

