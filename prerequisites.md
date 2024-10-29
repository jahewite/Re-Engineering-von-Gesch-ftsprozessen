# SSH Login und Server-Nutzung Guide

## SSH Login auf Remote Server

SSH (Secure Shell) ermöglicht eine sichere Verbindung zu einem entfernten Server. Hier sind die Schritte für den Login:

1. Installiere VS Code (https://code.visualstudio.com/download)
2. Installiere die Remote SSH Erweiterung in VS Code
3. Verbinde dich mit dem Remote Server über den Befehl:
   ```
   ssh benutzer@serveradresse
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
source /home/m_mustermann/venvs/uni_chatbot/bin/activate
```

## Clonen eines Git-Repos

Git ist ein Versionskontrollsystem. Mit dem Klonen eines Repos kopierst du ein bestehendes Repository auf deinen lokalen Rechner oder Server.

```bash
git clone path/to/repo
```

## Verwendung von Jupyter Notebooks

Jupyter Notebooks sind interaktive Dokumente, die Code, Visualisierungen und Text kombinieren.

1. Installiere die Jupyter Extension in VS Code
2. Führe folgende Befehle aus:
   ```bash
   pip install jupyter
   ipython kernel install --user --name uni_chatbot
   ```

## Installation requirements.txt

Eine `requirements.txt` Datei listet alle Python-Pakete auf, die für ein Projekt benötigt werden. Sie erleichtert die Installation aller notwendigen Abhängigkeiten.
```bash
pip install requirements.txt
```

## (Optional) Anpassung der .bashrc

Die `.bashrc` ist eine Konfigurationsdatei für die Bash-Shell, die bei jedem Start einer neuen Shell-Sitzung ausgeführt wird.

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