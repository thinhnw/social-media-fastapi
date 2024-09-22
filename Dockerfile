FROM python:3.10
WORKDIR /usr/srp/app
RUN pip install pipenv
RUN pipenv install --no-cache-dir
COPY . . 
RUN pipenv shell
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
