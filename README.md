# Flask LLM API

A lightweight Flask API that provides HTTP endpoints for text generation using Hugging Face transformers models. Configure your preferred LLM model via environment variables and start generating text through simple REST API calls.

## Features

- 🚀 **Easy Setup**: One-command installation and configuration
- 🔧 **Configurable**: Switch between different LLM models via `.env` file
- 🛡️ **Robust**: Comprehensive error handling and input validation
- 📊 **Monitoring**: Health check and model information endpoints
- 🎛️ **Flexible**: Configurable generation parameters (temperature, top_p, max_tokens)
- 📝 **Well-documented**: Clear API documentation and examples

## Installation

### Prerequisites

#### Linux (Ubuntu/Debian)

```bash
# Update package manager
sudo apt update

# Install Python 3.8+ and pip
sudo apt install python3 python3-pip python3-venv

# Install system dependencies (required for some ML packages)
sudo apt install build-essential python3-dev

# Optional: Install git if not present
sudo apt install git
```

#### Linux (CentOS/RHEL/Fedora)

```bash
# For CentOS/RHEL
sudo yum install python3 python3-pip python3-devel gcc gcc-c++ make

# For Fedora
sudo dnf install python3 python3-pip python3-devel gcc gcc-c++ make

# Optional: Install git if not present
sudo yum install git  # CentOS/RHEL
sudo dnf install git  # Fedora
```

#### macOS

```bash
# Install Homebrew if not present
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.8+ (if not using system Python)
brew install python@3.11

# Optional: Install git if not present
brew install git
```

#### Windows

```bash
# Install Python from python.org or Microsoft Store
# Ensure Python 3.8+ and pip are installed
# Git for Windows: https://git-scm.com/download/win
```

### Quick Start

#### 1. Clone or Download

```bash
git clone <your-repo-url>
cd thin_model_api
```

#### 2. Create Virtual Environment (Recommended)

**Linux/Mac:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

**Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

#### 3. Setup (Automated)

```bash
python setup.py
```

This will:
- Check Python version compatibility
- Install all required dependencies
- Create a `.env` file from `example.env`

#### 4. Start the Server

```bash
python app.py
```

#### 5. Test the API

```bash
python test_api.py
```

#### 6. Deactivate Virtual Environment (When Done)

```bash
deactivate
```

**Note:** Always activate your virtual environment before working on the project:
```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

## Manual Installation

If you prefer manual setup:

```bash
# Install dependencies
pip install -r requirements.txt

# Create environment file
cp example.env .env

# Edit .env with your preferred settings
nano .env

# Start the server
python app.py
```

## Configuration

Edit the `.env` file to customize your setup:

```env
# Model configuration
model_name=gpt2

# Server configuration
HOST=0.0.0.0
PORT=5000

# Generation parameters
MAX_TOKENS_DEFAULT=50
MAX_TOKENS_LIMIT=500
```

### Supported Models

The API supports any Hugging Face model that works with `AutoModelForCausalLM`. Popular options include:

- `gpt2` - Small, fast, good for testing
- `distilgpt2` - Smaller version of GPT-2
- `microsoft/DialoGPT-small` - Conversational model
- `microsoft/DialoGPT-medium` - Larger conversational model
- `EleutherAI/gpt-neo-1.3B` - Larger model (requires more RAM)

## API Endpoints

### Health Check
```http
GET /
```

**Response:**
```json
{
  "status": "healthy",
  "model": "gpt2",
  "version": "1.0.0"
}
```

### Generate Text
```http
POST /generate
Content-Type: application/json

{
  "prompt": "Once upon a time",
  "max_tokens": 100,
  "temperature": 0.8,
  "do_sample": true,
  "top_p": 0.9
}
```

**Response:**
```json
{
  "response": " there was a young princess who lived in a beautiful castle...",
  "full_text": "Once upon a time there was a young princess who lived in a beautiful castle...",
  "model": "gpt2",
  "tokens_generated": 45
}
```

### Model Information
```http
GET /model-info
```

**Response:**
```json
{
  "model_name": "gpt2",
  "vocab_size": 50257,
  "model_max_length": 1024,
  "pad_token": "<|endoftext|>",
  "eos_token": "<|endoftext|>"
}
```

## Usage Examples

### Python

```python
import requests

# Generate text
response = requests.post('http://localhost:5000/generate', json={
    "prompt": "The future of AI is",
    "max_tokens": 75,
    "temperature": 0.7
})

result = response.json()
print(result['response'])
```

### cURL

```bash
# Generate text
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "In a world where",
    "max_tokens": 50,
    "temperature": 0.8
  }'

