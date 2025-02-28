import requests 


def get_video_questions():
    return {
        "audio_url":"https://www.youtube.com/watch?v=XZCzgy3eGsE",
        "correct_answer":"1",
        "options":[
            {"title": "Option A", "id": "1"},
            {"title": "Option B", "id": "2"},
            {"title": "Option C", "id": "3"},
            {"title": "Option D", "id": "4"},
        ]
    }
    # response = requests.get('http://localhost:5000/video_questions')
    # return response.json()