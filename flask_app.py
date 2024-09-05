from flask import Flask, request, jsonify
from transformers import DistilBertTokenizerFast, pipeline, AutoModelForQuestionAnswering
# from flask_ngrok import run_with_ngrok
# from optimum.onnxruntime import ORTModelForQuestionAnswering

# Initialize Flask app
app = Flask(__name__)

# Load the quantized model and tokenizer
model_dir = "distillbert_squad"
model = AutoModelForQuestionAnswering.from_pretrained(model_dir)
tokenizer = DistilBertTokenizerFast.from_pretrained(model_dir)

# Set up a pipeline for Question Answering
qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)

# Define the /predict endpoint
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)

    # Extract question and context from request
    question = data.get("question", "")
    context = data.get("context", "")

    if not question or not context:
        return jsonify({"error": "Please provide both question and context"}), 400

    # Get the answer from the QA pipeline
    result = qa_pipeline({
        "question": question,
        "context": context
    })

    # Return the result as JSON
    return jsonify({
        "question": question,
        "context": context,
        "answer": result["answer"],
        "score": result["score"]
    })


if __name__ == '__main__':

    # run_with_ngrok(app)
    # app.run()
    app.run(host='0.0.0.0', port=5000)
