import json

class Checkpoint():

    def __init__(self, category, file_name):
        self.file = file_name
        self.category = category
    
    def reset_Checkpoint(self):
        checkpoint = {
                    "visited": [],
                    "urls_to_crawl": [f"https://en.wikipedia.org/wiki/Category:{self.category}-Class_articles"]
        }
        with open(self.file,"w") as json_file:
            json.dump(checkpoint, json_file, indent = 2)

    def load_Checkpoint(self):

        with open(self.file) as json_file:
            data = json.load(json_file)
            return data["visited"],data["urls_to_crawl"]

    def add(self, to_add_list, attribute, init = False):

        if(attribute == "urls_to_crawl" and not init):
            with open(self.file) as json_file:
                data = json.load(json_file)
                data[attribute] = to_add_list 
        else:    
            with open(self.file) as json_file:
                data = json.load(json_file)
                data[attribute] = data[attribute] + to_add_list 
        
        with open(self.file,"w") as json_file:
            json.dump(data,json_file,indent=2)

