release: cd src && alembic upgrade head
web: cd src && gunicorn -w 1 -k uvicorn.workers.UvicornWorker app.main:app