import json

def read_tsv(filepath):
    """
    READ tsv file in conll format
    Args:
        filepath: Path to the file
    Returns: List of words, List of labels
    """
    dataset_words: List[List[str]] = []
    dataset_labels: List[List[str]] = []
    with open(filepath, encoding="utf-8") as f:
        guid = 0
        tokens = []
        ner_tags = []
        for line in f:
            if line.startswith("#") or line == "" or line == "\n":
                if tokens:
                    dataset_words.append(tokens)
                    dataset_labels.append(ner_tags)

                    guid += 1
                    tokens = []
                    ner_tags = []
            else:
                # uner uses tab as delimiter
                # an examples is: 4	Miramar	B-LOC	-	stephen
                # tokens[0] = 4         : id
                # tokens[1] = Miramar   : token
                # tokens[2] = B-LOC     : ner tag
                # tokens[3] = -         : -
                # tokens[4] = stephen   : annotator
                splits = line.split("\t")
                tokens.append(splits[1])
                ner_tag = splits[2].rstrip()
                if ner_tag == "B-OTH" or ner_tag == "I-OTH":
                    ner_tag = "O"
                ner_tags.append(ner_tag)
        # last example        
        if tokens:
            dataset_words.append(tokens)
            dataset_labels.append(ner_tags)

    print(f"Read {len(dataset_words)} sentences from {filepath}")
    #dataset_labels = [rewrite_labels(labels, encoding="iob2") for labels in dataset_labels]
    return dataset_words, dataset_labels



for lang in ["ceb_gja", "da_ddt", "de_pud", "hr_set", "pt_bosque", "pt_pud", "ru_pud", "sk_snk", "sv_pud", "sr_set", "sv_pud",
"sv_talbanken", "tl_trg", "tl_ugnayan", "zh_gsd", "zh_gsdsimp", "zh_pud"]:
    data = read_tsv(f"dataset/uner-20231114-092426/{lang}/{lang}-ud-test.iob2")
    output = []
    for words in data[0]:
        input_sent = " ".join(words)
        output.append({"sentence": input_sent, "marker2label": ""})
    
    with open(f"data_translatetest/uner/uner_{lang}.jsonl", "w", encoding="utf-8") as f:
        for out in output:
            f.write(json.dumps(out, ensure_ascii=False) + "\n")        