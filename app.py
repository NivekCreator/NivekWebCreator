from flask import Flask, request, render_template, session
import openai

app = Flask(__name__)
app.secret_key = "5404"
openai.api_key = "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"

@app.route('/')
def index():
    session['conversation'] = []
    return render_template('index.html')

@app.route('/get', methods=['POST'])
def get_bot_response():
    user_input = request.form['user_input']
    conversation = session.get('conversation', [])
    conversation.append(f"User: {user_input}")

    conversation_str = "\n".join(conversation)
    prompt = f"{conversation_str}\nAI:"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.5,
    )
    response_text = response.choices[0].text.strip()
    conversation.append(f"AI: {response_text}")
    session['conversation'] = conversation

    return render_template('response.html', response_text=response_text)

if __name__ == '__main__':
    app.run(debug=True)
