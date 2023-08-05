# -*- coding: utf-8 -*-
# Copyright (C) 2023-- Michał Kopczyński
#
# This file is part of MiniFit.
#
# MiniFit is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# MiniFit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
"""
Module containing PolyFit class for curve fitting with polynomials.
"""
import random
import matplotlib
import numpy as np  # pylint: disable=W0611
from .fit_base import FitBase, log


matplotlib.use("Agg")


class PolyFit(FitBase):
    """
    This class makes a polynomial curve fitting.
    Order of the polynomial can be chosen.
    It reads data from a file given as the first argument.
    The data file must contain at least two columns.
    The first column represents x values,
    the second and following columns are the y values.
    """

    def __init__(self, filename, **kwargs):
        """
        **Arguments:**

        filename:
            (string) Name of the file that contains data.

        **Keyword arguments:**

        order:
            (int) Unique for PolyFit. Order of the polynomial. Optional. Default 1.

        guess:
            (tuple) A guess of the optimal parameters for the model.
            The number of guesses should match
            the arguments that the model function expects.
            For ax^2 + bx + c it expects (val1, val2, val3) etc.
            Otherwise, an exception will be raised. If not passed, a default guess adequate for
            the model function will be used.
        auto_guess:
            (bool) If true, tries to fit until chosen precision is reached. Default false.
        auto_range:
            (tuple) Sets boundaries for each parameter of the guess.
            If not set, the default range is used. Only used if auto_guess is True.
            Instead of guess = (5., 10., -3.)
            pass auto_range = ((0.,10.), (5., 15.), (-40., 30.))
            If fitting takes a lot of time, giving a better range might be helpful.
        precision:
            (float) Used by auto_guess. Default 0.4. Only used if auto_guess is True.
            If auto_guess is True and fitting takes a lot of time, lowering the precision may be
            necessary for convergence. Lowering the precision will make the fitting process faster,
            but the quality of popt may be worse.
        shift:
            (bool) If true, shifts the data. Default false.
                Data can be shifted and it may
                make the convergence of the least squares algorithm easier.
        """

        if kwargs.get("order") is None:
            log("=")
            log("Order of the polynomial wasn't given. Using default (1)")
            self.order = 1
        else:
            self.order = kwargs.get("order")
        super().__init__(filename, **kwargs)
        self.type_of_fit = "Polynomials"
        self.label_type = "polynomial_fit"

    def model_function(self, x, *args, **kwargs):
        """Depends on the module."""
        if len(args) != self.order + 1:
            raise TypeError("Wrong amount of guess parameters passed")
        val = 0.0
        # a + b*x + c*x^2 + etc.
        for exp in range(self.order + 1):
            val += args[exp] * x**exp
        return val

    def default_guess(self, context):
        """Default guess adequate for the model function."""
        guess = []
        for _ in range(self.order + 1):
            guess.append(1.0)
        return guess

    def random_guess(self, context):
        """
        Random guess adequate for the model function with constraints
        chosen by the user.
        """
        if self.auto_range is None:
            guess = []
            for _ in range(self.order + 1):
                guess.append(random.uniform(-150, 150))

        else:
            guess = [
                random.uniform(min_val, max_val)
                for min_val, max_val in self.auto_range
            ]

        return guess

    def print_info(self, popt):
        """
        Print info about popt in the format adequate for the model function.
        """
        for el in range(self.order + 1):
            log(f"\t {el}: {self.popt[el]:2.8f}")
