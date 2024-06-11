import json

def read_jsonl(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = [json.loads(l) for l in f]
    return data
    
for lang in ["es", "th"]:
    data = read_jsonl(f"/coc/pskynet6/ychen3411/transfusion/GoLLIE/data/processed_w_examples/multito.{lang}.ner.test.jsonl")
    output = []
    for d in data:
        output.append({"sentence": d["unlabelled_sentence"], "marker2label": ""})
    
    with open(f"/coc/pskynet6/ychen3411/transfusion/GoLLIE/data_translatetest/multito/{lang}.jsonl", "w", encoding="utf-8") as f:
        for out in output:
            f.write(json.dumps(out, ensure_ascii=False) + "\n")