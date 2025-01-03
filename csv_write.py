import csv   

class WriteCsv():
    def __init__(self, file_name):
        self.fields= ['time_stamp','company', 'title', 'sentiment']
        self.encoding = 'utf-8'
        self.file_name = file_name
    def create(self):
        with open(self.file_name, 'w', newline='',encoding= self.encoding) as f:
            writer = csv.writer(f) 
            writer.writerow(self.fields)

    def write(self, arr):
        title = arr
        with open(self.file_name, 'a', newline='',encoding= self.encoding) as f:
            writer = csv.writer(f)
            writer.writerow(title)