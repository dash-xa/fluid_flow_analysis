#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Emerson Vargas Niño
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

# SAMPLE GEOMETRY

# sample geometry #1
m = 20 # pipe length allotted to fittings, mm
is_length = 60.7 # Isolation valve, mm
cv_length = 61.7 # Check valve, mm
pipe_length = 10*m + 2*(is_length + cv_length) # mm

# SS-43GS4 ball valve (series 43G), Cv found on page 7 of https://drive.google.com/open?id=1dudDV-ymrLOydcFpjhFKooxjz_vgMfvv
IS_1 = 1.4
IS_1_D = 4.75/1000

# CH4 series check valve, Cv found on page 3 of https://drive.google.com/open?id=1nl7CwlfGZ0uxE3Dx-EOUgtRL-kqr0_Ph
CV_1 = .67 
CV_1_D = IS_1_D # not actually correct but cannot find the orifice size in the PDF
# TODO: get orifice size from CAD doc of check valve 

angles = [90]*4


def main():
    # DEFINE FLUIDS
    nitrogen = fc.Fluid_Definition(fluid                 = 'Nitrogen',
                                    pressure              = 40*10000,      # TODO: Get nitrogen tank pressure, Pa
                                      mass_fraction         = 0,            # 0 is liquid
                                      mdot                  = 54/1000,            # TODO: Get mass flow of nitrogen kg/s
                                      dynamic_viscosity     = 0,            # Pa*s
                                      kinematic_viscosity   = 0)            # m^2/s

    # DEFINE PIPES
    smooth_pipe = pc.Pipe(diameter_a     = 0.05*inch,   # m
                          diameter_b     = 2.5*inch,    # m
                          length         = .3,      # m
                          curve_angle    = 45,          # deg
                          material       = 'smooth',
                          fluid          = nitrogen)



    # RUN ANALYSIS
    analysis_smooth = pc.Pipe_FlowPath_liquid_study1(pipe     = smooth_pipe,
                                       fluid    = nitrogen,
                                       IS_1_cv  = IS_1,
                                       IS_1_D  = IS_1_D,
                                       CV_1_cv  = CV_1,
                                       CV_1_D  = CV_1_D,
                                       bend_angles = angles)

    analysis_smooth_og = pc.Pipe_FlowPath(pipe     = smooth_pipe,
                                       fluid    = nitrogen,
                                       )
    # RUN PLOTS
    fig, ax = plt.subplots()
    ax.plot(smooth_pipe.diameter/inch, analysis_smooth.deltaP/psi, 'k-', label='Smooth Pipe')
    #ax.plot(smooth_pipe.diameter/inch, analysis_smooth_og.deltaP/psi, 'k--', label='og Smooth Pipe')    
    ax.set_xlabel('Diameter (inch)')
    ax.set_ylabel('Pressure Drop (psi)')
    ax.set_title('Pressure drop for differing pipe diameters')
    plt.xlim(0,2.5)
    plt.ylim(0,200)
    legend = ax.legend()

# Get data from graph
    ax = plt.gca()
    line = ax.lines[0]
    x, y = line.get_xdata(), line.get_ydata()

# ----------------------------------------------------------------------
#   Core
# ----------------------------------------------------------------------
if __name__ == '__main__':
    plt.close('all')
    main()
    plt.show()
