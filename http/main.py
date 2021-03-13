from segment import get_dict_words, segment
from typing import List

from fastapi import FastAPI
import pkuseg
from pydantic import BaseModel


class Section(BaseModel):
    title: str
    content: str


class Book(BaseModel):
    title: str
    sections: List[Section]


class BookSegmentationQuery(BaseModel):
    book: Book
    dict_only: bool


class StringSegmentationQuery(BaseModel):
    string: str
    dict_only: bool


seg = pkuseg.pkuseg()
dict_words = get_dict_words()
app = FastAPI()


@app.post("/segmentBook")
def segment_book(query: BookSegmentationQuery):
    book = query.book
    segmented_sections = list()
    for i, section in enumerate(book.sections):
        s = ''
        if i == 0:
            s += book.title
        s += section.title
        s += section.content
        segmented_sections.append(segment(seg, s, query.dict_only, dict_words))
    return {'sections': segmented_sections}

@app.post("/segmentString")
def segment_string(query: StringSegmentationQuery):
    return {'segmented': segment(seg, query.string, query.dict_only, dict_words)}