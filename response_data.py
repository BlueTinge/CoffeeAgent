    

response = {}
response[111] = {0: ['My coffee is really good, @a and I can sell it to you for $@p', 'I sell coffee, its only $@p and @a', 'You can buy my coffee, it is only $@p and @a'], 1: []}
response[121] = {0: ['I can sell you coffee for $@p instead and @a', 'I sell coffee too, I can give it to you for $@p and @a'], 1: []}
response[120] = {0: ['There are some cheap, low-grade, coffee-pushing swindlers out there who would dare to sell you substandard coffee. I could not dishonor myself to such a level. Please accept my coffee for $@p. You will not regret it.', 'At the end of your life, every experience you have ever had will flash before your eyes, and one by one, you will forget each one. Except for the taste of my coffee. I implore you: buy my coffee. Not for me, but for you.'], 1: []}
response[131] = response[111]
response[211] = {0: ['You would love my coffee because @a.', 'People say my coffee is the best around, its because @a.', 'You should buy my coffee because @a.'], 1: []}
response[221] = response[121]
response[231] = {0: ['My coffee is good too, @a', 'That coffee sounds good, but is it as good as my coffee? After all, @a', 'But would you like to try my coffee? I think you would, since @a'], 1: []}
response[311] = {0: ['Great! Here is your coffee.', 'Sure! Here you go!', 'Hand over the cash.'], 1: []}
response[321] = {0: ['I can give it to you at a cheaper price of $@p.', 'My coffee can be bought for less, it\'s only $@p.', 'That price is still quite high, I can sell it for @p instead.'], 1: []}
response[320] = response[120]
response[331] = response[321]
response[320] = response[120]
response[411] = {0: ['I can give it to you for $@p. This is a great price for my coffee, since @a', 'Yes, I can give it to you for the incredible price of $@p. Did I mention @a?', 'Sure, @a But for you, I would be willing to sell my coffee for just $@p. '], 1: []}
response[410] = {0: ['I could not possibly lower the price even more, but once you taste it, you will understand that it is worth every cent.', 'I am really sorry but to maintain quality, I can\'t lower the price more.'], 1: []}
response[421] = response[321]
response[420] = response[120]
response[431] = response[411]
response[430] = response[410]
response[511] = {0: ['My coffee is just $@p.', 'You can get my coffee for $@p.'], 1: []}
response[521] = response[421]
response[531] = response[411]


def resetResponse(index):
    response[index][0] = response[index][1].copy()
    response[index][1] = []
    

def callResponse(index, yn=1):
    
    r = index * 10
    r = r + yn
    
    msg = response[r][0].pop()
    response[r][1].append(msg)
    
    if len(response[r][0]) == 0:
        resetResponse(r)
    
    return msg


advantages = {0: ['it\'s made using a special family technique.', 'I import my beans from the best plantations.', 'it\'s so popular I am sold out most days.', 'it\'s a local specialty.', 'it has the richest flavour you will ever taste', 'it is the only coffee that tastes as good as it smells', 'it is a special mixture of blends that no other coffee can match', 'I get tons of people coming back for more.', 'I\'m extremely strict in the quality of every cup.', 'to know this taste is to know true bliss'], 1: []}
