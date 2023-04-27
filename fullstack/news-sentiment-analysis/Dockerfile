# Set base image (host OS)
FROM python

# Copy the content of the project directory to the working directory
COPY . /news-sentiment-analysis

# Set the working directory in the container
WORKDIR /news-sentiment-analysis

# Install any dependencies
RUN pip install -r requirements.txt

# Specify the Flask environment
# ENV FLASK_RUN_PORT 6000
# ENV FLASK_APP main.py

# By default, listen on port 5000
# EXPOSE 6000

# Set the directive to specify the executable that will run when the container is initiated
ENTRYPOINT [ "sh" ]

# Specify the command to run on container start
CMD [ "run.sh" ]