# Health check
curl http://localhost:5000/

# Model info
curl http://localhost:5000/model-info
```

### JavaScript/Node.js

```javascript
const response = await fetch('http://localhost:5000/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    prompt: 'The most important thing about programming is',
    max_tokens: 60,
    temperature: 0.7
  })
});

const result = await response.json();
console.log(result.response);
```

## Request Parameters

### `/generate` endpoint

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | Yes | - | Text prompt to generate from |
| `max_tokens` | integer | No | 50 | Maximum tokens to generate |
| `temperature` | float | No | 1.0 | Sampling temperature (0.0-2.0) |
| `top_p` | float | No | 1.0 | Top-p sampling parameter |
| `do_sample` | boolean | No | true | Whether to use sampling |

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- `400 Bad Request` - Invalid input or missing required fields
- `500 Internal Server Error` - Model loading or generation errors

Example error response:
```json
{
  "error": "No prompt provided"
}
```

## Performance Considerations

- **Model Loading**: The model loads on startup, which may take a few minutes for larger models
- **Memory Usage**: Larger models require more RAM (GPT-2: ~500MB, GPT-Neo-1.3B: ~5GB)
- **Generation Speed**: Depends on model size and hardware (CPU vs GPU)

## Troubleshooting

### Common Issues

1. **Model Download Fails**
   - Check internet connection
   - Verify model name is correct
   - Some models require Hugging Face authentication

2. **Out of Memory**
   - Use a smaller model (`distilgpt2` instead of `gpt2`)
   - Reduce `max_tokens` in requests
   - Consider using a GPU or more RAM

3. **Slow Generation**
   - Use a smaller model for faster inference
   - Reduce `max_tokens` parameter
   - Consider using a GPU

### Platform-Specific Issues

#### Linux

**Issue: `gcc` compilation errors during pip install**
```bash
# Ubuntu/Debian
sudo apt install build-essential python3-dev

# CentOS/RHEL
sudo yum groupinstall "Development Tools"
sudo yum install python3-devel

# Fedora
sudo dnf groupinstall "Development Tools"
sudo dnf install python3-devel
```

**Issue: Permission denied errors**
```bash
# Use virtual environment instead of system Python
python3 -m venv venv
source venv/bin/activate
```

**Issue: `ModuleNotFoundError` even after installation**
```bash
# Make sure you're using the correct Python/pip
which python3
which pip3

# Or use python -m pip instead of pip
python3 -m pip install -r requirements.txt
```

#### macOS

**Issue: `clang` compilation errors**
```bash
# Install Xcode command line tools
xcode-select --install

# Or install via Homebrew
brew install gcc
```

**Issue: SSL certificate errors**
```bash
# Update certificates
/Applications/Python\ 3.x/Install\ Certificates.command

# Or install via Homebrew
brew install ca-certificates
```

**Issue: Python version conflicts**
```bash
# Use Homebrew Python
brew install python@3.11
export PATH="/opt/homebrew/bin:$PATH"

# Or use pyenv for version management
brew install pyenv
pyenv install 3.11.0
pyenv global 3.11.0
```

#### Windows

**Issue: `Microsoft Visual C++ 14.0 is required`**
- Install Visual Studio Build Tools
- Or install Visual Studio Community with C++ workload

**Issue: Long path errors**
```bash
# Run as administrator and enable long paths
git config --system core.longpaths true
```

**Issue: Permission errors with pip**
```bash
# Use --user flag or virtual environment
pip install --user -r requirements.txt
```

### Logs

The application logs important information to help with debugging:

```bash
python app.py
# INFO:__main__:Loading model: gpt2
# INFO:__main__:Model gpt2 loaded successfully
# INFO:__main__:Starting server on 0.0.0.0:5000
```

## Development

### File Structure

```
thin_model_api/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── example.env        # Configuration template
├── .env              # Your configuration (created by setup)
├── test_api.py       # API test script
├── setup.py          # Setup script
└── README.md         # This file
```

### Running Tests

```bash
# Start the server in one terminal
python app.py

# Run tests in another terminal
python test_api.py
```

## Requirements

- Python 3.8+
- 2-8GB RAM (depending on model size)
- Internet connection (for initial model download)

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

If you encounter any issues:

1. Check the logs for error messages
2. Verify your `.env` configuration
3. Ensure you have sufficient RAM for your chosen model
4. Check the [Hugging Face model page](https://huggingface.co/models) for model-specific requirements

---

**Happy generating!** 🚀 