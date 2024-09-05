from transformers import DistilBertTokenizerFast, pipeline, AutoModelForQuestionAnswering

# Load the quantized model and tokenizer
model_dir = "distillbert_squad"
model = AutoModelForQuestionAnswering.from_pretrained(model_dir)
tokenizer = DistilBertTokenizerFast.from_pretrained(model_dir)

# Set up a pipeline for Question Answering
qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)

def main():
    while True:
        # Get question and context from user input
        question = input("Enter your question (or 'exit' to quit): ")
        if question.lower() == 'exit':
            break
        context = input("Enter the context: ")

        if not question or not context:
            print("Please provide both question and context")
            continue

        # Get the answer from the QA pipeline
        result = qa_pipeline({
            "question": question,
            "context": context
        })

        # Print the result
        print(f"Question: {question}")
        print(f"Context: {context}")
        print(f"Answer: {result['answer']}")
        print(f"Score: {result['score']}")

if __name__ == '__main__':
    main()