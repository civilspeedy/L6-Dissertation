# Weather Data Through Conversation

## Description

The artefact was produced for my final year dissertation while studying Software Engineering at Bournemouth University. The artefact is made up of two parts: a React-Native mobile app and a Python Flask web server. The purpose of this artefact is to enable a user to request weather information from a chatbot in a human-like conversation. This conversation is had through the mobile app, and the web server is used to gather weather information and manage the large language model ([Gemma-7b](https://blog.google/technology/developers/gemma-open-models/)) the user is conversing with.

## Results

For this artefact and the written report I was awarded a 1st.

## Reason

The goal of my dissertation was to explore the possibilities of using a contemporary LLM to request and present data. Weather forecasts were the form of data chosen. This was ultimately done to explore the potential LLMs have as an interface, using human conversion over conventional graphical user interfaces.

## External Libraries

### Mobile

- [React](https://github.com/facebook/react)
- [React-Native](https://github.com/facebook/react-native)
- [React-Native Markdown Display](https://github.com/iamacup/react-native-markdown-display)
- [React-Native Async Storage](https://github.com/react-native-async-storage/async-storage)
- [Expo](https://github.com/expo/expo)
- [Axios](https://github.com/axios/axios)

### Websever

- [Flask](https://github.com/pallets/flask/)
- [Requests](https://github.com/psf/requests)
- [Open AI](https://github.com/openai/openai-python)

## Usage

### Mobile

1.  `npm install`
2.  `npm update`
3.  `npm start`
4.  "a" or "i" to open related emulator

### Webserver

1. `pip install -r requirements.txt`
2. `python main.py` or `python3 main.py`

### Caveats

- Current implementation is built with the assumption that the mobile app is run on an emulator (e.g. Android Emulator).
- Assumes web server and mobile device are on the same network.
- API keys are not included.
- Primarily proof-of-concept, not built for real-world use.

## Discussed Future Work (from report)

- Local instance of the language model enabling:
    - Training on custom data
    - Self-training of user and own output
    - Larger weather data processing
    - Larger overall input capabilities
    - Stronger context capabilities
- A mobile app built from the ground up to use an API to access LLMs, enabling:
    - On-device weather data acquisition
    - Faster response time for LM’s messages
    - Singular code base
- Production ready release:
    - Hosted via service like Azure, AWS, ect...
    - Mobile app compiled into APK or IPA
