#!/bin/bash

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print section headers
print_header() {
    echo -e "${YELLOW}"
    echo "============================================================================"
    echo "  $1"
    echo "============================================================================"
    echo -e "${NC}"
}

# Function to print subsection headers
print_subheader() {
    echo -e "${CYAN}--- $1 ---${NC}"
}

# Function to check if Ollama server is running
check_ollama_server() {
    if pgrep -x "ollama" > /dev/null
    then
        echo "Ollama server is already running."
    else
        echo "Starting Ollama server..."
        ollama serve > /dev/null 2>&1 &
        sleep 5 # Wait for the server to start
    fi
}

# Function to check if a model exists
model_exists() {
    ollama list | grep -q "$1"
}

# Function to pull a model if it doesn't exist
pull_model_if_needed() {
    local model="$1"
    if model_exists "$model"; then
        echo "Model $model is already available."
    else
        echo "Pulling model $model..."
        if ollama pull "$model"; then
            echo "Successfully pulled $model."
        else
            echo "Error: Unable to pull $model. It may not exist or there might be a network issue."
        fi
    fi
}

get_model_info() {
    local model="$1"
    print_subheader "Information for model $model"
    ollama list | grep "$model" | sed 's/^/  /'
    echo
}

display_all_models_info() {
    print_header "All Available Models"
    ollama list | sed 's/^/  /'
    echo
}

# Function to display instructions for loading other models
display_load_instructions() {
    print_header "Loading Other Models"
    echo "To load other models:"
    echo -e "${Green}  1. Enter the screen session: ${GREEN}screen -r ollama_session${NC}"
    echo -e "${Green}  2. Then use the command: ${GREEN}ollama pull 'model_name'${NC}"
    echo
}

# Function to display Screen session instructions
display_screen_instructions() {
    print_header "Screen Session Instructions"
    echo -e "${MAGENTA}To see a list of all active screens:${NC}"
    echo "  screen -ls"
    echo -e "${MAGENTA}To detach from the Screen session (exit without stopping):${NC}"
    echo "  Press Ctrl-A, then D"
    echo -e "${MAGENTA}To stop the Screen session completely:${NC}"
    echo "  Press Ctrl-A, then K, then Y"
    echo -e "${MAGENTA}To reattach to an existing session:${NC}"
    echo "  Run 'screen -r session_name or id'"
    echo
}

# Main execution
main() {
    print_header "Ollama Server Status"
    # Start Ollama server in a Screen session if it's not already running
    if ! pgrep -x "ollama" > /dev/null; then
        if screen -list | grep -q "ollama_session"; then
            echo "An Ollama Screen session already exists. Attaching to it..."
            screen -r ollama_session -X stuff $'ollama serve\n'
        else
            echo "Starting new Ollama Screen session..."
            screen -dmS ollama_session bash -c "ollama serve; exec bash"
        fi
        echo "Ollama server started in a Screen session named 'ollama_session'"
        echo "You can attach to it using: screen -r ollama_session"
        echo "-----------------------------"
        sleep 5 # Wait for the server to start
    else
        echo "Ollama server is already running."
    fi

    print_header "Model Information"

    # Check, pull if needed, and show info for llama3:8b
    pull_model_if_needed "llama3:8b"
    get_model_info "llama3:8b"

    # Check, pull if needed, and show info for llama3:70b
    pull_model_if_needed "llama3:70b"
    get_model_info "llama3:70b"

    # Display model storage location
    print_subheader "Model Storage Location"
    echo "Ollama models are stored in: $HOME/.ollama$"
    echo

    # Display instructions for loading other models
    display_load_instructions

    # Display Screen session instructions
    display_screen_instructions

    display_all_models_info
}

# Run the main function directly
main