from flask import Flask, render_template, request, jsonify
from ctransformers import AutoModelForCausalLM
import datetime
import requests
import sys
import os

import glob

app = Flask(__name__)

# Model handling
MODEL_FILE = None
llm = None

def select_model():
    print("\n=== Wybór Modelu LLM ===")
    # Look for gguf in models/ directory
    models_dir = "models"
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        
    files = glob.glob(os.path.join(models_dir, "*.gguf"))
    if not files:
        print(f"Błąd: Nie znaleziono żadnych plików .gguf w katalogu {models_dir}!")
        print("Uruchom jeden ze skryptów download_model_*.py aby pobrać model.")
        return None
    
    print("Dostępne modele:")
    for i, f in enumerate(files):
        print(f"[{i+1}] - {f}")
    
    while True:
        try:
            choice = input("\nWybierz model (podaj numer): ")
            idx = int(choice) - 1
            if 0 <= idx < len(files):
                return files[idx]
            else:
                print("Nieprawidłowy numer. Spróbuj ponownie.")
        except ValueError:
            print("To nie jest liczba. Spróbuj ponownie.")

def load_model():
    global llm, MODEL_FILE
    
    if not MODEL_FILE:
        print("Model file not selected!")
        return

    if os.path.exists(MODEL_FILE):
        # Try loading with GPU first
        try:
            print(f"Loading Model: {MODEL_FILE} with GPU support...")
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
        print(f"Model file {MODEL_FILE} not found.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/model_name')
def get_model_name():
    if MODEL_FILE:
        return jsonify({"model": os.path.basename(MODEL_FILE)})
    return jsonify({"model": ""})

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
        
        # LOGGING
        try:
            log_dir = "log"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            log_file = os.path.join(log_dir, f"{os.path.basename(MODEL_FILE)}.log")
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] User: {prompt}\n")
                f.write(f"[{timestamp}] LLM: {response_text}\n")
                f.write("-" * 40 + "\n")
                
        except Exception as log_err:
            print(f"Logging error: {log_err}")

    except Exception as e:
        response_text = f"Error generating: {str(e)}"

    return jsonify({"response": response_text})

if __name__ == '__main__':
    selected = select_model()
    if selected:
        MODEL_FILE = selected
        load_model()
        print("Starting Flask server on http://localhost:5000")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("Nie wybrano modelu lub brak plików. Serwer nie może zostać uruchomiony.")
        sys.exit(1)
