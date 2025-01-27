# Development Plan

## 1. Project Setup

### 1.1 Initialize the Project Repository

- Create a new Git repository for version control.
- Set up a .gitignore file to exclude sensitive information and temporary files.

### 1.2 Set Up the Development Environment

- **Python Version**: Ensure Python 3.8 or higher is installed.
- **Virtual Environment**: Create and activate a virtual environment.

```bash
python -m venv venv
source venv/bin/activate # On Windows use: venv\Scripts\activate
```

- **Install Dependencies**: Create a requirements.txt file and install necessary packages.

```bash
pip install -r requirements.txt
```

- **Dependencies**:
  - streamlit
  - azure-cognitiveservices-speech
  - openai
  - sounddevice
  - fpdf
  - Other packages as needed.

## 2. Azure Services Configuration

### 2.1 Azure Speech Services

- **Create Resource**: Set up a Speech Services resource in Azure.
- **Obtain Credentials**: Note down the API key and endpoint.
- **Configure SDK**: Install and configure the Azure Cognitive Services Speech SDK.

### 2.2 Azure OpenAI Service

- **Apply for Access**: Ensure you have access to Azure OpenAI Service.
- **Deploy Model**: Deploy the GPT-3.5 Turbo model.
- **Obtain Credentials**: Note down the API key and endpoint.
- **Configure Access**: Set up the OpenAI API to use Azure endpoints.

### 2.3 Secure API Keys

- **Environment Variables**: Store API keys in environment variables or a .env file.
- **Avoid Hardcoding**: Do not hardcode API keys in your code.

## 3. Application Architecture Design

### 3.1 Define Modules and Components

- Frontend Interface (Streamlit)
- Audio Capture Module
- Speech-to-Text Module
- Conversational AI Module
- Scoring and Feedback Module
- Session Management
- Reporting Module

### 3.2 Plan Module Interfaces

- Determine how modules will interact.
- Define input and output for each module.

## 4. Implementation Steps

### 4.1 Frontend Interface with Streamlit

- **Set Up Basic Layout**: Create a simple Streamlit app structure.
- **User Interface Elements**:
  - Title and description.
  - Mode selection (Practice or Test Mode).
  - Buttons and input fields for user interaction.
  - Display areas for questions and feedback.
- **Session State Management**:
  - Use `st.session_state` to maintain data across interactions.

### 4.2 Audio Capture and Speech-to-Text Integration

- **Audio Capture**:
  - Use the sounddevice library to access the user's microphone.
  - Ensure cross-platform compatibility.
- **Real-Time Transcription**:
  - Integrate Azure Speech Services SDK.
  - Implement functions to send audio data for transcription.
  - Handle transcription results and update the UI accordingly.
- **Error Handling**:
  - Provide user-friendly error messages for audio issues.

### 4.3 Conversational AI Examiner

- **Design Prompts**:
  - Create system prompts to guide the AI to simulate an IELTS examiner.
  - Ensure the AI follows the IELTS Speaking Test format.
- **Implement Conversation Flow**:
  - Maintain conversation history.
  - Handle user responses and generate appropriate examiner replies.
- **Context Management**:
  - Use message dictionaries to keep track of the conversation context required by the OpenAI API.

### 4.4 IELTS Scoring Simulation

- **Scoring Criteria Implementation**:
  - Define functions to evaluate user responses based on IELTS criteria.
  - Utilize the LLM to assess Fluency & Coherence, Lexical Resource, Grammatical Range & Accuracy, and Pronunciation.
- **Feedback Generation**:
  - Structure the feedback to include scores and detailed comments.
  - Provide actionable suggestions for improvement.

### 4.5 Session Management

- **Practice Mode**:
  - After each user response, provide immediate feedback.
  - Allow the user to retry or move to the next question.
- **Test Mode**:
  - Simulate the full IELTS Speaking Test sequence.
  - Implement timers for each part if necessary.
  - Collect all responses for end-of-session feedback.
