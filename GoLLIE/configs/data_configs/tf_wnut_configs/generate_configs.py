import json
high_plus_res = [
    'deu_Latn',
    'spa_Latn',
    'fra_Latn'
]

high_res = [
    'por_Latn',
    'rus_Cyrl',
    'swe_Latn',
    'zho_Hans',
    'zho_Hant',
    'arb_Arab',
    'ita_Latn',
    'pol_Latn'
]

mid_res = [
    'ceb_Latn',
    'hrv_Latn',
    'srp_Cyrl',
    'tgl_Latn',
    'swh_Latn',
    'tel_Telu',
    'slk_Latn'
]

low_res = [
    'bam_Latn',
    'ewe_Latn',
    'fon_Latn',
    'hau_Latn',
    'ibo_Latn',
    'kin_Latn',
    'lug_Latn',
    'luo_Latn',
    'mos_Latn',
    'nya_Latn',
    'sna_Latn',
    'tsn_Latn',
    'twi_Latn',
    'wol_Latn',
    'xho_Latn',
    'yor_Latn',
    'zul_Latn'
]
for lang in high_plus_res + high_res + mid_res + low_res:
    print(lang)
    tmp_config = {
    "dataset_name": "WNUT17",
    "tasks": ["NER"],
    "dataloader_cls": "src.tasks.wnut.data_loader.WnutTransFusionDatasetLoader",
    "sampler_cls": "src.tasks.wnut.data_loader.WnutSampler",
    "train_file": "/coc/pskynet6/ychen3411/transfusion/GoLLIE/data_easyproject/wnut/wnut_{}.jsonl".format(lang),
    "prompt_template": "templates/prompt_tf.txt",
    "output_name": "wnut.{}".format(lang),
    "label_noise_prob": [0.15],
    "include_date": False,
    "use_transfusion": True,
    "task_configuration": {
        "NER": {
            "parallel_instances": 1,
            "max_guidelines": -1,
            "guideline_dropout": 0.15,
            "scorer": "src.tasks.wnut.scorer.WnutEntityScorer",
            "paraphrase_train": True,
            "label_noise": 0.5
        }
    }
}

    with open("wnut_{}_config.json".format(lang), "w") as f:
        json.dump(tmp_config, f, indent=4)