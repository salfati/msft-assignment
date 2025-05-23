import openai
import os

# Set your OpenAI API key
openai.api_key = ""

def extract_pain_points(questions, model="gpt-4o-mini"):
    extracted_insights = []
    for q in questions:
        prompt = f"""
You are an AI assistant that helps product teams identify developer pain points.

Below is a Stack Overflow question:
---
Title: {q['title']}
Tags: {", ".join(q['tags'])}
Link: {q['link']}
---

Extract and summarize the main developer pain point from this content. Be concise and technical. Format the result like this:

- Pain Point: <short summary>
- Category: <UI/UX/API/Auth/Etc>
- Suggestion: <improvement or fix>
"""

        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You extract pain points from developer content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )

            ai_output = response["choices"][0]["message"]["content"]
            extracted_insights.append({
                "question_id": q["question_id"],
                "title": q["title"],
                "insight": ai_output
            })

        except Exception as e:
            extracted_insights.append({
                "question_id": q["question_id"],
                "title": q["title"],
                "insight": f"Error: {str(e)}"
            })

    return extracted_insights

if __name__ == "__main__":
    from fetch_data import fetch_stackoverflow_questions

    questions = fetch_stackoverflow_questions()
    insights = extract_pain_points(questions)

    for insight in insights:
        print(f"\nTitle: {insight['title']}\nInsight:\n{insight['insight']}\n")