- **Navigation and Control**:
  - Implement buttons and controls to navigate through the test.
  - Manage session state to keep track of progress.

### 4.6 Feedback and Reporting

- **Real-Time Feedback Display**:
  - Show feedback directly in the Streamlit app.
  - Use markdown or other formatting for readability.
- **PDF Report Generation**:
  - Use fpdf library to create PDF reports.
  - Include all relevant feedback and scores.
  - Provide a download link for the user.
- **Enhancements**:
  - Add charts or visual aids to the report.
  - Format the report professionally.

### 4.7 Pronunciation Assessment (Optional)

- **Integrate Pronunciation Assessment**:
  - Use Azure Speech Services Pronunciation Assessment features.
  - Evaluate user's pronunciation and include in feedback.
- **Display Results**:
  - Show pronunciation scores.
  - Provide insights on areas to improve.

### 4.8 Multi-language Support (Optional)

- **Translation Integration**:
  - Use Azure Translator Text API.
  - Allow users to select their preferred language for feedback.
- **Implement Language Selection**:
  - Add options in the UI for language selection.
  - Modify feedback generation to include translation.

## 5. Testing and Validation

### 5.1 Unit Testing

- **Test Individual Modules**:
  - Write tests for speech recognition, AI responses, scoring, and other critical functions.

### 5.2 Integration Testing

- **Test Module Interactions**:
  - Ensure that modules work together seamlessly.
  - Simulate user sessions and check end-to-end functionality.

### 5.3 User Acceptance Testing

- **Gather Feedback**:
  - Have users test the application.
  - Collect feedback on usability and performance.

### 5.4 Performance Testing

- **Assess Latency and Responsiveness**:
  - Measure the time taken for speech-to-text processing and AI responses.
- **Optimize Code**:
  - Identify bottlenecks and optimize as needed.

## 6. Deployment Preparation

### 6.1 Dockerization (Optional)

- **Create a Dockerfile**:
  - Define the environment and dependencies.
- **Build and Test the Docker Image**:
  - Ensure the application runs correctly inside the container.

### 6.2 Deployment Options

- **Local Deployment**:
  - Provide instructions for users to run the app locally.
- **Cloud Deployment**:
  - Consider deploying on Azure App Service or Streamlit Cloud.
  - Ensure compliance with Azure policies.

## 7. Documentation and Deliverables

### 7.1 Update README.md

- **Include**:
  - Project description.
  - Setup instructions.
  - Usage guide.
  - Contribution guidelines.

### 7.2 Create User Manual

- **Instructions for Users**:
  - How to install and run the application.
  - Overview of features and functionalities.

### 7.3 Prepare Demo Video

- **Content**:
  - Showcase key features.
  - Demonstrate both Practice and Test modes.
  - Highlight feedback and reporting capabilities.

### 7.4 Finalize SRS Document

- Ensure all requirements are met.
- Update any sections based on development changes.

## Additional Guidelines

### Code Quality

- Follow best coding practices.
- Use meaningful variable and function names.
- Add comments and docstrings where necessary.

### Version Control

- Commit changes regularly with meaningful commit messages.
- Use branches for new features or major changes.

### Security

- Securely handle all user data and API keys.
- Be mindful of Azure service quotas and costs.

### Compliance

- Ensure the application complies with all relevant licenses and terms of service, especially for Azure services and OpenAI.

### User Experience

- Design the UI to be clean and intuitive.
- Provide clear instructions and feedback to the user.

## Conclusion

By following this development plan and adhering to the outlined requirements, you will create a robust IELTS Speaking Test Simulator that provides valuable practice and feedback for users preparing for the IELTS exam. Remember to test thoroughly, document your work, and maintain good coding practices throughout the development process.

Feel free to refer back to this plan as you progress, and don't hesitate to adjust it as necessary to accommodate new insights or changes in requirements.
