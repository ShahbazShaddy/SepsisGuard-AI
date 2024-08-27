import os
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

def create_chatgroq_client():
    api_key = os.getenv("GROQ_API_KEY")
    groq_api_key = os.environ.get("API", api_key)
    model = 'llama3-70b-8192'
    return ChatGroq(groq_api_key=groq_api_key, model_name=model)

def create_conversation_chain():
    system_prompt = ''''You are a friendly conversational chatbot which help out the nurses in the field of medical. You also have the following information about sepsis:
    Factors on which sepsis depends:
    1) Temperature
    2) Heart Rate
    3) Respiratory Rate
    4) WBC (White Blood Cell) Count
    What is the normal ranges of factor?
    1) Temperature: 35 °C < Temperature < 39 °C
    2) Heart Rate: Heart Rate < 91 bpm
    3) Respiratory Rate: Respiratory Rate ≤ 20 breaths per min
    4) WBC: 4000 /mm³ ≤ WBC ≤ 12000 /mm³'''
    conversational_memory_length = 5
    memory = ConversationBufferWindowMemory(k=conversational_memory_length, memory_key="chat_history", return_messages=True)
    
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{human_input}"),
        ]
    )
    groq_chat = create_chatgroq_client()
    return LLMChain(
        llm=groq_chat,
        prompt=prompt,
        verbose=False,
        memory=memory,
    )

def get_chat_response(user_message):
    conversation = create_conversation_chain()
    response = conversation.predict(human_input=user_message)
    return response
