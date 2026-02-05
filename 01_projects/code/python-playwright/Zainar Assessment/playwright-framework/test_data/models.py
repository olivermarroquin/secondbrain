"""Test data models and constants"""
from dataclasses import dataclass

@dataclass
class ExpectedText:
    FINISH_MESSAGE = "Hello World!"

@dataclass
class TableDimensions:
    EXPECTED_ROWS = 10
    EXPECTED_COLUMNS = 7

@dataclass
class CanvasDimensions:
    MIN_WIDTH = 0
    MIN_HEIGHT = 0
