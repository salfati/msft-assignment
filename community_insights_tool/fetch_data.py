import requests

STACK_OVERFLOW_API_URL = "https://api.stackexchange.com/2.3/search"
DEFAULT_TAG = "microsoft-teams"

def fetch_stackoverflow_questions(tag=DEFAULT_TAG, pagesize=10):
    params = {
        "order": "desc",
        "sort": "activity",
        "tagged": tag,
        "site": "stackoverflow",
        "pagesize": pagesize
    }

    response = requests.get(STACK_OVERFLOW_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        questions = [{
            "title": item["title"],
            "link": item["link"],
            "body": item.get("body", ""),
            "tags": item.get("tags", []),
            "question_id": item["question_id"]
        } for item in data.get("items", [])]
        return questions
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

if __name__ == "__main__":
    results = fetch_stackoverflow_questions()
    for i, question in enumerate(results, 1):
        print(f"{i}. {question['title']} ({question['link']})")
