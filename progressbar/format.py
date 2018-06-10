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

    def percentage(self):
        return self.dividend / self.divisor * 100

    def svg(self):
        assert self.template, 'SVG template must be set.'
        file_path = os.path.join(SVG_PATH, self.template)
        with open(file_path) as svg_file:
            svg = svg_file.read()
            return svg.format(**self._svg_parameters())

    def text(self):
        text_format = '{}%' if self.divisor == 100 else '{}/{}'
        return text_format.format(self.dividend, self.divisor)

    def _svg_parameters(self):
        return {
            'text': self.text(),
            'width': self.percentage()
        }

    @staticmethod
    def create(dividend, divisor, theme):
        """Create and return a Format for the given theme"""

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


# FORMATS #####################################################################

class GradientFormat(Format):
    """A base format for progress bars with a gradient"""

    def __init__(self, dividend, divisor):
        super().__init__(dividend, divisor)
        self.template = 'progress_gradient.svg'

    def _colors(self):
        raise NotImplementedError('')

    def _svg_parameters(self):
        params = self._colors()
        params['text_alignment'] = self.__text_alignment()

        return {**params, **super()._svg_parameters()}

    def __text_alignment(self):
        percentage = self.percentage()
        if percentage < 5:
            return 'start'
        elif percentage > 95:
            return 'end'
        return 'middle'


class DefaultFormat(GradientFormat):
    """The default format"""

    def __init__(self, dividend, divisor):
        super().__init__(dividend, divisor)

    def _colors(self):
        return {
            'start_color': '#165bc4',
            'end_color': '#12499e'
        }


class CustomColorFormat(GradientFormat):
    """A format that allows the usage of a custom base color"""

    def __init__(self, dividend, divisor, color):
        super().__init__(dividend, divisor)
        self.color = color

    def _colors(self):
        return {
            'start_color': '#{}'.format(self.color),  # TODO
            'end_color': '#{}'.format(self.color)
        }


class MinimalFormat(Format):
    """A format for minimal progress bars without any text or extras"""

    def __init__(self, dividend, divisor):
        super().__init__(dividend, divisor)
        self.template = 'progress_minimal.svg'


class BadgeFormat(Format):
    """A format for .svgs that look similar to the badges by shields.io"""

    def __init__(self, dividend, divisor):
        super().__init__(dividend, divisor)
        self.template = 'progress_badge.svg'

    def _svg_parameters(self):
        params = super()._svg_parameters()
        params['color'] = self.__color()
        return params

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
