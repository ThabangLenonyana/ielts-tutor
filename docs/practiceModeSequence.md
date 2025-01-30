# Session Initialization

1. **User starts Practice Mode through the frontend interface**
2. **Frontend initiates a new practice session with the Session Manager**
3. **System displays available topic selections**
4. **User selects their preferred topic for practice**

# Real-time Practice Loop

## Question Generation:

1. **Session Manager requests a practice question from the LLM Service**
2. **LLM generates a contextually appropriate question based on the selected topic**
3. **Question is displayed to the user through the frontend**

## Response Handling:

1. **User speaks their response through the microphone**
2. **Frontend continuously streams audio to the Speech-to-Text service**
3. **Speech-to-Text service converts audio to text in real-time**
4. **Transcribed text is sent to the Session Manager**

### Parallel Processing (happens simultaneously):

#### a. Scoring and Feedback:

1. **Session Manager sends transcribed response to Scoring Engine**
2. **Scoring Engine evaluates the response across IELTS criteria:**
   - Fluency & Coherence
   - Lexical Resource
   - Grammatical Range & Accuracy
   - Pronunciation
3. **Feedback Generator creates immediate, detailed feedback including:**
   - Grammar corrections with explanations
   - Alternative vocabulary suggestions
   - Pronunciation improvement tips
   - Fluency score with specific areas for improvement

#### b. Next Question Preparation:

1. **Session Manager sends response to LLM Service**
2. **LLM analyzes response to prepare relevant follow-up questions**
3. **System maintains conversation coherence based on previous responses**

# Feedback Display

1. **Frontend receives and displays comprehensive feedback**
2. **User sees:**
   - Specific grammar corrections highlighted in their response
   - Suggested alternative vocabulary with examples
   - Pronunciation guidance for specific words/phrases
   - Fluency score with detailed breakdown
3. **System presents option to:**
   - Review feedback in detail
   - Practice the same question again
   - Move to the next question

# User Decision Phase

## User can choose to:

### a. Continue Practice:

1. **Request next question**
2. **Session Manager maintains context and difficulty level**
3. **Practice loop continues with new question**

### b. End Session:

1. **User opts to end practice**
2. **Session Manager requests final summary from Scoring Engine**
3. **System generates comprehensive practice report including:**
   - Overall performance metrics
   - Pattern of errors and improvements
   - Specific areas needing attention
   - Recommendations for future practice
4. **Frontend displays session results and offers download option**

# Key Features Throughout the Session:

- **Adaptive Difficulty:**

  - System adjusts question complexity based on user performance
  - Follow-up questions target areas needing improvement

- **Contextual Continuity:**

  - Questions maintain logical flow within the chosen topic
  - Follow-up questions build on previous responses

- **Immediate Intervention:**

  - Real-time error detection and correction
  - Instant feedback allows immediate learning and improvement

- **User Control:**

  - Flexible pacing based on user comfort
  - Option to focus on specific aspects of speaking
  - Ability to end session at any time

- **Comprehensive Feedback:**
  - Multi-dimensional feedback covering all IELTS criteria
  - Actionable suggestions for improvement
  - Visual representation of progress
