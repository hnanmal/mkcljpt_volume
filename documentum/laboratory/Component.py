
from dataclasses import dataclass
from typing import List

@dataclass
class Position:
    x: float = 0
    y: float = 0
    z: float = 0

    def __add__(self, pos):
        return Position(self.x + pos.x, self.y + pos.y, self.z + pos.z)

    def __iadd__(self, pos):
        self.x += pos.x
        self.y += pos.y
        self.z += pos.z
        return self


class Component:
    def __init__(self, name: str, pos: Position):
        self._name: str = name
        self._position: Position = pos

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: Position):
        self._name = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: Position):
        self._position = value

    def get_composite(self):
        raise NotImplementedError

    def move(self, delta: Position):
        raise NotImplementedError

    def scale(self, factor: float):
        raise NotImplementedError

class Composite(Component):
    def __init__(self, name: str, pos: Position):
        super().__init__(name, pos)
        self._leafs: List[Component] = []

    def get_composite(self):
        return self

    def move(self, delta: Position):
        for leaf in self._leafs:
            leaf.move(delta)

    def scale(self, factor: float):
        for leaf in self._leafs:
            leaf.scale(factor)

    def add_component(self, comp: Component):
        self._leafs.append(comp)

    def remove_component(self, comp: Component):
        self._leafs.remove(comp)

    def get_childs(self) -> List[Component]:
        return self._leafs

class Leaf(Component):
    def __init__(self, name: str, pos: Position):
        super().__init__(name, pos)

    def get_composite(self):
        return None

    def move(self, delta: Position):
        self.position += delta
        print(f"{self.name} move {self.position}")

    def scale(self, factor: float):
        print(f"{self.name} scale : {factor}")
