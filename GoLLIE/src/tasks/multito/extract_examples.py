from collections import defaultdict, Counter

def read_tsv(filepath):
    """
    READ tsv file in conll format
    Args:
        filepath: Path to the file
    Returns: List of words, List of labels
    """

    dataset_words = []
    dataset_labels = []
    with open(filepath, "r", encoding="utf-8") as f:
        words = []
        labels = []
        for line in f:
            line = line.strip()
            if line.startswith("#") or line == "" or line == "\n":
                if words:
                    dataset_words.append(words)
                    dataset_labels.append(labels)
                    words = []
                    labels = []
            else:
                try:
                    _, word, _, label = line.split()
                except ValueError:
                    try:
                        word, label, _ = line.split()
                    except ValueError:
                        raise ValueError(f"Cannot path_or_split line: {line}")
                if word:
                    words.append(word)
                    labels.append(label)
        if words:
            dataset_words.append(words)
            dataset_labels.append(labels)

    print(f"Read {len(dataset_words)} sentences from {filepath}")
    return dataset_words, dataset_labels


def summarize_examples(dataset_words, dataset_labels):
    entities = defaultdict(Counter)
    for words, labels in zip(dataset_words, dataset_labels):
        # Some of the CoNLL02-03 datasets are in IOB1 format instead of IOB2,
        # we convert them to IOB2, so we don't have to deal with this later.
        # labels = rewrite_labels(labels=labels, encoding="iob2")
        # Get labeled word spans
        spans = []
        for i, label in enumerate(labels):
            if label == "NoLabel":
                continue
            elif label.startswith("B-"):
                
                spans.append([label[2:], i, i + 1])
                
            elif label.startswith("I-"):
                try:
                    spans[-1][2] += 1
                except:
                    pass
            elif label == "Orecurring_datetime":
                continue
            else:
                raise ValueError(f"Found an unexpected label: {label}")

        # Get entities
        for label, start, end in spans:
            entities[label][" ".join(words[start:end])] += 1
    return entities

words, labels = read_tsv("/coc/pskynet6/ychen3411/transfusion/GoLLIE/dataset/MultiTO/en/train-en.conllu")

entities = summarize_examples(words, labels)

for label in entities:
    print(label, entities[label].most_common()[:10])

for label in entities:
    print(label)