import Pyro4

@Pyro4.expose
class WheelMatrix(object):
    __forwards = 0
    __backwards = 1
    _matrix = [0,0]

    def __init__(self, f, b):
        self._matrix = [0,0]
        self.forwards = f
        self.backwards = b

    @property
    def forwards(self):
        return self._matrix[self.__forwards]

    @forwards.setter
    def forwards(self, value):
        self.__set_wheel(value, self.__forwards)

    @property
    def backwards(self):
        return self._matrix[self.__backwards]

    @backwards.setter
    def backwards(self, value):
        self.__set_wheel(value, self.__backwards)

    def __set_wheel(self,value,index):
        assert type(value) is int
        assert value >= 0
        assert value <= 100
        self._matrix[index] = value

@Pyro4.expose
class WheelsMatrix(object):

    _leftWheelIndex = 0
    _rightWheelIndex = 1
    _matrix = [[0,0],[0,0]]

    def __init__(self, rf,rb,lf,lb):
        self._matrix = [[0,0],[0,0]]
        self.left_wheel = WheelMatrix(lf,lb)
        self.right_wheel = WheelMatrix(rf,rb)

    def __str__(self):
        return "<WheelsMatrix [[{0},{1}],[{2},{3}]]>".format(self.left_wheel.forwards,
                                                            self.left_wheel.backwards,
                                                            self.right_wheel.forwards,
                                                            self.right_wheel.backwards)

    def __repr__(self):
        return self.__str__()

    @property
    def left_wheel(self):
        return self._matrix[self._leftWheelIndex]

    @left_wheel.setter
    def left_wheel(self,value):
        self.__set_wheel(value, self._leftWheelIndex)

    @property
    def right_wheel(self):
        return self._matrix[self._rightWheelIndex]

    @right_wheel.setter
    def right_wheel(self, value):
        self.__set_wheel(value,self._rightWheelIndex)

    def __set_wheel(self,value,index):
        if type(value) is not WheelMatrix:
            assert type(value) is list
            assert len(value) == 2
            value = WheelMatrix(*value)
        self._matrix[index] = value
