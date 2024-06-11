import inspect
import json
from typing import Dict, List, Tuple, Type, Union

from src.tasks.tydiqa.guidelines import GUIDELINES
# from src.tasks.tydiqa.guidelines_gold import EXAMPLES
from src.tasks.tydiqa.prompts import (
    Entity,
    ShortAnswer,
    ANSWER_DEFINITIONS,
)

from ..utils_data import DatasetLoader, Sampler

def get_tydiqa_hf(
    split: str,
    language: str,
) -> Tuple[List[str], List[List[Entity]], List[str]]:
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

    dataset = load_dataset("tydiqa", "secondary_task")

    dataset_sentences: List[str] = []
    dataset_id: List[str] = []
    dataset_answers: List[List[Entity]] = []
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

        text = "Context: {}; Question: {}".format(context, question)
        dataset_sentences.append(text)
        dataset_id.append(example["id"])

        # Get answers
        answers = set()
        for ans in example["answers"]["text"]:
            answers.add(ans)

        filtered_answers = [ShortAnswer(span=text) for text in list(answers)]

        dataset_answers.append(filtered_answers)

    return dataset_sentences, dataset_answers, dataset_id

class TyDiQADatasetLoader(DatasetLoader):
    """
    A `DatasetLoader` for the TydiQA dataset.

    Args:
        path (`str`):
            The location of the dataset directory.

    Raises:
        `ValueError`:
            raised when a not defined value found.
    """
    
    def __init__(self, split: str, **kwargs) -> None:
        self.elements = {}

        assert split in ["train", "validation"], f"split only in train, validation."

        dataset_sentences, dataset_answers, dataset_id = get_tydiqa_hf(
                split=split, 
                language=kwargs["language"]
        )
        
        for key, (sentence, answer, data_id) in enumerate(zip(dataset_sentences, dataset_answers, dataset_id)):
            self.elements[key] = {
                "id": data_id,
                "doc_id": data_id,
                "text": sentence,
                "answer": [answer[0]],
                "gold": answer,
            }

def load_translation(language):
    path = f"data_translatetest/tydiqa/{language}_eng_Latn.jsonl"
    with open(path, "r", encoding="utf-8") as f:
        data = [json.loads(l)["output_sentence"] for l in f]

    path = f"data_translatetest/tydiqa/ques_{language}_eng_Latn.jsonl"
    with open(path, "r", encoding="utf-8") as f:
        ques_data = [json.loads(l)["output_sentence"] for l in f]

    output = []
    for d, q in zip(data, ques_data):
        output.append("Context: {} Question: {}".format(d, q))

    return output

class TyDiQATransFusionDatasetLoader(DatasetLoader):
    """
    A `DatasetLoader` for the TydiQA dataset.

    Args:
        path (`str`):
            The location of the dataset directory.

    Raises:
        `ValueError`:
            raised when a not defined value found.
    """
    
    def __init__(self, split: str, **kwargs) -> None:
        self.elements = {}

        assert split in ["train", "validation"], f"split only in train, validation."

        dataset_sentences, dataset_answers, dataset_id = get_tydiqa_hf(
                split=split, 
                language=kwargs["language"]
        )
        
        translation_data = load_translation(language=kwargs["language"])

        for key, (sentence, answer, data_id, translation) in enumerate(zip(dataset_sentences, dataset_answers, dataset_id, translation_data)):
            self.elements[key] = {
                "id": data_id,
                "doc_id": data_id,
                "text": sentence,
                "en_text": translation,
                "answer": [answer[0]],
                "en_answer": [],
                "gold": answer,
                "en_gold": [],
            }

class TyDiQASampler(Sampler):
    """
    A data `Sampler` for the TydiQA dataset.

    Args:
        dataset_loader (`TydiQADatasetLoader`):
            The dataset loader that contains the data information.
        task (`str`, optional):
            The task to sample. It must be one of the following: NER, RE.
            Defaults to `None`.
        split (`str`, optional):
            The split to sample. It must be one of the following: "train", "dev" or
            "test". Depending on the split the sampling strategy differs. Defaults to
            `"train"`.
        parallel_instances (`Union[int, Tuple[int, int]]`, optional):
            The number of sentences sampled in parallel. Options:

                * **`int`**: The amount of elements that will be sampled in parallel.
                * **`tuple`**: The range of elements that will be sampled in parallel.

            Defaults to 1.
        max_guidelines (`int`, optional):
            The number of guidelines to append to the example at the same time. If `-1`
            is given then all the guidelines are appended. Defaults to `-1`.
        guideline_dropout (`float`, optional):
            The probability to dropout a guideline definition for the given example. This
            is only applied on training. Defaults to `0.0`.
        seed (`float`, optional):
            The seed to sample the examples. Defaults to `0`.
        prompt_template (`str`, optional):
            The path to the prompt template. Defaults to `"templates/prompt.txt"`.
        ensure_positives_on_train (bool, optional):
            Whether to ensure that the guidelines of annotated examples are not removed.
            Defaults to `False`.
        dataset_name (str, optional):
            The name of the dataset. Defaults to `None`.
        scorer (`str`, optional):
           The scorer class import string. Defaults to `None`.
        sample_only_gold_guidelines (`bool`, optional):
            Whether to sample only guidelines of present annotations. Defaults to `False`.
    """

    def __init__(
        self,
        dataset_loader: TyDiQADatasetLoader,
        task: str = None,
        split: str = "validation",
        parallel_instances: Union[int, Tuple[int, int]] = 1,
        max_guidelines: int = -1,
        guideline_dropout: float = 0.0,
        seed: float = 0,
        ensure_positives_on_train: bool = False,
        dataset_name: str = None,
        scorer: str = None,
        sample_only_gold_guidelines: bool = False,
        use_transfusion: bool = False,
        use_transfusionv2: bool = False,
        **kwargs,
    ) -> None:
        assert task in [
            "QA"
        ], f"{task} must be QA."

        if use_transfusion:
            if use_transfusionv2:
                task_definitions, task_target, task_template = ANSWER_DEFINITIONS, "answer", "templates/prompt_qa_tfv2.txt"
            else:
                task_definitions, task_target, task_template = ANSWER_DEFINITIONS, "answer", "templates/prompt_qa_tf.txt"
        else:
            task_definitions, task_target, task_template = ANSWER_DEFINITIONS, "answer", "templates/prompt_qa.txt"

        is_coarse_to_fine = False
        COARSE_TO_FINE = None
        FINE_TO_COARSE = None

        kwargs.pop("prompt_template")

        super().__init__(
            dataset_loader=dataset_loader,
            task=task,
            split=split,
            parallel_instances=parallel_instances,
            max_guidelines=max_guidelines,
            guideline_dropout=guideline_dropout,
            seed=seed,
            prompt_template=task_template,
            ensure_positives_on_train=ensure_positives_on_train,
            sample_only_gold_guidelines=sample_only_gold_guidelines,
            dataset_name=dataset_name,
            scorer=scorer,
            task_definitions=task_definitions,
            task_target=task_target,
            is_coarse_to_fine=is_coarse_to_fine,
            coarse_to_fine=COARSE_TO_FINE,
            fine_to_coarse=FINE_TO_COARSE,
            definitions=GUIDELINES,
            use_transfusion=use_transfusion,
            # examples=EXAMPLES,
            **kwargs,
        )
