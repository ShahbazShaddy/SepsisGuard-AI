import os
from bayesian_training import train_bayesian_filter
from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

def process_data(form_data):
    """
    Process the form data and classify the chatbot's response for sepsis.
    
    :param form_data: Dictionary containing the form data
    :return: Sepsis status ('Positive' or 'Negative')
    """
    api_key = os.getenv("GROQ_API_KEY")
    groq_api_key = os.environ.get("API", api_key)
    model = 'llama3-8b-8192'
    
    groq_chat = ChatGroq(groq_api_key=groq_api_key, model_name=model)
    
    system_prompt = '''You are tasked with determining whether a patient has sepsis based on the following criteria. If the patient meets any of these criteria, provide a short alert and strongly recommend early intervention. Here are the criteria:

Temperature:
> 39 °C and
< 36 °C
Heart Rate:
≥ 91 bpm
Respiratory Rate:
Should not greater than 20 breaths per minute
White Blood Cells (WBC):
Should not increase than 12,000 /mm³ or
Sgould not decrease than 4,000 /mm³
If a patient meets any of these criteria, generate a strong alert and recommendation for early medical intervention. The input includes the following patient details:

{human_input}

Please analyze the data and provide the appropriate response. Note that only values strictly greater than the specified thresholds should be considered for a positive sepsis status, except for exact threshold values, which should be carefully assessed based on clinical guidelines.'''



    memory = ConversationBufferWindowMemory(k=5, memory_key="chat_history", return_messages=True)

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{human_input}")
        ]
    )

    conversation = LLMChain(llm=groq_chat, prompt=prompt, verbose=False, memory=memory)

    user_input = (
    f"Patient Details:\n\n"
    f"First Name: {form_data['fname']}\n"
    f"Last Name: {form_data['Lname']}\n"
    f"Gender: {form_data['gender']}\n"
    f"Temperature: {form_data['temperature']} °C\n"
    f"Heart Rate: {form_data['heart-rate']} bpm\n"
    f"Respiratory Rate: {form_data['respiratory-rate']} breaths per minute\n"
    f"White Blood Cells: {form_data['wcb']} /mm³\n"
    f"Blood Group: {form_data['blood-group']}\n"
    f"Concerns: {form_data['You Concerns']}\n\n"
    f"Based on the details provided, please assess the patient for sepsis. "
    f"Determine if the patient meets any of the sepsis criteria and if so, "
    f"provide an appropriate alert for early medical intervention."
)

    print(user_input)

    response = conversation.predict(human_input=user_input)
    print("Chatbot Response:", response)

    # Initialize Bayesian filter by training it with the sepsis data
    bayesian_filter = train_bayesian_filter()

    # Classify the response
    sepsis_status = bayesian_filter.calculate_prob(response)
    
    # Print the sepsis status for debugging
    print("Sepsis Status:", sepsis_status)
    
    # Return the sepsis status
    return sepsis_status
