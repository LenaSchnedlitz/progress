""""""

import os

__all__ = ['Format']

SVG_PATH = os.path.join('static', 'svg', 'progress.svg')


class Format:
    def __init__(self, dividend, divisor, palette):
        self.__validate(dividend, divisor, palette)
        self.dividend = dividend
        self.divisor = divisor
        self.palette = palette

    def percentage(self):
        return self.dividend / self.divisor * 100

    def svg(self):
        with open(SVG_PATH) as svg_file:
            svg = svg_file.read()
            return svg.format(*self.__svg_parameters())

    def __svg_parameters(self):
        return self.percentage(), '{}/{}'.format(self.dividend, self.divisor)

    @staticmethod
    def __validate(dividend, divisor, palette):
        if not (0 <= dividend < divisor):
            raise ValueError('Invalid dividend.')
        if not (0 < divisor):
            raise ValueError('Invalid divisor.')
