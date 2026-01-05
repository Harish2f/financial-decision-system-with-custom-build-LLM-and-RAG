import subprocess

class LLMClient:
    def __init__(self, model="mistral"):
        self.model = model

    def generate(self, prompt: str) -> str:
        """Call Ollama LLM using stdin (latest CLI)."""
        try:
            result = subprocess.run(
                ["ollama", "run", self.model],
                input=prompt,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print("Ollama error:", e)
            return ""
        except FileNotFoundError:
            print("Ollama executable not found!")
            return ""