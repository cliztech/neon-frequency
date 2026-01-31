import time
print("Importing langchain...")
start = time.time()
try:
    import langchain
    print(f"langchain imported in {time.time() - start:.2f}s")
except Exception as e:
    print(f"langchain failed: {e}")

print("Importing langgraph...")
start = time.time()
try:
    import langgraph
    print(f"langgraph imported in {time.time() - start:.2f}s")
except Exception as e:
    print(f"langgraph failed: {e}")

print("Importing langchain_google_genai...")
start = time.time()
try:
    import langchain_google_genai
    print(f"langchain_google_genai imported in {time.time() - start:.2f}s")
except Exception as e:
    print(f"langchain_google_genai failed: {e}")
