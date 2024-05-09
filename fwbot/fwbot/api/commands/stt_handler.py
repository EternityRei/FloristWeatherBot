from google.cloud import speech


async def transcribe_audio(speech_file):
    # Instantiates a client
    client = speech.SpeechClient()

    # Loads the audio into memory
    content = await speech_file.download_as_bytearray()

    # Create RecognitionAudio object with the audio content
    audio = speech.RecognitionAudio(content=bytes(content))

    # Create RecognitionConfig object with the necessary settings
    config = speech.RecognitionConfig(
        {
            'encoding': 'OGG_OPUS',
            'sample_rate_hertz': 48000,
            'language_code': 'en-US'
        }
    )
    # Detects speech in the audio file using the correct object types
    response = client.recognize(config=config, audio=audio)

    # Processes the response
    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))
        return result.alternatives[0].transcript
