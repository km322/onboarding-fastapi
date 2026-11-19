"""Default settings so the tests run without a backend/.env file or a running MongoDB."""

import os

os.environ.setdefault("MONGODB_URI", "mongodb://127.0.0.1:27017/todoList-test")
os.environ.setdefault("FRONTEND_ORIGIN", "http://localhost:5173")
