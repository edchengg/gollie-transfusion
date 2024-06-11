import re
import json

def easyproject_encoding_ace(tokens, entities):
    """
    Example:
    {'tokens': ['An', 'art', 'exhibit', 'at', 'the', 'Hakawati', 'Theatre', 'in', 
    'Arab', 'east', 'Jerusalem', 'was', 'a', 'series', 'of', 'portraits', 'of', 'Palestinians', 
    'killed', 'in', 'the', 'rebellion', '.'], 
    'entities': [{'type': 'Org', 'start': 5, 'end': 7}, 
                {'type': 'Other', 'start': 8, 'end': 9}, 
                {'type': 'Loc', 'start': 10, 'end': 11}, 
                {'type': 'Other', 'start': 17, 'end': 18}], 
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
    
    return encoded_sentence, marker2label

def has_overlap(spans):
    # Iterate through the sorted spans
    for i in range(1, len(spans)):
        # Check if the current span's start time is less than the previous span's end time
        if spans[i]["start"] < spans[i-1]["end"]:
            return True

    return False

def encode_data(
    path
):
    output = []
    with open("/srv/nlprx-lab/share6/dminh6/X-Gear/processed_data/ace05_en_mT5/train.json", "rt") as in_f:
        for line in in_f:
            line = json.loads(line.strip())
            tokens = line["tokens"]
            # token length filter
            if len(tokens) <= 15:
                continue
            entities = [{"start": entity["start"], "end": entity["end"], "type": entity["id"]}
                for entity in line["entity_mentions"]
            ]
            events = []
            for event in line["event_mentions"]:
                events.append({"start": event["trigger"]["start"], "end": event["trigger"]["end"], "type": event["id"]})

            span_mentions = entities + events
            # sort span_mentions based on start
            span_mentions.sort(key=lambda x: x["start"])
            # check span has overlap
            is_overlap = has_overlap(span_mentions)
            if not is_overlap:
                encoded_sentence, marker2label = easyproject_encoding_ace(tokens, span_mentions)
                marker2label["annotation"] = line # save all information for decoding
                output.append({ 
                            "sentence": encoded_sentence, 
                            "marker2label": marker2label}
                            )
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