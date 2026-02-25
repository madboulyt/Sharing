import json
import os
from typing import Generator

import pytest


@pytest.fixture(scope="function")
def sample_docs():
    doc_0 = " osayd@mozn.sa آهلاً وسهلاً بالأخوين الكريمين"
    doc_1 = "  آهلاً وسهلاًي بالحاضرين في جمعتنا الجميلة هذه في بيتنا الرهيب"
    doc_2 = "  آهلاً وسهلاًي في جمعتنا الجميلة هذه في بيتنا osayd@mozn.sa"
    return [doc_0, doc_1, doc_2]


@pytest.fixture(scope="function")
def cleaned_docs():
    return [
        "آهلا وسهلاي بالحاضرين في جمعتنا الجميلة هذه في بيتنا الرهيب",
        "آهلا وسهلاي في جمعتنا الجميلة هذه في بيتنا [رابط] ",
    ]


@pytest.fixture(scope="function")
def prepare_jsonl_files(sample_docs) -> Generator:
    in_path = "/tmp/arabic_cleaning_lib_file.josnl"
    text_fieled = "text"
    out_path = "/tmp/arabic_cleaning_lib_file_result.jsonl"
    with open(in_path, "w") as f_w:
        for doc in sample_docs:
            f_w.write(json.dumps({text_fieled: doc}, ensure_ascii=False))
            f_w.write("\n")
    yield in_path, text_fieled, out_path
    os.remove(in_path)
    os.remove(out_path)
