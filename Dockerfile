FROM python:3.10
WORKDIR /usr/srp/app
RUN pipenv install --no-cache-dir
COPY . . 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
