# Software Requirements Specification (SRS) for IELTS Speaking Test Simulator

## 1. Introduction

### 1.1 Purpose

The purpose of this document is to outline the software requirements for the development of a real-time IELTS Speaking Test Simulator. This tool is intended to help users practice their English speaking skills and receive performance assessments based on IELTS criteria.

### 1.2 Scope

The IELTS Speaking Test Simulator will be a standalone application that simulates the IELTS speaking examination. It will provide real-time conversation practice, performance scoring, and feedback. The application will support both Practice and Test modes and will offer additional features such as detailed feedback reports.

### 1.3 Definitions, Acronyms, and Abbreviations

- **IELTS**: International English Language Testing System
- **LLM**: Large Language Model
- **API**: Application Programming Interface
- **Azure**: Microsoft Azure Cloud Services
- **SRS**: Software Requirements Specification

## 2. Overall Description

### 2.1 Product Perspective

The tool will function independently and will not rely on platforms like ChatGPT. It will utilize Microsoft Azure services for speech recognition and AI capabilities.

### 2.2 Product Functions

- Simulate real-time IELTS Speaking Test conversations.
- Provide performance assessments based on IELTS criteria:
  - Fluency & Coherence
  - Lexical Resource
  - Grammatical Range & Accuracy
  - Pronunciation
- Offer Practice Mode with instant feedback.
- Offer Test Mode simulating the full IELTS Speaking Test with feedback at the end.
- Generate downloadable PDF reports with scores and feedback.

### 2.3 User Characteristics

- Individuals preparing for the IELTS speaking examination.
- Users seeking to improve their English speaking proficiency.

### 2.4 Constraints

- Must use free or open-source tools and packages.
- Leverage Microsoft Azure services.
- Provide a web interface using Streamlit.

### 2.5 Assumptions and Dependencies

- Users have access to a microphone for speech input.
- Users have a stable internet connection for accessing Azure services.
- Azure OpenAI Service access is approved.

## 3. Specific Requirements

### 3.1 Functional Requirements

#### 3.1.1 Real-Time Conversation Simulation

- The system shall capture the user's speech via microphone.
- The system shall transcribe speech to text in real time using Azure Speech Services.
- The system shall simulate an IELTS examiner using Azure OpenAI Service.

#### 3.1.2 Performance Assessment

- The system shall evaluate user responses based on IELTS criteria.
- The system shall provide scores out of 9 for each criterion.
- The system shall offer detailed feedback on user performance.

#### 3.1.3 Modes of Operation

##### Practice Mode:

- The system shall provide instant feedback after each response.

##### Test Mode:

- The system shall simulate the full IELTS Speaking Test (Parts 1, 2, and 3).
- The system shall provide feedback at the end of the session.

#### 3.1.4 Feedback and Reporting

- The system shall generate downloadable PDF reports summarizing the user's performance.
- The system shall include corrected sentences, pronunciation tips, and vocabulary suggestions in the feedback.

### 3.2 Non-Functional Requirements

#### 3.2.1 Usability

- The interface shall be user-friendly and intuitive.
- The system shall provide clear instructions and prompts to the user.

#### 3.2.2 Performance

- The system shall process speech input and provide responses with minimal delay.
- The system shall handle real-time transcription without significant lag.

#### 3.2.3 Reliability

- The system shall handle network interruptions gracefully.
- The system shall provide error messages when services are unavailable.

#### 3.2.4 Security

- The system shall securely handle user data and API keys.
- The system shall comply with data protection regulations.

### 3.3 Constraints

- Must use Streamlit for the web interface.
- Must utilize Microsoft Azure services.
- All tools and packages must be free or open-source.

## 4. System Features

### 4.1 Speech-to-Text Integration

- Real-time transcription using Azure Speech Services.

### 4.2 Conversational AI Examiner

- Simulate IELTS examiner using Azure OpenAI Service.

### 4.3 IELTS Scoring Simulation

- Evaluate user responses based on IELTS criteria.
- Provide detailed feedback and scoring.

### 4.4 Session Management

- Support for Practice Mode and Test Mode.
- Manage conversation flow and timing.

### 4.5 Feedback and Reporting

- Provide instant or end-of-session feedback.
- Generate downloadable PDF reports.
