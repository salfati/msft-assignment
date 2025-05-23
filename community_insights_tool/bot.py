from flask import Flask, request, render_template_string, session, redirect, url_for
from extract_feedback import extract_pain_points
from fetch_data import fetch_stackoverflow_questions
import openai
import os
from flask_session import Session

openai.api_key = ""

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Configure server-side session
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_FILE_DIR"] = "./flask_session"
Session(app)

@app.route("/clear")
def clear_session():
    session.clear()
    return redirect(url_for("chat"))

@app.route("/", methods=["GET", "POST"])
def chat():
    if "questions" not in session:
        session["questions"] = fetch_stackoverflow_questions()
        session["insights"] = extract_pain_points(session["questions"])
        session["conversation"] = []

    questions = session["questions"]
    insights = session["insights"]
    conversation = session["conversation"]

    if request.method == "POST":
        if "question_index" in request.form:
            selected_index = int(request.form["question_index"])
            session["selected_index"] = selected_index

            selected_question = questions[selected_index]
            selected_insight = insights[selected_index]["insight"]

            conversation.clear()
            conversation.append({
                "from": "user",
                "message": f"{selected_question['title']}"
            })
            conversation.append({
                "from": "bot",
                "message": f"<b>Insight:</b><br><pre>{selected_insight}</pre><br><a href='{selected_question['link']}' target='_blank'>View on Stack Overflow</a>"
            })

        elif "followup" in request.form:
            user_input = request.form["followup"]
            conversation.append({
                "from": "user",
                "message": user_input
            })

            messages = [
                {"role": "system", "content": "You are a helpful AI assistant who provides technical product suggestions based on extracted developer insights."}
            ]
            for msg in conversation:
                role = "user" if msg["from"] == "user" else "assistant"
                messages.append({"role": role, "content": msg["message"]})

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=messages,
                    temperature=0.5
                )
                reply = response["choices"][0]["message"]["content"]
            except Exception as e:
                reply = f"Error calling OpenAI API: {str(e)}"

            conversation.append({
                "from": "bot",
                "message": reply
            })

        session["conversation"] = conversation
        return redirect(url_for("chat"))

    return render_template_string("""
        <html>
        <head>
            <title>Community Insights Chatbot</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: #f4f4f4;
                    display: flex;
                    justify-content: center;
                }
                .chat-container {
                    margin-top: 40px;
                    background: white;
                    padding: 20px;
                    width: 700px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }
                .message { margin-bottom: 15px; }
                .user { text-align: right; color: #444; }
                .bot { text-align: left; color: #0078d4; }
                .button-container {
                    margin-top: 20px;
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                }
                form { display: inline; }
                button {
                    padding: 10px 15px;
                    border: none;
                    background: #0078d4;
                    color: white;
                    border-radius: 5px;
                    cursor: pointer;
                    text-align: left;
                    white-space: normal;
                    word-wrap: break-word;
                }
                button:hover { background: #005ea2; }
                pre {
                    background: #f0f0f0;
                    padding: 10px;
                    border-radius: 5px;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }
                input[type='text'] {
                    width: 100%;
                    padding: 10px;
                    margin-top: 10px;
                    border-radius: 5px;
                    border: 1px solid #ccc;
                }
            </style>
        </head>
        <body>
            <div class="chat-container">
                <h2>Community Insights Chatbot</h2>
                <div style="text-align: right;">
                    <a href="{{ url_for('clear_session') }}">Clear Session</a>
                </div>
                {% for msg in conversation %}
                    <div class="message {{ msg['from'] }}">
                        <div>{{ msg['message']|safe }}</div>
                    </div>
                {% endfor %}

                <form method="POST">
                    <input type="text" name="followup" placeholder="Type your response here..." required />
                    <button type="submit">Send</button>
                </form>

                <hr>
                <div class="button-container">
                    {% for q in questions %}
                        <form method="POST">
                            <input type="hidden" name="question_index" value="{{ loop.index0 }}" />
                            <button type="submit">{{ q['title'] }}</button>
                        </form>
                    {% endfor %}
                </div>
            </div>
        </body>
        </html>
    """, questions=questions, insights=insights, conversation=conversation)

if __name__ == "__main__":
    app.run(debug=True)
