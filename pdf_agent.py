from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.google import Gemini
from persona import Personas

from pdf2embed import parse_pdfs

from dotenv import load_dotenv
import streamlit as st

persona_lookup = {
    'G.A.B.E': Personas.GABE,
    'The Beaver': Personas.BEAVER,
    'Maple': Personas.MAPLE,
    'Section 245': Personas.SECTION245,
}

if 'persona' in st.session_state:
    st.session_state['prompt'] = persona_lookup.get(st.session_state['persona'], Personas.GABE)


BASE_PROMPT = """You should use the provided documents to answer the user's question. If the answer is not in the documents, you can use your knowledge of Canadian tax law and the persona's voice to provide a helpful response. Always cite the source of your information when possible."""

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
        description=st.session_state['prompt'],
        instructions= BASE_PROMPT,
        enable_agentic_knowledge_filters=False,
        show_tool_calls=True,
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
                                     stream_intermediate_steps=False)
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
    with st.sidebar:
        st.session_state['persona'] = st.selectbox(
            "Select a persona",
            options=list(persona_lookup.keys()),
            help="Choose the persona that best fits your needs. Each persona has a unique approach to answering tax-related questions.",
        )
    st.write("Ask the agent a question about Canadian tax deductions based on the provided documents.")

    question = st.chat_input("Enter your question:")
    if question:
        ask_agent(question)
    else:
        st.write("Please enter a question to ask the agent.")

    