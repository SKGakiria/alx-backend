#!/usr/bin/env python3
"""Module containing function that calculates the start and end
index for a specific page based on the provided page size"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Function returns a tuple containing the start and end index"""
    start_idx, end_idx = 0, 0
    for i in range(page):
        start_idx = end_idx
        end_idx += page_size

    return (start_idx, end_idx)
