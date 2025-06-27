from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.google import Gemini

from pdf2embed import parse_pdfs

from dotenv import load_dotenv
import streamlit as st

def ask_agent(user_query: str) -> None:
    """
    Function to ask the agent a question and print the response.
    
    Args:
        question (str): The question to ask the agent.
    """

    # Load environment variables from .env file
    load_dotenv()

    agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        knowledge=parse_pdfs,
        search_knowledge=True,
        description="You are a tax consultant in Canada that can answer questions based on the provided documents.",
        goal="Provide tax advices around possible tax deductions",
    )

    if user_query:
        with st.chat_message("user"):
            st.markdown(user_query)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            try:
                response = agent.run(user_query,
                                     stream=True,
                                     stream_intermediate_steps=True)
                for chunk in response:
                    if chunk.content and isinstance(chunk.content, str):
                        if "search_knowledge_base" in chunk.content:
                            # skip internal debug message
                            continue
                        full_response += chunk.content
                        # Display the current accumulated response with a cursor
                        message_placeholder.markdown(full_response + "▌")
                # When done, display the final response (remove the blinking cursor)
                message_placeholder.markdown(full_response)
            except Exception as e:
                st.error(f"An error occurred: {e}\nPlease check your API keys and try again.")
                st.exception(e)  # for debug, print full traceback in the app

if __name__ == "__main__":

    st.title("Tax Consultant Agent")
    st.write("Ask the agent a question about Canadian tax deductions based on the provided documents.")

    question = st.chat_input("Enter your question:")
    if question:
        ask_agent(question)
    else:
        st.write("Please enter a question to ask the agent.")

    