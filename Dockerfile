FROM python:3.12-slim

WORKDIR /app

COPY . /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8000

CMD bash -c "cd src && python manage.py migrate --noinput && \
             gunicorn --bind 0.0.0.0:8000 conf.wsgi:application"