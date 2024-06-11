import json
import os
import importlib

def encode_data_from_task(task_name):
    module_name = f"src.tasks.{task_name}.easyproject_data"
    module = importlib.import_module(module_name)
    encode_data_func = getattr(module, "encode_data")
    return encode_data_func

def process_tasks(task_names, output_dir):
    for task_name in task_names:
        print("Processing:", task_name)
        encode_data = encode_data_from_task(task_name)
        encoded_output = encode_data("train")
        
        output_folder = os.path.join(output_dir, task_name)
        os.makedirs(output_folder, exist_ok=True)
        
        output_file = os.path.join(output_folder, f"{task_name}.jsonl")
        with open(output_file, "w", encoding="utf-8") as f:
            for line in encoded_output:
                f.write(json.dumps(line, ensure_ascii=False) + "\n")

def main():
    task_names = ["ace"]
    output_dir = "data_easyproject"
    process_tasks(task_names, output_dir)

if __name__ == "__main__":
    main()