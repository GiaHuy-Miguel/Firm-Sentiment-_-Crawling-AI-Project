import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class Model():
    def __init__(self,checkpoint, title):
        # checkpoint = "mr4/phobert-base-vi-sentiment-analysis"
        self.checkpoint = checkpoint
        self.title = title
    
    def load_model(self):
        # Get input & model
        article = self.title[2]
        tokenizer = AutoTokenizer.from_pretrained(self.checkpoint)
        model = AutoModelForSequenceClassification.from_pretrained(self.checkpoint)

        inputs = tokenizer(article, padding=True,
                        truncation=True, return_tensors="pt")
        
        #Load model      
        with torch.no_grad():  # Disable gradient calculation for inference
            outputs = model(**inputs)
        
        #Get prediction
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        predicted_label = 'Trung tính' # Nếu không pass điều kiện (không có label nào trên 50%) thì chọn cái này
        max_prob, max_index = torch.max(predictions, dim=1)
        if max_prob.item() >= 0.5:  # Threshold check
            predicted_label = model.config.id2label[max_index.item()]

        # Return result   
        self.title.insert(3, predicted_label)
        print (self.title)  
        return self.title 
