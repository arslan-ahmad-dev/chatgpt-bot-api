import os
import openai
from dotenv import load_dotenv
from flask import Flask, request, jsonify, abort

load_dotenv()
app = Flask(__name__)

class ChatGPTBotAPI:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.prompts = []
        
        if not self.api_key:
            print("OpenAI API key is missing. Set OPENAI_API_KEY in environment variables.")
        else:
            openai.api_key = self.api_key

    def create_prompt(self, prompt):
        self.prompts.append(prompt)
        return {"message": "Prompt added successfully", "index": len(self.prompts) - 1}

    def get_response(self, prompt_index):
        if 0 <= prompt_index < len(self.prompts):
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": self.prompts[prompt_index]}]
            )

            return {"response": response.choices[0].message.content}

        return {"error": "Invalid prompt index"}

    def update_prompt(self, prompt_index, new_prompt):
        if 0 <= prompt_index < len(self.prompts):
            self.prompts[prompt_index] = new_prompt
            return {"message": "Prompt updated successfully"}
        
        abort(400, "Invalid prompt index")

    def list_prompts(self):
        return {"prompts": self.prompts}

chatbot = ChatGPTBotAPI()

@app.route("/create_prompt", methods=["POST"])
def create_prompt():
    data = request.json
    if "prompt" not in data:
        abort(400, "Missing 'prompt' field in request")
    
    return jsonify(chatbot.create_prompt(data["prompt"]))

@app.route("/get_response/<int:prompt_index>", methods=["GET"])
def get_response(prompt_index):
    return jsonify(chatbot.get_response(prompt_index))

@app.route("/update_prompt/<int:prompt_index>", methods=["PUT"])
def update_prompt(prompt_index):
    data = request.json
    if "new_prompt" not in data:
        abort(400, "Missing 'new_prompt' field in request")
    
    return jsonify(chatbot.update_prompt(prompt_index, data["new_prompt"]))

@app.route("/list_prompts", methods=["GET"])
def list_prompts():
    """Fetch all stored prompts."""
    return jsonify(chatbot.list_prompts())

if __name__ == "__main__":
    app.run(debug=True)
