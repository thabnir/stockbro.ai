import cohere
co = cohere.Client('3Mbg1ik6CxQKc2zS3iJMMzYB72ySlG8rFPTVr4Zj')

# generate a prediction for a prompt
prediction = co.generate(
    model='large',
    prompt='co:here',
    max_tokens=100)

# print the predicted text
print('prediction: {}'.format(prediction.generations[0].text))