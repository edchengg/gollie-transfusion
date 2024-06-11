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
    "dataset_name": "ACE05",
    "tasks": [
        "NER",
        "VER",
        "RE",
        "RC",
        "EE",
        "EAE"
    ],
    "dataloader_cls": "src.tasks.ace.data_loader.ACETransFusionDatasetLoader",
    "sampler_cls": "src.tasks.ace.data_loader.ACESampler",
    "train_file": "/coc/pskynet6/ychen3411/transfusion/GoLLIE/data_easyproject/ace/ace_{}.jsonl".format(lang),
    "output_name": "ace.{}".format(lang),
    "prompt_template": "templates/prompt.txt",
    "seed": [0],
    "label_noise_prob": [0.15],
    "use_transfusion": True,
    "use_transfusionv2": True,
    "task_configuration": {
        "NER": {
            "group_by": "sentence",
            "parallel_instances": 1,
            "max_guidelines": -1,
            "guideline_dropout": 0.15,
            "scorer": "src.tasks.ace.scorer.ACEEntityScorer"
        },
        "VER": {
            "group_by": "sentence",
            "parallel_instances": 1,
            "max_guidelines": -1,
            "guideline_dropout": 0.15,
            "scorer": "src.tasks.ace.scorer.ACEValueScorer"
        },
        "RE": {
            "group_by": "sentence",
            "parallel_instances": 1,
            "max_guidelines": -1,
            "guideline_dropout": 0.15,
            "scorer": "src.tasks.ace.scorer.ACECoarseRelationScorer"
        },
        "RC": {
            "group_by": "sentence",
            "parallel_instances": 1,
            "max_guidelines": -1,
            "guideline_dropout": 0.15,
            "scorer": "src.tasks.ace.scorer.ACERelationScorer",
            "ensure_positives_on_train": True
        },
        "EE": {
            "group_by": "sentence",
            "parallel_instances": 1,
            "max_guidelines": -1,
            "guideline_dropout": 0.15,
            "scorer": "src.tasks.ace.scorer.ACEEventScorer"
        },
        "EAE": {
            "group_by": "sentence",
            "parallel_instances": 1,
            "max_guidelines": -1,
            "sample_total_guidelines": 5,
            "guideline_dropout": 0.15,
            "scorer": "src.tasks.ace.scorer.ACEEventArgumentScorer",
            "ensure_positives_on_train": True
        }
    }
}

    with open("ace_{}_config.json".format(lang), "w") as f:
        json.dump(tmp_config, f, indent=4)