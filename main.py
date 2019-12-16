#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Authors: Emerson Vargas Niño, Alex Shevchuk
# Date: July 2019

# ------------------------------------------------------------------------------
#   Imports
# ------------------------------------------------------------------------------
import Fluid_Analysis.Fluid_Classes as fc
import Fluid_Analysis.Pipe_Classes as pc
from scipy.constants import foot, psi, inch
import matplotlib.pyplot as plt


# ------------------------------------------------------------------------------
#   Main
# ------------------------------------------------------------------------------

# Sample geometry 1
def get_test_geometry1():
    # pipes
    pipe = pc.Pipe(length=.3, diameter=.25 * inch)

    # components
    IS_1 = pc.Component.from_Cv(name='IS_1', length=0, diameter=4.75 / 1000, Cv=1.4)
    CV_1 = pc.Component.from_Cv(name='CV_1', length=10, diameter=4.75 / 1000, Cv=.67)

    # fluid
    fluid = fc.N2(pressure=40 * 10000, mass_fraction=0, mdot=54 / 1000)  # data copied from last version

    parts = [pipe, IS_1, CV_1]
    return pc.Geometry(fluid, parts)


def main():
    geometry_1 = get_test_geometry1()
    geometry_1.plot()


# ----------------------------------------------------------------------
#   Core
# ----------------------------------------------------------------------
if __name__ == '__main__':
    main()

# Ignore what is below

# SAMPLE GEOMETRY

# # sample geometry #1
# m = 20 # pipe length allotted to fittings, mm
# is_length = 60.7 # Isolation valve, mm
# cv_length = 61.7 # Check valve, mm
# pipe_length = 10*m + 2*(is_length + cv_length) # mm

# # SS-43GS4 ball valve (series 43G), Cv found on page 7 of https://drive.google.com/open?id=1dudDV-ymrLOydcFpjhFKooxjz_vgMfvv
# IS_1 = 1.4
# IS_1_D = 4.75/1000

# # CH4 series check valve, Cv found on page 3 of https://drive.google.com/open?id=1nl7CwlfGZ0uxE3Dx-EOUgtRL-kqr0_Ph
# CV_1 = .67 
# CV_1_D = IS_1_D # not actually correct but cannot find the orifice size in the PDF
# # TODO: get orifice size from CAD doc of check valve 

# Get data from graph
#   ax = plt.gca()
#  line = ax.lines[0]
# x, y = line.get_xdata(), line.get_ydata()


# DEFINE FLUIDS
# nitrogen = fc.Fluid_Definition(fluid                 = 'Nitrogen',
#                                 pressure              = 40*10000,      # TODO: Get nitrogen tank pressure, Pa
#                                   mass_fraction         = 0,            # 0 is liquid
#                                   mdot                  = 54/1000,            # TODO: Get mass flow of nitrogen kg/s
#                                   dynamic_viscosity     = 0,            # Pa*s
#                                   kinematic_viscosity   = 0)            # m^2/s

# Sample geometry 1: straight pipe
# parts = [ ['pipe', pipe_length, .25*inch, 'smooth', 0],
#                 ['component_name', pipe_length, .25*inch, .25]]
# geometry_1 = pc.Geometry.from_data(nitrogen, parts)
