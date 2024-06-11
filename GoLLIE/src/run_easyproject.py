import os
import argparse
import json
import random
from tqdm import tqdm
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

def translate(args):
    src_lang = args.src_lang
    tgt_lang = args.tgt_lang
    max_length = args.max_length
    batch_size = args.batch_size
    input_file = args.input_file
    output_file = args.output_file
    max_sent_size = args.max_sent_size

    if os.path.exists(output_file):
        return

    tokenizer = AutoTokenizer.from_pretrained(
        "facebook/nllb-200-distilled-600M", src_lang=src_lang)
    print("Loading model")
    model = AutoModelForSeq2SeqLM.from_pretrained("ychenNLP/nllb-200-3.3B-easyproject")
    model.cuda()

    # Load input chunks from the input file
    with open(input_file, "r", encoding="utf-8") as f:
        input_data = [json.loads(line) for line in f]

    if len(input_data) > max_sent_size:
        labeled_data = []
        unlabeled_data = []
        for d in input_data:
            if d["marker2label"] == {}:
                unlabeled_data.append(d)
            else:
                labeled_data.append(d)

        random.shuffle(unlabeled_data)
        random.shuffle(labeled_data)

        if len(unlabeled_data) != 0:
            input_data = labeled_data[:int(max_sent_size * 0.75)] + unlabeled_data[:int(max_sent_size * 0.25)]
        else:
            input_data = labeled_data[:max_sent_size]

    input_chunks = [d["sentence"] for d in input_data]
    print("Start translation...")
    output_result = []
    for idx in tqdm(range(0, len(input_chunks), batch_size)):
        start_idx = idx
        end_idx = idx + batch_size
        inputs = tokenizer(input_chunks[start_idx: end_idx], padding=True, truncation=True, max_length=max_length, return_tensors="pt").to('cuda')
        with torch.no_grad():
            translated_tokens = model.generate(**inputs, forced_bos_token_id=tokenizer.lang_code_to_id[tgt_lang],
                                               max_length=max_length, num_beams=5, num_return_sequences=1, early_stopping=True)
            output = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)
            output_result.extend(output)

    # Save the output to a JSONL file
    with open(output_file, "w", encoding="utf-8") as f:
        for text, inp_d in zip(output_result, input_data):
            input_sent = inp_d["sentence"]
            marker2label = inp_d["marker2label"]
            f.write(json.dumps({"output_sentence": text, 
                                "input_sentence": input_sent, 
                                "marker2label": marker2label}, ensure_ascii=False) + '\n')

    print(f"Translation completed. Output saved to {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Translation Script')
    parser.add_argument('--src_lang', type=str, default='eng_Latn', help='Source language')
    parser.add_argument('--tgt_lang', type=str, default='zho_Hans', help='Target language')
    parser.add_argument('--max_length', type=int, default=128, help='Maximum sequence length')
    parser.add_argument('--batch_size', type=int, default=4, help='Batch size')
    parser.add_argument('--max_sent_size', type=int, default=100, help='Maximum data size')
    parser.add_argument('--input_file', type=str, required=True, help='Input JSONL file')
    parser.add_argument('--output_file', type=str, required=True, help='Output JSONL file')
    args = parser.parse_args()

    translate(args)