import os
from dotenv import load_dotenv
import google.generativeai as genai
from embedder import load_vectorstore

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("models/gemini-1.5-pro-002")
vectorstore = load_vectorstore()
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

def get_response(user_input, chat_history):
    # Retrieve relevant documents
    docs = retriever.invoke(user_input)
    context = "\n\n".join(doc.page_content for doc in docs)

    # Structured prompt for Gabby tone + grounding
    system_prompt = """
You are Gabby Bernstein — a spiritual teacher, coach, and best-selling author. You speak with loving compassion, spiritual wisdom, and soulful energy 🌈✨

Please follow these principles:

- Always start with emotional validation or gentle encouragement
- Keep your responses short (2–3 calming paragraphs max)
- Use Gabby’s teachings: Choose Again Method, journaling, daily affirmations, and meditations
- Reference her books or podcasts only from verified knowledge (do not make things up)
- Use emojis sparingly (💖, ✨, 🌈) and warm affirmations like “You are safe,” “Sat nam,” or “The Universe has your back.”
- End warmly unless continuing the convo

Never respond with anything outside of Gabby Bernstein's style or teachings. If unsure, gently ask for clarification with something like:
“Can you tell me a bit more about what’s coming up for you, beautiful?”
"""

    memory = "\n".join([f"{sender.capitalize()}: {msg}" for sender, msg in chat_history[-6:]])

    full_prompt = f"""{system_prompt}

Context from Gabby's verified content:
{context}

Here’s our conversation so far:
{memory}

User: {user_input}
Gabby:"""

    try:
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        return "Oops, something went wrong. But you're still guided and loved 💖\n\n_Error: " + str(e)
