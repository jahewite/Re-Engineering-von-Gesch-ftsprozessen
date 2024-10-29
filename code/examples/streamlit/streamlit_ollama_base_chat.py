import streamlit as st
from ollama import Client
import time
from datetime import datetime

# Set page config at the very beginning, before any other Streamlit commands
st.set_page_config(
    page_title="Lokaler KI-Assistent",
    page_icon="💬",
    layout="wide"
)

class OllamaChat:
    """
    Main class to handle interactions with the Ollama API.
    Manages model selection, message generation, and chat settings.
    """
    def __init__(self, model_name="llama3:70b"):
        self.client = Client(host='http://localhost:11434')
        self.model_name = model_name
        self.temperature = 0.7
        
    def get_response(self, messages, temperature=None):
        """
        Get a response from the model using the complete message history
        Args:
            messages (list): List of message dictionaries
            temperature (float, optional): Model temperature
        Returns:
            str: The model's response text
        """
        response = self.client.chat(
            model=self.model_name,
            messages=messages,
            options={
                "temperature": temperature or self.temperature,
            }
        )
        return response['message']['content']
    
    def get_models(self):
        """
        Fetch list of available models from Ollama server
        Returns:
            list: Names of available models
        """
        models = self.client.list()
        return [model['name'] for model in models['models']]

def initialize_session_state():
    """
    Initialize or retrieve Streamlit session state variables.
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "ollama_chat" not in st.session_state:
        st.session_state.ollama_chat = OllamaChat()
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "current_chat" not in st.session_state:
        st.session_state.current_chat = "New Chat"

def save_chat_history():
    """
    Save current chat to history with timestamp
    """
    if st.session_state.messages:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        first_message = st.session_state.messages[0]["content"][:50] + "..."
        chat_name = f"{timestamp} - {first_message}"
        st.session_state.chat_history.append({
            "name": chat_name,
            "messages": st.session_state.messages.copy(),
            "timestamp": timestamp
        })

def main():
    """
    Main application function with Streamlit's default styling
    """
    # Sidebar
    with st.sidebar:
        st.title("⚙️ Einstellungen")
        
        # Model selection
        available_models = st.session_state.ollama_chat.get_models()
        selected_model = st.selectbox(
            "Modellauswahl",
            available_models,
            index=available_models.index(st.session_state.ollama_chat.model_name)
            if st.session_state.ollama_chat.model_name in available_models
            else 0
        )
        
        # Model parameters
        st.session_state.ollama_chat.temperature = st.slider(
            "Temperatur",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Höhere Werte machen die Antworten kreativer, aber auch ungenauer."
        )
        
        # Chat management
        st.subheader("💾 Chat Management")
        if st.button("Starte neuen Chat"):
            save_chat_history()
            st.session_state.messages = []
            st.session_state.current_chat = "Neuer Chat"
            st.rerun()
            
        if st.button("Export Chat"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            chat_content = "\n\n".join([
                f"{msg['role'].upper()}: {msg['content']}"
                for msg in st.session_state.messages
            ])
            st.download_button(
                label="Download Chat",
                data=chat_content,
                file_name=f"chat_export_{timestamp}.txt",
                mime="text/plain"
            )
    
    # Main chat interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.title("💬 Lokaler KI-Assistent")
        
        # Display chat messages
        messages_container = st.container()
        with messages_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Schreibe eine Nachricht..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Lass mich nachdenken... 🤔"):
                    response = st.session_state.ollama_chat.get_response(
                        st.session_state.messages,
                        temperature=st.session_state.ollama_chat.temperature
                    )
                    st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
    # Chat history sidebar
    with col2:
        st.subheader("📚 Chat Verlauf")
        for chat in reversed(st.session_state.chat_history):
            if st.button(f"📝 {chat['name']}", key=chat['timestamp']):
                st.session_state.messages = chat['messages']
                st.session_state.current_chat = chat['name']
                st.rerun()

if __name__ == "__main__":
    initialize_session_state()
    main()