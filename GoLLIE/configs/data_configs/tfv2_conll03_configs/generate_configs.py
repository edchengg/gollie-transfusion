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
for lang in low_res:
    print(lang)
    tmp_config = {
    "dataset_name": "CoNLL03",
    "tasks": ["NER"],
    "dataloader_cls": "src.tasks.conll03.data_loader.CoNLLTransFusionDatasetLoader",
    "sampler_cls": "src.tasks.conll03.data_loader.CoNLL03Sampler",
    "train_file": "/coc/pskynet6/ychen3411/project03_ace_event/few-shot-learning-main/masakhane-ner/NLLB/easyproject_conll/output-nllb_3Bft_parallel/nllb_3Bft_parallel-en-{}-marker.json".format(lang.split("_")[0]),
    "prompt_template": "templates/prompt_tfv2.txt",
    "output_name": "conll03.{}".format(lang),
    "label_noise_prob": [0.15],
    "include_misc": False,
    "use_transfusion": True,
    "task_configuration": {
        "NER": {
            "parallel_instances": 1,
            "max_guidelines": -1,
            "guideline_dropout": 0.15,
            "scorer": "src.tasks.conll03.scorer.CoNLLEntityScorer",
            "paraphrase_train": True,
            "label_noise": 0.5
        }
    }
}

    with open("conll03_{}_config.json".format(lang), "w") as f:
        json.dump(tmp_config, f, indent=4)