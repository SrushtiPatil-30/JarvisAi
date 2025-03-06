import openai
from config import apikey

# Set OpenAI API Key
openai.api_key =apikey

def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are an AI assistant."},
                      {"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while generating the response."

if __name__ == "__main__":
    prompt = "Write an email to my boss for resignation?"
    result = generate_response(prompt)
    print(result)
