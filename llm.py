from llama_cpp import Llama
import re

class PyLlama():
    def __init__(self):
        self.llm = Llama(
            model_path="models/llama-7b/mistral-7b.gguf",
            n_gpu_layers=1,
            n_threads=6,
        )
        self.response: str  = ""


    def clean_response(self, response)-> str:

        try:

            if msg := response['choices'][0]['message']['content']:
                
                return re.sub(r'^\s*\[INST\]\s*|\s*$', '', msg).strip()
        
        except KeyError as e:
            print(f"KeyError: {e}")
            return ""

    def  ask_ai(self, prompt):

        print("Asking AI:", prompt)

        response = self.llm.create_chat_completion(
            messages = [{"role": "user", "content": prompt}],max_tokens=100,
            stop=["[/INST]"],
            # temperature=0.7,
        )
        tmp = self.clean_response(response)
        print("clean Response:", tmp)
        self.response = tmp