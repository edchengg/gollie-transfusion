import json

def get_tydiqa_hf(
    split: str,
    language: str,
):
    """
    Get the TydiQA-Gold dataset from the huggingface datasets library
    Args:
        split (str): The path_or_split to load. Can be one of `train`, `validation` or `test`.
        language (str): The language to load. Can be one of Chinese (zh), Dutch (nl), English (en), French (fr),
                        German (de), Italian (it), Polish (pl), Portuguese (pt), Russian (ru), Spanish (es).
    Returns:
        (List[str],List[Entity], List[str]): The text and answer, id
    """
    from datasets import load_dataset

    dataset = load_dataset("tydiqa", "secondary_task", cache_dir="/coc/pskynet6/ychen3411/cache/")

    dataset_sentences = []
    dataset_questions = []
    
    lang2langid = {"arabic": "ar",
                    "russian": "ru",
                    "korean": "ko",
                    "telugu": "te",
                    "finnish": "fi",
                    "indonesian": "id",
                    "bengali": "bn",
                    "swahili": "sw",
                    "thai": "th",
                    "english": "en",
                }

    for example in dataset[split]:
        lang = example["id"].split("-")[0]
        lang = lang2langid[lang]
        if lang != language:
            continue
        context = example["context"]
        question = example["question"]

        dataset_sentences.append(context)
        dataset_questions.append(question)
        
    return dataset_sentences, dataset_questions


for lang in ["ar", "ru", "ko", "te", "fi", "id", "bn", "sw", "th"]:
    sentence, question = get_tydiqa_hf("validation", lang)

    with open(f"/coc/pskynet6/ychen3411/transfusion/GoLLIE/data_translatetest/tydiqa/{lang}.jsonl", "w", encoding="utf-8") as f:
        for s in sentence:
            out = {"sentence": s, "mark2label": ""}
            f.write(json.dumps(out, ensure_ascii=False) + "\n")
    
    with open(f"/coc/pskynet6/ychen3411/transfusion/GoLLIE/data_translatetest/tydiqa/ques_{lang}.jsonl", "w", encoding="utf-8") as f:
        for q in question:
            out = {"sentence": q, "mark2label": ""}
            f.write(json.dumps(out, ensure_ascii=False) + "\n")