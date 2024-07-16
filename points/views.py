from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse

from .models import Point, PointFile
from .forms import (PointForm, ExcelUploadForm, CoordinateCalculatorForm)
from .services import (get_row,
                       find_word,
                       get_column,
                       CoordinateCalculator,
                       handle_uploaded_file,
                       COLUMN_MAPPING)


def point_list(request):
    """
    Отображает список точек.
    """
    file_name = request.GET.get('file_name')
    if file_name:
        points = Point.objects.filter(point_file__file_name=file_name)
    else:
        points = Point.objects.all()

    file_names = PointFile.objects.all()
    return render(request, 'points/point_list.html', {
        'points': points,
        'file_names': file_names,
        'selected_file': file_name
    })


@login_required
def point_delete(request, pk):
    """
    Удаляет указанную точку.
    """
    point = get_object_or_404(Point, pk=pk)
    point.delete()
    return redirect(reverse('points:point_list'))


@login_required
def point_create(request):
    """
    Создает новую точку.
    """
    if request.method == "POST":
        form = PointForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('points:point_list')
    else:
        form = PointForm()
    return render(request, 'points/point_form.html', {'form': form})


@login_required
@permission_required('points.change_point', raise_exception=True)
def point_edit(request, pk):
    """
    Редактирует указанную точку.
    """
    point = get_object_or_404(Point, pk=pk)
    if request.method == "POST":
        form = PointForm(request.POST, instance=point)
        if form.is_valid():
            form.save()
            return redirect('points:point_list')
    else:
        form = PointForm(instance=point)
    return render(request, 'points/point_form.html', {'form': form})


def import_points(request):
    """
    Представление страницы Импорта точек из файла Excel.
    """
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'],
                                 form.cleaned_data['range_str'])
            return redirect('points:point_list')
    else:
        form = ExcelUploadForm()
    return render(request, 'points/import_points.html', {'form': form})


def point_analysis(request):
    """
    Представление страницы Анализа данных.
    """
    points = Point.objects.all()

    row_number = request.GET.get('row_number')
    column_name = request.GET.get('column_name')
    search_word = request.GET.get('search_word')
    cell_number = request.GET.get('cell_number')

    cell_data = None

    if cell_number:
        column_key = cell_number[0].upper()
        row_num = cell_number[1:]

        if column_key in COLUMN_MAPPING and row_num.isdigit():
            row_num = int(row_num)
            point = points.filter(row_number=row_num).first()
            if point:
                if column_key == 'A':
                    cell_data = point.name
                elif column_key == 'B':
                    cell_data = point.x
                elif column_key == 'C':
                    cell_data = point.y
                elif column_key == 'D':
                    cell_data = point.z
                elif column_key == 'E':
                    cell_data = point.part.name

    row_data = get_row(points, row_number) if row_number else None
    column_data = get_column(points, column_name) if column_name else None
    word_locations = find_word(points, search_word) if search_word else None

    return render(request, 'points/point_analysis.html', {
        'row_data': row_data,
        'column_data': column_data,
        'word_locations': word_locations,
        'cell_data': cell_data,
        'row_number': row_number,
        'column_name': column_name,
        'search_word': search_word,
        'cell_number': cell_number,
    })


def coordinate_calculator(request):
    """
    Вычисляет сумму или разность координат двух точек.
    """
    result = None

    if request.method == 'POST':
        form = CoordinateCalculatorForm(request.POST)
        if form.is_valid():
            ax = form.cleaned_data['ax']
            ay = form.cleaned_data['ay']
            az = form.cleaned_data['az']
            bx = form.cleaned_data['bx']
            by = form.cleaned_data['by']
            bz = form.cleaned_data['bz']

            point_a = Point(x=ax, y=ay, z=az)
            point_b = Point(x=bx, y=by, z=bz)

            calculator = CoordinateCalculator()

            if 'add' in request.POST:
                result = calculator.add_coordinates(point_a, point_b)
            elif 'subtract' in request.POST:
                result = calculator.subtract_coordinates(point_a, point_b)

    else:
        form = CoordinateCalculatorForm()

    return render(request, 'points/coordinate_calculator.html',
                  {'form': form, 'result': result})