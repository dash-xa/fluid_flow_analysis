#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Emerson Vargas Niño
# Date: July 2019

import numpy as np
from CoolProp.CoolProp import PropsSI


##TODO: Add units of measurement for each variable
class Fluid:
    def __init__(self, fluid_name, pressure, mass_fraction, mdot, dynamic_viscosity=0, kinematic_viscosity=0):
        self.mdot = mdot
        self.T = PropsSI('T', 'P', pressure, 'Q', mass_fraction, fluid_name)
        self.density = PropsSI('D', 'P', pressure, 'Q', mass_fraction, fluid_name)

        self.dynamic_viscosity = dynamic_viscosity  # mu, Dynamic viscosity, Pa*s
        self.kinematic_viscosity = kinematic_viscosity  # nu, Kinematic viscosity, m^2/s


class N2(Fluid):
    def __init__(self, pressure, mass_fraction, mdot, dynamic_viscosity=0, kinematic_viscosity=0):
        super().__init__("Nitrogen", pressure, mass_fraction, mdot, dynamic_viscosity, kinematic_viscosity)
        self.dynamic_viscosity = PropsSI('VISCOSITY', 'P', pressure, 'Q', mass_fraction,
                                         "Nitrogen")  # mu, Dynamic viscosity, Pa*s
        ##TODO: set kinematic viscosity


##TODO: get parameters for EtOH
class EtOH(Fluid):
    def __init__(self, pressure, mass_fraction, mdot, dynamic_viscosity=0, kinematic_viscosity=0):
        super().__init("Ethanol", pressure, mass_fraction, mdot, dynamic_viscosity, kinematic_viscosity)
        self.dynamic_viscosity = PropsSI('VISCOSITY', 'P', pressure, 'Q', mass_fraction,
                                         "Ethanol")  # mu, Dynamic viscosity, Pa*s


class N2O(Fluid):
    Tc_N2O = 309.57  # Critical Temperature, K

    def __init__(self, pressure, mass_fraction, mdot, dynamic_viscosity=0, kinematic_viscosity=0):
        super().__init__("Nitrogen", pressure, mass_fraction, mdot, dynamic_viscosity, kinematic_viscosity)
        if kinematic_viscosity == 0 and dynamic_viscosity == 0:
            if mass_fraction == 0:
                self.dynamic_viscosity = self.dynamicViscosity_saturatedLiquid_N2O(self.T)
            elif mass_fraction == 1:
                self.dynamic_viscosity = self.dynamicViscosity_saturatedVapour_N2O(self.T)
            else:
                'Not implemented yet'

    # Kinematic Viscosity, or Dynamic Viscosity and density
    # nu, or mu and rho
    # Dynamic Viscosity - η/μ - eta/mu - N s/m2
    # Kinematic Viscosity - ν - nu - N s/m2
    # REF: http://edge.rit.edu/edge/P07106/public/Nox.pdf
    def dynamicViscosity_saturatedLiquid_N2O(self, T):  # T in K
        # page 17
        # Dynamic Viscosity of the Saturated Liquid - η/μ(l) - eta/mu - N s/m2
        # -90 to 30 C
        b1 = 1.6089
        b2 = 2.0439
        b3 = 5.24
        b4 = 0.0293423
        theta = (self.Tc_N2O - b3) / (T - b3)
        eta_l = b4 * np.exp(b1 * (theta - 1) ** (1 / 3) + b2 * (theta - 1) ** (4 / 3))  # mN*s/m^2
        eta_l = eta_l / 1e3  # N*s/m^2 = Pa*s
        return eta_l

    def dynamicViscosity_saturatedVapour_N2O(self, T):
        # page 17
        # Dynamic Viscosity of the Saturated Vapour - η/μ(g)
        # -90 to 30 C
        b1 = 3.3281
        b2 = -1.18237
        b3 = -0.055155
        Tr = T / self.Tc_N2O
        eta_g = np.exp(b1 + b2 * ((1 / Tr) - 1) ** (1 / 3) + b3 * ((1 / Tr) - 1) ** (4 / 3))  # µN*s/m^2
        eta_g = eta_g / 1e6  # N*s/m^2 = Pa*s
        return eta_g

    def dynamicViscosity_diluteGas_N2O(self, T):
        # page 19
        # Dynamic Viscosity of the Dilute Gas - η/μ(ο)(g)
        # -90 to 727 C
        b1 = -0.955565
        b2 = 18.8315
        b3 = -2.34589
        b4 = 0.164927
        Tr = T / self.Tc_N2O
        eta_og = b1 + b2 * Tr + b3 * Tr ** 2 + b4 * Tr ** 3  # µN*s/m^2
        eta_og = eta_og / 1e6  # N*s/m^2 = Pa*s
        return eta_og
