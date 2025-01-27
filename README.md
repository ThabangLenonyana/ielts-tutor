# IELTS Speaking Test Simulator

Welcome to the IELTS Speaking Test Simulator, a real-time application designed to help you practice and improve your English speaking skills based on the IELTS speaking examination format. This tool provides instant feedback and comprehensive assessments to aid you in your preparation for the IELTS test.

## Features

- **Real-Time Conversation Simulation:** Interact with a simulated IELTS examiner in real time.
- **Speech-to-Text Integration:** Transcribe your spoken responses using Microsoft Azure Speech Services.
- **IELTS Scoring Simulation:** Receive assessments based on IELTS criteria:
  - Fluency & Coherence
  - Lexical Resource
  - Grammatical Range & Accuracy
  - Pronunciation
- **Practice Mode:** Get instant feedback after each response.
- **Test Mode:** Simulate the full IELTS Speaking Test with feedback at the end.
- **Detailed Feedback Reports:** Generate and download PDF reports with scores and improvement suggestions.
- **User-Friendly Interface:** Easy-to-use web interface built with Streamlit.

## System Architecture

![System Architecture](docs/System_Architecture.svg)

**Components:**

- Frontend (Streamlit): User interacts with the application via the web interface.
- Audio Capture Module: Captures user's speech using the microphone.
- Speech-to-Text Module (Azure Speech Services): Converts speech to text.
- Conversational AI Module (Azure OpenAI): Simulates the IELTS examiner.
- Scoring and Feedback Module: Analyzes responses and generates feedback.
- Pronunciation Assessment Module: Evaluates pronunciation (optional).
- Reporting Module: Generates PDF reports.
- Session Management: Manages Practice and Test modes.

## Usage Guide

**Selecting a Mode**

Upon launching, you'll be prompted to select a mode:

- **Practice Mode:** Receive instant feedback after each response.
- **Test Mode:** Simulate a full IELTS Speaking Test with feedback at the end.

**Practice Mode**

1. **Begin Practice:** Click on "Start Practice".
2. **Respond to Questions:** Speak into your microphone when prompted.
3. **View Feedback:** After each response, feedback will be displayed, including scores and suggestions.
4. **Proceed or Retry:** Choose to move to the next question or retry the current one.

**Test Mode**

1. **Begin Test:** Click on "Start Test".
2. **Test Parts:** The test consists of three parts:
   - Part 1: Introduction and interview
   - Part 2: Long turn (Cue Card activity with preparation time)
   - Part 3: Two-way discussion
3. **Respond to Questions:** Speak your responses as prompted.
4. **Complete Test:** After all parts are completed, you will receive a comprehensive feedback report.
5. **Download Report:** Optionally, download a PDF report summarizing your performance.
