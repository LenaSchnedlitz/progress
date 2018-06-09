""""""

import os
import re

__all__ = ['Format']

SVG_PATH = os.path.join('static', 'svg')
HEX_COLOR_RE = re.compile('^[0-9a-fA-F]{3}([0-9a-fA-F]{3})?$')


class Format:
    def __init__(self, dividend, divisor, theme):
        self.__validate(dividend, divisor)
        self.dividend = dividend
        self.divisor = divisor
        self.theme = theme

    def percentage(self):
        return self.dividend / self.divisor * 100

    def svg(self):
        file_path = os.path.join(SVG_PATH, self.__template())
        with open(file_path) as svg_file:
            svg = svg_file.read()
            return svg.format(**self.__svg_parameters())

    def text(self):
        text_format = '{}%' if self.divisor == 100 else '{}/{}'
        return text_format.format(self.dividend, self.divisor)

    def __svg_parameters(self):
        start_color, end_color = self.__colors()
        return {
            'width': self.percentage(),
            'text_alignment': self.__text_alignment(),
            'text': self.text(),
            'start_color': start_color,
            'end_color': end_color
        }

    # HELPERS

    def __colors(self):
        if re.match(HEX_COLOR_RE, self.theme):
            color = '#{}'.format(self.theme)
            return color, color
        return '#165bc4', '#12499e'

    def __template(self):
        return {
            'default': 'progress_default.svg',
            'minimal': 'progress_minimal.svg'
        }.get(self.theme, 'progress_default.svg')

    def __text_alignment(self):
        percentage = self.percentage()
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
