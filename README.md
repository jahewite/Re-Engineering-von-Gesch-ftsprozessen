![logo](assets/bilder/uni_chatbot.jpg)

# Entwicklung eines Universitäts-Chatbots mittels RAG-Pipeline

## Übersicht Kurs
Ziel ist es, einen universitätsbezogenen Chatbot zu entwickeln, an den Studierende sich richten können, um spezifische Informationen zur Universität, angebotenen Studiengängen, Prüfungsordnungen oder Sonstigen zu erhalten.

## RAG-Pipeline
Die Implementierung basiert auf einer RAG-Pipeline (Retrieval Augmented Generation), die es ermöglicht, große Language Models (LLMs) mit spezifischen, aktuellen Daten anzureichern.

### Hauptkomponenten der RAG-Pipeline:

1. **Datenerfassung und -aufbereitung**
   - Extraktion aus PDFs
   - Verarbeitung strukturierter Daten (CSV, Excel)
   - Crawling von Webseiten (fortgeschritten)
   - *Frameworks:*LLamaIndex, BeautifulSoup, Scrapy, PyPDF2, pandas

2. **Chunking und Preprocessing**
   - Aufteilung der Dokumente in verarbeitbare Einheiten
   - Textbereinigung und Normalisierung
   - *Frameworks:* LLamaIndex, LangChain, NLTK, spaCy

3. **Embedding-Generierung**
   - Umwandlung von Text in Vektoren
   - Optimierung der Vektorrepräsentationen
   - *Frameworks:* LlamaIndex, LangChain

4. **Vektorspeicher**
   - Effiziente Speicherung der Embeddings
   - Ähnlichkeitssuche
   - Kann mithilfe von Frameworks wie LlamaIndex oder LangChain erreicht werden, oder in separaten Vektordatenbanken wie *FAISS, Pinecone, Chroma, Weaviate*

5. **Retrieval-System**
   - Semantische Suche
   - Kontextauswahl
   - *Frameworks:* LlamaIndex, LangChain

6. **Large Language Model (LLM)**
   - Verarbeitung der Anfragen
   - Generierung der Antworten
   - *Frameworks:* Ollama

7. **Prompt Engineering**
   - Strukturierung der Systemanweisungen
   - Kontextintegration
   - *Frameworks:* LangChain, LlamaIndex

### Ablauf der Pipeline:
```
[Nutzeranfrage] 
    → [Embedding der Anfrage]
    → [Ähnlichkeitssuche im Vektorspeicher]
    → [Retrieval relevanter Dokumente]
    → [Prompt-Konstruktion mit Kontext]
    → [LLM-Verarbeitung]
    → [Generierte Antwort]
```
Frameworks wie LlamaIndex oder LangChain bieten für sämtliche Schritte entsprechende Lösungen, es lohnt sich jedoch auch, einen Blick auf andere Frameworks zu werden, die einzelne Schritte vielleicht noch tiefergehende Lösungen bieten.

Code-Beispiele können im [code](./code/) Verzeichnis eingesehen werden.

### Hinweise:
- Integration universitätsspezifischer Daten
- Berücksichtigung zu Fragestellungen bezüglich Datenschutzaspekten
- Mehrsprachige Unterstützung (Deutsch/Englisch)
- Personalisierung der Antworten
- Aktualisierbarkeit der Wissensbasis
