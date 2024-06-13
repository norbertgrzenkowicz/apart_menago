FROM python:3.12-slim
WORKDIR /app
COPY . /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV NAME APART_MENAGO

# Run app.py when the container launches
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
