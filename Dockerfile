FROM python:3
# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN echo "deb http://deb.debian.org/debian/ unstable main contrib non-free" >> /etc/apt/sources.list.d/debian.list
RUN apt-get update
RUN apt-get install -y --no-install-recommends firefox

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz
RUN tar -x geckodriver -zf geckodriver-v0.30.0-linux64.tar.gz -O > /usr/local/bin/geckodriver
RUN chmod +x /usr/local/bin/geckodriver
RUN rm geckodriver-v0.30.0-linux64.tar.gz

RUN pip install -r requirements.txt
# Run app.py when the container launches
CMD ["python", "main.py"]
