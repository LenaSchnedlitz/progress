""""""

import os

__all__ = ['Format']

SVG_PATH = os.path.join('static', 'svg', 'progress_default.svg')


class Format:
    def __init__(self, dividend, divisor, palette):
        self.__validate(dividend, divisor)
        self.dividend = dividend
        self.divisor = divisor
        self.palette = palette

    def percentage(self):
        return self.dividend / self.divisor * 100

    def svg(self):
        with open(SVG_PATH) as svg_file:
            svg = svg_file.read()
            return svg.format(**self.__svg_parameters())

    def text(self):
        text_format = '{}%' if self.divisor == 100 else '{}/{}'
        return text_format.format(self.dividend, self.divisor)

    def __svg_parameters(self):
        percentage = self.percentage()
        text_alignment = self.__text_alignment(percentage)
        text = self.text()

        return {
            'width': percentage,
            'text_alignment': text_alignment,
            'text': text,
            'start_color': '#165bc4',
            'end_color': '#12499e'
        }

    @staticmethod
    def __text_alignment(percentage):
        if percentage <= 5:
            return 'start'
        elif percentage >= 95:
            return 'end'
        return 'middle'

    @staticmethod
    def __validate(dividend, divisor):
        if not (0 <= dividend <= divisor):
            raise ValueError('Invalid dividend.')
        if not (0 < divisor):
            raise ValueError('Invalid divisor.')
