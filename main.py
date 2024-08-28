from flask import Flask, render_template, request, jsonify
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

app = Flask(__name__, template_folder='')

template = """
Answer the question below. 
Here is the conversation history {context}
Question: {question}
Answer:
"""

prompt = ChatPromptTemplate.from_template(template)
model = OllamaLLM(model="llama3")
chain = prompt | model


@app.route('/')
def index():
    app.logger.info("Rendering index.html")
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    context = data.get('context', "")
    question = data['question']

    result = chain.invoke({"context": context, "question": question})

    context += f"\nUser: {question}\nAI: {result}"

    return jsonify({"answer": result, "context": context})


if __name__ == "__main__":
    app.run(debug=True)
