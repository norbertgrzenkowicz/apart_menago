FROM python:3.12-slim
WORKDIR /app
COPY . /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

ENV NAME APART_MENAGO

# Run app.py when the container launches
# CMD ["python", "-m ", "src.interface"]
