import json

def read_jsonl(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = [json.loads(l) for l in f]
    return data
    
for lang in ["bn", "de", "es", "fa", "fr", "hi", "it", "pt", "sv", "uk", "zh"]:
    data = read_jsonl(f"data/processed_w_examples/multiconer2.{lang}.ner.test.jsonl")
    output = []
    for d in data:
        output.append({"sentence": d["unlabelled_sentence"], "marker2label": ""})
    
    with open(f"data_translatetest/multiconer2/{lang}.jsonl", "w", encoding="utf-8") as f:
        for out in output:
            f.write(json.dumps(out, ensure_ascii=False) + "\n")
     