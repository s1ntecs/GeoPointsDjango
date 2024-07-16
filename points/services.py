from dataclasses import dataclass
from typing import List

from .models import Point


def get_row(points, row_number):
    return points.filter(row_number=row_number)


def get_column(points, column_name):
    column_mapping = {
        'A': 'name',
        'B': 'x',
        'C': 'y',
        'D': 'z',
        'E': 'part__name'
    }
    if column_name in column_mapping:
        return points.values_list(column_mapping[column_name], flat=True)
    else:
        return []


def find_word(points: List[Point], word="нет данных"):
    results = []
    for point in points:
        if word in point.x:
            results.append(f"Ячейка: B{point.row_number}")
        if word in point.y:
            results.append(f"Ячейка: С{point.row_number}")
        if word in point.z:
            results.append(f"Ячейка: В{point.row_number}")
    return results


def column_letter(n):
    """Конвертирует номер столбца в букву столбца"""
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string


def safe_cell_value(row, index):
    return row[index].value if index < len(row) and \
        row[index].value is not None else 'нет данных'


@dataclass
class PointData:
    x: float
    y: float
    z: float


class CoordinateCalculator:
    @staticmethod
    def add_coordinates(point_a: PointData,
                        point_b: PointData) -> Point:
        return Point(x=point_a.x + point_b.x,
                     y=point_a.y + point_b.y,
                     z=point_a.z + point_b.z)

    @staticmethod
    def subtract_coordinates(point_a: PointData,
                             point_b: PointData) -> Point:
        return Point(x=point_a.x - point_b.x,
                     y=point_b.y - point_b.y,
                     z=point_a.z - point_b.z)
