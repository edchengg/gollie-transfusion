from datasets import load_dataset

def load_data():

    result = []
    for lang in ["ar", "de", "en", "es", "fr", "it", "zh"]:
        output = []
        dataset = load_dataset("Babelscape/REDFM", 
                        lang)
                
        for key, instance in enumerate(dataset["test"]):
            
            text = instance["text"]

            output.append({"sentence": text, "marker2label": ""})
        
        result.append([lang, output])
    
    return result