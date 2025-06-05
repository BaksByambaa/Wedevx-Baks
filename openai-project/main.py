from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main():
   # Get API key from environment variable
   api_key = os.getenv("OPENAI_API_KEY")
   print(f"API Key loaded: {'Yes' if api_key else 'No'}")
   
   if not api_key:
       raise ValueError("OPENAI_API_KEY environment variable is not set")

   # Initialize the OpenAI client with your API key
   client = OpenAI(api_key=api_key)

   resp = client.chat.completions.create(
       
    model="gpt-4o",

    messages = [
        {"role": "system", "content": "You are the technical resume creator with experience at OpenAI, Google, Notion as a head of recruiting, you have seen thousands of resumes, you know what resumes are bad and which ones make a great first impression and get a initial screening call request"},
        
        {"role": "user",   "content": "Create a resume for an AI Engineering role"}
    ],
    stream=True
    )
   
   for chunk in resp:
    if chunk.choices[0].delta.content is not None:
       print(chunk.choices[0].delta.content, end="", flush=True)
    
print()



if __name__ == "__main__":
    main()