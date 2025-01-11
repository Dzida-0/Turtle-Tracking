FROM python:3.11-alpine
ENV FLASK_ENV=production
WORKDIR /turtle_app
COPY . /turtle_app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:application"]
