"""Module with coordinate system transformation classes and functions."""
from typing import Tuple

import numpy as np


class CoordinateMapper2D:
    """Maps points in cartesian coordinates."""

    def __init__(
        self,
        src_dim_x: Tuple[int, int],
        src_dim_y: Tuple[int, int],
        dst_dim_x: Tuple[int, int],
        dst_dim_y: Tuple[int, int],
    ) -> None:
        self._src_dim = src_dim_x, src_dim_y
        self._dst_dim = dst_dim_x, dst_dim_y
        self._scale_matrix = self._calc_scale_matrix()

    @property
    def src_dim(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        return self._src_dim

    @src_dim.setter
    def src_dim(self, src_dim: Tuple[Tuple[int, int], Tuple[int, int]]) -> None:
        self._src_dim = src_dim
        self._scale_matrix = self._calc_scale_matrix()

    @property
    def dst_dim(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        return self._dst_dim

    @dst_dim.setter
    def dst_dim(self, dst_dim: Tuple[Tuple[int, int], Tuple[int, int]]) -> None:
        self._dst_dim = dst_dim
        self._scale_matrix = self._calc_scale_matrix()

    def map_coordinates(self, pos_sim: np.ndarray) -> np.ndarray:
        return np.matmul(pos_sim, self._scale_matrix)

    def _calc_scale_matrix(self) -> np.ndarray:
        src_dim_x, src_dim_y = self._src_dim
        dst_dim_x, dst_dim_y = self._dst_dim
        src_range_x = abs(src_dim_x[0] - src_dim_x[1])
        src_range_y = abs(src_dim_y[0] - src_dim_y[1])
        dst_range_x = abs(dst_dim_x[0] - dst_dim_x[1])
        dst_range_y = abs(dst_dim_y[0] - dst_dim_y[1])
        factor_width = dst_range_x / src_range_x
        factor_height = dst_range_y / src_range_y
        return np.asarray([[factor_width, 0], [0, factor_height]])
