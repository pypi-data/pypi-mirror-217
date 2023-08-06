def sentiment_analysis(text: str) -> str:
    prompt = f"Analyze the sentiment of the following text: '{text}'"
    return prompt

def generate_text(prompt: str, length: int = 50) -> str:
    prompt = f"Generate {length} words of text based on the following prompt: '{prompt}'"
    return prompt

def extract_entities(text: str) -> str:
    prompt = f"Extract named entities from the following text: '{text}'"
    return prompt

def topic_modeling(texts: List[str], num_topics: int = 5) -> str:
    prompt = f"Identify {num_topics} topics in the following collection of documents: {texts}"
    return prompt

def summarize_text(input_text: str):
    prompt = f"summarize the following text: '{input_text}'"
    return prompt