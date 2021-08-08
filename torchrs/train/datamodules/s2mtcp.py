from typing import Optional

from torchrs.transforms import Compose, ToTensor
from torchrs.datasets.utils import dataset_split
from torchrs.train.datamodules import BaseDataModule
from torchrs.datasets import S2MTCP


class S2MTCPDataModule(BaseDataModule):

    def __init__(
        self,
        root: str = ".data/s2mtcp",
        transform: Compose = Compose([ToTensor()]),
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.root = root
        self.transform = transform

    def setup(self, stage: Optional[str] = None):
        dataset = S2MTCP(root=self.root, transform=self.transform)
        self.train_dataset, self.val_dataset, self.test_dataset = dataset_split(
            dataset, val_pct=self.val_split, test_pct=self.test_split
        )
