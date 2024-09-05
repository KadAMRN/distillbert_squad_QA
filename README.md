# distillbert_squad_QA




### Dockerfile for Flask API Containerization

This Dockerfile encapsulates the Flask-based Question Answering API, along with its dependencies, into a Docker container for easy deployment. Below is an explanation of each section:

1. **Base Image**: 
    - The base image is `python:3.11-slim`, which is a lightweight version of Python 3.11. Using a slim image helps reduce the size of the container, making deployment faster and more efficient.

2. **Working Directory**:
    - The working directory is set to `/flask_app`, meaning all commands that follow will be run within this directory. This keeps the file structure inside the container organized and ensures the application code is in the right place.

3. **Dependency Installation**:
    - The `requirements.txt` file, which lists all the Python dependencies (like `Flask`, `transformers`, etc.), is copied into the container. 
    - The `RUN pip install --no-cache-dir -r requirements.txt` command installs the dependencies, ensuring the environment is set up correctly. The `--no-cache-dir` flag prevents pip from storing temporary files, reducing the final image size.

4. **Copying Application Code**:
    - The `COPY . .` command copies the entire content of the current directory (including the Flask app and associated files) from the host machine into the working directory of the container.

5. **Port Exposure**:
    - The Flask app will run on port `5000` by default, so the `EXPOSE 5000` directive makes this port accessible from outside the container, allowing clients to interact with the API.

6. **Running the Application**:
    - The command `CMD ["python", "flask_app.py"]` tells the container to run the Flask app when the container starts. This executes the `flask_app.py` file using Python.

### Building and Running the Docker Image

1. **Build the Docker Image**:
   - To build the Docker image, use the following command:
     ```bash
     sudo docker build -t flask-qa-api .
     ```

2. **Run the Docker Container**:
   - Once the image is built, run the container using:
     ```bash
     sudo docker run -p 5000:5000 flask-qa-api
     ```
   - This will map port `5000` of the container to port `5000` of the host machine, allowing access to the API at `http://localhost:5000`.

3. **Verify the API**:
   - After the container is running, you can test the API by sending requests to the `/predict` endpoint, as done during local testing. The containerized version should function identically to the local version.

### Conclusion

By containerizing the Flask application with this Dockerfile, the API and its environment can be consistently deployed across different machines or cloud platforms. This allows for ease of deployment and scaling.
