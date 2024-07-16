from openpyxl import load_workbook
from dataclasses import dataclass
from typing import List

from .models import Point, PointFile, Part

COLUMN_MAPPING = {
    'A': 'name',
    'B': 'x',
    'C': 'y',
    'D': 'z',
    'E': 'part__name'
}


@dataclass
class PointData:
    x: float
    y: float
    z: float


class CoordinateCalculator:
    @staticmethod
    def add_coordinates(point_a: PointData, point_b: PointData) -> Point:
        """
        Складывает координаты двух точек и возвращает новую точку.
        """
        return Point(x=point_a.x + point_b.x,
                     y=point_a.y + point_b.y,
                     z=point_a.z + point_b.z)

    @staticmethod
    def subtract_coordinates(point_a: PointData, point_b: PointData) -> Point:
        """
        Вычитает координаты второй точки из координат первой и возвращает новую точку.

        """
        return Point(x=point_a.x - point_b.x,
                     y=point_a.y - point_b.y,
                     z=point_a.z - point_b.z)


def get_row(points, row_number):
    """
    Возвращает все точки из указанного ряда.
    """
    return points.filter(row_number=row_number)


def get_column(points, column_name):
    """
    Возвращает значения указанного столбца.
    """
    
    if column_name in COLUMN_MAPPING:
        return points.values_list(COLUMN_MAPPING[column_name], flat=True)
    else:
        return []


def find_word(points: List[Point], word="нет данных"):
    """
    Ищет указанное слово в координатах точек и возвращает список ячеек,
    где это слово найдено.
    """
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
    """
    Конвертирует номер столбца в букву столбца.
    """
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string


def safe_cell_value(row, index):
    return row[index].value if index < len(row) and row[index].value is not None else 'нет данных'


def process_sheet(sheet, range_str, point_file):
    """
    Обрабатывает указанный диапазон листа и добавляет точки в базу данных.
    """
    for row in sheet[range_str]:
        try:
            process_row(row, point_file)
        except Exception:
            pass


def handle_uploaded_file(excel_file, range_str):
    """
    Обрабатывает загруженный файл Excel и добавляет данные в базу данных.
    """
    wb = load_workbook(excel_file)
    sheet = wb.active
    point_file = PointFile.objects.create(file_name=excel_file.name)
    process_sheet(sheet, range_str, point_file)


def process_row(row, point_file):
    """
    Обрабатывает строку данных и добавляет точку в базу данных.


    """
    idx = row[0].row if len(row) > 0 else None
    name = safe_cell_value(row, 0)
    x = safe_cell_value(row, 1)
    y = safe_cell_value(row, 2)
    z = safe_cell_value(row, 3)
    part_name = safe_cell_value(row, 4)
    part, created = Part.objects.get_or_create(name=part_name)
    Point.objects.create(
        name=name,
        x=x,
        y=y,
        z=z,
        part=part,
        point_file=point_file,
        row_number=idx
    )
