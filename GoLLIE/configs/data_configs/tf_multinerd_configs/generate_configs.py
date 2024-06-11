import json
for lang in ["es", "nl", "de", "ru", "it", "fr", "pl", "pt", "zh"]:
    print(lang)
    tmp_config = {
        "dataset_name": "MultiNERD",
        "tasks": ["NER"],
        "dataloader_cls": "src.tasks.multinerd.data_loader.MultinerdTransFusionDatasetLoader",
        "sampler_cls": "src.tasks.multinerd.data_loader.MultinerdSampler",
        # "dev_file": "validation",
        "test_file": "test",
        "language": lang,
        "output_name": "multinerd.{}".format(lang),
        "prompt_template": "templates/prompt_tf.txt",
        "seed": [0],
        "label_noise_prob": [0.15],
        "use_transfusion": True,
        "task_configuration": {
            "NER": {
                "parallel_instances": 1,
                "max_guidelines": -1,
                "guideline_dropout": 0.15,
                "scorer": "src.tasks.multinerd.scorer.MultinerdEntityScorer",
                "paraphrase_train": True,
                "label_noise": 0.5
            }
        }
    }

    with open("multinerd_{}_config.json".format(lang), "w") as f:
        json.dump(tmp_config, f, indent=4)

    print(lang)
    tmp_config = {
        "dataset_name": "MultiNERD",
        "tasks": ["NER"],
        "dataloader_cls": "src.tasks.multinerd.data_loader.MultinerdTransFusionDatasetLoader",
        "sampler_cls": "src.tasks.multinerd.data_loader.MultinerdSampler",
        # "dev_file": "validation",
        "test_file": "test",
        "language": lang,
        "output_name": "multinerd.{}".format(lang),
        "prompt_template": "templates/prompt_tfv2.txt",
        "seed": [0],
        "label_noise_prob": [0.15],
        "use_transfusion": True,
        "task_configuration": {
            "NER": {
                "parallel_instances": 1,
                "max_guidelines": -1,
                "guideline_dropout": 0.15,
                "scorer": "src.tasks.multinerd.scorer.MultinerdEntityScorer",
                "paraphrase_train": True,
                "label_noise": 0.5
            }
        }
    }

    with open("multinerd_{}_config_v2.json".format(lang), "w") as f:
        json.dump(tmp_config, f, indent=4)