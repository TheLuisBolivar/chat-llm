#pip install langchain streamlit langchain-openai python-dotenv
#streamlit run src/main.py

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

#carga la configuración de las variables de entorno del archivo .env
load_dotenv()

#configuración inicial de streamlit:
st.set_page_config(page_title="lebc chat")
st.title("lebc chat")

#configuración del chat:
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

#obtener el response desde el llm:
def get_response(user_query, chat_history):

    #creación del prompt template:
    template = """
        You are a helpful assistant, answer the following questions based on your knowledge
        chat history: {chat_history}
        user question: {user_query}
        """
    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatOpenAI()

    chain = prompt | llm | StrOutputParser()

    # esta es una solución sincrona.
    # return chain.invoke({
    #     "chat_history": chat_history,
    #     "user_query": user_query
    # })

    #esta es la solución asincrona:
    return chain.stream({
        "chat_history": chat_history,
        "user_query": user_query
    })

#mostrar la conversation:
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("human"):
            st.markdown(message.content)
    else:
        with st.chat_message("ai"):
            st.markdown(message.content)

# chat:
user_query = st.chat_input("your message")

if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(user_query)) 

    with st.chat_message("human"):
        st.markdown(user_query)

    with st.chat_message("ai"):
        # esto es para una solución sincrona:
        # ai_response = get_response(user_query, st.session_state.chat_history)
        # st.markdown(ai_response)

        #eso es para una solución asincrona:
        ai_response = st.write_stream(get_response(user_query, st.session_state.chat_history))
    
    st.session_state.chat_history.append(AIMessage(ai_response))