import json
from datasets import load_dataset

def extract_trans(language, split="test"):
    dataset = load_dataset("AmazonScience/massive", language, split=split)

    output = []

    for i in range(len(dataset)):
        output.append(dataset[i]["utt"])
    
    return output

low_resource_symbols = [
        "af-ZA", "am-ET", "az-AZ", "bn-BD", "hy-AM", "ka-GE", 
        "km-KH", "mn-MN", "my-MM", "kn-IN", "ml-IN", 
        "ta-IN", "te-IN", "tl-PH", "cy-GB"
    ]

for lang in low_resource_symbols:
    print(lang)
    output = extract_trans(lang)[:2000]
    
    with open(f"data_translatetest/massive/{lang}.jsonl", "w", encoding="utf-8") as f:
        for out in output:
            tmp = {"sentence": out.strip('"'), "marker2label": ""}
            f.write(json.dumps(tmp, ensure_ascii=False) + "\n")