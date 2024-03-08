FROM python:3-alpine3.17
WORKDIR /BOOKRECOMMENDATIONSYSTEM
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 3000
CMD python ./app.py
