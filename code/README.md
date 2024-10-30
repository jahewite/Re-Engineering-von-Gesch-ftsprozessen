# Code Beispiele

Bevor die Beispiele durchgeführt werden könnnen, müssen die gezeigten Schritte in der README durchgeführt werden.

## SSH Login auf Remote Server

SSH (Secure Shell) ermöglicht eine sichere Verbindung zu einem entfernten Server. Hier sind die Schritte für den Login:

1. Falls keine IDE vorhanden, installiere VS Code (https://code.visualstudio.com/download)
2. Installiere die Remote SSH Erweiterung in VS Code
3. Verbinde dich mit dem Remote Server über den Befehl:
   ```
   ssh benutzer@serveradresse (Nutzerdaten werden separat in der Veranstaltung ausgegeben.)
   ```

## Allgemeine Befehle

Hier sind einige wichtige Befehle und ihre Erklärungen:

- `mkdir`: Erstellt ein neues Verzeichnis
- `cd`: Wechselt das aktuelle Verzeichnis
- `htop`: Zeigt eine interaktive Prozess- und Systemressourcenübersicht
- `nvidia-smi`: Zeigt Informationen über NVIDIA GPUs an

## Anlegen einer Python venv

Eine venv (virtuelle Umgebung) ist eine isolierte Python-Umgebung, die es ermöglicht, projektspezifische Abhängigkeiten zu installieren, ohne das globale System zu beeinflussen.

```bash
mkdir venvs
cd venvs
python3.12 -m venv uni_chatbot
source /home/your_username/venvs/uni_chatbot/bin/activate
```

## Laden und Entpacken des Codes eines Git-Repos

Git ist ein Versionskontrollsystem. Mit dem Klonen eines Repos kopierst du ein bestehendes Repository auf deinen lokalen Rechner oder Server. In diesem Fall wird das Repo jedoch nicht gecloned, der Code wird direkt als ZIP heruntergeladen und im entsprechenden Verzeichnis entpackt.

```bash
wget https://github.com/jahewite/Re-Engineering-von-Gesch-ftsprozessen/archive/refs/heads/master.zip
unzip /pfad/zum/verzeichnis
```

## Installation requirements.txt

Eine `requirements.txt` Datei listet alle Python-Pakete auf, die für ein Projekt benötigt werden. Sie erleichtert die Installation aller notwendigen Abhängigkeiten.
```bash
pip install -r requirements.txt
```

## Sarten des Ollama-Servers
Der Ollama-Server muss gestartet werden, bevor die Code Beispiele und generell jeweilig ausgewählte LLM-Modelle genutzt werden können. Dazu wird das Script `run_ollama.sh` verwendet.

### Ausführung des Scripts

1. Navigiere ins Root-Verzeichnis des Projekts.
2. Gebe dem Script Ausführungsrechte:
   ```bash
   chmod +x run_ollama.sh
   ```

3. Starte das Script:
   ```bash
   ./run_ollama.sh
   ```

### Funktionen des Scripts

Das Script führt automatisch folgende Aktionen aus:

- Startet den Ollama-Server in einer Screen-Session
- Überprüft und lädt bei Bedarf die erforderlichen Modelle (llama3:8b und llama3:70b)
- Zeigt Informationen über verfügbare Modelle
- Bietet Anleitungen zur Screen-Session-Verwaltung

### Screen-Session Management

Nach dem Start läuft der Server in einer Screen-Session namens 'ollama_session'. Wichtige Befehle:

- Liste aller aktiven Sessions anzeigen:
  ```bash
  screen -ls
  ```
- Session verlassen ohne zu beenden (detach):
  ```bash
  # Drücke Ctrl-A, dann D
  ```
- Zur Session zurückkehren:
  ```bash
  screen -r ollama_session
  ```
- Session komplett beenden:
  ```bash
  # In der Session: Drücke Ctrl-A, dann K, dann Y
  ```

### Zusätzliche Modelle laden

Um weitere Modelle zu laden, stelle sicher das ein Ollama-Server läuft und führe folgenden Befehl in einem Terminal-Fenster aus:
```bash
ollama pull 'füge_modell_namen_ein'
```

## Verwendung von Jupyter Notebooks

Jupyter Notebooks sind interaktive Dokumente, die Code, Visualisierungen und Text kombinieren.

1. Installiere die Jupyter Extension in VS Code
2. Führe folgende Befehle aus:
   ```bash
   ipython kernel install --user --name uni_chatbot
   ```
3. Im jeweiligen Notebook, wähle die zuvor erstelle venv als Kernel aus.

## (Optional, aber empfohlen) Anpassung der .bashrc

Die `.bashrc` ist eine Konfigurationsdatei für die Bash-Shell, die bei jedem Start einer neuen Shell-Sitzung ausgeführt wird. Mit dieser Anpassung wird die venv direkt bei SSH-Anmeldung aktiviert.

1. Öffne die Datei mit einem Texteditor:
   ```bash
   nano ~/.bashrc
   ```
2. Navigiere zum Ende der Datei
3. Füge folgende Zeilen hinzu:
   ```bash
   # activate venv
   source /home/username/venvs/uni_chatbot/bin/activate
   ```
4. Speichere und schließe die Datei (STRG+X, dann Y, dann Enter)
5. Aktiviere die Änderungen:
   ```bash
   source ~/.bashrc
   ```