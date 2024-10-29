from datetime import datetime
from pathlib import Path
from typing import Dict

import streamlit as st
from ollama import Client
import time
from datetime import datetime
from pathlib import Path

from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader, PromptTemplate
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

# Set page config at the very beginning
st.set_page_config(
    page_title="Lokaler KI-Assistent mit RAG",
    page_icon="💬",
    layout="wide"
)

def create_personalized_prompt(student_info: Dict[str, str]) -> PromptTemplate:
    return PromptTemplate(
    f"""
    WICHTIG: Antworte ausschließlich auf Deutsch

    Du bist ein KI-Assistent für die deutsche Carl von Ossietzky Universität Oldenburg. Du sprichst gerade mit einem Studenten mit folgenden Informationen:
    
    Name: {student_info.get('name', 'Nicht angegeben')}
    Studiengang: {student_info.get('studiengang', 'Nicht angegeben')}
    Semester: {student_info.get('semester', 'Nicht angegeben')}
    Matrikelnummer: {student_info.get('matrikelnummer', 'Nicht angegeben')}
    Fakultät: {student_info.get('fakultaet', 'Nicht angegeben')}

    Benutze diese Informationen, um deine Antworten zu personalisieren und relevanter zu gestalten. Beachte dabei folgende Richtlinien:

    1. Antworte immer in deutscher Sprache.
    2. Sei höflich, geduldig und respektvoll. Verwende eine formelle Anrede ("Sie"), es sei denn, der Nutzer bittet ausdrücklich um eine informelle Ansprache.
    3. Deine Antworten sollten klar, prägnant und informativ sein. Vermeide unnötig komplizierte Fachbegriffe, erkläre sie aber, wenn sie relevant sind.
    4. Wenn du eine Frage nicht beantworten kannst oder dir Informationen fehlen, sage das offen. Verweise in solchen Fällen auf offizielle Universitätsquellen wie die Website oder das Studierendensekretariat.
    5. Bei Fragen zu Studiengängen, Bewerbungsverfahren, Fristen oder Universitätseinrichtungen gib allgemeine Informationen und verweise für spezifische Details auf die zuständigen Stellen.
    6. Respektiere die Privatsphäre. Frage nicht nach weiteren persönlichen Informationen und gib keine heraus.
    7. Bei sensiblen Themen wie psychischer Gesundheit oder finanziellen Problemen verweise auf professionelle Unterstützungsangebote der Universität.
    8. Sei dir deiner Rolle als KI-Assistent bewusst. Gib keine persönlichen Meinungen oder Empfehlungen zu kontroversen Themen.
    9. Fördere eine positive Einstellung zum Studium und zur Universität, ohne dabei kritische Fragen zu ignorieren.
    10. Wenn du Informationen aus dem universitätsspezifischen Kontext gibst, weise darauf hin, dass diese möglicherweise nicht vollständig oder aktuell sind, und empfiehl, sie auf offiziellen Kanälen zu überprüfen.
    11. Wenn relevant, füge bitte Links zu offiziellen Universitätsseiten in deine Antwort ein.
    12. Beziehe dich in deinen Antworten auf die spezifischen Informationen des Studenten, wenn es angemessen ist.

    Dein Ziel ist es, eine zuverlässige und freundliche Anlaufstelle für alle universitätsbezogenen Fragen zu sein und den Nutzern dabei zu helfen, die benötigten Informationen oder den richtigen Ansprechpartner zu finden.

    Menschliche Anfrage: {{query_str}}
    Relevanter Kontext:
    {{context_str}}

    Basierend auf dem gegebenen Kontext, den Studenteninformationen und unter Berücksichtigung der oben genannten Richtlinien, hier ist meine personalisierte Antwort auf Deutsch:
    """
    )


