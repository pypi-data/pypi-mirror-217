#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FiberFusing.fiber_base_class import GenericFiber

micro = 1e-6


class CapillaryTube(GenericFiber):
    def __init__(self, wavelength: float,
                       radius: float,
                       position: tuple = (0, 0)) -> None:

        self.structure_dictionary = {}
        self._wavelength = wavelength
        self.position = position
        self.radius = radius
        self._index = None

    @property
    def index(self) -> float:
        if self._index is None:
            raise ValueError("Index hasn't been defined for object")
        return self._index

    @index.setter
    def index(self, value: float) -> None:
        self._index = value
        self.initialize()

    def set_delta_n(self, value: float) -> None:
        self.index = self.pure_silica_index + value

    def initialize(self):
        self.structure_dictionary = {}

        self.add_air()

        self.add_next_structure_with_index(
            name='inner-clad',
            index=self.index,
            radius=self.radius
        )


class FluorineCapillaryTube(GenericFiber):
    def __init__(self, wavelength: float,
                       radius: float,
                       delta_n: float = -15e-3,
                       position: tuple = (0, 0)):

        self.structure_dictionary = {}
        self._wavelength = wavelength
        self.position = position
        self.delta_n = delta_n
        self.radius = radius

        self.initialize()

    def initialize(self):
        self.structure_dictionary = {}

        self.add_air()

        self.add_next_structure_with_index(
            name='inner-clad',
            index=self.pure_silica_index + self.delta_n,
            radius=self.radius
        )

# -
