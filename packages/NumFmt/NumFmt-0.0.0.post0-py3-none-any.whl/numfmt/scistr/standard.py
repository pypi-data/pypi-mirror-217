import typing as _tp
from . import ieee754
from . import calc as ss_math


def floatstr(float_setup: ieee754.FloatSetup = ieee754.FLOAT32_SETUP):

	def f(base: int, x: float, figures=6) -> str:
		digs = ss_math.sci_digits(base, figures)(*ss_math.frac_sci(base)(*ieee754.float_frac(float_setup)(x)))
		# print(digs)
		s = ss_math.sci_str()(*digs)
		return s

	return f
