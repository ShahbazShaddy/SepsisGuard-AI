import os
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
    model = 'llama3-70b-8192'
    
    groq_chat = ChatGroq(groq_api_key=groq_api_key, model_name=model)
    
    system_prompt = '''Your Role: Assess patient data for potential sepsis.
    Factors on which sepsis depends:
    1) Temperature
    2) Heart Rate
    3) Respiratory Rate
    4) WBC (White Blood Cell) Count
    What is the normal ranges of factor?
    1) Temperature: 36 °C < Temperature < 39 °C
    2) Heart Rate: Heart Rate < 91 bpm
    3) Respiratory Rate: Respiratory Rate ≤ 20 breaths per min
    4) WBC: 4000 /mm³ ≤ WBC ≤ 12000 /mm³
    What information do you get below?
    1) First Name
    2) Last Name
    3) Gender
    4) Temperature
    5) Heart Rate
    6) Respiratory Rate
    7) White Blood Cells
    8) Blood Group
    9) Concerns
    What is your task?
    Your task is to check wheather the patient information lies within the normal range and to strictly follow the ranges. Do not consider Upper or Lower limit as a threat.
    
    Now the real task begin. The input includes the following patient details. Give appropriate response:
    If any factor falls outside the normal range, generate a response in only one word i.e., 'Positive' otherwise say 'Negative'. Provide only this one-word response.
    {human_input}
    '''
# 

    # Patient Detail:
    # First Name: Shahbaz
    # Last Name: Ali
    # Gender: Male
    # Temperature: 38 °C
    # Heart Rate: 80 bpm
    # Respiratory Rate: 20 breaths per minute
    # White Blood Cells: 11000 /mm³
    # Blood Group: A
    # Concerns: none

    # Temperature: 38 °C is within the normal range (35 °C < Temperature < 39 °C), so this is NORMAL.
    # Heart Rate: 80 bpm is within the normal range (less than 91 bpm is normal), so this is NORMAL.
    # Respiratory Rate: 20 breaths per minute is within the normal range (20 breaths/min and less than 20 breaths/min is normal), so this is NORMAL.
    # WBC count: 11000 /mm³ is within the normal range (greater than 3999 /mm³ and less than 12001 /mm³ is normal), so this is NORMAL.
    # Since no abnormalities are detected in the patient's vitals, there is no indication of potential sepsis based on the provided data.
    # Your Response: Negative
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

    # Generate the first response
    response = conversation.predict(human_input=user_input)
    print("Chatbot Response:", response)

    # Return the sepsis status
    return response
