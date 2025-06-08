
from fastapi import FastAPI
from pydantic import BaseModel
from kafka import KafkaProducer
import json
import logging
from app.nlp import classify_message
from app.db import get_contacts_and_address
from app.pdf_generator import generate_pdf

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()

class MessageRequest(BaseModel):
    text: str
    driver_id: int
    company_id: int
    order_id: int
    vehicle_id: int
    route_id: int

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

@app.post("/messages")
def process_message(data: MessageRequest):
    logging.info(f"New message from driver {data.driver_id}: {data.text}")

    classification = classify_message(data.text)
    logging.info(f"Category: {classification['category']} (confidence: {classification['confidence']})")

    payload = {
        "text": data.text,
        "category": classification["category"],
        "confidence": classification["confidence"],
        "driver_id": data.driver_id,
        "company_id": data.company_id,
        "order_id": data.order_id,
        "vehicle_id": data.vehicle_id,
        "route_id": data.route_id,
    }

    if classification["category"] == "contact_problem":
        contacts, address = get_contacts_and_address(data.order_id, data.company_id, data.route_id)
        payload["contacts"] = contacts
        payload["destination_address"] = address
        logging.info(f"Contacts: {contacts}, address: {address}")

    pdf_path = generate_pdf(payload)
    payload["pdf_url"] = pdf_path
    logging.info(f"PDF generated: {pdf_path}")

    producer.send("nlp.result", payload)
    producer.flush()

    return {"status": "ok", "result": payload}
