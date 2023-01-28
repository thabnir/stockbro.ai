import cohere
co = cohere.Client("<<TaTahdTgwZi7MIAPmTqwQQkhOJXxyX9ANEsvcuzR>>")

prompt = f"""  
This program generates a sassy bot comment given a (stock and a google search word) correlation coefficient

Word: Bananas
Stock: Microsoft  
Comment: You can't be ugly AND not know the difference between causation and correlation, pick a struggle 
--  
Word: Covid-19 
Stock: Amazon  
Comment: Based on my calculations, you should invest all your money into Amazon as Covid-19's popularity grows. 
--  
Word: Hippopotamus 
Stock: Tesla
Comment: 

--  
Word: Education  
Stock: Apple  
Comment: 

--  
Word: Canada
Stock: Instacart
Comment: 

--
Word: 
Stock:
Comment: 

--
Word: 
Stock:
Comment: 

--
Word: 
Stock:
Comment: 

--
Word: 
Stock:
Comment: 

--
Word: 
Stock:
Comment: 

--
Word: 
Stock:
Comment: 

"""
response = co.generate(
    model='xlarge',
    prompt = prompt,
    max_tokens=50,
    temperature=0.4,
    stop_sequences=["--"])

comment = response.generations[0].text