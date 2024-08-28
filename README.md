
# Local AI ChatBot 

This project sets up a web-based chat application using Flask, integrated with LangChain and the Ollama LLM for providing AI-driven responses. The system consists of a Flask backend to handle API requests and a frontend HTML template for user interaction.

## 🔍 Key Steps

**1. Backend (Flask Application)**
-   **Imports and Setup**
	- `Flask`: Web framework to handle HTTP requests and serve web pages.
	-   `render_template`,  `request`,  `jsonify`: Flask functions for rendering templates, handling incoming requests, and sending JSON responses.
	-   `OllamaLLM`: LangChain class for the Ollama language model.
	-   `ChatPromptTemplate`: Class for creating prompt templates to structure questions and responses.
- **Application Initialization**
	- `app = Flask(__name__)`: Creates a Flask application instance.
- **Prompt Template Configuration**
	- Defines the template for the chat prompt including placeholders for conversation history and the user's question.
- **Model and Chain Setup**
	- `model = OllamaLLM(model="llama3")`: Initializes the Ollama language model.
	- `chain = prompt | model`: Creates a processing chain that combines the prompt template and the language model.
- **Routes and Handlers**
	- `/`: Renders the main HTML page.
	- `/ask`: Handles POST requests to process user questions, updates the context, and returns the AI's response in JSON format.
- **Execution**
	- `app.run(debug=True)`: Runs the Flask application in debug mode.

**2. Frontend (HTML Template)**
- **HTML Structure**
	-  Basic HTML layout with Bootstrap for styling.
	- Includes  `header`,  `main`, and  `footer`  sections.
- **Styling**
	- Custom CSS for chatbox, input fields, and buttons.
	- Bootstrap classes for responsive design and layout.
- **JavaScript**
	- Handles user input submission and displays chat history.
	- Sends user input to the Flask backend and processes the response.
	- Updates the chatbox with user questions and AI responses.

## 🌟 Outcome

The web application allows users to interact with an AI chatbot via a simple web interface. It maintains context between interactions and processes user questions to provide intelligent responses. This setup demonstrates integrating a language model into a Flask application to create an interactive and context-aware chatbot experience. Additionally, LLM is installed locally. 

## 🛠️Step-by-Step Code Explanation (main.py file) -> backend 

### 1. Set Up the Flask Application 
Initialize the Flask application and set up the necessary imports: 
```
from flask import Flask, render_template, request, jsonify 
from langchain_ollama import OllamaLLM from langchain_core.prompts import ChatPromptTemplate 
app = Flask(__name__, template_folder='')
```

### 2. Define the Prompt Template
Create a template for structuring the chat prompt that includes conversation history and the user's question:
```
template = """
Answer the question below. 
Here is the conversation history {context}
Question: {question}
Answer:
"""

prompt = ChatPromptTemplate.from_template(template)

```

### 3. Initialize the Language Model and Chain
Set up the Ollama language model and create a processing chain with the prompt template:
```
model = OllamaLLM(model="llama3")
chain = prompt | model
```

### 4. Create Routes and Handlers
Define routes to render the main HTML page and handle chat interactions:
```
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
```
### 5. Run the Flask Application
Start the Flask application with debugging enabled:
```
if __name__ == "__main__":
    app.run(debug=True)
```

