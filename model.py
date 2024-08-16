import os
import csv
from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq

def process_data(form_data):
    """
    This function processes the form data to check against the sepsis criteria.
    """
    # Get Groq API key
    groq_api_key = os.environ.get("API", "ADD_YOUR_API")
    model = 'llama3-8b-8192'
    
    # Initialize Groq Langchain chat object
    groq_chat = ChatGroq(
        groq_api_key=groq_api_key, 
        model_name=model
    )
    
    # Prepare the system prompt
    system_prompt = '''You are tasked with determining whether a patient has sepsis based on the following criteria. If the patient meets any of these criteria, provide a short alert and strongly recommend early intervention. Here are the criteria:
1. **Temperature**:
   - Greater than 38 °C (100.4 °F) or
   - Less than 36 °C (96.8 °F)

2. **Heart Rate**:
   - Greater than 90 beats per minute (bpm)

3. **Respiratory Rate**:
   - Greater than 20 breaths per minute or
   - Less than 32 mmHg PaCO₂

4. **White Blood Cells (WBC)**:
   - Greater than 12,000/mm³ or
   - Less than 4,000/mm³ or
   - Greater than 10% bands

If a patient meets any of these criteria, respond with an alert message and strongly advise the patient to seek early medical intervention immediately.'''

    conversational_memory_length = 5  # Number of previous messages the chatbot will remember

    memory = ConversationBufferWindowMemory(k=conversational_memory_length, memory_key="chat_history", return_messages=True)

    # Construct a chat prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{human_input}")
        ]
    )

    # Create a conversation chain
    conversation = LLMChain(
        llm=groq_chat,
        prompt=prompt,
        verbose=False,
        memory=memory,
    )

    # Construct the input based on form data
    user_input = (
        f"Patient Details:\n"
        f"First Name: {form_data['fname']}\n"
        f"Last Name: {form_data['Lname']}\n"
        f"Gender: {form_data['gender']}\n"
        f"Temperature: {form_data['temperature']}\n"
        f"Heart Rate: {form_data['heart-rate']}\n"
        f"Respiratory Rate: {form_data['respiratory-rate']}\n"
        f"White Blood Cells: {form_data['wcb']}\n"
        f"Blood Group: {form_data['blood-group']}\n"
        f"Concerns: {form_data['You Concerns']}\n"
    )

    # Get the model's response
    response = conversation.predict(human_input=user_input)
    print("Chatbot:", response)
