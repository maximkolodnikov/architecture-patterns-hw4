class Vector(list):
    """Класс реализации вектора."""

    def __add__(self, other: 'Vector') -> 'Vector':
        if len(self) != len(other):
            raise ValueError('Vectors lengths do not match')

        _vector = [self[i] + other[i] for i in range(len(self))]
        return Vector(_vector)

    def __radd__(self, other) -> 'Vector':
        if len(self) != len(other):
            raise ValueError('Objects lengths do not match')

        _vector = [self[i] + other[i] for i in range(len(self))]
        return Vector(_vector)
