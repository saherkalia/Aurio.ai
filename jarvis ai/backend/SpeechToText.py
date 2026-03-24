import os
import time
import mtranslate as mt
from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Load environment variables
env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage", "en")

# HTML template with fixed JS SpeechRecognition
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
    const output = document.getElementById('output');
    let recognition;

    function startRecognition() {
        recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = '';  // will be replaced
        recognition.continuous = true;

        recognition.onresult = function(event) {
            const transcript = event.results[event.results.length - 1][0].transcript;
            output.textContent += transcript + ' ';
        };

        recognition.onend = function() {
            recognition.start();  // keep listening
        };

        recognition.start();
    }

    function stopRecognition() {
        if (recognition) recognition.stop();
        output.innerHTML = "";
    }
    </script>
</body>
</html>'''

# Inject language setting
HtmlCode = HtmlCode.replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

# Platform-agnostic path setup
base_dir = os.getcwd()
data_dir = os.path.join(base_dir, "Data")
temp_dir = os.path.join(base_dir, "Frontend", "Files")
os.makedirs(data_dir, exist_ok=True)
os.makedirs(temp_dir, exist_ok=True)

# Save HTML file
html_path = os.path.join(data_dir, "Voice.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(HtmlCode)

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")  # Auto-accept mic
chrome_options.add_argument("--disable-infobars")
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
chrome_options.add_argument(f"user-agent={user_agent}")
# chrome_options.add_argument("--headless")  # DO NOT USE headless when mic is needed

# === Fallback: Use local ChromeDriver if offline ===
try:
    service = Service(ChromeDriverManager().install())
except Exception as e:
    print("[WARNING] Falling back to local ChromeDriver. Reason:", e)
    # Manually downloaded driver path — replace with your real path
    local_driver_path = os.path.join(base_dir, "chromedriver.exe")
    service = Service(local_driver_path)

driver = webdriver.Chrome(service=service, options=chrome_options)

# File to communicate assistant status
def SetAssistantStatus(Status):
    status_file = os.path.join(temp_dir, "Status.data")
    with open(status_file, "w", encoding="utf-8") as f:
        f.write(Status)

# Format query
def QueryModifier(Query):
    q = Query.strip().lower()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "can you", "what's", "how's"]
    is_question = any(q.startswith(word) for word in question_words)
    if q and q[-1] not in ['.', '?', '!']:
        q += "?" if is_question else "."
    return q.capitalize()

# Translate to English
def UniversalTranslator(Text):
    return mt.translate(Text, "en", "auto").capitalize()

# Speech recognition loop
def SpeechRecognition():
    driver.get(f"file://{html_path}")  # Optional: change to http://localhost if Flask used
    driver.find_element(By.ID, "start").click()

    while True:
        try:
            Text = driver.find_element(By.ID, "output").text
            if Text.strip():
                driver.find_element(By.ID, "end").click()
                if InputLanguage and "en" in InputLanguage.lower():
                    return QueryModifier(Text)
                else:
                    SetAssistantStatus("Translating...")
                    return QueryModifier(UniversalTranslator(Text))
        except Exception:
            time.sleep(0.2)

# Run the recognizer
if __name__ == "__main__":
    while True:
        print(SpeechRecognition())
        