#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Emerson Vargas Niño
# Date: July 2019

import numpy as np
from fluids.vectorized import *
import matplotlib.pyplot as plt
from scipy.constants import psi, inch


# abstract class, a Part is a Component or a Pipe
class Part:
    def __init__(self, name, length, diameter):
        self.name = name
        self.length = length
        self.diameter = diameter

    def deltaP(fluid):
        pass


class Component(Part):
    def __init__(self, name, length, diameter, K):
        super().__init__(name, length, diameter)
        self.K = K

    @classmethod
    def from_Cv(cls, name, length, diameter, Cv):
        return cls(name, length, diameter, Cv_to_K(Cv, D=diameter))

    # @Override
    def deltaP(self, fluid):
        pipe_area = np.pi * (self.diameter / 2) ** 2  # m^2
        fluid_velocity = fluid.mdot / (fluid.density * pipe_area)
        return dP_from_K(self.K, rho=fluid.density, V=fluid_velocity)  # calculate total resulting pressure drop


class Pipe(Part):
    def __init__(self, length, diameter, curve_angles=[], material='smooth'):
        super().__init__('pipe', length, diameter)
        self.area = np.pi * (self.diameter / 2) ** 2  # m^2
        self.curve_angles = curve_angles

        if material == 'flex':
            # For a flexible pipe, the roughness shall be given by ε = ID/250.0 unless alternative specification is given.
            # https://digitalcommons.lsu.edu/cgi/viewcontent.cgi?article=2312&context=gradschool_disstheses
            self.relative_roughness = 1 / 250
        elif material == 'smooth':
            absolute_roughness = 0.03 / 1000  # https://neutrium.net/fluid_flow/absolute-roughness/
            self.relative_roughness = absolute_roughness / self.diameter

    # @Override
    def deltaP(self, fluid):
        self.velocity = fluid.mdot / (fluid.density * self.area)  # m/s
        if fluid.dynamic_viscosity != 0:
            self.Re = Reynolds(V=self.velocity, D=self.diameter, rho=fluid.density, mu=fluid.dynamic_viscosity)
        elif fluid.kinematic_viscosity != 0:
            self.Re = Reynolds(V=self.velocity, D=self.diameter, nu=fluid.kinematic_viscosity)
        self.darcy_friction_factor = friction_factor(self.Re, eD=self.relative_roughness)  # f

        self.K = K_from_f(L=self.length, D=self.diameter,
                          fd=self.darcy_friction_factor)  # loss caused by fluid friction
        for alpha in self.curve_angles:
            self.K += bend_rounded(angle=alpha, Di=self.diameter,
                                   fd=self.darcy_friction_factor)  # loss caused by bent pipe geometry
        return dP_from_K(self.K, rho=fluid.density, V=self.velocity)


class Geometry:
    # parts is a list of Parts
    def __init__(self, fluid, parts):
        self.parts = parts
        self.fluid = fluid
        self.drops = self.pressure_drops()
        self.cumulative_drops = list(self.accumulate(self.drops))

    # Equivalent of static constructor. Allows shorthand to create geometry by calling 
    # Geometry.from_array(fluid, [ ['pipe', length, diameter[, material='smooth', angle=[]]], 
    #                              ['component name', length, diameter, K], ... ]
    #                                                                           )
    @classmethod
    def from_data(cls, fluid, data):
        parts = []
        for arr in data:
            if arr[0] == 'pipe':
                if len(arr) < 5: arr.append('smooth', [])  # bend angles optinal param
                parts.append(Pipe(arr[1], arr[2], arr[3], arr[4]))
            else:
                parts.append(Component(arr[0], arr[1], arr[2], arr[3]))
        return cls(fluid, parts)

    # return a list of tuples [pipe_length, pressure]
    def pressure_drops(self):
        drops = [[0, 0]]
        cumulative_drops = []
        drop = 0
        length = 0
        for comp in self.parts:
            dP = comp.deltaP(self.fluid)

            drop += dP
            length += comp.length

            drops.append([length, dP])
            cumulative_drops.append([length, drop])

        return drops

    # generator used to map arr[i] to arr[0] + ... + arr[i]
    def accumulate(self, drops):
        cumulative_drop = 0
        for d in drops:
            cumulative_drop += d[1]
            yield [d[0], cumulative_drop]

    def plot(self):
        plt.close('all')

        # for now just print the values
        print("pressure drop points: ", self.cumulative_drops)
        x, y = list(map(lambda pt: pt[0] / inch, self.cumulative_drops)), list(
            map(lambda pt: pt[1] / psi, self.cumulative_drops))

        fig, ax = plt.subplots()

        ax.set_title('Pressure drop for differing pipe diameters')
        ax.set_xlabel('Length (inch)')
        ax.set_ylabel('Pressure drop (psi)')
        ax.set_title('Pressure across geometry')

        ax.plot(x, y, '-o', label='Pressure drop')
        legend = ax.legend()
        plt.show()
        # get pressure drop due to each component:
        for p in self.parts:
            print('deltaP due to ', p.name, ': ', p.deltaP(nitrogen) / psi)
