# distillbert_squad_QA

## Author
**Abdelkader AMROUN**

All scripts and configurations were executed using **Python 3.11**. The dependencies required to run the project can be found in the `requirements.txt` file.

---

## Fine-Tuned Model
The fine-tuned model used in this project can be found [here](https://drive.google.com/drive/folders/1btXNz1qEdSaRBirMsomtSScyy3Gn5zV-) on Google Drive.

> **Note:** Please download the model and place it in the root directory of the project as `fine_tuned_model.pth` (or whatever the model file's extension is).

---


## 1. Model Selection

### Objective:
The goal is to select a pre-trained Large Language Model (LLM) from the Hugging Face Model Hub, considering computational efficiency, suitability for the target task, and hardware constraints.

### Selected Model: **DistilBERT**

### Justification:
I chose **DistilBERT**, a distilled version of BERT, due to several key factors, especially given my intention to perform a **Question-Answering (QA) task**:

1. **Computational Efficiency**:  
   Given the limited computational resources I have available, my model choices were constrained. DistilBERT is ideal because it retains 97% of BERT’s language understanding while being 60% faster and having 40% fewer parameters, making it much lighter to deploy. This allows me to perform NLP tasks, including QA, efficiently without compromising too much on performance.

2. **Model Size**:  
   DistilBERT has **66 million parameters**, significantly smaller than its parent model, BERT-base, which has **110 million parameters**. This reduction in size while maintaining strong performance metrics is crucial for my use case, given the hardware limitations.

3. **Suitability for QA Task**:  
   DistilBERT has been widely used for a variety of NLP tasks, including Question Answering, due to its ability to efficiently process and understand large amounts of text while maintaining high accuracy. I considered **T5-small**, but I encountered issues with quantization, and going too small with mobile-optimized LLMs could compromise the quality of answers in the QA task.

4. **Pre-training Dataset**:  
   DistilBERT is pre-trained on the same data as BERT—comprising **BooksCorpus (800M words)** and **English Wikipedia (2.5B words)**. This broad exposure makes it well-suited for general-purpose language understanding tasks, including Question Answering.

5. **DistilBERT Architecture**:  
   DistilBERT uses a **Transformer architecture** similar to BERT but with some key differences. It employs the same bidirectional encoder but with fewer layers—**6 layers** instead of BERT's 12. This reduction in layers helps DistilBERT achieve its efficiency while maintaining robust language understanding, which is essential for tasks like QA that require precise comprehension of context.

6. **Distillation Process**:  
   DistilBERT was trained using knowledge distillation, a technique that compresses a larger model into a smaller one by transferring knowledge. This was an attractive factor as it keeps the core strengths of BERT while making it faster and lighter, which is crucial for operating under hardware constraints.

### Comparison with Similar Models:

| Model        | Parameters | Layers | Speed vs BERT-base | Task Suitability | Notes |
|--------------|------------|--------|--------------------|------------------|-------|
| **DistilBERT**   | 66M        | 6      | 60% faster         | General-purpose NLP, QA  | Distilled version of BERT, balanced for efficiency and performance |
| **BERT-base**    | 110M       | 12     | Baseline           | General-purpose NLP, QA  | Larger and more computationally expensive than DistilBERT |
| **T5-small**     | 60M        | 6      | Fast               | Text-to-text tasks, Summarization | Issues with quantization, not ideal for QA due to task specialization |
| **MobileBERT**   | 25M        | 24     | Faster than BERT-base, slower than DistilBERT | Mobile device-focused NLP | Optimized for mobile, but may compromise performance for larger tasks like QA |

- **DistilBERT vs BERT-base**:  
   While BERT-base offers more layers and parameters (110M vs 66M), DistilBERT is 60% faster and uses fewer resources. For my QA task, DistilBERT maintains strong language comprehension while being much more efficient on limited hardware.
  
- **DistilBERT vs T5-small**:  
   T5-small is a versatile text-to-text model with similar size (60M parameters), but it is more suited to tasks like summarization and translation. Quantization issues and its specific task focus make T5-small less suitable for a QA task, especially with hardware limitations.

- **DistilBERT vs MobileBERT**:  
   MobileBERT is optimized for mobile devices with only 25M parameters. However, this optimization leads to performance compromises for more intensive tasks like QA. DistilBERT provides better overall performance while still being efficient enough for limited hardware environments.

### Summary:
Given my limited hardware resources and the goal of performing a **Question-Answering task**, DistilBERT offers the best balance between model size, computational efficiency, and performance. Compared to BERT-base, T5-small, and MobileBERT, DistilBERT maintains a high level of language understanding while being optimized for resource-constrained environments, making it the most suitable model for this task.




## 3. Model Fine-Tuning

### Objective:
Fine-tune the selected model on a specific task using a dataset of choice.

### Selected Task: **Question Answering (QA)**

I chose a **Question Answering (QA)** task because it aligns well with the **chatbot functionality** of Gemini, a system at Valeo. QA tasks offer a **generative aspect**, which is critical for creating dynamic, conversation-like interactions, in contrast to more rigid classification tasks.

### Dataset: **SQuAD (Stanford Question Answering Dataset)**

#### Description:
The **SQuAD (Stanford Question Answering Dataset)** is a widely-used dataset for QA tasks. It contains over **100,000 question-answer pairs** based on passages from **Wikipedia** articles. The questions are fact-based, and the answers are either exact spans of text from the corresponding passages or can be derived from the passage context.

#### Source:
- **SQuAD v1.1** can be accessed from the Hugging Face Datasets library: [SQuAD Dataset on Hugging Face](https://huggingface.co/datasets/squad).
- It was originally published by Stanford University and is one of the most popular datasets for training and benchmarking QA models.

#### Why SQuAD?:
- **Rich Context for QA**: SQuAD is ideal for my task since it provides both the **context (passage)** and **questions**, enabling the model to learn how to find or generate the correct answer within a given text.
- **High-Quality Annotations**: The dataset includes **human-annotated answers**, ensuring that the quality of the answers is reliable, which is crucial for a QA task aimed at chatbot-like interactions.
- **Proven Benchmark**: SQuAD is a standard benchmark for QA models, meaning that fine-tuning on it allows me to easily compare my model’s performance to other state-of-the-art models.

### Preprocessing and Fine-tuning Implementation:
All details about the preprocessing steps and the fine-tuning implementation can be found in the **QA_pipeline.ipynb** file. This notebook covers the tokenization, dataset preparation, and training process used to fine-tune DistilBERT on the SQuAD dataset.


## 4. Model Evaluation (Bonus)

### Objective:
Assess the performance of the fine-tuned model compared to the original model.

### Evaluation Metrics:
To evaluate the performance of the fine-tuned model, I used the standard **SQuAD evaluation metrics**:

1. **Exact Match (EM)**:  
   Measures the percentage of predictions that match exactly with the ground truth answer. It’s a strict metric where only an exact match between the predicted and actual answers counts.
   
2. **F1 Score**:  
   The F1 score is the harmonic mean of precision and recall. It takes partial matches into account, making it a more lenient metric for QA tasks. The F1 score rewards answers that overlap significantly with the correct answer, even if they aren’t exactly the same.

### Results:
After fine-tuning the model on the SQuAD dataset, the performance metrics are as follows:

- **Exact Match (EM):** 54.34%  
- **F1 Score:** 64.99%

### Comparison of Original vs Fine-Tuned Model:
- **Original Model**: The pre-trained **DistilBERT** model, without fine-tuning, is designed for general language understanding but lacks the specialized knowledge to handle the intricacies of QA tasks.
- **Fine-Tuned Model**: After fine-tuning on the SQuAD dataset, the model shows a significant improvement in its ability to handle question answering, as seen in the **Exact Match** and **F1 scores**.

While the fine-tuned model demonstrates solid performance in QA tasks, there’s still room for improvement, especially in achieving higher exact match accuracy. However, the **F1 score** suggests that the model captures relevant information even if it doesn’t always provide the exact answer.

### Further Details:
All evaluation details, including the model’s performance before and after fine-tuning, as well as the full evaluation pipeline, can be found in the **QA_pipeline.ipynb** file.



## 5. API Creation

### Objective:
Develop an API to serve the fine-tuned model, enabling easy access for inference.

### API Design:
I used **Flask** to implement the API. The API code can be found in the file **flask_app.py**.

To launch the API, simply run the following command in your terminal:

```bash
python flask_app.py
```
Once the server is running, the API will be able to process incoming requests and return predictions from the fine-tuned model.

### Functionality:


The API exposes a single endpoint, /predict, which accepts a POST request with the following JSON payload:

- question: The question you want the model to answer.
- context: The text passage that contains the answer to the question.

Example usage with `curl`:

```bash
curl -X POST "http://localhost:5000/predict" \
-H "Content-Type: application/json" \
-d '{"question": "What is quantization?", "context": "Quantization is a technique to reduce model size and speed up inference."}'
```

This will return a JSON response with the model's predicted answer and a confidence score.

### Testing:

Unit tests for the API are implemented in **test_api.py**. The tests ensure that the API functions as expected under various scenarios, including valid requests and handling of missing data.

To run the tests, use the following command:
```bash
python test_api.py
```

**Test Description:**

The tests are structured using Python's unittest framework and include the following cases:

- **test_predict_success:**
This test verifies that the API correctly processes a valid request. It checks that:

    - The response is in JSON format.
    - The status code is 200 (OK).
    - The response contains an answer and a confidence score.
    - The confidence score is above a reasonable threshold (0.1 in this case).


- **test_predict_missing_data:**
    - This test handles the scenario where either the question or context is missing from the input payload. It checks that:

    - The response returns a 400 (Bad Request) status.
    - The response includes an error message indicating that required data is missing.
    - These tests ensure the API is robust and can handle both successful and erroneous requests appropriately.

These tests ensure the API is robust and can handle both successful and erroneous requests appropriately.

More detailed implementation information, including the API functionality, preprocessing steps, and fine-tuning process, can be found in the `QA_pipeline.ipynb` file.



## 6. Containerization

### Objective:
Encapsulate the entire application, including the API, into a Docker container for ease of deployment.

### Dockerfile Explanation:
I created a Dockerfile to automate the setup of the environment and ensure that all dependencies are installed correctly.

```Dockerfile
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

# Download the model folder as a zip file from Google Drive
RUN gdown https://drive.google.com/drive/folders/1btXNz1qEdSaRBirMsomtSScyy3Gn5zV- -O /flask_app/ --folder

# Copy the rest of the application code into the container
COPY . .

# Expose the port that Flask will run on
EXPOSE 5000

# Define the command to run the app
CMD ["python", "flask_app.py"]
```





## Dockerfile for Flask API Containerization

This Dockerfile encapsulates the Flask-based Question Answering API, along with its dependencies, into a Docker container for easy deployment. Below is an explanation of each section:

1. **Base Image**: 
    - The base image is `python:3.11-slim`, which is a lightweight version of Python 3.11. Using a slim image helps reduce the size of the container, making deployment faster and more efficient.

2. **Working Directory**:
    - The working directory is set to `/flask_app`, meaning all commands that follow will be run within this directory. This keeps the file structure inside the container organized and ensures the application code is in the right place.

3. **Dependency Installation**:
    - The `requirements.txt` file, which lists all the Python dependencies (like `Flask`, `transformers`, etc.), is copied into the container. 
    - The `RUN pip install --no-cache-dir -r requirements.txt` command installs the dependencies, ensuring the environment is set up correctly. The `--no-cache-dir` flag prevents pip from storing temporary files, reducing the final image size.

4. **Install gdown**:
    - To facilitate the downloading of models from Google Drive, the `gdown`package is installed.

5. **Download Model**:
    - The model files are downloaded from Google Drive using gdown, with the model folder being saved directly into the `/flask_app/` directory.


6. **Copying Application Code**:
    - The `COPY . .` command copies the entire content of the current directory (including the Flask app and associated files) from the host machine into the working directory of the container.

7. **Port Exposure**:
    - The Flask app will run on port `5000` by default, so the `EXPOSE 5000` directive makes this port accessible from outside the container, allowing clients to interact with the API.

8. **Running the Application**:
    - The command `CMD ["python", "flask_app.py"]` tells the container to run the Flask app when the container starts. This executes the `flask_app.py` file using Python.

## Building and Running the Docker Image

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
   <!-- - After the container is running, you can test the API by sending requests to the `/predict` endpoint, as done during local testing. The containerized version should function identically to the local version. -->
   - To test the API, use the following curl command to send a POST request to the `/predict` endpoint:
   ```bash
   curl -X POST "http://localhost:5000/predict" \
    -H "Content-Type: application/json" \
    -d '{"question": "How is life?", "context": "Life is beautiful."}'
   ```

3. **Running Unit Tests in the Container**:
    - You can execute the unit tests inside the running container using the following command:

    ```bash
    docker exec flask_qa_api python test_api.py
    ```


### Conclusion

By containerizing the Flask application with this Dockerfile, the API and its environment can be consistently deployed across different machines or cloud platforms. This allows for ease of deployment and scaling.


## CI/CD Pipeline Flow for Flask API with Github Actions

This CI pipeline, defined in the `.github/workflows/ci.yml` file, automates the process of code quality checks, Docker image builds, and API testing. It is triggered on code changes in the `main` branch via a push or pull request.

### Pipeline Trigger
The pipeline runs automatically when:
- Code is pushed to the `main` branch.
- A pull request is opened or updated targeting the `main` branch.
  
The pipeline consists of two key jobs: **Lint (Code Quality Checks)** and **Docker Build and API Testing**.

---

### Job 1: Code Quality Checks (Lint)

#### Trigger: 
The pipeline begins with the `lint` job after code is pushed or a pull request is created for the `main` branch.

#### Steps:

1. **Checkout Repository Code**:
   - The code from the repository is pulled using `actions/checkout@v2`.
   - This step allows the pipeline to access the entire codebase so subsequent steps can work with the project files.
   
2. **Set up Python 3.11**:
   - The Python environment is configured using `actions/setup-python@v2` with version 3.11.
   - This ensures the correct Python version is available to run the application and any tests.
   
3. **Install Dependencies**:
   - The pipeline installs the project dependencies by upgrading `pip` and running `pip install -r requirements.txt`.
   - This includes all necessary packages such as Flask, testing libraries, and linting tools, so the environment mirrors your local development setup.

4. **Run Flake8 Linter**:
   - **Flake8** is used to check the Python code (`flask_app.py` and `test_api.py`) for issues such as:
     - PEP 8 style violations.
     - Unused imports, variables, or functions.
     - Improper indentation or line spacing.
   - The linter ensures that the code meets quality and style standards, and any errors or warnings are reported.
   - If `flake8` identifies issues, the pipeline stops here, prompting you to fix the issues before continuing to the next stage.

---

### Job 2: Docker Build and API Testing

#### Trigger: 
The `docker_build` job starts only after the successful completion of the `lint` job. This ensures that the code quality checks have passed before proceeding with the Docker build and API testing.

#### Steps:

1. **Checkout Repository Code**:
   - The code is checked out again, as each job runs in an isolated environment. This allows the Docker build job to access the necessary files.
   
2. **Build Docker Image**:
   - The Docker image is built from the `Dockerfile` in the project directory using the command `docker build -t flask-qa-api .`.
   - This step packages the Flask API and all its dependencies into a Docker image tagged as `flask-qa-api`.
   - Any issues during the Docker build, such as missing files or configuration errors, will stop the pipeline at this point.

3. **Run Docker Container**:
   - After building the image, the Docker container is started with the Flask API running inside it using `docker run -d -p 5000:5000 --name flask_qa_api flask-qa-api`.
   - The API is exposed on port 5000, which allows the next steps to interact with it.
   - A delay (`sleep 10`) ensures the container has enough time to start up before proceeding with API tests.

4. **API Testing with `curl`**:
   - A **basic API functionality test** is performed using the `curl` command.
   - A POST request is sent to the API's `/predict` endpoint with a sample JSON payload: 
     ```json
     {
       "question": "How is life?",
       "context": "Life is beautiful."
     }
     ```
   - The API response is checked to ensure it contains the expected keyword (`"beautiful"`), confirming that the API is processing requests correctly.
   - If the API does not respond as expected, the pipeline will stop, indicating an issue with the application.

5. **Run Unit Tests**:
   - The **unit tests from Question 5** are executed inside the running Docker container using the command `docker exec flask_qa_api python test_api.py`.
   - These unit tests verify various aspects of the API's behavior, including:
     - Whether the API routes are functioning as intended.
     - The correctness of the response content and format.
     - Error handling and edge cases.
   - If the unit tests fail, the pipeline will provide feedback on which tests failed and why.

6. **Stop and Remove Docker Container**:
   - After the API tests and unit tests complete, the running Docker container is stopped and removed using `docker stop flask_qa_api` and `docker rm flask_qa_api`.
   - This cleanup step ensures that no Docker containers are left running after the pipeline finishes, keeping the environment clean for future runs.

---

### CI Pipeline Summary
1. **Code Quality Checks (Lint)**: 
   - The code is checked for quality and PEP 8 compliance using `flake8`.
   - If the code passes linting, the next job starts.
   
2. **Docker Build and API Testing**:
   - A Docker image is built, and the Flask API is deployed in a container.
   - A basic API test is performed using `curl` to ensure the API responds correctly.
   - The unit tests from Question 5 are executed inside the container to verify the functionality of the API.
   - The Docker container is stopped and removed after the tests complete.

This pipeline ensures that every change to the codebase is thoroughly linted, built, and tested automatically, improving the reliability and quality of the application over time.



## Thank You!