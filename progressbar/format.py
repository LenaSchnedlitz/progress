""""""

import os
import re

__all__ = ['Format']

HEX_COLOR_REGEX = re.compile('^[0-9a-f]{3}([0-9a-f]{3})?$')
SVG_PATH = os.path.join('static', 'svg')


class Format:
    def __init__(self, dividend, divisor):
        self.__validate(dividend, divisor)
        self.dividend = dividend
        self.divisor = divisor
        self.template = None
        self._svg_parameters = {
            'width': self.percentage(),
            'text': self.text()
        }

    def percentage(self):
        return self.dividend / self.divisor * 100

    def svg(self):
        file_path = os.path.join(SVG_PATH, self.template)
        with open(file_path) as svg_file:
            svg = svg_file.read()
            return svg.format(**self._svg_parameters)

    def text(self):
        text_format = '{}%' if self.divisor == 100 else '{}/{}'
        return text_format.format(self.dividend, self.divisor)

    @staticmethod
    def create(dividend, divisor, theme):
        Format.__validate(dividend, divisor)
        theme = theme.lower()
        try:
            return {
                'default': DefaultFormat,
                'minimal': MinimalFormat,
                'badge': BadgeFormat
            }[theme](dividend, divisor)
        except KeyError:
            if re.match(HEX_COLOR_REGEX, theme):
                return CustomColorFormat(dividend, divisor, theme)
            else:
                raise ValueError('Unknown theme.')

    @staticmethod
    def __validate(dividend, divisor):
        if not (0 <= dividend <= divisor):
            raise ValueError('Invalid dividend.')
        if not (0 < divisor):
            raise ValueError('Invalid divisor.')


class DefaultFormat(Format):
    def __init__(self, dividend, divisor):
        super().__init__(dividend, divisor)
        self.template = 'progress_default.svg'
        self._svg_parameters = self.__svg_parameters()

    def _colors(self):
        return {
            'start_color': '#165bc4',
            'end_color': '#12499e'
        }

    def __svg_parameters(self):
        params = self._colors()
        params['text_alignment'] = self.__text_alignment()

        return {**params, **self._svg_parameters}

    def __text_alignment(self):
        percentage = self.percentage()
        if percentage < 5:
            return 'start'
        elif percentage > 95:
            return 'end'
        return 'middle'


class CustomColorFormat(DefaultFormat):
    def __init__(self, dividend, divisor, color):
        super().__init__(dividend, divisor)
        self.color = color

    def _colors(self):
        return {
            'start_color': '#{}'.format(self.color),  # TODO
            'end_color': '#{}'.format(self.color)
        }


class MinimalFormat(Format):
    def __init__(self, dividend, divisor):
        super().__init__(dividend, divisor)
        self.template = 'progress_minimal.svg'


class BadgeFormat(Format):
    def __init__(self, dividend, divisor):
        super().__init__(dividend, divisor)
        self.template = 'progress_badge.svg'
        self._svg_parameters['color'] = self.__color()

    def __color(self):
        # Colors taken from shields.io
        percentage = self.percentage()
        if percentage <= 20:
            return '#e05d44'
        if percentage <= 35:
            return '#fe7d37'
        if percentage <= 50:
            return '#dfb317'
        if percentage <= 65:
            return '#a4a61d'
        if percentage <= 80:
            return '#97ca00'
        if percentage <= 100:
            return '#44cc11'
        return '#9f9f9f'
