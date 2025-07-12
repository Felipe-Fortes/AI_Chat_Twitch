from openai import OpenAI
from dotenv import load_dotenv
import os
from elevenlabs import ElevenLabs, play

load_dotenv()

# Configurar cliente ElevenLabs
elevenlabs_client = ElevenLabs(
    api_key=os.getenv('ELEVENLABS_API_KEY')
)

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv('AI_API_KEY'),
)

# Carregar o prompt do arquivo JSON
with open("prompts.json", "r", encoding="utf-8") as file:
    prompt_content = file.read().strip()

completion = client.chat.completions.create(
  extra_body={},
  model="deepseek/deepseek-chat-v3-0324:free",
  messages=[
    {
      "role": "user",
      "content": prompt_content
    }
  ]
)

# Obter a resposta da IA
response_text = completion.choices[0].message.content

# Exibir o texto original (com formatação)
print(response_text)

# Limpar o texto para áudio (remover asteriscos e outras formatações)
audio_text = response_text.replace('*', '').replace('#', '').replace('**', '')

print("\n🔊 Gerando áudio com ElevenLabs...")
audio = elevenlabs_client.text_to_speech.convert(
    voice_id="33B4UnXyTNbgLmdEDh5P", 
    text=audio_text,
    model_id="eleven_multilingual_v1"
)

# Reproduzir o áudio
play(audio)

print("✅ Áudio reproduzido com sucesso!")