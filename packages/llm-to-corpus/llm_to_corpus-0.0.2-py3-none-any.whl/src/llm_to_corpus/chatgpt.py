import openai
import time


class ChatGPT:
    def __init__(self, prompt):
        self.prompt = prompt

    def query_thread(self, text, translations, index):
        #    print(f"translate_thread. Entry: {text}")
        while True:
            try:
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    temperature=0,
                    max_tokens=2000,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant.",
                        },
                        {
                            "role": "user",
                            "content": f'"{self.prompt} {text}',
                        },
                    ],
                )
                break
            except Exception as error:
                print(f"Error call OpenAI: {error}")
                time.sleep(30)

        translated = completion.choices[0].message["content"]
        if "\n" in translated or "\r" in translated:
            print(f"error line feed: {translated}")
            translated = text

        translations[index] = translated
