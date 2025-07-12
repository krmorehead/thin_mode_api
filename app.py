from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration from environment variables
MODEL_NAME = os.getenv("model_name", "gpt2")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "5000"))
MAX_TOKENS_DEFAULT = int(os.getenv("MAX_TOKENS_DEFAULT", "50"))
MAX_TOKENS_LIMIT = int(os.getenv("MAX_TOKENS_LIMIT", "500"))

# Global variables for model and tokenizer
model = None
tokenizer = None

def load_model():
    """Load the model and tokenizer"""
    global model, tokenizer
    try:
        logger.info(f"Loading model: {MODEL_NAME}")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
        
        # Add padding token if it doesn't exist
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            model.config.pad_token_id = model.config.eos_token_id
            
        logger.info(f"Model {MODEL_NAME} loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model {MODEL_NAME}: {str(e)}")
        raise

@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model": MODEL_NAME,
        "version": "1.0.0"
    })

@app.route("/generate", methods=["POST"])
def generate():
    """Generate text based on prompt"""
    try:
        # Check if model is loaded
        if model is None or tokenizer is None:
            return jsonify({"error": "Model not loaded"}), 500
        
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        prompt = data.get("prompt", "")
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400
        
        # Get max_tokens with validation
        max_tokens = data.get("max_tokens", MAX_TOKENS_DEFAULT)
        if max_tokens > MAX_TOKENS_LIMIT:
            max_tokens = MAX_TOKENS_LIMIT
        
        # Get other generation parameters
        do_sample = data.get("do_sample", True)
        temperature = data.get("temperature", 1.0)
        top_p = data.get("top_p", 1.0)
        
        # Tokenize input
        inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
        
        # Generate response
        with torch.no_grad():
            outputs = model.generate(
                inputs.input_ids,
                max_new_tokens=max_tokens,
                do_sample=do_sample,
                temperature=temperature,
                top_p=top_p,
                pad_token_id=tokenizer.pad_token_id,
                attention_mask=inputs.attention_mask if 'attention_mask' in inputs else None
            )
        
        # Decode the generated text
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Remove the original prompt from the response
        response_text = generated_text[len(prompt):].strip()
        
        return jsonify({
            "response": response_text,
            "full_text": generated_text,
            "model": MODEL_NAME,
            "tokens_generated": len(outputs[0]) - len(inputs['input_ids'][0])
        })
        
    except Exception as e:
        logger.error(f"Error generating text: {str(e)}")
        return jsonify({"error": f"Generation failed: {str(e)}"}), 500

@app.route("/model-info", methods=["GET"])
def model_info():
    """Get information about the loaded model"""
    if model is None or tokenizer is None:
        return jsonify({"error": "Model not loaded"}), 500
    
    return jsonify({
        "model_name": MODEL_NAME,
        "vocab_size": tokenizer.vocab_size,
        "model_max_length": tokenizer.model_max_length,
        "pad_token": tokenizer.pad_token,
        "eos_token": tokenizer.eos_token
    })

if __name__ == "__main__":
    try:
        # Load model on startup
        load_model()
        
        logger.info(f"Starting server on {HOST}:{PORT}")
        app.run(host=HOST, port=PORT, debug=False)
        
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        logger.error("Make sure you have internet connection and the model name is correct in .env file")
        exit(1) 