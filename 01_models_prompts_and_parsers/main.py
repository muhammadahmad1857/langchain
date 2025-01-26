from services.gemini_service import call_llm


# Creating a prompt with simple python

# text = "I am just playing cricket and I am so tired I don't know why today I have to do so much work"

# style="In american english with calm and respective way"

# prompt = f"""
# Write a story based on the following context in triple backticks: 

# ```
# {text}
# ```


# Include at least three specific examples to illustrate the events or themes in the story.

# Style: {style}
# """

# # Calling the LLM to generate a response
# response = call_llm(prompt)

# print(response)



# Now using langchain prompt templates

# from langchain.prompts import ChatPromptTemplate

# # Define the prompt template

# text = "I am just playing cricket and I am so tired I don't know why today I have to do so much work"

# style="In american english with calm and respective way"

# prompt = """
# Write a story based on the following context in triple backticks: 

# ```
# {text}
# ```


# Include at least three specific examples to illustrate the events or themes in the story.

# Style: {style}
# """


# # Create a ChatPromptTemplate from the prompt

# chat_prompt = ChatPromptTemplate.from_template(prompt)
# # print(chat_prompt.messages[0].prompt.input_variables)


# llm_prompt = chat_prompt.format_messages(
#     text=text,
#     style=style,
# )

# resp = call_llm(llm_prompt[0].content)

# print(resp)


customer_review = """\
This leaf blower is pretty amazing.  It has four settings:\
candle blower, gentle breeze, windy city, and tornado. \
It arrived in two days, just in time for my wife's \
anniversary present. \
I think my wife liked it so much she was speechless. \
So far I've been the only one using it, and I've been \
using it every other morning to clear the leaves on our lawn. \
It's slightly more expensive than the other leaf blowers \
out there, but I think it's worth it for the extra features.
"""

review_template = """\
For the following text, extract the following information:

gift: Was the item purchased as a gift for someone else? \
Answer True if yes, False if not or unknown.

delivery_days: How many days did it take for the product \
to arrive? If this information is not found, output -1.

price_value: Extract any sentences about the value or price,\
and output them as a comma separated Python list.

Format the output as JSON with the following keys:
gift
delivery_days
price_value

text: {text}
"""


from langchain.prompts import ChatPromptTemplate

prompt_template = ChatPromptTemplate.from_template(review_template)
print(prompt_template)
messages = prompt_template.format_messages(text=customer_review)
response = call_llm(messages[0].content)
print(response)

print("Type of response -> ",type(response)) # str

# You will get an error by running this line of code 
# because'gift' is not a dictionary
# 'gift' is a string
# response.content.get('gift') # throw error



# To fix this error, you can parse the JSON response into a dictionary using langchain parsers

from langchain.output_parsers import ResponseSchema, StructuredOutputParser


gift_schema = ResponseSchema(name="gift",
                             description="Was the item purchased\
                             as a gift for someone else? \
                             Answer True if yes,\
                             False if not or unknown.")
delivery_days_schema = ResponseSchema(name="delivery_days",
                                      description="How many days\
                                      did it take for the product\
                                      to arrive? If this \
                                      information is not found,\
                                      output -1.")
price_value_schema = ResponseSchema(name="price_value",
                                    description="Extract any\
                                    sentences about the value or \
                                    price, and output them as a \
                                    comma separated Python list.")

response_schemas = [gift_schema, 
                    delivery_days_schema,
                    price_value_schema]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas) # strucutring the ouptut

format_instructions = output_parser.get_format_instructions() # getting instructions

print(format_instructions)

review_template_2 = """\n
For the following text, extract the following information:

gift: Was the item purchased as a gift for someone else? \n
Answer True if yes, False if not or unknown.

delivery_days: How many days did it take for the product\n
to arrive? If this information is not found, output -1.

price_value: Extract any sentences about the value or price,\n
and output them as a comma separated Python list.

text: {text}

{format_instructions}
"""

prompt = ChatPromptTemplate.from_template(template=review_template_2)

messages = prompt.format_messages(text=customer_review, 
                                format_instructions=format_instructions)

response = call_llm(messages[0].content)

print("response ->",response)

parsed_response = output_parser.parse(response)

print("Parsed Response -> ",parsed_response)

print("Type of parsed_response -> ",type(parsed_response)) # dict

# Now you can access the parsed information like this
print("Gift -> ", parsed_response['gift'])
print("Delivery Days -> ", parsed_response['delivery_days'])
print("Price Value -> ", parsed_response['price_value'])