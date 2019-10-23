import watson_assistant
import price_identify
import response_data

MIN_PRICE = 1.98
DEC = True

class Agent:

    def __init__(self, name, room_num):
        self.my_name = name
        self.room_num = room_num
        
        self.user_intent = ""
        self.user_price = -1
        self.opponent_intent = ""
        self.opponent_price = -1
        
        self.my_price = 12.0
        self.min_price_said = self.my_price
        
        self.firstRound = True
        self.hasSpokenAlreadyThisRound = False

    
    def get_intent_index(self, intent):
    # User: buy_coffee (Only first round. Switch to coffee_info if detected in other rounds.)
    
      if intent == "buy_coffee":
        if self.firstRound:
          return 1
        else:
          intent = "coffee_info"
      
      if intent == "coffee_info":
        return 2
        
      if intent == "coffee_buy":
        return 3

      if intent == "cheaper_coffee":
        return 4

      if intent == "coffee_price":
        return 5
        
      # if it gets to this point just do coffee_info
      return 2

    def get_context_index(self, addressee):
      
      # 1 if we direct respond to user
      
      if addressee == self.my_name:
        return 1
      
      # 2 if other agent gave price
      elif self.opponent_price != -1:
        return 2
        
      # 3 if other agent did not give price:
      else: return 3
    
    # given dictionary, return reply
    def get_response(self,msg):
          
        reply = {}
        reply['inReplyTo'] = msg['currentState']
        reply['sender'] = self.my_name
        reply['transcript'] = "Please buy my coffee. I know you want to." #this shouldnt be said. only here as emergency backup
        reply['room'] = self.room_num
         
        sender = msg["sender"]
        if (sender == None or sender == "null"): sender = "User"
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
            print("Will respond. Has been addressed directly.")
        elif addressee == other_name:
            willRespond = False;
            print("Will not respond. Other agent has been addressed directly.")
        else:
            if sender == my_name:
                print("Will not respond. Is own message.")
                willRespond = False;
            else:
                print("Will respond. Is not addressed to anyone in particular.")
                willRespond = True;
        
        # Store data to preserve between passes
        if sender == my_name:
          print("Message from self") #just here as a placeholder really
        elif sender == "User":
          # get opponent_intent and opponent_price
          self.user_intent = watson_assistant.get_intent(transcript)
          self.hasSpokenAlreadyThisRound = False
          print("New round begin. User intent Id'd as ",self.user_intent)
          #user_price = price_identify.priceIdentify(transcript)
        else:# if sender == other_name:
          # get opponent_intent and opponent_price
          self.opponent_intent = watson_assistant.get_intent(transcript)
          self.opponent_price = price_identify.priceIdentify(transcript)
        
        # dont respond more than once per round
        if self.hasSpokenAlreadyThisRound:
          willRespond = False
          print("Will not respond. Has already spoken in this round.")
        
        # update min price
        if self.opponent_price != -1:
          self.min_price_said = min(self.min_price_said, self.opponent_price)
        self.min_price_said = min(self.min_price_said, self.my_price)
        
        if willRespond:
            self.hasSpokenAlreadyThisRound = True
            DidLower = True;
            
            #index = int(str(self.get_intent_index(self.user_intent))+str(self.get_context_index(addressee)))
            intent_index = self.get_intent_index(self.user_intent)
            context_index = self.get_context_index(addressee)
            index = int(str(intent_index)+str(context_index))
            
            #lower price if we can
            if index != 51 and index != 53:
              # is the opponents price bigger than mine?
              if self.min_price_said < self.my_price or intent_index == 4:
                # calc new price
                new_lowered_price = price_identify.lowerPrice(self.min_price_said, MIN_PRICE, DEC)
                if (new_lowered_price == -1):
                  DidLower = False;
                  self.my_price = MIN_PRICE
                else:
                  self.my_price = new_lowered_price
                  self.min_price_said = self.my_price
                  # Change context index to 2, if price changed
                  context_index = 2 #CHANGE (TODO: DISCUSS)
                  print("New lowest price, so 2nd digit changed to 2.")
              else:
                context_index = 1
            
            #TODO: Ensure didlower agrees with indices
            
            index = int(str(intent_index)+str(context_index))
            print("Calling response: ",index,self.my_price,DidLower)
            reply["transcript"] = response_data.callResponse(index, self.my_price, DidLower, DEC)
            
            self.firstRound = False;
            
        return reply;
        
        
# for testing
if __name__ == "__main__" :

    agent = Agent("Watson", 1001)

    # read transcript from input
    user_input = ""
    while(user_input != "quit"):
        msg = {}
        user_input = input('Sender: ')
        if user_input == "null": user_input = None
        msg["sender"] = user_input
        user_input = input('Transcript: ')
        msg["transcript"] = user_input
        user_input = input('Addressee: ')
        msg["addressee"] = user_input
        msg['currentState'] = ""
        
        # print response
        print(agent.get_response(msg))
    
