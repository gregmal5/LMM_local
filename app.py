from flask import Flask, render_template, request, jsonify
from ctransformers import AutoModelForCausalLM
import datetime
import requests
import sys
import os

app = Flask(__name__)

# Model handling
MODEL_FILE = "Bielik-11B-v2.3-Instruct.Q4_K_M.gguf"
llm = None

def load_model():
    global llm
    if os.path.exists(MODEL_FILE):
        # Try loading with GPU first
        try:
            print("Loading Model with GPU support...")
            llm = AutoModelForCausalLM.from_pretrained(
                MODEL_FILE, 
                model_type="llama", 
                context_length=2048,
                gpu_layers=50
            )
            print("Model Loaded Successfully (GPU).")
        except Exception as e:
            print(f"Failed to load with GPU: {e}")
            print("Falling back to CPU only...")
            try:
                llm = AutoModelForCausalLM.from_pretrained(
                    MODEL_FILE, 
                    model_type="llama", 
                    context_length=2048
                )
                print("Model Loaded Successfully (CPU).")
            except Exception as e2:
                print(f"Failed to load model (CPU): {e2}")
    else:
        print("Model file not found. Please wait for download or run download_model.py")

# Try initial load
load_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/time')
def get_time():
    now = datetime.datetime.now()
    return f"{now.strftime('%H:%M')}"

@app.route('/weather')
def get_weather():
    try:
        # Katowice
        url = "https://api.open-meteo.com/v1/forecast?latitude=50.2584&longitude=19.0275&current=temperature_2m,weather_code"
        r = requests.get(url, timeout=2).json()
        current = r['current']
        temp = current['temperature_2m']
        code = current['weather_code']
        
        # Simple WMO to OpenWeatherMap icon mapping
        icon_code = "01d" # clear
        if code in [1, 2, 3]: icon_code = "02d" # clouds
        elif code in [45, 48]: icon_code = "50d" # fog
        elif code in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82]: icon_code = "10d" # rain
        elif code in [71, 73, 75, 77, 85, 86]: icon_code = "13d" # snow
        elif code in [95, 96, 99]: icon_code = "11d" # thunder
        elif code >= 4: icon_code = "03d" # overcast/other

        icon_url = f"https://openweathermap.org/img/wn/{icon_code}.png"
        return jsonify({"temp": f"{temp} C", "icon": icon_url}) 
    except Exception as e:
        print(e)
        return jsonify({"error": "failed"})

@app.route('/generate', methods=['POST'])
def generate():
    global llm
    if not llm:
        # Try loading again if it finished downloading
        load_model()
        if not llm:
            return jsonify({"response": "Model is still loading or not found. Please wait."})
            
    data = request.json
    prompt = data.get('prompt', '')
    
    # Bielik Chat Template
    # <s>[INST] Instruction [/INST] Model answer</s>
    # We will just append the user prompt
    full_prompt = f"[INST] {prompt} [/INST]"
    
    response_text = ""
    try:
        # Stream response or generate at once
        # Using simple generate for now
        response_text = llm(full_prompt, max_new_tokens=512)
    except Exception as e:
        response_text = f"Error generating: {str(e)}"

    return jsonify({"response": response_text})

if __name__ == '__main__':
    print("Starting Flask server on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
