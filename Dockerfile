# # Use an official Python runtime as a base image
# FROM python:3.11-slim

# # Set the working directory in the container
# WORKDIR /flask_app

# # Copy the requirements.txt file into the container
# COPY requirements.txt .

# # Install any dependencies specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# # Install gdown to download files from Google Drive
# RUN pip install gdown

# # Install unzip to extract the model folder
# RUN apt-get update && apt-get install -y unzip

# # Download the model folder as a zip file from Google Drive
# # Replace 'your_google_drive_file_id' with the actual file ID
# RUN gdown --id your_google_drive_file_id -O /flask_app/distillbert_squad.zip

# # Unzip the model folder
# RUN unzip /flask_app/distillbert_squad.zip -d /flask_app

# # Remove the zip file after extraction
# RUN rm /flask_app/distillbert_squad.zip

# # Copy the rest of the application code into the container
# COPY . .

# # Expose the port that Flask will run on
# EXPOSE 5000

# # Define the command to run the app
# CMD ["python", "flask_app.py"]


# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /flask_app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install gdown to download files from Google Drive
RUN pip install gdown

# Install unzip to extract the model folder
RUN apt-get update && apt-get install -y unzip

# Download the model folder as a zip file from Google Drive
RUN gdown https://drive.google.com/drive/folders/1btXNz1qEdSaRBirMsomtSScyy3Gn5zV- -O /flask_app/distillbert_squad.zip

# Unzip the model folder
RUN unzip /flask_app/distillbert_squad.zip -d /flask_app

# Remove the zip file after extraction
RUN rm /flask_app/distillbert_squad.zip

# Copy the rest of the application code into the container
COPY . .

# Expose the port that Flask will run on
EXPOSE 5000

# Define the command to run the app
CMD ["python", "flask_app.py"]