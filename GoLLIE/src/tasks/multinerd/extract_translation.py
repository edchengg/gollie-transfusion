import json

def get_multinerd_hf(
    split: str,
    language: str,
    # ENTITY_TO_CLASS_MAPPING: Dict[str, Type[Entity]],
):
    """
    Get the Multi-NERD dataset from the huggingface datasets library
    Args:
        split (str): The path_or_split to load. Can be one of `train`, `validation` or `test`.
        language (str): The language to load. Can be one of Chinese (zh), Dutch (nl), English (en), French (fr),
                        German (de), Italian (it), Polish (pl), Portuguese (pt), Russian (ru), Spanish (es).
    Returns:
        (List[str],List[Entity]): The text and the entities
    """
    from datasets import load_dataset

    dataset = load_dataset("Babelscape/multinerd")
    # Dirty fix to prevent errors reading the labels
    label2id = {
        "O": 0,
        "B-PER": 1,
        "I-PER": 2,
        "B-ORG": 3,
        "I-ORG": 4,
        "B-LOC": 5,
        "I-LOC": 6,
        "B-ANIM": 7,
        "I-ANIM": 8,
        "B-BIO": 9,
        "I-BIO": 10,
        "B-CEL": 11,
        "I-CEL": 12,
        "B-DIS": 13,
        "I-DIS": 14,
        "B-EVE": 15,
        "I-EVE": 16,
        "B-FOOD": 17,
        "I-FOOD": 18,
        "B-INST": 19,
        "I-INST": 20,
        "B-MEDIA": 21,
        "I-MEDIA": 22,
        "B-MYTH": 23,
        "I-MYTH": 24,
        "B-PLANT": 25,
        "I-PLANT": 26,
        "B-TIME": 27,
        "I-TIME": 28,
        "B-VEHI": 29,
        "I-VEHI": 30,
    }

    id2label = {v: k for k, v in label2id.items()}

    dataset_sentences: List[List[str]] = []
    dataset_entities: List[List[Entity]] = []

    for example in dataset[split]:
        lang = example["lang"]
        if lang != language:
            continue
        words = example["tokens"]
        dataset_sentences.append(words)
        # dataset_entities.append(entities)

    return dataset_sentences, dataset_entities


for lang in ["de", "es", "fr", "it", "nl", "pl", "pt", "ru", "zh"]:
    data = get_multinerd_hf("test", lang)
    output = []
    for d in data[0]:
        output.append({"sentence": " ".join(d), "marker2label": ""})
    
    with open(f"data_translatetest/multinerd/{lang}.jsonl", "w", encoding="utf-8") as f:
        for out in output:
            f.write(json.dumps(out, ensure_ascii=False) + "\n")
     