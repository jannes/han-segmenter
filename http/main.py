from __future__ import annotations
from segment import get_dict_words, segment
from typing import List

from fastapi import FastAPI
import pkuseg
from pydantic import BaseModel


class Chapter(BaseModel):
    title: str
    text: str
    subchapters: List[Chapter]

# make self-reference in subchapter's type work
# https://pydantic-docs.helpmanual.io/usage/postponed_annotations/#self-referencing-models
Chapter.update_forward_refs()


class Book(BaseModel):
    title: str
    author: str
    preface_content: str
    chapters: List[Chapter]


class BookSegmentationQuery(BaseModel):
    book: Book
    dict_only: bool


class StringSegmentationQuery(BaseModel):
    string: str
    dict_only: bool


seg = pkuseg.pkuseg()
dict_words = get_dict_words()
app = FastAPI()


def segment_chapter(chapter: Chapter, dict_only: bool) -> dict: 
    title_segmented = segment(seg, chapter.title, dict_only, dict_words)
    text_segmented = segment(seg, chapter.text, dict_only, dict_words)
    subchapters_segmented = [segment_chapter(c, dict_only) for c in chapter.subchapters]
    return {
        'title': title_segmented,
        'text': text_segmented,
        'subchapters': subchapters_segmented
    }


@app.post("/segmentBook")
def segment_book(query: BookSegmentationQuery):
    book = query.book
    title_segmented = segment(seg, book.title, query.dict_only, dict_words)
    author_segmented = segment(seg, book.author, query.dict_only, dict_words)
    preface_content_segmented = segment(seg, book.preface_content, query.dict_only, dict_words)
    chapters_segmented = [segment_chapter(c, query.dict_only) for c in book.chapters]
    return {
        'title': title_segmented,
        'author': author_segmented,
        'preface_content': preface_content_segmented,
        'chapters': chapters_segmented
    }

@app.post("/segmentString")
def segment_string(query: StringSegmentationQuery):
    return {'segmented': segment(seg, query.string, query.dict_only, dict_words)}