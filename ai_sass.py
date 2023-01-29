import cohere
co = cohere.Client('TaTahdTgwZi7MIAPmTqwQQkhOJXxyX9ANEsvcuzR')

response = co.generate(  
    model='xlarge',  
    prompt = "Given a correlation coefficient between a google search's popularity and a stock's prices, this program generates a sassy bot comment.\n\nCorrelation Coefficient:-1\nComment:You can't be ugly AND not know the difference between causation and correlation, pick a struggle.\n--\nCorrelation Coefficient: 1\nComment: Based on my calculations, you should invest all your money into this stock. An AI told you to do it, so it must be true, right?\n--\nCorrelation Coefficient-0.6\nComment: Bro just give up already; getting rich via the stock market is no way to get b*tches\n--\nCorrelation Coefficient: 0.5\nComment: If she's talking to you once a day im sorry bro thats not flirting that standup\n--\nCorrelation Coefficient:-0.1\nComment:You know what would be a fun game to play with your friends? Buy some stocks, and then watch them get more and more worthless. Wait, do you even have friends?\n--\nCorrelation Coefficient:0\nComment:Why would your dumbass ever think that the search volume of bananas will be able to predict the stock prices of CQB???\n--\nCorrelation Coefficient:0.4\nComment: You know what would be a fun game to play with your friends? Buy some stocks, and then watch them get more and more worthless.\n", 
    max_tokens=100,  
    temperature=0.6,  
    stop_sequences=["--"])

print('Insight: {}'.format(response.generations[0].text))
