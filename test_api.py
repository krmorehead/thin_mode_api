#!/usr/bin/env python3
"""
Simple test script for the Flask LLM API
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_model_info():
    """Test the model info endpoint"""
    print("Testing model info...")
    response = requests.get(f"{BASE_URL}/model-info")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_generate(prompt, max_tokens=50, temperature=1.0):
    """Test the generate endpoint"""
    print(f"Testing text generation with prompt: '{prompt}'")
    
    data = {
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "do_sample": True
    }
    
    response = requests.post(
        f"{BASE_URL}/generate",
        headers={"Content-Type": "application/json"},
        json=data
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Generated text: {result['response']}")
        print(f"Model used: {result['model']}")
        print(f"Tokens generated: {result['tokens_generated']}")
    else:
        print(f"Error: {response.json()}")
    print()

if __name__ == "__main__":
    # Test all endpoints
    test_health_check()
    test_model_info()
    
    # Test text generation with different prompts
    test_generate("Once upon a time", max_tokens=100)
    test_generate("The future of AI is", max_tokens=75)
    test_generate("In a world where", max_tokens=50, temperature=0.8)
    
    print("All tests completed!") 