## 🛠️Step-by-Step Code Explanation (index.html file) -> frontend
### 1. HTML Structure
Create the HTML layout for the chat interface using Bootstrap for styling:
```
<!doctype html>
<html lang="en" class="h-100" data-bs-theme="auto">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Local AI ChatBot</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; }
        #chatbox { width: 100%; height: 500px; border: 1px solid #ccc; padding: 10px; overflow-y: scroll; margin-top: 20px; }
        #userInput { width: calc(100% - 22px); padding: 10px; margin-top: 10px; border: 1px solid #ccc; }
        #submitBtn { background-color: #712cf9; color: white; border: none; padding: 10px 20px; margin-top: 10px; cursor: pointer; }
        #submitBtn:hover { background-color: #5a1f8f; }
        .nav-link { color: white; }
        .nav-link.active { color: #712cf9; }
    </style>
</head>
<body class="d-flex h-100 text-center text-bg-dark">
    <div class="cover-container d-flex w-100 h-100 p-3 mx-auto flex-column">
        <header class="mb-auto">
            <div>
                <h3 class="float-md-start mb-0">Local AI ChatBot</h3>
                <nav class="nav nav-masthead justify-content-center float-md-end">
                    <a class="nav-link fw-bold py-1 px-0 active" aria-current="page" href="#">Home</a>
                </nav>
            </div>
        </header>
        <main class="px-3">
            <div id="chatbox"></div>
            <input type="text" id="userInput" placeholder="Ask me anything...">
            <button id="submitBtn" class="btn btn-light">Submit</button>
        </main>
        <footer class="mt-auto text-white-50">
            <p>Created by <a href="https://getbootstrap.com/" class="text-white">Michał Surmacz</a></p>
        </footer>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        let context = "";

        document.getElementById("submitBtn").addEventListener("click", function() {
            let question = document.getElementById("userInput").value;
            if (question.trim() === "") return;
            fetch("/ask", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question: question, context: context })
            })
            .then(response => response.json())
            .then(data => {
                let chatbox = document.getElementById("chatbox");
                chatbox.innerHTML += `<p><strong>You:</strong> ${question}</p>`;
                chatbox.innerHTML += `<p><strong>Bot:</strong> ${data.answer}</p>`;
                context = data.context;
                document.getElementById("userInput").value = "";
                chatbox.scrollTop = chatbox.scrollHeight;
            });
        });
    </script>
</body>
</html>
```
### 2. JavaScript for Handling User Input
Script to manage user interactions, send requests to the Flask backend, and update the chatbox:
```
let context = "";

document.getElementById("submitBtn").addEventListener("click", function() {
    let question = document.getElementById("userInput").value;
    if (question.trim() === "") return;
    fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: question, context: context })
    })
    .then(response => response.json())
    .then(data => {
        let chatbox = document.getElementById("chatbox");
        chatbox.innerHTML += `<p><strong>You:</strong> ${question}</p>`;
        chatbox.innerHTML += `<p><strong>Bot:</strong> ${data.answer}</p>`;
        context = data.context;
        document.getElementById("userInput").value = "";
        chatbox.scrollTop = chatbox.scrollHeight;
    });
});
```

## 🛠️ Step-by-Step Guide Before Running the Code

### 1. Install Required Packages
Ensure you have all the necessary packages installed. You can install them using pip:
```
pip install flask langchain_ollama langchain_core
```

### 2. Set Up Your Flask Application
Make sure you have Flask installed and that your application is set up correctly. The Flask app should be saved in a file. 

### 3. Verify Language Model Integration
-   `OllamaLLM`  should be correctly initialized with the  `"llama3"`  model.
-   `ChatPromptTemplate`  should be set up with the right template string for processing chat prompts.

### 4. Check the HTML Template
Ensure the HTML file, typically named  `index.html`, is properly set up in your project directory and contains the correct structure:
-   It should include Bootstrap for styling.
-   Ensure that the JavaScript code for handling user input and interaction is correctly implemented.

### 5. Validate Routes and Handlers
Check that your Flask routes are correctly defined:
-   The  `'/'`  route should render the main HTML page.
-   The  `'/ask'`  route should handle POST requests, process the user's question, and return a JSON response with the answer and updated context.

### Checklist Before Running the Code:

-   **Installed Packages:**  Ensure  `flask`,  `langchain_ollama`, and  `langchain_core`  are installed.
-   **Flask Setup:**  Verify that  `main.py`  contains the correct Flask application setup.
-   **Language Model Configuration:**  Check that  `OllamaLLM`  and  `ChatPromptTemplate`  are correctly configured.
-   **HTML File:**  Ensure  `index.html`  is in the correct location and properly formatted.
-   **Routes and Handlers:**  Confirm that Flask routes are correctly defined and functional.
-   **Running the Application:**  Use  `python main.py`  to start your Flask server and verify it runs without issues.

After confirming these steps, you should be able to successfully run and interact with your chat application. 
