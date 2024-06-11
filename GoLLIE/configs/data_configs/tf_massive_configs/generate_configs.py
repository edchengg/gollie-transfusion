import json
for lang in ["af-ZA", "am-ET", "az-AZ", "bn-BD", "hy-AM", "ka-GE", 
        "km-KH", "mn-MN", "my-MM", "kn-IN", "ml-IN", 
        "ta-IN", "te-IN", "tl-PH", "cy-GB"]:
    print(lang)
    tmp_config = {
    "dataset_name": "Massive",
    "tasks": ["NER"],
    "dataloader_cls": "src.tasks.massive.data_loader.MassiveTransFusionDatasetLoader",
    "sampler_cls": "src.tasks.massive.data_loader.MassiveSampler",
    "test_file": "",
    "language": "{}".format(lang),
    "prompt_template": "templates/prompt_tf.txt",
    "output_name": "massive.{}".format(lang),
    "use_transfusion": True,
    "seed": [0, 24, 42],
    "label_noise_prob": [0.15, 0.50, 0.75],
    "task_configuration": {
        "NER": {
            "parallel_instances": 1,
            "max_guidelines": -1,
            "guideline_dropout": 0.15,
            "scorer": "src.tasks.massive.scorer.MassiveEntityScorer",
            "paraphrase_train": True,
            "label_noise": 0.5
        }
    }
}


    with open("massive_{}_config.json".format(lang), "w") as f:
        json.dump(tmp_config, f, indent=4)