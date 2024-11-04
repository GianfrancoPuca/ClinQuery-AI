from flask import Flask, request, jsonify, render_template
from bot import load_intents, get_response


app = Flask(__name__, static_folder="static", template_folder="templates")


intents = load_intents()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_input = data.get("question")
    
    response = get_response(user_input, intents)
    

    return jsonify({"answer": response})

if __name__ == '__main__':
    app.run(debug=True)

