from typing import Union, List

from numpy import ndarray

from cerebrium.models.base import BaseModel
from torch import tensor, Tensor


class TorchModel(BaseModel):
    def predict(self, input: Union[Tensor, ndarray, List]) -> list:
        if not isinstance(input, Tensor):
            input = tensor(input)
        return self.model(input)
