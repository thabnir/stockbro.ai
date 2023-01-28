import cohere
co = cohere.Client("<<TaTahdTgwZi7MIAPmTqwQQkhOJXxyX9ANEsvcuzR>>")

response = co.generate(  
    model='xlarge',  
    prompt = "Given a correlation coefficient between a google search's popularity and a stock's prices, this program generates a sassy bot comment.\n\nCorrelation Coefficient: -1\nComment:You can't be ugly AND not know the difference between causation and correlation, pick a struggle.\n--\nCorrelation Coefficient: 1\nComment: Based on my calculations, you should invest all your money into this stock. An AI told you to do it, so it must be true, right?\n--Correlation Coefficient: -0.6\nComment: Bro just give up already; getting rich via the stock market is no way to get b*tches\n--\nCorrelation Coefficient: 0.5\nComment: If shes talking to you once a day im sorry bro thats not flirting that standup\n--Correlation Coefficient: -0.1\nComment: --\nPost: Going to unmute at the end of the Zoom meeting to say bye and realizing you were actually unmuted the whole call\nComment:",
    max_tokens=50,  
    temperature=0.4,  
    stop_sequences=["--"])

print('Insight: {}'.format(response.generations[0].text))
