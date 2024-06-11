import re
import json

def easyproject_encoding_re(tokens, entities, relations):
    """
    Example:
    {'tokens': ['An', 'art', 'exhibit', 'at', 'the', 'Hakawati', 'Theatre', 'in', 
    'Arab', 'east', 'Jerusalem', 'was', 'a', 'series', 'of', 'portraits', 'of', 'Palestinians', 
    'killed', 'in', 'the', 'rebellion', '.'], 
    'entities': [{'type': 'Org', 'start': 5, 'end': 7}, 
                {'type': 'Other', 'start': 8, 'end': 9}, 
                {'type': 'Loc', 'start': 10, 'end': 11}, 
                {'type': 'Other', 'start': 17, 'end': 18}], 
    'relations': [{'type': 'OrgBased_In', 'head': 0, 'tail': 2}], 
    'orig_id': 17}
    """
    marker_idx = 0
    marker2label = {}
    for ent in entities:
        start, end = ent["start"] + marker_idx * 2, ent["end"] + marker_idx * 2
        tokens.insert(start, "[{}]".format(marker_idx))
        tokens.insert(end + 1, "[/{}]".format(marker_idx))
        marker2label[marker_idx] = ent["type"]
        marker_idx += 1

    encoded_sentence = " ".join(tokens)
    marker2label["relations"] = relations
    return encoded_sentence, marker2label

def encode_data(
    path
):
    with open("dataset/conll04/conll04_train.json", "rt") as in_f:
        data = json.load(in_f)
    
    output = []
    for line in data:
        key = line["orig_id"]
        tokens = line["tokens"]
        entities = line["entities"]
        relations = line["relations"]
        
        encoded_sentence, marker2label = easyproject_encoding_re(tokens, entities, relations)

        output.append({"sentence": encoded_sentence, 
                        "marker2label": marker2label})

    return output

def extract_entities(sentence):
    pattern = r'\[(\d+)\](.*?)\[/\1\]'
    entities = re.findall(pattern, sentence)
    # filter out empty entity
    entities = [(idx, ent) for idx, ent in entities if ent.strip() != ""]
    return entities
  
def verify_entities(input_entities, output_entities, marker2label):

    if len(output_entities) != len(input_entities):
        #print("Number of entities mismatch!")
        return False

    output_label_count = {}
    input_label_count = {}

    for marker, entity in output_entities:
        label = marker
        output_label_count[label] = output_label_count.get(label, 0) + 1

    for marker, entity in input_entities:
        label = marker
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
    # keep key
    clean_sentence = remove_markers(output_sentence, marker2label)
    entities = [(key, word.strip()) for key, word in output_entities]
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