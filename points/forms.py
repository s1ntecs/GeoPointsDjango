from django import forms
from .models import Point


class PointForm(forms.ModelForm):
    class Meta:
        model = Point
        fields = ['name', 'x', 'y', 'z', 'part']


class ExcelUploadForm(forms.Form):
    file = forms.FileField(label='Выбери Excel файл')
    range_str = forms.CharField(label='Диапазон ячеек',
                                initial='A1:E35',
                                help_text='Например, A1:E35')


class CoordinateCalculatorForm(forms.Form):
    ax = forms.FloatField(label='Point A X')
    ay = forms.FloatField(label='Point A Y')
    az = forms.FloatField(label='Point A Z')
    bx = forms.FloatField(label='Point B X')
    by = forms.FloatField(label='Point B Y')
    bz = forms.FloatField(label='Point B Z')
