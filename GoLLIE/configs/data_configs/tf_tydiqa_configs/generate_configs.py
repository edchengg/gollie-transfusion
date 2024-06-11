import json
for lang in ["ko", "bn", "fi", "te", "ar", "sw", "ru", "id", "en"]:
    print(lang)
    tmp_config = {
        "dataset_name": "TyDiQA",
        "tasks": ["QA"],
        "dataloader_cls": "src.tasks.tydiqa.data_loader.TyDiQATransFusionDatasetLoader",
        "sampler_cls": "src.tasks.tydiqa.data_loader.TyDiQASampler",
        "test_file": "validation",
        "language": lang,
        "use_transfusion": True,
        "use_transfusionv2": False,
        "output_name": "tydiqa.{}".format(lang),
        "prompt_template": "templates/prompt_qa_tf.txt",
        "seed": [0, 24, 42],
        "label_noise_prob": [0.15, 0.50, 0.75],
        "task_configuration": {
            "QA": {
                "parallel_instances": 1,
                "max_guidelines": -1,
                "guideline_dropout": 0.15,
                "scorer": "src.tasks.tydiqa.scorer.TyDiQAScorer",
                "paraphrase_train": True,
                "label_noise": 0.5
            }
        }
    }

    with open("tydiqa_{}_config.json".format(lang), "w") as f:
        json.dump(tmp_config, f, indent=4)

    tmp_config = {
        "dataset_name": "TyDiQA",
        "tasks": ["QA"],
        "dataloader_cls": "src.tasks.tydiqa.data_loader.TyDiQATransFusionDatasetLoader",
        "sampler_cls": "src.tasks.tydiqa.data_loader.TyDiQASampler",
        "test_file": "validation",
        "language": lang,
        "use_transfusion": True,
        "use_transfusionv2": True,
        "output_name": "tydiqa.{}".format(lang),
        "prompt_template": "templates/prompt_qa_tf.txt",
        "seed": [0, 24, 42],
        "label_noise_prob": [0.15, 0.50, 0.75],
        "task_configuration": {
            "QA": {
                "parallel_instances": 1,
                "max_guidelines": -1,
                "guideline_dropout": 0.15,
                "scorer": "src.tasks.tydiqa.scorer.TyDiQAScorer",
                "paraphrase_train": True,
                "label_noise": 0.5
            }
        }
    }

    with open("tydiqa_{}_config_v2.json".format(lang), "w") as f:
        json.dump(tmp_config, f, indent=4)