import json
import os
import importlib

def save_data_from_task(task_name):
    module_name = f"src.tasks.{task_name}.easyproject_data"
    module = importlib.import_module(module_name)
    load_data_func = getattr(module, "load_data")
    return load_data_func

def process_tasks(task_names, output_dir):
    for task_name in task_names:
        print("Processing:", task_name)
        load_data = save_data_from_task(task_name)
        outputs = load_data()
        
        output_folder = os.path.join(output_dir, task_name)
        os.makedirs(output_folder, exist_ok=True)
        
        for lang, output in outputs:
            output_file = os.path.join(output_folder, f"{task_name}_{lang}.jsonl")
            with open(output_file, "w", encoding="utf-8") as f:
                for line in output:
                    f.write(json.dumps(line, ensure_ascii=False) + "\n")

def main():
    task_names = ["redfm"]
    output_dir = "data_translatetest"
    process_tasks(task_names, output_dir)

if __name__ == "__main__":
    main()