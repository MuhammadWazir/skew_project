# Skew AI Backend Service

A backend service for PDF knowledge management with semantic search and AI-powered chat capabilities.

## Features

- **PDF Management**: Upload and delete PDF files
- **Semantic Search**: Natural language search across PDF content using vector embeddings
- **AI Chat**: Intelligent chat endpoint with selective tool calling for context-aware responses
- **Vector Database**: Efficient storage and retrieval using embeddings
- **API Documentation**: Interactive Swagger UI for easy testing

## Tech Stack

- **Framework**: FastAPI (Python 3.9+)
- **Vector Database**: QDrant
- **Embeddings**: OpenAI text-embedding-3-small
- **LLM**: OpenAI GPT-5-mini
- **API Docs**: Swagger UI (built-in with FastAPI)


## Installation


1. **Clone the repository**
```bash
git clone https://github.com/MuhammadWazir/skew_project
```

2. **Create a virtual environment**
Create the .venv with the dependencies using uv sync

4. **Set up environment variables**
The variables should be same as in src/infrastructure/config/config.py

5. **Run the service**
```bash
uv run main.py
```

## Usage

Once the service is running, access:
- **API Documentation**: http://localhost:8000/docs


## Key Implementation Details

### PDF Processing
- Extracts text using PDFPlumber
- Cleans text by removing excessive whitespace and special characters
- Chunks text into 512 tokens with 128 tokens overlap

### Embeddings
- Uses OpenAI's `text-embedding-3-small` model (1536 dimensions)
- Generates embeddings for each text chunk
- Stores with metadata: filename, chunk_index, original_text

### Vector Search
- QDrant for efficient similarity search
- Cosine similarity scoring
- Returns top-k results sorted by relevance score

### Selective Tool Calling
The chat endpoint intelligently decides when to search the vector database

## Testing

### Using Swagger UI
1. Navigate to http://localhost:8000/docs
2. Try the endpoints in order:
   - Upload a PDF file
   - Search with a query
   - Chat with questions about the content
   - Delete the PDF when done


All errors return appropriate HTTP status codes and descriptive messages.



## Future Enhancements

- Support for multiple file formats (DOCX, TXT, etc.)
- User authentication and file ownership
- Conversation history in chat
- Rate limiting and usage quotas
- Batch upload support
