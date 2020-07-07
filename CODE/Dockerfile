FROM python:3.7.7
RUN python3 -m venv venv
RUN /bin/bash -c "source venv/bin/activate"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt 
ENV FLASK_APP=app.py
EXPOSE 5000 
ENTRYPOINT ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]