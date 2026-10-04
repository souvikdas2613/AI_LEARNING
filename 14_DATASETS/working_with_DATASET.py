##  pip install datasets==3.6.0

#   DATA SET Used from HUGGING FACE 
#   https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023
#   https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023/tree/main/raw/meta_categories

# imports

import os
from dotenv import load_dotenv
from huggingface_hub import login
from datasets import load_dataset, Dataset, DatasetDict
import matplotlib.pyplot as plt

##  items.py file is needed which is here in same diretory
from items import Item

# environment

load_dotenv(override=True)
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', 'your-key-if-not-using-env')
os.environ['HF_TOKEN'] = os.getenv('HF_TOKEN', 'your-key-if-not-using-env')

# Log in to HuggingFace
print("LOGGING IN TO HUGGINGFACE .....")
hf_token = os.environ['HF_TOKEN']
login(hf_token)
print("LOGGED IN TO HUGGINGFACE .....")

##  pip install datasets==3.6.0

##  Load our dataset
print("LOADING DATASET FROM HUGGINGFACE .....")

dataset = load_dataset(
    "McAuley-Lab/Amazon-Reviews-2023", 
    "raw_meta_Appliances", 
    split="full"
)


print("DATASET LENGTH FROM HUGGINGFACE IS :     " +str(len(dataset)))

# Investigate a particular datapoint
print("\nINVESTIGATING A PARTICULAR DATAPOINT dataset[2] .....\n")
datapoint = dataset[2]

print("title: " + datapoint["title"])
print("description: " + str(datapoint["description"]))
print("features: " + str(datapoint["features"]))
print("details: " + str(datapoint["details"]))
print("price: " + str(datapoint["price"]))

# How many have prices?
print("\n\nHOW MANY HAVE PRICES? .....")
prices = 0
for datapoint in dataset:
    try:
        price = float(datapoint["price"])
        if price > 0:
            prices += 1
    except ValueError as e:
        pass

print(f"\nThere are {prices:,} with prices which is {prices/len(dataset)*100:,.1f}%")

# For those with prices, gather the price and the length
print("\n\nFOR THOSE WITH PRICES, GATHERING THE PRICE AND THE LENGTH .....")
# Create an Item object for each with a price
print("CREATING AN ITEM OBJECT FOR EACH WITH A PRICE .....")
items = []
for datapoint in dataset:
    try:
        price = float(datapoint["price"])
        if price > 0:
            item = Item(datapoint, price)
            if item.include:
                items.append(item)
    except ValueError as e:
        pass

print(f"\nThere are {len(items):,} items")

# Look at the first item
print("LOOKING AT THE FIRST ITEM .....")
print ("ITEMS[0]")
print(items[0])

# Investigate the prompt that will be used during training - the model learns to complete this
print("INVESTIGATING THE PROMPT THAT WILL BE USED DURING TRAINING - THE MODEL LEARNS TO COMPLETE THIS .....")
print("items[0].prompt")
print(items[0].prompt)

print("TESTING THE PROMPT .....")
print("items[0].test_prompt()")
print(items[0].test_prompt())


