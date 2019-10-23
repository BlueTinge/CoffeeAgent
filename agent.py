import watson_assistant
import price_identify

class Agent:

    def __init__(self, name, room_num):
        self.my_name = name
        self.room_num = room_num
        
        self.user_intent = ""
        self.user_price = -1
        self.opponent_intent = ""
        self.opponent_price = -1

    # given dictionary, return reply
    def get_response(self,msg):
          
        reply = {}
        reply['inReplyTo'] = msg['currentState']
        reply['sender'] = self.my_name
        reply['transcript'] = "null"
        reply['room'] = self.room_num
         
        sender = msg["sender"]
        transcript = msg["transcript"]
        addressee = msg["addressee"]
        
        my_name = self.my_name
        if my_name == "Watson":
            other_name = "Celia"
        else:
            other_name = "Watson"
        
        # Determine whether we will respond to this message
        willRespond = False;
        if addressee == my_name:
            willRespond = True;
        elif addressee == other_name:
            willRespond = False;
        else:
            if sender == my_name:
                willRespond = False;
            else:
                willRespond = True;
        
        # Store data to preserve between passes
        if sender == my_name:
          print("Message from self") #just here as a placeholder really
        elif sender == "User":
          # get opponent_intent and opponent_price
          self.user_intent = watson_assistant.get_intent(transcript)
          #user_price = price_identify.priceIndentify(transcript)
        else:# if sender == other_name:
          # get opponent_intent and opponent_price
          self.opponent_intent = watson_assistant.get_intent(transcript)
          other_price = price_identify.priceIndentify(transcript)
          self.opponent_price = other_price
          
        # now select correct response
        
        
        return reply;
        
        
# for testing
if __name__ == "__main__" :

    agent = Agent("Watson", 1001)

    # read transcript from input
    user_input = ""
    while(user_input != "quit"):
        msg = {}
        user_input = input('Sender: ')
        msg["sender"] = user_input
        user_input = input('Transcript: ')
        msg["transcript"] = user_input
        user_input = input('Addressee: ')
        msg["addressee"] = user_input
        msg['currentState'] = ""
        
        # print response
        print(agent.get_response(msg))
    
