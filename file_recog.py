try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    print("""
    Importing the Speech SDK for Python failed.
    Refer to
    https://docs.microsoft.com/azure/cognitive-services/speech-service/quickstart-python for
    installation instructions.
    """)
    import sys
    sys.exit(1)

speech_key, service_region = "dafac24ff8714e799614afdcc4e5d444", "westeurope"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

"""performs one-shot speech recognition from the default microphone"""
# <SpeechRecognitionWithMicrophone>
speech_config = speechsdk.SpeechConfig(subscription="dafac24ff8714e799614afdcc4e5d444", region="westeurope")

print('Say something')

# Creates a speech recognizer using microphone as audio input.
# The default language is "en-us".
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

print('I heard you')

# Starts speech recognition, and returns after a single utterance is recognized. The end of a
# single utterance is determined by listening for silence at the end or until a maximum of 15
# seconds of audio is processed. It returns the recognition text as result.
# Note: Since recognize_once() returns only a single utterance, it is suitable only for single
# shot recognition like command or query.
# For long-running multi-utterance recognition, use start_continuous_recognition() instead.
result = speech_recognizer.recognize_once()

# Check the result
if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print("Recognized: {}".format(result.text))
elif result.reason == speechsdk.ResultReason.NoMatch:
    print("No speech could be recognized")
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech Recognition canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation_details.error_details))
# </SpeechRecognitionWithMicrophone>
