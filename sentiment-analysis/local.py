from flask import Flask, request, jsonify
import torch
import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import time



start_time = time.time()

# test dataset
data_to_test = ["Dow Jones Slumps 225 Points Despite Big JPMorgan Rally; Boeing Dives On 737 MAX Halt; On Holding Jumps 3.5%",
"GLOBAL MARKETS-Dollar, yields gain as expectations of Fed rate hike increase",
"Key Indexes Have Turned Bullish: What That Means for Stocks",
"Dow Jones Falls As Boeing Skids On 737 Woes; JPMorgan Jumps On Earnings",
"Stocks fall, JPMorgan surges after earnings: Stock market news today",
"US STOCKS-Wall St mixed as retail sales data offsets bank earnings cheer",
"Bank stocks rally following earnings data, tech under pressure"]

# load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

inputs = tokenizer(data_to_test, padding = True, truncation = True, return_tensors='pt')
outputs = model(**inputs)
predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

positive = predictions[:, 0].tolist()
negative = predictions[:, 1].tolist()
neutral = predictions[:, 2].tolist()

table = {'Headline':data_to_test,
         "Positive":positive,
         "Negative":negative, 
         "Neutral":neutral}

end_time = time.time()
total_time = end_time - start_time

print(f"Running Time：{total_time:.2f} seconds")

# Running Time：9.63 seconds

