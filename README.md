# ClinQuery-AI

# ClinQuery-AI

**ClinQuery-AI** is an advanced web application designed to streamline data querying and retrieval in healthcare settings. With a **BERT-powered AI chatbot**, the project offers real-time interaction capabilities that recognize user intent and respond to complex questions about clinical and administrative data. ClinQuery-AI combines robust backend logic in Python with a responsive, interactive frontend.

## Key Features

- **AI-driven Chatbot**: Utilizes a BERT-based model to recognize and respond to healthcare-related queries with high accuracy.
- **Backend Support**: Powered by Flask, facilitating efficient API management.
- **Database Integration**: Connects with a MySQL database via `mysql-connector-python` to process and retrieve data.
- **Intent Recognition and Extraction**: Recognizes complex user intents and extracts relevant data points for precise query execution.
- **Interactive Frontend**: Built with HTML, CSS, and JavaScript, providing a user-friendly interface that works on both desktop and mobile devices.
- **Scalability and Modularity**: Easy integration with other web services, designed for extensibility across various healthcare applications.

## Project Structure

- **Backend**: Flask-based Python API with endpoints to interact with the chatbot and database.
- **Frontend**: HTML/CSS/JavaScript interface, ensuring real-time, dynamic responses from the AI.
- **Database**: MySQL setup to handle clinical and administrative queries, managed by SQLAlchemy for ORM operations.
- **Machine Learning**: Implements the `transformers` library for NLP, with BERT fine-tuning for customized intent recognition.

## Training and Intent Recognition

**ClinQuery-AI** is trained using a detailed JSON-based dataset, `mydetails.json`, containing over 10,000 patterns to map complex user queries into actionable SQL responses. The training process uses **BERT**, optimized through the `transformers` library, and includes advanced techniques such as **parameter extraction**, allowing dynamic input handling without static keyword matching.

## Installation and Setup

### Requirements

The project requires several packages, listed in `requirements.txt`, including:

- **Core AI and NLP**: `transformers`, `torch`
- **Web Framework**: `flask`
- **Database**: `mysql-connector-python`
- **Environment Management**: `python-dotenv`


## System Requirements

- **Python 3.8+**
- **MySQL Database**
- **Tested on major web browsers** for frontend compatibility.

## Future Enhancements

- **Additional NLP Models**: Potential to incorporate DeBERTa or other models for even higher accuracy.
- **Expanded Intent Recognition**: Addition of more intents and refined training for improved query understanding.
- **Customizable Query Parameters**: Real-time parameter tuning based on user query patterns.

**ClinQuery-AI** represents a powerful tool for real-time, AI-powered interaction with clinical data, enhancing accessibility and usability across various healthcare operations.







