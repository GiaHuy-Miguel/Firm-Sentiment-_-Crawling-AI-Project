import pandas as pd
import torch
from optimized_1 import list_titles
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.utils.data import Dataset,DataLoader

def get_data():
    data = []
    for i in list_titles:
        headline = i[1]
        # print(headline)
        data.append(headline)
    return data

class TextDataset(Dataset):
    def __init__(self, texts, tokenizer, max_len):
        self.texts = texts
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_len,
            return_token_type_ids=False,
            padding='max_length', #Them dieu kien
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten()
        }
    
# def get_time():
#     time = []
#     for i in list_titles:
#         timestamp = i[0]
#         time.append(timestamp)
#     return time 



checkpoint = "mr4/phobert-base-vi-sentiment-analysis"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSequenceClassification.from_pretrained(checkpoint)

# time = get_time()
raw = get_data()
# raw = ['Metro số 1 đón lượng khách gấp 5,5 lần dự kiến, lên phương án cho Noel và Tết']

# inputs = tokenizer(raw, padding=True,
#                    truncation=True, return_tensors="pt")
# outputs = model(**inputs)
# predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

#Batch 
max_len = 128  # or whatever the max length you want for your text
batch_size = 120
dataset = TextDataset(raw, tokenizer, max_len)
data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=False)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

predictions = []
with torch.no_grad():
    for batch in data_loader:
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        batch_predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        predictions.extend(batch_predictions.cpu().tolist())


for i, prediction in enumerate(predictions):
    # print(time[i] +':'+ raw[i])
    flag = False
    # print(raw[i])
    for j, value in enumerate(prediction):
        if value >= 0.5: #Đặt threshold. Nếu chiếm hơn 0.5 thì sẽ pick cái nì 
            list_titles[i].insert(2, model.config.id2label[j])
            # print(
            #     "    " + model.config.id2label[j]) #+ ": " + str(value.item())
            flag = True
        # print(model.config.id2label[j])
    if not flag:
        list_titles[i].insert(2,'Trung tính') 
    #     print("Trung tính")
    # print (list_titles[i])    

df = pd.DataFrame(list_titles, columns=['time_stamp', 'title', 'sentiment'])
df.to_csv('OUTPUT.csv', header=True, index=False, encoding='utf-8')
# with pd.ExcelWriter('OUTPUT.xlsx') as writer:
#     df.to_excel(writer)
print(df)