
"""
Code chunk that will take input and determine if there is a price present in it
follows a rule of the price being followed by the currency or preceded by $


"""



def priceIdentify(sentence):
    
    currencies = ['dollar', 'yuan', 'kuai', 'RMB']
    curr = 'None'
    price = -1
    
    for i in currencies:
        if i in sentence:
            curr = i
    
    if curr != 'None':
        curr_start = sentence.find(curr) - 1
        
        temp = curr_start - 1
        
        
        while (sentence[temp] != ' '):
            temp = temp - 1
            if temp == -1:
                break
            
        temp = temp + 1
        
        try:
            price = float(sentence[curr_start : temp])
        except:
            price = -1
    
    
    if '$' in sentence:
        curr_start = sentence.find('$') + 1
        
        temp = curr_start
        
        while (sentence[temp] != ' '):
            temp = temp + 1
            if temp == len(sentence):
                break
        
        try:
            price = float(sentence[curr_start : temp])
        except:
            price = -1
        

    return price



def lowerPrice(price, dec = True):
    
    min_price = 2.00
    
    if price < min_price:
        return -1
    
    price_new = price - min_price
    price_new = price_new * 0.9
    price_new = price_new + min_price
    
    
    if dec:
        price_new = round(price_new, 2)
        
    else:
        if price - min_price < 10:
            price_new = price - 1        
        price_new = int(round(price_new, 0))
    
    return price_new
    


