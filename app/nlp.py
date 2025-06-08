
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("DeepPavlov/rubert-base-cased")
model = AutoModelForSequenceClassification.from_pretrained("model/")
labels = ["contact_problem", "delay", "document_issue", "address_error"]

def classify_message(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
        probs = F.softmax(logits, dim=1).numpy()[0]
    best_index = probs.argmax()
    return {
        "category": labels[best_index],
        "confidence": float(probs[best_index])
    }
