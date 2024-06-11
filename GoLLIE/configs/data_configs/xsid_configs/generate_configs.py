import json
for lang in ["ar", "da", "de", "en", "id", "it", "ja", "kk", "nl", "sr", "tr", "zh"]:
    print(lang)
    tmp_config = {
    "dataset_name": "XSID",
    "tasks": ["NER"],
    "dataloader_cls": "src.tasks.xsid.data_loader.XSIDDatasetLoader",
    "sampler_cls": "src.tasks.xsid.data_loader.XSIDSampler",
    "test_file": f"/coc/pskynet6/ychen3411/transfusion/GoLLIE/dataset/xSID/xSID-0.4/{lang}.test.conll",
    "prompt_template": "templates/prompt.txt",
    "output_name": "xsid.{}".format(lang),
    "seed": [0, 24, 42],
    "label_noise_prob": [0.15, 0.50, 0.75],
    "task_configuration": {
        "NER": {
            "parallel_instances": 1,
            "max_guidelines": -1,
            "guideline_dropout": 0.15,
            "scorer": "src.tasks.xsid.scorer.XSIDEntityScorer",
            "paraphrase_train": True,
            "label_noise": 0.5
        }
    }
}


    with open("xsid_{}_config.json".format(lang), "w") as f:
        json.dump(tmp_config, f, indent=4)