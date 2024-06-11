import json
for lang in ["ceb_gja", "da_ddt", "de_pud",  "hr_set", "pt_bosque", "pt_pud", "ru_pud",
"sk_snk", "sr_set", "sv_pud", "sv_talbanken", "tl_trg", "tl_ugnayan", "zh_gsd", "zh_gsdsimp", "zh_pud"]:
    print(lang)
    tmp_config = {
    "dataset_name": "UNER",
    "tasks": ["NER"],
    "dataloader_cls": "src.tasks.uner.data_loader.UNERTransFusionDatasetLoader",
    "sampler_cls": "src.tasks.uner.data_loader.UNERSampler",
    "test_file": "/coc/pskynet6/ychen3411/transfusion/GoLLIE/dataset/uner-20231114-092426/{}/{}-ud-test.iob2".format(lang, lang),
    "prompt_template": "templates/prompt_tf.txt",
    "output_name": "uner.{}".format(lang),
    "use_transfusion": True,
    "seed": [0],
    "label_noise_prob": [0.15],
    "include_date": False,
    "task_configuration": {
        "NER": {
            "parallel_instances": 1,
            "max_guidelines": -1,
            "guideline_dropout": 0.15,
            "scorer": "src.tasks.uner.scorer.UNEREntityScorer",
            "paraphrase_train": True,
            "label_noise": 0.5
        }
    }
}


    with open("uner_{}_config.json".format(lang), "w") as f:
        json.dump(tmp_config, f, indent=4)

    tmp_config = {
    "dataset_name": "UNER",
    "tasks": ["NER"],
    "dataloader_cls": "src.tasks.uner.data_loader.UNERTransFusionDatasetLoader",
    "sampler_cls": "src.tasks.uner.data_loader.UNERSampler",
    "test_file": "/coc/pskynet6/ychen3411/transfusion/GoLLIE/dataset/uner-20231114-092426/{}/{}-ud-test.iob2".format(lang, lang),
    "prompt_template": "templates/prompt_tfv2.txt",
    "output_name": "uner.{}".format(lang),
    "seed": [0],
    "label_noise_prob": [0.15],
    "include_date": False,
    "use_transfusion": True,
    "task_configuration": {
        "NER": {
            "parallel_instances": 1,
            "max_guidelines": -1,
            "guideline_dropout": 0.15,
            "scorer": "src.tasks.uner.scorer.UNEREntityScorer",
            "paraphrase_train": True,
            "label_noise": 0.5
        }
    }
}


    with open("uner_{}_config_v2.json".format(lang), "w") as f:
        json.dump(tmp_config, f, indent=4)