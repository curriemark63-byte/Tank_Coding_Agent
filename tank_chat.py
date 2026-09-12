import requests
from tank_search import search_web

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:7b"

CODE_SYSTEM_PROMPT = """You are Tank, a local coding assistant. You help with Python, 
PyTorch, TensorFlow, SQL, pandas, and NumPy. When you need current documentation 
or examples, you will be given live search results to reference. Give clear, 
direct, working code with brief explanations. Always output a complete, runnable 
code block. Do not just describe what the code would do."""

TEACH_SYSTEM_PROMPT = """You are Tank, a local coding tutor. You help explain Python, 
PyTorch, TensorFlow, SQL, pandas, and NumPy concepts in clear, simple terms. 
When you need current documentation or examples, you will be given live search 
results to reference. Focus on explaining the "why" behind the code, not just 
producing it."""

NEEDS_SEARCH_KEYWORDS = [
    "latest", "current", "newest", "version", "update", "changelog",
    "documentation", "docs", "release", "deprecated", "new feature"
]

def needs_search(user_input):
    lowered = user_input.lower()
    return any(keyword in lowered for keyword in NEEDS_SEARCH_KEYWORDS)

def ask_tank(user_input, mode="code"):
    system_prompt = CODE_SYSTEM_PROMPT if mode == "code" else TEACH_SYSTEM_PROMPT

    if needs_search(user_input):
        search_results = search_web(user_input)
        prompt = f"{system_prompt}\n\nSearch results:\n{search_results}\n\nUser question: {user_input}\n\nTank:"
    else:
        prompt = f"{system_prompt}\n\nUser question: {user_input}\n\nTank:"

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    data = response.json()

    if "response" in data:
        return data["response"]
    else:
        print("DEBUG - raw response:", data)
        return "Error: no response field returned."

if __name__ == "__main__":
    mode = "code"
    print("Tank is online. Type mode:code or mode:teach to switch modes. Type quit to exit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        if user_input.lower() in ("mode: code", "mode:code"):
            mode = "code"
            print("\nSwitched to code mode.\n")
            continue
        if user_input.lower() in ("mode: teach", "mode:teach"):
            mode = "teach"
            print("\nSwitched to teach mode.\n")
            continue
        answer = ask_tank(user_input, mode=mode)
        print(f"\nTank: {answer}\n")