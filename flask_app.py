from flask import Flask, request, jsonify
from transformers import (
    DistilBertTokenizerFast,
    pipeline,
    AutoModelForQuestionAnswering,
)

# from flask_ngrok import run_with_ngrok  # Uncomment if using ngrok
# for local deployment

# from optimum.onnxruntime import ORTModelForQuestionAnswering
# Optional: For ONNX runtime

# Initialize Flask app
app = Flask(__name__)

# Load the fine-tuned DistilBERT model and tokenizer from
# the specified directory
model_dir = "distillbert_squad"
model = AutoModelForQuestionAnswering.from_pretrained(
    model_dir
)  # Load the model for Question Answering
tokenizer = DistilBertTokenizerFast.from_pretrained(
    model_dir
)  # Load the corresponding tokenizer

# Set up a HuggingFace pipeline for Question Answering using the loaded
# model and tokenizer
qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)


# Define an API endpoint at /predict that accepts POST requests
@app.route("/predict", methods=["POST"])
def predict():
    # Parse the JSON request body for the question and context
    data = request.get_json(force=True)

    # Extract the question and context from the request
    question = data.get(
        "question", ""
    )  # Default to empty string if question is not provided
    context = data.get(
        "context", ""
    )  # Default to empty string if context is not provided

    # Validate the input to ensure both question and context are present
    if not question or not context:
        return (
            jsonify({"error": "Please provide both question and context"}),
            400,
        )  # Return error if missing

    # Use the QA pipeline to generate the answer based on the input
    # question and context
    result = qa_pipeline({"question": question, "context": context})

    # Return the result as a JSON response, including the question, context,
    # answer, and confidence score
    return jsonify(
        {
            "question": question,
            "context": context,
            "answer": result["answer"],  # Extract the predicted answer
            "score": result[
                "score"
            ],  # Extract the confidence score of the prediction
        }
    )


if __name__ == "__main__":
    # Optional: For running the app with ngrok if testing locally
    # run_with_ngrok(app)

    # Start the Flask app on host 0.0.0.0 (all network interfaces)
    # and port 5000
    app.run(host="0.0.0.0", port=5000)
