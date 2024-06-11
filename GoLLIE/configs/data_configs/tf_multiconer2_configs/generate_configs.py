import json
for lang in ["en", "bn", "de", "es", "fa", "fr", "hi", "it", "pt", "sv", "uk", "zh"]:
    print(lang)
    lang2name = {"bn": "BN-Bangla", "de": "DE-German", "en": "EN-English",
    "es": "ES-Spanish", "fa": "FA-Farsi", "fr": "FR-French",
    "hi": "HI-Hindi", "it": "IT-Italian", "pt": "PT-Portuguese",
    "sv": "SV-Swedish", "uk": "UK-Ukrainian",
    "zh": "ZH-Chinese"}

    dataname = lang2name[lang]
    tmp_config = {
    "dataset_name": "MultiCoNER2",
    "tasks": ["NER"],
    "dataloader_cls": "src.tasks.multiconer2.data_loader.MultiCoNERTransFusionDatasetLoader",
    "sampler_cls": "src.tasks.multiconer2.data_loader.MultiCoNERSampler",
    "test_file": "/coc/pskynet6/ychen3411/transfusion/GoLLIE/dataset/MultiCoNER2/{}/{}_dev.conll".format(dataname, lang),
    "prompt_template": "templates/prompt_tf.txt",
    "output_name": "multiconer2.{}".format(lang),
    "do_not_shuffle": True,
    "use_transfusion": True,
    "seed": [0, 24, 42],
    "label_noise_prob": [0.15, 0.50, 0.75],
    "task_configuration": {
        "NER": {
            "parallel_instances": 1,
            "max_guidelines": -1,
            "guideline_dropout": 0.15,
            "scorer": "src.tasks.multiconer2.scorer.MultiCoNEREntityScorer",
            "paraphrase_train": True,
            "label_noise": 0.5,
            "do_not_shuffle": True,
        }
    }
}


    with open("multiconer_{}_config.json".format(lang), "w") as f:
        json.dump(tmp_config, f, indent=4)