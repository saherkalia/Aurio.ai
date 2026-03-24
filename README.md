# Jarvis AI 🤖

## Overview
Jarvis AI is an advanced AI-powered voice assistant built using Python. It integrates natural language processing, automation, speech recognition, and image generation into a single system.

## Features
- AI Chatbot (Groq LLM)
- Voice Input (Speech-to-Text)
- Voice Output (Text-to-Speech)
- App & System Automation
- YouTube & Google Search Integration
- Image Generation using Stable Diffusion
- Real-time Information Retrieval

## Tech Stack
- Python
- Groq API (LLM)
- Cohere (Decision Model)
- HuggingFace (Image Generation)
- Selenium (Speech Recognition)
- Pygame + Edge TTS

## Project Structure
backend/
- chatbot.py
- automation.py
- decision_model.py
- speech_to_text.py
- text_to_speech.py
- realtime_search.py
- image_generation.py

## Setup Instructions
1. Clone the repository
2. Install dependencies:
   pip install -r requirements.txt

3. Create a `.env` file and add:
   GROQ_API_KEY=your_key
   CohereAPIKey=your_key
   HuggingFaceAPIKey=your_key

4. Run:
   python Main.py

## Future Improvements
- Add memory system
- Build GUI
- Deploy as web app
