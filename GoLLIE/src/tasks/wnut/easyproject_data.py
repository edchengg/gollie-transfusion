import re
import json
from ..utils_easyproject import easyproject_encoding_ner
from src.tasks.label_encoding import rewrite_labels

def encode_data(
    split
):
    from datasets import load_dataset

    dataset = load_dataset("wnut_17")
    # Dirty fix to prevent errors reading the labels
    label_names = dataset["train"].features["ner_tags"].feature.names
    i = label_names.index("B-creative-work")
    label_names[i] = "B-creative_work"
    i = label_names.index("I-creative-work")
    label_names[i] = "I-creative_work"

    id2label = dict(enumerate(label_names))
    output = []

    for example in dataset[split]:
        words = example["tokens"]
        # Ensure IOB2 encoding
        labels = rewrite_labels(labels=[id2label[label] for label in example["ner_tags"]], encoding="iob2")

        # Get entities
        encoded_sentence, marker2label = easyproject_encoding_ner(words, labels)

        output.append({"sentence": encoded_sentence, 
        "marker2label": marker2label})

    return output

def extract_entities(sentence):
    pattern = r'\[(\d+)\](.*?)\[/\1\]'
    entities = re.findall(pattern, sentence)
    entities = [(idx, ent) for idx, ent in entities if ent.strip() != ""]
    return entities
  
def verify_entities(input_entities, output_entities, marker2label):

    if len(output_entities) != len(input_entities):
        #print("Number of entities mismatch!")
        return False

    output_label_count = {}
    input_label_count = {}

    for marker, entity in output_entities:
        label = marker2label.get(marker, None)
        output_label_count[label] = output_label_count.get(label, 0) + 1

    for marker, entity in input_entities:
        label = marker2label.get(marker, None)
        input_label_count[label] = input_label_count.get(label, 0) + 1

    if output_label_count != input_label_count:
        #print("NER type count mismatch!")
        return False

    return True

def remove_markers(output_sentence, marker2label):
    for marker in marker2label:
        start_tag = f'[{marker}]'
        end_tag = f'[/{marker}]'
        output_sentence = output_sentence.replace(start_tag, '').replace(end_tag, '')
    return output_sentence

def prepare_data(output_sentence, output_entities, marker2label):
    # remove markers
    clean_sentence = remove_markers(output_sentence, marker2label)
    entities = [(marker2label[key], word.strip()) for key, word in output_entities]
    return clean_sentence, entities

def decode_data(input_sentence, output_sentence, marker2label):
    input_entities = extract_entities(input_sentence)
    output_entities = extract_entities(output_sentence)
    is_valid = verify_entities(input_entities, output_entities, marker2label)
    if is_valid:
        # Get entities
        clean_sentence, entities = prepare_data(output_sentence, output_entities, marker2label)
        return clean_sentence, entities
    else:
        return None, None