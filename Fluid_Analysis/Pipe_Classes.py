#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Emerson Vargas Niño
# Date: July 2019

import numpy as np
from fluids.vectorized import *

# for a uni-diameter pipe, meaning start and end diameter are the same
# can be adjusted for when start and end diameter are NOT the same
class Pipe:
    def __init__(self, diameter_a, diameter_b, length, curve_angle, material, fluid):
        self.diameter    = np.linspace(diameter_a, diameter_b, 500) # m
        self.area        = np.pi*(self.diameter/2)**2 # m^2
        self.velocity    = fluid.mdot/(fluid.density*self.area) # m/s
        self.length      = length
        self.curve_angle = curve_angle

        if material == 'flex':
            # For a flexible pipe, the roughness shall be given by ε = ID/250.0 unless alternative specification is given.
            # https://digitalcommons.lsu.edu/cgi/viewcontent.cgi?article=2312&context=gradschool_disstheses
            self.relative_roughness = 1/250
        elif material == 'smooth':
            absolute_roughness      = 0.03/1000 # https://neutrium.net/fluid_flow/absolute-roughness/
            self.relative_roughness = absolute_roughness/self.diameter

class Pipe_FlowPath: #define your flow path here
    def __init__(self, pipe, fluid):

        if fluid.dynamic_viscosity != 0:
            self.Re = Reynolds(V=pipe.velocity, D=pipe.diameter, rho=fluid.density, mu=fluid.dynamic_viscosity)
        elif fluid.kinematic_viscosity != 0:
            self.Re = Reynolds(V=pipe.velocity, D=pipe.diameter, nu=fluid.kinematic_viscosity)

        self.darcy_friction_factor = friction_factor(self.Re, eD =pipe.relative_roughness) # f
        self.K                     = bend_rounded(angle=pipe.curve_angle, Di=pipe.diameter, fd=self.darcy_friction_factor) # loss caused by bent pipe geometry
        self.K                    += K_from_f(L=pipe.length, D=pipe.diameter, fd=self.darcy_friction_factor) # loss caused by fluid friction
        self.deltaP                = dP_from_K(self.K, rho=fluid.density, V=pipe.velocity) # calculate total resulting pressure drop
