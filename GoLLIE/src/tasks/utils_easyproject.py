import copy

def decode_label_span(label):
        label_tags = label
        span_labels = []
        last = 'O'
        start = -1
        for i, tag in enumerate(label_tags):
            pos, _ = (None, 'O') if tag == 'O' else tag.split('-')
            if (pos == 'B' or tag == 'O') and last != 'O':  # end of span
                span_labels.append((start, i, last.split('-')[1]))
            if pos == 'B' or last == 'O':  # start of span or move on
                start = i
            last = tag
        if label_tags[-1] != 'O':
            span_labels.append((start, len(label_tags), label_tags[-1].split('-')[1]))

        return span_labels

def extract_entity(word, label):

    span_labels = decode_label_span(label)
    entity_list = []
    tag_list = []
    for span in span_labels:
        s, e, tag = span
        entity = word[s: e]
        entity_list.append(entity)
        tag_list.append(tag)

    return entity_list, tag_list, span_labels

def encode(tokens, label, tag2mark):
    copy_tokens = copy.deepcopy(tokens)
    prev_start_lab = 'O'
    for idx, lab in enumerate(label):
        if lab != 'O' and (prev_start_lab == 'I' or prev_start_lab == 'B'):
            start_lab = lab.split('-')[0]
            tag = lab.split('-')[1]

            # check if its the same label
            if start_lab == 'B':
                # new label span
                token = copy_tokens[idx]
                token_new = '{} {} {}'.format(tag2mark[prev_tag]['e'], tag2mark[tag]['s'], token)
                copy_tokens[idx] = token_new
                prev_start_lab = start_lab
                prev_tag = tag
            else:
                prev_start_lab = start_lab
                prev_tag = tag
        elif lab != 'O':
            start_lab = lab.split('-')[0]
            tag = lab.split('-')[1]

            if start_lab == 'B':
                token = copy_tokens[idx]
                # modify token
                token_new = '{} {}'.format(tag2mark[tag]['s'], token)
                copy_tokens[idx] = token_new

            prev_start_lab = start_lab
            prev_tag = tag

        elif lab == 'O' and (prev_start_lab == 'I' or prev_start_lab == 'B'):
            token = copy_tokens[idx - 1]
            # modify token
            token_new = '{} {}'.format(token, tag2mark[prev_tag]['e'])
            copy_tokens[idx - 1] = token_new

            prev_start_lab = 'O'
            prev_tag = 'O'
        else:
            prev_start_lab = 'O'
            prev_tag = 'O'

    # last
    if label[-1] != 'O':
        start_lab = label[-1].split('-')[0]
        tag = label[-1].split('-')[1]

        if start_lab == 'B' or start_lab == 'I':
            new_token = copy_tokens[-1] + ' {}'.format(tag2mark[tag]['e'])
            copy_tokens[-1] = new_token

    encoded_sentence = ' '.join(copy_tokens)
    return encoded_sentence

def easyproject_encoding_ner(words, labels):
    # encode labels into words
    # return encoded sentence with marker2label mapping
    entity_list, tag_list, span_labels = extract_entity(words, labels)
    tag2mark = {}
    marker2label = {}
    idx = 0
    for _, tag in enumerate(tag_list):
        if tag not in tag2mark:
            tag2mark[tag] = {"s": "[{}]".format(idx), "e": "[/{}]".format(idx)}
            marker2label[idx] = tag
            idx += 1

    encoded_sentence = encode(words, labels, tag2mark)
    return encoded_sentence, marker2label


# id2label = {0: 'O',
#  1: 'B-PERSON',
#  2: 'I-PERSON',
#  3: 'B-NORP',
#  4: 'I-NORP',
#  5: 'B-FAC',
#  6: 'I-FAC',
#  7: 'B-ORG',
#  8: 'I-ORG',
#  9: 'B-GPE',
#  10: 'I-GPE',
#  11: 'B-LOC',
#  12: 'I-LOC',
#  13: 'B-PRODUCT',
#  14: 'I-PRODUCT',
#  15: 'B-DATE',
#  16: 'I-DATE',
#  17: 'B-TIME',
#  18: 'I-TIME',
#  19: 'B-PERCENT',
#  20: 'I-PERCENT',
#  21: 'B-MONEY',
#  22: 'I-MONEY',
#  23: 'B-QUANTITY',
#  24: 'I-QUANTITY',
#  25: 'B-ORDINAL',
#  26: 'I-ORDINAL',
#  27: 'B-CARDINAL',
#  28: 'I-CARDINAL',
#  29: 'B-EVENT',
#  30: 'I-EVENT',
#  31: 'B-WORK_OF_ART',
#  32: 'I-WORK_OF_ART',
#  33: 'B-LAW',
#  34: 'I-LAW',
#  35: 'B-LANGUAGE',
#  36: 'I-LANGUAGE'}

# sentences = [['The', 'Senate', 'has', 'overwhelmingly', 'approved', 'an', 'agriculture', 'spending', 'bill', 'that', 'includes', 'a', 'provision', 'to', 'ease', 'trade', 'sanctions', 'against', 'China', '.'],
# ['Violence', 'in', 'the', 'West', 'Bank', 'and', 'Gaza', 'has', 'claimed', 'the', 'lives', 'of', 'eight', 'Palestinians', 'today', '.'],
# ['A', 'one', '-', 'time', 'federal', 'judge', 'who', 'has', 'seen', 'the', 'law', 'from', 'both', 'sides', 'of', 'the', 'bench', 'is', 'now', 'hoping', 'to', 'keep', 'his', 'job', 'making', 'laws', '.']]

# labels = [[0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0],
# [0, 0, 9, 10, 10, 0, 9, 0, 0, 0, 0, 0, 27, 3, 15, 0],
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


# for sent, label in zip(sentences, labels):
#     label_annotation = [id2label[l] for l in label]
#     encoded_sentence, mark2label = easyproject_encoding_ner(sent, label_annotation)

#     print(encoded_sentence)
#     print(mark2label)
#     print("========")