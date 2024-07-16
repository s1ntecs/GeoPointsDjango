from django.http import HttpResponse
from openpyxl import load_workbook

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse

from .models import Point, Part, PointFile
from .forms import (PointForm,
                    ExcelUploadForm,
                    CoordinateCalculatorForm)
from .services import (get_row,
                       find_word,
                       get_column,
                       safe_cell_value,
                       CoordinateCalculator)


def point_list(request):
    file_name = request.GET.get('file_name')
    if file_name:
        points = Point.objects.filter(point_file__file_name=file_name)
    else:
        points = Point.objects.all()

    file_names = PointFile.objects.all()
    return render(request, 'points/point_list.html',
                  {'points': points,
                   'file_names': file_names,
                   'selected_file': file_name})


@login_required
def point_delete(request, pk):
    point = get_object_or_404(Point, pk=pk)
    point.delete()
    return redirect(reverse('points:point_list'))


@login_required
def point_create(request):
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
    if request.method == 'POST':
        print("XUI")
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            print("PIZDA")
            excel_file = request.FILES['file']
            range_str = form.cleaned_data['range_str']

            try:
                wb = load_workbook(excel_file)
                sheet = wb.active
            except Exception as e:
                print(f"Error loading workbook: {e}")
                return HttpResponse("Error loading workbook")

            try:
                point_file = PointFile.objects.create(
                    file_name=excel_file.name)
            except Exception as e:
                print(f"Error creating PointFile: {e}")
                return HttpResponse("Error creating PointFile")

            for row in sheet[range_str]:
                try:
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
                except Exception as e:
                    print(f"Error processing row {row}: {e}")

            return redirect('points:point_list')
    else:
        form = ExcelUploadForm()
    return render(request, 'points/import_points.html', {'form': form})


def create_point(request):
    if request.method == 'POST':
        form = PointForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('points:point_list')
    else:
        form = PointForm()
    return render(request, 'points/point_form.html', {'form': form})


def point_analysis(request):
    points = Point.objects.all()

    row_number = request.GET.get('row_number')
    column_name = request.GET.get('column_name')
    search_word = request.GET.get('search_word')

    row_data = get_row(points, row_number) if row_number else None
    column_data = get_column(points, column_name) if column_name else None
    word_locations = find_word(points, search_word) if search_word else None

    return render(request, 'points/point_analysis.html', {
        'row_data': row_data,
        'column_data': column_data,
        'word_locations': word_locations,
        'row_number': row_number,
        'column_name': column_name,
        'search_word': search_word,
    })


def coordinate_calculator(request):
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
