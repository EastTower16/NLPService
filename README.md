# Text Sentiment Analysis Service

A high-performance sentiment analysis service that supports both Chinese and English text analysis, built with FastAPI and PaddlePaddle.

## Features

- Real-time sentiment analysis for single texts
- Batch processing for multiple texts
- Automatic language detection (Chinese/English)
- High concurrency support
- Containerized deployment
- RESTful API interface

## Prerequisites

- Python 3.9+
- Docker (for containerized deployment)
- PaddlePaddle models (Senta)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd NLPService
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download models:
Place the Senta models in the `models/senta` directory with the following structure:
```
models/senta/
├── cn_model/
│   ├── model.pdmodel
│   └── model.pdiparams
└── en_model/
    ├── model.pdmodel
    └── model.pdiparams
```

## Running the Service

### Local Development

```bash
uvicorn main:app --reload
```

### Docker Deployment

```bash
docker build -t sentiment-service .
docker run -p 8000:8000 sentiment-service
```

## API Usage

### Single Text Analysis

```bash
curl -X POST "http://localhost:8000/analyze" \
     -H "Content-Type: application/json" \
     -d '{"text": "我很喜欢这个产品"}'
```

Response:
```json
{
    "label": "positive",
    "confidence": 0.95
}
```

### Batch Analysis

```bash
curl -X POST "http://localhost:8000/batch_analyze" \
     -H "Content-Type: application/json" \
     -d '{"texts": ["我很喜欢这个产品", "差评", "还不错"]}'
```

Response:
```json
[
    {"label": "positive", "confidence": 0.95},
    {"label": "negative", "confidence": 0.87},
    {"label": "neutral", "confidence": 0.65}
]
```

## API Documentation

Once the service is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Monitoring

The service logs are stored in `logs/app.log`. Key metrics are exposed for Prometheus monitoring.

## License

[Your License] 