class OllamaChat:
    """
    Enhanced OllamaChat class with RAG capabilities and custom prompts
    """
    def __init__(self, model_name="llama3:70b"):
        self.client = Client(host='http://localhost:11434')
        self.model_name = model_name
        self.temperature = 0.7
        
        # Set up the data directory path
        curr_dir = Path.cwd()
        root_dir = curr_dir
        self.data_directory = root_dir / 'assets' / 'BIS'
        
        self.query_engine = None
        self.index = None
        self.setup_rag()
    
    def get_models(self):
        """
        Get list of available models from Ollama
        Returns:
            list: List of available model names
        """
        try:
            response = self.client.list()
            return [model['name'] for model in response['models']] if 'models' in response else [self.model_name]
        except Exception as e:
            st.warning(f"Failed to fetch models: {str(e)}")
            return [self.model_name]  # Return current model as fallback
    
    def setup_rag(self):
        """
        Initialize RAG components using Settings
        """
        try:
            # Set up embedding model
            embed_model = OllamaEmbedding(
                model_name=self.model_name,
            )
            
            # Set up LLM
            llm = Ollama(
                model=self.model_name.split(':')[0],
                temperature=self.temperature,
                context_window=8192,
                base_url='http://localhost:11434',
            )
            
            # Configure settings
            Settings.embed_model = embed_model
            Settings.llm = llm
            
            # Load and index documents
            if self.data_directory.exists():
                st.info(f"Loading documents from: {self.data_directory}")
                documents = SimpleDirectoryReader(input_dir=str(self.data_directory)).load_data()
                # Create index using the configured settings
                self.index = VectorStoreIndex.from_documents(documents)
                self.query_engine = self.index.as_query_engine()
                st.success(f"Successfully loaded {len(documents)} documents")
            else:
                st.warning(f"Directory {self.data_directory} not found. RAG features will be disabled.")
        except Exception as e:
            st.error(f"Error setting up RAG: {str(e)}")
    
    def update_query_engine_with_student_info(self, student_info: Dict[str, str]):
        """
        Updates query engine with personalized prompt
        """
        if self.index:
            personalized_prompt = create_personalized_prompt(student_info)
            self.query_engine = self.index.as_query_engine()
            self.query_engine.update_prompts(
                {"response_synthesizer:text_qa_template": personalized_prompt}
            )

    def get_response(self, messages, temperature=None, use_custom_prompt=False):
        """
        Get a response using both chat history and RAG context
        """
        try:
            # Get the latest user message
            latest_message = messages[-1]["content"] if messages else ""
            
            if self.query_engine:
                # Get relevant context from documents
                try:
                    rag_response = self.query_engine.query(latest_message)
                    context = str(rag_response)
                    st.info("Retrieved relevant context from documents")  # Debug info
                    st.info(f"Debug - Retrieved context: {context[:200]}...")  # Show first 200 chars of context
                except Exception as e:
                    st.warning(f"Error retrieving context: {str(e)}")
                    context = "No relevant context found."
                
                # Enhance the prompt with context
                if use_custom_prompt:
                    # Use the custom prompt template with RAG context
                    enhanced_prompt = f"""
                    Kontext aus den Dokumenten:
                    {context}

                    Basierend auf diesem Kontext und dem Chatverlauf, bitte beantworte folgende Frage:
                    {latest_message}
                    """
                    
                    response = self.client.chat(
                        model=self.model_name,
                        messages=[{"role": "user", "content": enhanced_prompt}],
                        options={
                            "temperature": temperature or self.temperature,
                        }
                    )
                else:
                    # Use standard prompt with RAG context
                    enhanced_prompt = f"""
                    Context from documents:
                    {context}

                    Based on this context and our conversation history, please respond to:
                    {latest_message}
                    """
                    
                    response = self.client.chat(
                        model=self.model_name,
                        messages=messages[:-1] + [{"role": "user", "content": enhanced_prompt}],
                        options={
                            "temperature": temperature or self.temperature,
                        }
                    )
            else:
                # Fallback to regular chat if RAG is not available
                st.warning("RAG features are disabled - no document context available")
                response = self.client.chat(
                    model=self.model_name,
                    messages=messages,
                    options={
                        "temperature": temperature or self.temperature,
                    }
                )
            
            return response['message']['content']
        except Exception as e:
            return f"Error generating response: {str(e)}"

def initialize_session_state():
    """
    Initialize or retrieve Streamlit session state variables
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "ollama_chat" not in st.session_state:
        st.session_state.ollama_chat = OllamaChat()
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "current_chat" not in st.session_state:
        st.session_state.current_chat = "New Chat"
    if "use_custom_prompt" not in st.session_state:
        st.session_state.use_custom_prompt = False
    if "student_info" not in st.session_state:
        st.session_state.student_info = {
            "name": "",
            "studiengang": "",
            "semester": "",
            "matrikelnummer": "",
            "fakultaet": ""
        }

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
    Main application function
    """
    # Add minimal CSS for fixed chat input
    st.markdown("""
        <style>
        .stChatFloatingInputContainer {
            position: fixed;
            bottom: 3rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
# Sidebar
    with st.sidebar:
        st.title("⚙️ Einstellungen")
        
        # Custom prompt toggle and student info
        st.subheader("🎯 Prompt-Einstellungen")
        use_custom_prompt = st.toggle("Personalisierten Prompt verwenden", 
                                    value=st.session_state.use_custom_prompt)
        
        if use_custom_prompt:
            st.subheader("📚 Studenten-Informationen")
            student_info = {
                "name": st.text_input("Name", value=st.session_state.student_info["name"]),
                "studiengang": st.text_input("Studiengang", value=st.session_state.student_info["studiengang"]),
                "semester": st.text_input("Semester", value=st.session_state.student_info["semester"]),
                "matrikelnummer": st.text_input("Matrikelnummer", value=st.session_state.student_info["matrikelnummer"]),
                "fakultaet": st.text_input("Fakultät", value=st.session_state.student_info["fakultaet"])
            }
            
            # Update session state
            st.session_state.student_info = student_info
            st.session_state.use_custom_prompt = use_custom_prompt
            
            # Update query engine with new student info
            st.session_state.ollama_chat.update_query_engine_with_student_info(student_info)


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
            value=0.1,
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
                        temperature=st.session_state.ollama_chat.temperature,
                        use_custom_prompt=st.session_state.use_custom_prompt
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