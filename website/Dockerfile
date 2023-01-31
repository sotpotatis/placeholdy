#Dockerfile for running the server
#Note: The Pillow library works without extra installion on Buster, that's why I'm using it
#rather than the standard "Alpine" image that is used everywhere
FROM python:slim-buster
#Copy and install stuff
COPY . /placeholdy
WORKDIR /placeholdy
RUN pip install -r requirements.txt
#Expose ports and run server
EXPOSE 8080
#Run Gunicorn
CMD ["gunicorn", "app:create_app()", "--bind=0.0.0.0:8080"]
