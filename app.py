from flask import Flask, render_template, request, jsonify
from llama_cpp import Llama
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
        try:
            print(f"Loading Model: {MODEL_FILE}")
            # llama-cpp-python handles GPU automatically if compiled with CUDA
            # n_gpu_layers=50 tries to offload layers to GPU
            llm = Llama(
                model_path=MODEL_FILE,
                n_ctx=2048,
                n_gpu_layers=50,
                verbose=False
            )
            print("Model Loaded Successfully.")
        except Exception as e:
            print(f"Failed to load model: {e}")
            print("Trying CPU only...")
            try:
                llm = Llama(
                    model_path=MODEL_FILE,
                    n_ctx=2048,
                    n_gpu_layers=0,
                    verbose=False
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
        
        icon_code = "01d"
        if code in [1, 2, 3]: icon_code = "02d"
        elif code in [45, 48]: icon_code = "50d"
        elif code in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82]: icon_code = "10d"
        elif code in [71, 73, 75, 77, 85, 86]: icon_code = "13d"
        elif code in [95, 96, 99]: icon_code = "11d"
        elif code >= 4: icon_code = "03d"

        icon_url = f"https://openweathermap.org/img/wn/{icon_code}.png"
        return jsonify({"temp": f"{temp} C", "icon": icon_url}) 
    except Exception as e:
        print(e)
        return jsonify({"error": "failed"})

@app.route('/questions')
def get_questions():
    file_path = "pytania.txt"
    if not os.path.exists(file_path):
        return jsonify({"error": "File pytania.txt not found", "questions": []})
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            questions = [line.strip() for line in f.readlines() if line.strip()]
        return jsonify({"questions": questions})
    except Exception as e:
        return jsonify({"error": str(e), "questions": []})

@app.route('/generate', methods=['POST'])
def generate():
    global llm
    if not llm:
        load_model()
        if not llm:
            return jsonify({"response": "Model is still loading or not found. Please wait."})
            
    data = request.json
    prompt = data.get('prompt', '')
    
    # Simple prompt wrap
    full_prompt = f"[INST] {prompt} [/INST]"
    
    response_text = ""
    try:
        # llama-cpp-python output processing
        output = llm(full_prompt, max_tokens=512, echo=False)
        response_text = output['choices'][0]['text'].strip()
        
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
        print(f"Starting Flask server on http://localhost:5000")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("Nie wybrano modelu lub brak plików. Serwer nie może zostać uruchomiony.")
        sys.exit(1)
