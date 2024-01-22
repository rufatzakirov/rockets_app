FROM python:slim
COPY . .
RUN pip3 install Flask
CMD python app.py
