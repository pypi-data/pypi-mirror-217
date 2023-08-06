from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional

import numpy as np
import xarray as xr

from ert._c_wrappers.enkf.config.parameter_config import ParameterConfig
from ert.storage.field_utils import field_utils

if TYPE_CHECKING:
    import numpy.typing as npt

    from ert.storage import EnsembleAccessor, EnsembleReader

_logger = logging.getLogger(__name__)


@dataclass
class Field(ParameterConfig):
    nx: int
    ny: int
    nz: int
    file_format: str
    output_transformation: str
    input_transformation: str
    truncation_min: Optional[float]
    truncation_max: Optional[float]
    forward_init_file: str
    output_file: Path
    grid_file: str

    def load(self, run_path: Path, real_nr: int, ensemble: EnsembleAccessor):
        t = time.perf_counter()
        file_name = self.forward_init_file
        if "%d" in file_name:
            file_name = file_name % real_nr
        file_path = run_path / file_name

        key = self.name
        grid_path = ensemble.experiment.grid_path
        data = field_utils.get_masked_field(file_path, key, grid_path)

        trans = self.input_transformation
        data_transformed = field_transform(data, trans)
        ds = field_utils.create_field_dataset(grid_path, data_transformed)
        ensemble.save_parameters(key, real_nr, ds)
        _logger.debug(f"load() time_used {(time.perf_counter() - t):.4f}s")

    def save(self, run_path: Path, real_nr: int, ensemble: EnsembleReader):
        t = time.perf_counter()
        file_out = run_path.joinpath(self.output_file)
        if os.path.islink(file_out):
            os.unlink(file_out)
        param_info = ensemble.experiment.parameter_info[self.name]
        export_field(
            self.name,
            real_nr,
            file_out,
            param_info,
            ensemble.mount_point,
            ensemble.experiment.grid_path,
        )
        _logger.debug(f"save() time_used {(time.perf_counter() - t):.4f}s")


# pylint: disable=unnecessary-lambda
TRANSFORM_FUNCTIONS = {
    "LN": np.log,
    "LOG": np.log,
    "LN0": lambda v: np.log(v + 0.000001),
    "LOG10": np.log10,
    "EXP": np.exp,
    "EXP0": lambda v: np.exp(v) - 0.000001,
    "POW10": lambda v: np.power(10.0, v),
    "TRUNC_POW10": lambda v: np.maximum(np.power(10, v), 0.001),
}


def field_transform(
    data: npt.NDArray[np.double], transform_name: Optional[str]
) -> npt.NDArray[np.double]:
    if transform_name is None:
        return data
    return TRANSFORM_FUNCTIONS[transform_name](data)


def _field_truncate(data: npt.ArrayLike, min_: float, max_: float) -> Any:
    if min_ is not None and max_ is not None:
        vfunc = np.vectorize(lambda x: max(min(x, max_), min_))
        return vfunc(data)
    elif min_ is not None:
        vfunc = np.vectorize(lambda x: max(x, min_))
        return vfunc(data)
    elif max_ is not None:
        vfunc = np.vectorize(lambda x: min(x, max_))
        return vfunc(data)
    return data


def export_field(
    key: str,
    realization: int,
    output_path: Path,
    param_info: str,
    mount_point: Path,
    grid_path: Path,
) -> None:
    data_path = mount_point / f"realization-{realization}"

    if not data_path.exists():
        raise KeyError(
            f"Unable to load FIELD for key: {key}, realization: {realization} "
        )
    da = xr.open_dataarray(data_path / f"{key}.nc", engine="scipy")
    # Squeeze to get rid of realization-dimension
    data: npt.NDArray[np.double] = da.values.squeeze(axis=0)
    data = field_transform(data, transform_name=param_info["output_transformation"])
    data = _field_truncate(
        data,
        param_info["truncation_min"],
        param_info["truncation_max"],
    )

    field_utils.save_field(
        data,
        key,
        grid_path,
        field_utils.Shape(param_info["nx"], param_info["ny"], param_info["nz"]),
        output_path,
        param_info["file_format"],
    )
