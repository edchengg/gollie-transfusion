import json
for lang in ["bam", "bbj", "ewe", "fon", "hau", "ibo", "kin", "lug", "luo", 
    "mos", "nya", "pcm", "sna", "swh", "tsn", "twi", "wol", "xho", "yor", "zul"]:
    print(lang)
    tmp_config = {
    "dataset_name": "MasakhaNER",
    "tasks": ["NER"],
    "dataloader_cls": "src.tasks.masakhaner.data_loader.MasakhaNERTransFusionDatasetLoader",
    "sampler_cls": "src.tasks.masakhaner.data_loader.MasakhaNERSampler",
    "test_file": "/coc/pskynet6/ychen3411/project03_ace_event/few-shot-learning-main/masakhane-ner/MasakhaNER2.0/data/{}/test.txt".format(lang),
    "translation_file": "/coc/pskynet6/ychen3411/project03_ace_event/few-shot-learning-main/masakhane-ner/NLLB/fusion_experiment/data/masakhaner-translation/{}/test.txt.eng_Latn".format(lang),
    "prompt_template": "templates/prompt_tfv2.txt",
    "output_name": "masakhaner.{}".format(lang),
    "use_transfusion": True,
    "seed": [0],
    "label_noise_prob": [0.15],
    "include_date": False,
    "task_configuration": {
        "NER": {
            "parallel_instances": 1,
            "max_guidelines": -1,
            "guideline_dropout": 0.15,
            "scorer": "src.tasks.masakhaner.scorer.MasakhaNEREntityScorer",
            "paraphrase_train": True,
            "label_noise": 0.5
        }
    }
}


    with open("masakhaner_{}_config.json".format(lang), "w") as f:
        json.dump(tmp_config, f, indent=4)