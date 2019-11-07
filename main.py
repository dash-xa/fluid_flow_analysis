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
                          length         = 3*foot,      # m
                          curve_angle    = 45,          # deg
                          material       = 'smooth',
                          fluid          = nitrous)

    flex_pipe = pc.Pipe(diameter_a       = 0.75*inch,     # m
                        diameter_b       = 2.5*inch,      # m
                        length           = 3*foot,        # m
                        curve_angle      = 45,            # deg
                        material         = 'flex',
                        fluid            = nitrous)

    IS_1 = 1.4 # SS-43GS4 ball valve (series 43G), Cv found on page 7 of https://drive.google.com/open?id=1dudDV-ymrLOydcFpjhFKooxjz_vgMfvv
    IS_1_D = 4.75/1000

    CV_1 = .67 # CH4 series check valve, Cv found on page 3 of https://drive.google.com/open?id=1nl7CwlfGZ0uxE3Dx-EOUgtRL-kqr0_Ph
    CV_1_D = IS_1_D # not actually correct but cannot find the orifice size in the PDF

    angles = [90]*4

    # RUN ANALYSIS
    analysis_smooth = pc.Pipe_FlowPath_liquid_study1(pipe     = smooth_pipe,
                                       fluid    = nitrous,
                                       IS_1_cv  = IS_1,
                                       IS_1_D  = IS_1_D,
                                       CV_1_cv  = CV_1,
                                       CV_1_D  = CV_1_D,
                                       bend_angles = angles)

    # analysis_flex = pc.Pipe_FlowPath(pipe       = flex_pipe,
    #                                  fluid      = nitrous)

    # RUN PLOTS
    fig, ax = plt.subplots()
    ax.plot(smooth_pipe.diameter/inch, analysis_smooth.deltaP/psi, 'k--', label='Smooth Pipe')
    # ax.plot(flex_pipe.diameter/inch, analysis_flex.deltaP/psi, 'k-', label='Flex Pipe')
    ax.set_xlabel('Diameter (inch)')
    ax.set_ylabel('Pressure Drop (psi)')
    ax.set_title('Pressure drop for differing pipe diameters')
    legend = ax.legend()

# ----------------------------------------------------------------------
#   Core
# ----------------------------------------------------------------------
if __name__ == '__main__':
    plt.close('all')
    main()
    plt.show()
