# 🏥 Hospital Information System RAG Assistant

A AI-powered healthcare information system with natural language querying capabilities using RAG (Retrieval-Augmented Generation) and CRUD operations management.

## Features

- **Medical Q&A**: Ask natural language questions about hospital services, physicians, and policies
- **Vector Search**: FAISS-based similarity search for relevant medical information
- **Admin Panel**: Streamlit-based CRUD operations for database management
- **AI Integration**: Google Gemini for embeddings and response generation
- **SQL Backend**: Microsoft SQL Server database integration

## Project Structure
hospital-rag-system/</br>
├── app.py # FastAPI backend</br>
├── streamlit_app.py # Patient-facing chatbot UI</br>
├── streamlit_admin.py # Admin CRUD interface</br>
├── database.py # Database connection & operations</br>
├── embeddings.py # Custom Gemini embeddings</br>
├── vector_store.py # FAISS vector store management</br>
├── query_processor.py # RAG pipeline logic</br>
├── requirements.txt # Dependency list</br>
└── .env.example # Environment variables template

----------------

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- [SQL Server](https://www.microsoft.com/en-us/sql-server/) database
- [Google Gemini API Key](https://ai.google.dev/)
- ODBC Driver 17 for SQL Server

### Installation

1. Clone repository:
```bash
git clone https://github.com/yourusername/hospital-rag-system.git
cd hospital-rag-system
```
2. Install dependencies:

```bash
pip install -r requirements.txt
```
3. Create .env file:

```bash
cp .env.example .env
```
Edit .env with your credentials or use them directly on code:

```bash
GEMINI_API_KEY=your_google_ai_key
DB_SERVER=your_sql_server_name
DB_NAME=your_database_name
```
Database Setup
Create SQL Server database with these tables:

Physicians

Policy

Pricelist

Schedules

Specialities

Configure table structures according to database.py

## Running the System
Start FastAPI backend:

```bash
uvicorn app:app --reload
```
Start Streamlit Chat UI:

```bash
streamlit run streamlit_app.py
```
Start Admin Panel (optional):
```bash
streamlit run streamlit_admin.py
```

### 🖥️ Usage
#### Chat Interface (Patient)
Access at http://localhost:8501

##### **Ask questions like**:

"What's the price of MRI scan?"

"Show me available cardiologists"

"What are your visiting hours?"

##### **Admin Panel**
Access at http://localhost:8502

Features:

Create/Update/Delete records

Manage physician schedules

Update service prices

Modify hospital policies