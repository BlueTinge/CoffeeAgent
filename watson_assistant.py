# connects to watson 

from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

api_key = "RBOj7ntUMp9NUo96Iy4clBDZi3m1ERCLAJLrTU2zLj1-"
assistant_id = "ff2388bb-4e1e-4eea-8f79-2f032f04cf8a"

# Set up Assistant service.
authenticator = IAMAuthenticator(api_key) # replace with API key
service = AssistantV2(
    version = '2019-02-28',
    authenticator = authenticator
)


def get_intent(transcript):

  # Create session.
  session_id = service.create_session(
      assistant_id = assistant_id
  ).get_result()['session_id']

  # Initialize message_input with transcript (input text)
  message_input = {
    'message_type:': 'text',
    'text': transcript
    }

  
  # Start conversation with empty message.
  response = service.message(
      assistant_id,
      session_id,
      input = message_input
  ).get_result()

  intent = ""
  # If an intent was detected, set it to be returned.
  if response['output']['intents']:
      intent = response['output']['intents'][0]['intent']
  
  # Print the output from dialog, if any. Supports only a single
  # text response.
  #if response['output']['generic']:
  #    if response['output']['generic'][0]['response_type'] == 'text':
  #        print(response['output']['generic'][0]['text'])

  # We're done, so we delete the session.
  service.delete_session(
      assistant_id = assistant_id,
      session_id = session_id
  )
  
  # Return the intent 
  return intent

# for testing
if __name__ == "__main__" :

    # read transcript from input
    user_input = input('>> ')
    
    # get intent
    print(get_intent(user_input))
    