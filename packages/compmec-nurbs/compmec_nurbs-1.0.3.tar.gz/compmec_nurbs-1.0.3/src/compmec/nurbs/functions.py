import abc
from typing import Any, Optional, Tuple, Union

import numpy as np

from compmec.nurbs.__classes__ import Intface_BaseFunction, Intface_Evaluator
from compmec.nurbs.algorithms import N, R
from compmec.nurbs.knotspace import KnotVector


class BaseFunction(Intface_BaseFunction):
    def __init__(self, knotvector: KnotVector):
        self.__U = KnotVector(knotvector)

    @property
    def degree(self) -> int:
        return self.__U.degree

    @property
    def npts(self) -> int:
        return self.__U.npts

    @property
    def knotvector(self) -> KnotVector:
        return self.__U

    @property
    def knots(self) -> Tuple[float]:
        return self.__U.knots

    def knot_insert(self, knot: float, times: Optional[int] = 1):
        self.knotvector.knot_insert(knot, times)

    def knot_remove(self, knot: float, times: Optional[int] = 1):
        self.knotvector.knot_remove(knot, times)


class BaseEvaluator(Intface_Evaluator):
    def __init__(self, F: BaseFunction, i: Union[int, slice], j: int):
        self.__U = F.knotvector
        self.__first_index = i
        self.__second_index = j
        self.__A = F.A

    @property
    def knotvector(self) -> KnotVector:
        return self.__U

    @property
    def first_index(self) -> Union[int, range]:
        return self.__first_index

    @property
    def second_index(self) -> int:
        return self.__second_index

    @abc.abstractmethod
    def compute_one_value(self, i: int, u: float, span: int) -> float:
        raise NotImplementedError

    def compute_vector(self, u: float, span: int) -> np.ndarray:
        """
        Given a 'u' float, it returns the vector with all BasicFunctions:
        compute_vector(u, span) = [F_{0j}(u), F_{1j}(u), ..., F_{npts-1,j}(u)]
        """
        result = np.zeros(self.__U.npts, dtype="float64")
        # for i in range(span, span+self.second_index):
        for i in range(self.__U.npts):
            result[i] = self.compute_one_value(i, u, span)
        return result

    def compute_all(
        self, u: Union[float, np.ndarray], span: Union[int, np.ndarray]
    ) -> np.ndarray:
        u = np.array(u, dtype="float64")
        if span.ndim == 0:
            return self.compute_vector(float(u), int(span))
        result = np.zeros([self.__U.npts] + list(u.shape))
        for k, (uk, sk) in enumerate(zip(u, span)):
            result[:, k] = self.compute_all(uk, sk)
        return result

    def evalf(self, u: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        If i is integer, u is float -> float
        If i is integer, u is np.ndarray, ndim = k -> np.ndarray, ndim = k
        If i is slice, u is float -> 1D np.ndarray
        if i is slice, u is np.ndarray, ndim = k -> np.ndarray, ndim = k+1
        """
        u = np.array(u, dtype="float64")
        span = self.__U.span(u)
        span = np.array(span, dtype="int16")
        return self.compute_all(u, span)

    def __call__(self, u: np.ndarray) -> np.ndarray:
        result = self.evalf(u)
        result = self.__A @ result
        return result[self.first_index]


class SplineEvaluatorClass(BaseEvaluator):
    def __init__(self, F: BaseFunction, i: Union[int, slice], j: int):
        super().__init__(F, i, j)

    def compute_one_value(self, i: int, u: float, span: int) -> float:
        return N(i, self.second_index, span, u, self.knotvector)


class RationalEvaluatorClass(BaseEvaluator):
    def __init__(self, F: BaseFunction, i: Union[int, slice], j: int):
        super().__init__(F, i, j)
        self.__weights = F.weights

    def compute_one_value(self, i: int, u: float, span: int) -> float:
        j = self.second_index
        U = self.knotvector
        w = self.__weights
        return R(i, j, span, u, U, w)


class BaseFunctionDerivable(BaseFunction):
    def __init__(self, knotvector: KnotVector):
        super().__init__(knotvector)
        self.__q = self.degree
        self.__A = np.eye(self.npts, dtype="float64")

    @property
    def q(self) -> int:
        return self.__q

    @property
    def A(self) -> np.ndarray:
        return np.copy(self.__A)

    def derivate(self):
        avals = np.zeros(self.npts)
        for i in range(self.npts):
            diff = (
                self.knotvector[i + self.degree] - self.knotvector[i]
            )  # Maybe it's wrong
            if diff != 0:
                avals[i] = self.degree / diff
        newA = np.diag(avals)
        for i in range(self.npts - 1):
            newA[i, i + 1] = -avals[i + 1]
        self.__A = self.__A @ newA
        self.__q -= 1


class BaseFunctionGetItem(BaseFunctionDerivable):
    def __init__(self, knotvector: KnotVector):
        super().__init__(knotvector)

    def __valid_first_index(self, index: Union[int, slice]):
        if not isinstance(index, (int, slice)):
            raise TypeError
        if isinstance(index, int):
            if not (-self.npts <= index < self.npts):
                raise IndexError

    def __valid_second_index(self, index: int):
        if not isinstance(index, int):
            raise TypeError
        if not (0 <= index <= self.degree):
            error_msg = f"Second index (={index}) "
            error_msg += f"must be in [0, {self.degree}]"
            raise IndexError(error_msg)

    @abc.abstractmethod
    def create_evaluator_instance(self, i: Union[int, slice], j: int):
        raise NotImplementedError

    def __getitem__(self, tup: Any):
        if isinstance(tup, tuple):
            if len(tup) > 2:
                raise IndexError
            i, j = tup
        else:
            i, j = tup, self.q
        self.__valid_first_index(i)
        self.__valid_second_index(j)
        return self.create_evaluator_instance(i, j)

    def __call__(self, u: np.ndarray) -> np.ndarray:
        i, j = slice(None, None, None), self.degree
        evaluator = self.create_evaluator_instance(i, j)
        return evaluator(u)

    def __eq__(self, obj: object) -> bool:
        if type(self) != type(obj):
            raise TypeError
        if self.knotvector != obj.knotvector:
            return False
        if self.q != obj.q:
            return False
        return True


class SplineFunction(BaseFunctionGetItem):
    def __doc__(self):
        """
        This function is recursively determined like

        N_{i, 0}(u) = { 1   if  knotvector[i] <= u < knotvector[i+1]
                      { 0   else

                          u - knotvector[i]
        N_{i, j}(u) = --------------- * N_{i, j-1}(u)
                       knotvector[i+j] - knotvector[i]
                            knotvector[i+j+1] - u
                      + ------------------- * N_{i+1, j-1}(u)
                         knotvector[i+j+1] - knotvector[i+1]

        As consequence, we have that

        N_{i, j}(u) = 0   if  ( u not in [knotvector[i], knotvector[i+j+1]] )

        """

    def __init__(self, knotvector: KnotVector):
        super().__init__(knotvector)

    def create_evaluator_instance(self, i: Union[int, slice], j: int):
        return SplineEvaluatorClass(self, i, j)


class RationalFunction(BaseFunctionGetItem):
    def __init__(self, knotvector: KnotVector):
        super().__init__(knotvector)

    def create_evaluator_instance(self, i: Union[int, slice], j: int):
        return RationalEvaluatorClass(self, i, j)

    def __eq__(self, obj):
        if not super().__eq__(obj):
            return False
        if np.any(self.weights != obj.weights):
            return False
        return True

    @property
    def weights(self):
        try:
            return self.__weights
        except AttributeError:
            self.__weights = np.ones(self.npts, dtype="float64")
        return self.__weights

    @weights.setter
    def weights(self, value: Tuple[float]):
        value = np.array(value, dtype="float64")
        if value.ndim != 1:
            raise ValueError("Input must be 1D array")
        if len(value) != self.npts:
            error_msg = "Lenght of weights must be equal to knotvector.npts"
            raise ValueError(error_msg)
        if np.any(value <= 0):
            raise ValueError("All the weights must be positive")
        self.__weights = value
