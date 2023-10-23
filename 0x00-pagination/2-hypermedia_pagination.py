#!/usr/bin/env python3
"""Module containing class Server with methods to create simple pagination from
csv data"""
import csv
from typing import List
index_range = __import__('0-simple_helper_function').index_range


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    @staticmethod
    def assert_positive_integer_type(value: int) -> None:
        """Method asserts that the value is a positive integer"""
        assert type(value) is int and value > 0

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Method that returns the appropriate page of the dataset based
        on the specified page and page size"""
        self.assert_positive_integer_type(page)
        self.assert_positive_integer_type(page_size)

        dataset = self.dataset()
        start_idx, end_idx = index_range(page, page_size)
        try:
            data = dataset[start_idx:end_idx]
        except IndexError:
            data = []
        return data

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """Method that calculates additional information about the current page
        and its pagination context and returns it in a dictionary format"""
        total_pages = len(self.dataset()) // page_size + 1
        data = self.get_page(page, page_size)
        result = {
            "page": page,
            "page_size": page_size if page_size <= len(data) else len(data),
            "total_pages": total_pages,
            "data": data,
            "prev_page": page - 1 if page > 1 else None,
            "next_page": page + 1 if page + 1 <= total_pages else None
        }
        return result
