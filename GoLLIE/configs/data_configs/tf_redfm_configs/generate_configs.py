import json
for lang in ["ar", "de", "en", "es", "fr", "it", "zh"]:
    print(lang)
    tmp_config = {
        "dataset_name": "REDFM",
        "tasks": ["RE"],
        "dataloader_cls": "src.tasks.redfm.data_loader.REDFMTransFusionDatasetLoader",
        "sampler_cls": "src.tasks.redfm.data_loader.REDFMSampler",
        "test_file": "test",
        "language": lang,
        "output_name": "redfm.{}".format(lang),
        "prompt_template": "templates/prompt_redfm_re_tfv2.txt",
        "use_transfusion": True,
        "seed": [0],
        "label_noise_prob": [0.15],
        "task_configuration": {
            "RE": {
                "parallel_instances": 1,
                "max_guidelines": -1,
                "guideline_dropout": 0.15,
                "scorer": "src.tasks.redfm.scorer.REDFMRelationScorer",
                "paraphrase_train": True,
                "label_noise": 0.5
            }
        }
    }

    with open("redfm_{}_config.json".format(lang), "w") as f:
        json.dump(tmp_config, f, indent=4)