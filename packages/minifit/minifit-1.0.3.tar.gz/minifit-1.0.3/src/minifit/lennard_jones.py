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
Module containing LennardJonesFit class for curve fitting with Lennard-Jones.
"""

import random
import numpy as np  # pylint: disable=W0611
import matplotlib
from .fit_base import FitBase, log

matplotlib.use("Agg")


class LennardJonesFit(FitBase):
    """
    This class makes curve fitting using the Lennard-Jones potential formula.
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

        super().__init__(filename, **kwargs)
        self.type_of_fit = "Lennard-Jones potential"
        self.label_type = "lennard_jones_fit"

    def model_function(self, x, *args, **kwargs):
        """Depends on the module."""
        r = x
        if len(args) != 2:
            raise TypeError("Wrong amount of guess parameters passed")
        sigma, epsilon = args
        return 4 * epsilon * ((sigma / r) ** 12 - (sigma / r) ** 6)

    def default_guess(self, context):
        """Default guess adequate for the model function."""
        guess = [1, 1]

        return guess

    def random_guess(self, context):
        """
        Random guess adequate for the model function with constraints
        chosen by the user.
        """
        if self.auto_range is None:

            guess = [random.uniform(-60, 60), random.uniform(-60, 60)]
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
        name_temp = ("sigma", "epsilon")
        for el in range(2):
            log(f"\t {name_temp[el]}: {popt[el]:2.8f}")
