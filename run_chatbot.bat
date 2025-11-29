@echo off

echo Setting up the environment...
pip install google-genai

echo Starting Chatbot Application...
python.exe ./interview/main_chatbot.py

:end