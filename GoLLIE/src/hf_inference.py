import os
import json
import argparse
from typing import Dict, List
import logging
import shutil

from src.easy_eval import evaluate
from src.model.load_model import merge_lora_model, load_model
from src.run import clean_cache

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from tqdm import tqdm

def load_jsonl(path: str) -> List[dict]:
    """Load JSON data from a file."""
    print("##### loading json: ", path)
    with open(path, "r", encoding="utf-8") as f:
        data = [json.loads(l) for l in f]
    return data

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def save_json(data: List[dict], path: str) -> None:
    """Save JSON data to a file."""
    print("##### save json to: ", path)
    with open(path, "w", encoding="utf-8") as f:
        for d in data:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")


def create_folder_if_not_exists(folder_path: str) -> None:
    """Create a folder at the given path if it doesn't already exist."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")

masakhan_task_list = [
"masakhaner.bam.ner", 
"masakhaner.bbj.ner", 
"masakhaner.ewe.ner", 
"masakhaner.fon.ner",
"masakhaner.hau.ner", 
"masakhaner.ibo.ner", 
"masakhaner.kin.ner", 
"masakhaner.lug.ner", 
"masakhaner.luo.ner", 
"masakhaner.mos.ner", 
"masakhaner.nya.ner", 
"masakhaner.pcm.ner", 
"masakhaner.sna.ner", 
"masakhaner.swh.ner",
"masakhaner.tsn.ner",
"masakhaner.twi.ner", 
"masakhaner.wol.ner", 
"masakhaner.xho.ner", 
"masakhaner.yor.ner", 
"masakhaner.zul.ner"
]


uner_task_list = [
'uner.ceb_gja.ner',
'uner.da_ddt.ner',
'uner.de_pud.ner',
'uner.en_ewt.ner',
'uner.en_pud.ner',
'uner.hr_set.ner',
'uner.pt_bosque.ner',
'uner.pt_pud.ner',
'uner.ru_pud.ner',
'uner.sk_snk.ner',
'uner.sr_set.ner',
'uner.sv_pud.ner',
'uner.sv_talbanken.ner',
'uner.tl_trg.ner',
'uner.tl_ugnayan.ner',
'uner.zh_gsd.ner',
'uner.zh_gsdsimp.ner',
'uner.zh_pud.ner'
]

multinerd_task_list = [
'multinerd.de.ner',
'multinerd.es.ner',
'multinerd.fr.ner',
'multinerd.it.ner',
'multinerd.nl.ner',
'multinerd.pl.ner',
'multinerd.pt.ner',
'multinerd.ru.ner',
'multinerd.zh.ner',
'multinerd.ner'
]

multiconer2_task_list = [
'multiconer2.bn.ner',
'multiconer2.de.ner',
'multiconer2.es.ner',
'multiconer2.fa.ner',
'multiconer2.fr.ner',
'multiconer2.hi.ner',
'multiconer2.it.ner',
'multiconer2.pt.ner',
'multiconer2.sv.ner',
'multiconer2.uk.ner',
'multiconer2.zh.ner',
'multiconer2.en.ner',
]

ace_task_list = [
'multiace.zh.ner',
'multiace.zh.ee',
'multiace.zh.eae',
'multiace.zh.re',
'multiace.ar.ner',
'multiace.ar.ee',
'multiace.ar.eae',
'multiace.ar.re',
'ace.en.ner',
'ace.en.ee',
'ace.en.eae',
'ace.en.re'
]

redfm_task_list = [
'redfm.ar.re',
'redfm.de.re',
'redfm.en.re',
'redfm.es.re',
'redfm.fr.re',
'redfm.it.re',
'redfm.zh.re'
]

conll03_task_list = [
'conll03.ner'
]

xsid_task_list = [
'xsid.ar.ner', 
'xsid.da.ner', 
'xsid.de.ner', 
'xsid.en.ner', 
'xsid.id.ner', 
'xsid.it.ner', 
'xsid.ja.ner', 
'xsid.kk.ner', 
'xsid.nl.ner',
'xsid.sr.ner', 
'xsid.tr.ner', 
'xsid.zh.ner'
]

multito_task_list = [
    'multito.en.ner',
    'multito.es.ner',
    'multito.th.ner',
]

massive_task_list = [
    "massive.en-us.ner",
    "massive.af-za.ner",
    "massive.am-et.ner",
    "massive.az-az.ner",
    "massive.bn-bd.ner",
    "massive.hy-am.ner",
    "massive.ka-ge.ner",
    "massive.km-kh.ner",
    "massive.mn-mn.ner",
    "massive.my-mm.ner",
    "massive.kn-in.ner",
    "massive.ml-in.ner",
    "massive.ta-in.ner",
    "massive.te-in.ner",
    "massive.tl-ph.ner",
    "massive.cy-gb.ner"
]


task2list = {
"masakhaner": masakhan_task_list,
"uner": uner_task_list,
"ace": ace_task_list,
"conll03": conll03_task_list,
"multinerd": multinerd_task_list,
"redfm": redfm_task_list,
"multiconer2": multiconer2_task_list,
"xsid": xsid_task_list,
"multito": multito_task_list,
"massive": massive_task_list,
}

def read_scores(task_name, task_scores, task_type):
    if task_name == "ace":
        output = []
        tmp = []
        for k in ["ace.en.eae", "multiace.ar.eae", "multiace.zh.eae"]:
            score = task_scores[k]["events"]["f1-score"]
            output.append(f"{k}\t{score}")
            tmp.append(score)
        avg = sum(tmp)/len(tmp)
        output.append(f"average\t{avg}")
        
        tmp = []
        for k in ["ace.en.ee", "multiace.ar.ee", "multiace.zh.ee"]:
            score = task_scores[k]["events"]["f1-score"]
            output.append(f"{k}\t{score}")
            tmp.append(score)
        avg = sum(tmp)/len(tmp)
        output.append(f"average\t{avg}")

        tmp = []
        for k in ["ace.en.ner", "multiace.ar.ner", "multiace.zh.ner"]:
            score = task_scores[k]["entities"]["f1-score"]
            output.append(f"{k}\t{score}")
            tmp.append(score)
        avg = sum(tmp)/len(tmp)
        output.append(f"average\t{avg}")

        tmp = []
        for k in ["ace.en.re", "multiace.ar.re", "multiace.zh.re"]:
            score = task_scores[k]["relations"]["f1-score"]
            output.append(f"{k}\t{score}")
            tmp.append(score)
        avg = sum(tmp)/len(tmp)
        output.append(f"average\t{avg}")
    else:
        tmp = []
        output = []
        for k in task_scores:
            score = task_scores[k][task_type]["f1-score"]
            tmp.append(score)
            output.append(f"{k}\t{score}")
        avg = sum(tmp)/len(tmp)
        output.append(f"average\t{avg}")
    return output

def batch_inference(model, tokenizer, prompts, batch_size=1):
    device = model.device
    all_outputs = []

    # Process prompts in batches
    for i in tqdm(range(0, len(prompts), batch_size), desc="Processing Batches"):
        batch_prompts = prompts[i:i + batch_size]
        
        # Tokenize the batch prompts
        # model_input = tokenizer(batch_prompts, return_tensors="pt", padding=True, truncation=True, max_length=4096).to(device)
        model_input = tokenizer(batch_prompts, return_tensors="pt", padding=True, truncation=True, max_length=8000).to(device)
        
        # print(model_input.input_ids)
        # Remove EOS
        model_input["input_ids"] = model_input["input_ids"][:, :-1]
        model_input["attention_mask"] = model_input["attention_mask"][:, :-1]
        
        # Generate output for the batch
        model_output = model.generate(
            **model_input,
            max_new_tokens=512,
            do_sample=False,
            min_new_tokens=0,
            num_beams=1,
            num_return_sequences=1,
        )
        
        # Decode the generated tokens to text
        batch_output = tokenizer.batch_decode(model_output, skip_special_tokens=True)
        # print(batch_output)
        all_outputs.extend(batch_output)
    
    return all_outputs

def main(dataset_path: str, task_name_list: str, num_size: int, use_lora: bool, output_path: str, lora_path: str, batch_size: int) -> None:
    """Main function to generate predictions and evaluate the model."""

    predictions_folder = os.path.join(output_path, "predictions")
    create_folder_if_not_exists(predictions_folder)
    
    if use_lora:
        model_path = os.path.join(output_path, "merged_model")
        if not os.path.exists(model_path):
            
            print(f"##### Merging lora from {lora_path} to GoLLIE-7B and save to {model_path}")
            merge_lora_model(weights_path="HiTZ/GoLLIE-7B",
                            lora_weights_name_or_path=lora_path,
                            output_path=model_path,
                            torch_dtype="bfloat16")
            clean_cache()
    else:
        model_path = "HiTZ/GoLLIE-7B"
    
    model, tokenizer = load_model(
        inference=True,
        model_weights_name_or_path=model_path,
        quantization=None,
        use_lora=False,
        force_auto_device_map=True,
        use_flash_attention=True,
        torch_dtype="bfloat16"
    )

    for task_name in task_name_list.split(","):
        print("Task Name: ", task_name)
        task_list = task2list[task_name]
        for data_file in task_list:
            save_file_name = os.path.join(predictions_folder, f"{data_file}.predictions.jsonl")
            # check if pred exists
            if os.path.exists(save_file_name):
                print(f"already exist, pass: {save_file_name}...")
                continue
            data = load_jsonl(os.path.join(dataset_path, data_file + ".test.jsonl"))
            prompts = [l["text"].split("result =")[0] + "result =" for l in data][:num_size]
            
            outputs = batch_inference(model, tokenizer, prompts, batch_size)
            
            # for output in outputs:
            #     print(output)
                
            save_output = [{"model_prediction": output} for output in outputs]
            
            save_json(save_output, save_file_name)

        # Run evaluation
        gold_data_dir = "GoLLIE/data/processed_w_examples"
        evaluate(task_list, output_path, gold_data_dir, max_example=num_size, save_prefix=task_name)

    # delete merged model
    if use_lora:
        logging.info(f"Deleting merged model at {model_path}")
        
        # try:
        #     shutil.rmtree(model_path)
        # except OSError as e:
        #     logging.error(
        #         f"Unable to delete the merged model {model_path} : {e.strerror}\n"
        #         "You may need to delete the merged model manually."
        #     )
    
    # save results in a txt file
    score_output_list = []
    for task_name in task_name_list.split(","):
        print("Task Name: ", task_name)
        task_scores = load_json(os.path.join(output_path, f"{task_name}_task_scores_summary.json"))
        if task_name == "redfm":
            score_output = read_scores(task_name, task_scores, "relations")
        elif task_name == "tydiqa":
            score_output = read_scores(task_name, task_scores, "qa")
        else:
            score_output = read_scores(task_name, task_scores, "entities")
        score_output_list.extend(score_output)
    # save to txt
    print(f"Save result txt to: {output_path}/results.txt")
    with open(os.path.join(output_path, "results.txt"), "w") as f:
        f.write("\n".join(score_output_list))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_path", type=str, help="Path to the dataset folder")
    parser.add_argument("--task_name_list", type=str, help="Name of the task")
    parser.add_argument("--num_size", type=int, default=200, help="Size of the test set")
    parser.add_argument("--batch_size", type=int, default=8, help="Size of the batch")
    parser.add_argument("--use_lora", action="store_true", help="Whether to use LoRA or not")
    parser.add_argument("--output_path", type=str, default=None, help="Path to save the generated outputs (optional)")
    parser.add_argument("--lora_path", type=str, default=None, help="Path to the LoRA weights file (required if --use_lora is True)")

    args = parser.parse_args()
    main(args.dataset_path, args.task_name_list, args.num_size, args.use_lora, args.output_path, args.lora_path,
        args.batch_size)