import os
from groq import Groq

class GroqClient:
    def __init__(self, api_key: str = None):
        """
        Initializes the Groq API client.
        Looks for GROQ_API_KEY in the environment if not explicitly provided.
        """
        # If API key is not passed, Groq client automatically loads GROQ_API_KEY env var
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        
        # We don't crash on init if key is missing, so we can run server health checks 
        # but we will fail gracefully when trying to run queries.
        self.client = None
        if self.api_key:
            self.client = Groq(api_key=self.api_key)

    def generate_answer(self, system_prompt: str, user_prompt: str, model_name: str = "llama3-8b-8192") -> str:
        """
        Queries the Groq API to generate an answer based on RAG prompt context.
        
        Args:
            system_prompt (str): High-level steering instructions (rules, boundaries).
            user_prompt (str): Document context segments and user question.
            model_name (str): Groq LLM model name (default: Llama 3 8B).
            
        Returns:
            str: Generated textual response.
        """
        if not self.client:
            # Check env again in case it was set after initialization
            self.api_key = self.api_key or os.getenv("GROQ_API_KEY")
            if not self.api_key:
                return "Error: GROQ_API_KEY is not set. Please add it to your environment or .env file."
            self.client = Groq(api_key=self.api_key)

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model=model_name,
                temperature=0.0  # Set to 0.0 for deterministic, factual, RAG replies
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error connecting to Groq: {str(e)}"
