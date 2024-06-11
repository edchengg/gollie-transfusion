import json
for lang in ["en", "es", "th"]:
    print(lang)
    tmp_config = {
    "dataset_name": "MultiTO",
    "tasks": ["NER"],
    "dataloader_cls": "src.tasks.multito.data_loader.MultiTOTransFusionDatasetLoader",
    "sampler_cls": "src.tasks.multito.data_loader.MultiTOSampler",
    "test_file": f"/coc/pskynet6/ychen3411/transfusion/GoLLIE/dataset/MultiTO/{lang}/test-{lang}.conllu",
    "prompt_template": "templates/prompt_tf.txt",
    "output_name": "multito.{}".format(lang),
    "seed": [0, 24, 42],
    "label_noise_prob": [0.15, 0.50, 0.75],
    "use_transfusion": True,
    "do_not_shuffle": True,
    "task_configuration": {
        "NER": {
            "parallel_instances": 1,
            "max_guidelines": -1,
            "guideline_dropout": 0.15,
            "scorer": "src.tasks.multito.scorer.MultiTOEntityScorer",
            "paraphrase_train": True,
            "label_noise": 0.5
        }
    }
}


    with open("multito_{}_config.json".format(lang), "w") as f:
        json.dump(tmp_config, f, indent=4)