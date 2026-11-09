"""Emotion classification client using the Watson NLP service."""

import requests

WATSON_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text_to_analyze):
    """Return the five emotion scores and the dominant emotion for input text."""
    payload = {"raw_document": {"text": text_to_analyze}}
    response = requests.post(WATSON_URL, json=payload, headers=HEADERS, timeout=30)

    if response.status_code == 400:
        return {**dict.fromkeys(EMOTIONS), "dominant_emotion": None}

    response.raise_for_status()
    data = response.json()
    scores = data["emotionPredictions"][0]["emotion"]
    dominant = max(scores, key=scores.get)
    return {
        **{emotion: scores[emotion] for emotion in EMOTIONS},
        "dominant_emotion": dominant,
    }
