from flask import Flask, request, json
import torch
import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification


app = Flask(__name__)

@app.route("/")
def hello_world():
    data_to_test = ["Dow Jones Slumps 225 Points Despite Big JPMorgan Rally; Boeing Dives On 737 MAX Halt; On Holding Jumps 3.5%",
                    "GLOBAL MARKETS-Dollar, yields gain as expectations of Fed rate hike increase",
                    "Key Indexes Have Turned Bullish: What That Means for Stocks",
                    "Dow Jones Falls As Boeing Skids On 737 Woes; JPMorgan Jumps On Earnings",
                    "Stocks fall, JPMorgan surges after earnings: Stock market news today",
                    "US STOCKS-Wall St mixed as retail sales data offsets bank earnings cheer",
                    "Bank stocks rally following earnings data, tech under pressure"]
    
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
    
    df = pd.DataFrame(table, columns = ["Headline", "Positive", "Negative", "Neutral"])
    response = df.to_json(orient='records')[1:-1].replace('},{', '} {')

    return response



if __name__ == '__main__':
    app.run(debug=True)
