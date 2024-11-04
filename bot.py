import json
import random
import re
import mysql.connector
from transformers import BertTokenizer, BertForSequenceClassification
import torch
from dotenv import load_dotenv
import os

load_dotenv()

bert_tokenizer = BertTokenizer.from_pretrained('./fine-tuned-bert')
bert_model = BertForSequenceClassification.from_pretrained('./fine-tuned-bert')

device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
bert_model.to(device)

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        if connection.is_connected():
            print("Connessione al database riuscita!")
        return connection
    except mysql.connector.Error as e:
        print(f"Errore di connessione: {e}")
        return None

def execute_dynamic_query(query, connection):
    if connection is None:
        return "Errore: Connessione al database non riuscita."
    
    try:
        print(f"Eseguo la query: {query}")
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        
        print(f"Risultati della query: {results}")
        
        if results:
            output = "\n".join([str(row) for row in results])
            return f"Ho trovato i seguenti risultati:\n{output}"
        else:
            return "Nessun risultato trovato."
    except mysql.connector.Error as e:
        return f"Errore nell'esecuzione della query: {e}"
    finally:
        if 'cursor' in locals():
            cursor.close()

def load_intents():
    with open('mydetails.json') as file:
        data = json.load(file)
        return data

def classify_intent(user_input):
    inputs = bert_tokenizer(user_input, return_tensors="pt", padding=True, truncation=True).to(device)
    outputs = bert_model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=-1)
    return predictions.item()

def get_response(user_input, intents):
    intent_id = classify_intent(user_input)
    matched_intent = list(intents['intents'])[intent_id]
    print(f"Intento primario riconosciuto: {matched_intent['tag']}")
    
    query_template = random.choice(matched_intent['responses'])
    params = matched_intent.get('params', [])
   
    extracted_values = extract_parameters(user_input, params)
    missing_params = [param for param in params if not extracted_values.get(param)]
    
    if missing_params:
        return f"Errore: Non sono riuscito a trovare il valore per {', '.join(missing_params)} nell'input."
    
    for param, value in extracted_values.items():
        query_template = query_template.replace(f"{{{param}}}", value)
    
    print(f"Query SQL da eseguire: {query_template}")
    connection = connect_to_db()
    if connection and connection.is_connected():
        response = execute_dynamic_query(query_template, connection)
        connection.close()
    else:
        response = "Errore: Connessione al database fallita."
    return response

def extract_parameters(user_input, params):
    extracted_values = {}
    param_patterns = {
        'location': r'\b(?:in|nella|a|per|su|da)\s+([A-Za-z\s]+)\b',
        'device_type': r'\b(?:tipo|dispositivo|di tipo)\s+([A-Za-z\s]+)\b',
        'name': r'\b(?:nome|intitolato|denominato|chiamato)\s+([A-Za-z\s]+)\b',
        'id': r'\b(?:ID|identificatore|numero)\s+(\d+)\b',
        'hq': r'\b(?:HQ|sede|quartiere)\s+([A-Za-z0-9]+)\b',
        'mail': r'\b(?:email|mail)\s+([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})\b',
    }
    for param in params:
        pattern = param_patterns.get(param)
        if pattern:
            match = re.search(pattern, user_input)
            if match:
                extracted_values[param] = match.group(1)
    return extracted_values

def load_google_credentials():
    google_creds = {
        "type": os.getenv("GOOGLE_TYPE"),
        "project_id": os.getenv("GOOGLE_PROJECT_ID"),
        "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
        "private_key": os.getenv("GOOGLE_PRIVATE_KEY").replace('\\n', '\n'),
        "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
        "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("GOOGLE_AUTH_PROVIDER_CERT_URL"),
        "client_x509_cert_url": os.getenv("GOOGLE_CLIENT_CERT_URL"),
    }
    return google_creds
