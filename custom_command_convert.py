import os

func = os.getenv("function")

print(func[func.find(":", 8)+1:].strip())