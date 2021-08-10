from typing import Union, Any, Sequence, Callable, Tuple

import torch
import einops
import numpy as np
import torchvision.transforms as T


__all__ = ["Compose", "ToTensor", "ToDtype", "ExtractChips"]


class Compose(T.Compose):
    """ Custom Compose which processes a list of inputs """
    def __init__(self, transforms: Sequence[Callable]):
        self.transforms = transforms

    def __call__(self, x: Union[Any, Sequence]):
        if isinstance(x, Sequence):
            for t in self.transforms:
                x = [t(i) for i in x]
        else:
            for t in self.transforms:
                x = t(x)
        return x


class ToTensor(object):
    """ Custom ToTensor op which doesn't perform min-max normalization """
    def __init__(self, permute_dims: bool = True):
        self.permute_dims = permute_dims

    def __call__(self, x: np.ndarray) -> torch.Tensor:

        if x.dtype == "uint16":
            x = x.astype("int32")

        if isinstance(x, np.ndarray):
            x = torch.from_numpy(x)

        if x.ndim == 2:
            if self.permute_dims:
                x = x[:, :, None]
            else:
                x = x[None, :, :]

        # Convert HWC->CHW
        if self.permute_dims:
            x = x.permute((2, 0, 1)).contiguous()

        return x


class ToDtype(object):
    """ Convert input tensor to specified dtype """
    def __init__(self, dtype: torch.dtype):
        self.dtype = dtype

    def __call__(self, x: torch.Tensor) -> torch.Tensor:
        return x.to(self.dtype)


class ExtractChips(object):
    """ Convert an tensor or ndarray into patches """
    def __init__(self, shape: Tuple[int, int]):
        self.h, self.w = shape

    def __call__(self, x: Union[torch.Tensor, np.ndarray]) -> Union[torch.Tensor, np.ndarray]:
        return einops.rearrange(x, "c (h p1) (w p2) -> (h w) c p1 p2", p1=self.h, p2=self.w)
