from gemini_webapi import GeminiClient
import asyncio
import requests

Secure_1PSID = "YOUR 1PSID KEY"
Secure_1PSIDTS = "YOUR 1PSIDTS KEY"
url = "https://bff.listnr.tech/backend/ttsNewDemo"


async def speech(a):
    data = {
        "ttsService": "azure",
        "audioKey": "62cc2f1bff7e29001da9e16f",
        "storageService": "s3",
        "audioOutput": {
            "fileFormat": "mp3",
            "sampleRate": 24000
        },
        "text": f"""<speak><p>{a}</p></speak>""",
        "voice": {
            "value": "hi-IN-MadhurNeural",
            "lang": "hi-IN"
        },
        "lang": "hi-IN",
        "wordCount": 8
    }
    try:
        r = requests.post(url, json=data)
        r.raise_for_status()
        response_data = r.json()
        print(response_data)
    except requests.RequestException as e:
        print("Request failed:", e)


async def process_question(chat, question):
    response = await chat.send_message(question)
    print("Response from Gemini:", response.text)

    await speech(response.text)


async def main():
    client = GeminiClient(Secure_1PSID, Secure_1PSIDTS, proxies=None)
    await client.init(timeout=30, auto_close=False, close_delay=300, auto_refresh=True)

    youtube_link = input("YouTube video link: ")

    previous_session = None

    while True:
        full_query = f"give the text speech from the following video {youtube_link}"

        chat = client.start_chat()
        if previous_session:
            chat = client.start_chat(metadata=previous_session)

        response = await chat.send_message(full_query)
        speech_text = response.text

        hindi_conversion_query = "convert the above text into Hindi"
        hindi_response = await chat.send_message(hindi_conversion_query)

        print("Translated text in Hindi:")
        a = hindi_response.text
        await speech(a)

        choice = input("Do you want to continue? (yes/no): ")
        if choice.lower() != "yes":
            break
        else:
            question = input("Specify your question clearly: ")
            await process_question(chat, question)

        previous_session = chat.metadata

asyncio.run(main())
