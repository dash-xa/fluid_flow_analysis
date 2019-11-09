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

# sample geometries

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
    nitrous = fc.Fluid_Definition(fluid                 = 'N2O',
                                  pressure              = 700*psi,      # Pa
                                  mass_fraction         = 0,            # 0 is liquid
                                  mdot                  = 4,            # kg/s
                                  dynamic_viscosity     = 0,            # Pa*s
                                  kinematic_viscosity   = 0)            # m^2/s

    # DEFINE PIPES
    smooth_pipe = pc.Pipe(diameter_a     = 0.75*inch,   # m
                          diameter_b     = 2.5*inch,    # m
                          length         = pipe_length/1000,      # m
                          curve_angle    = 45,          # deg
                          material       = 'smooth',
                          fluid          = nitrous)



    # RUN ANALYSIS
    analysis_smooth = pc.Pipe_FlowPath_liquid_study1(pipe     = smooth_pipe,
                                       fluid    = nitrous,
                                       IS_1_cv  = IS_1,
                                       IS_1_D  = IS_1_D,
                                       CV_1_cv  = CV_1,
                                       CV_1_D  = CV_1_D,
                                       bend_angles = angles)

    # RUN PLOTS
    fig, ax = plt.subplots()
    ax.plot(smooth_pipe.diameter/inch, analysis_smooth.deltaP/psi, 'k--', label='Smooth Pipe')
    ax.set_xlabel('Diameter (inch)')
    ax.set_ylabel('Pressure Drop (psi)')
    ax.set_title('Pressure drop for differing pipe diameters')
    plt.xlim(0.1,2.5)
    legend = ax.legend()

# ----------------------------------------------------------------------
#   Core
# ----------------------------------------------------------------------
if __name__ == '__main__':
    plt.close('all')
    main()
    plt.show()
