try:
    from langchain_ollama import ChatOllama
    print("FOUND: langchain_ollama")
except ImportError:
    try:
        from langchain_community.chat_models import ChatOllama
        print("FOUND: langchain_community")
    except ImportError:
        print("MISSING")
