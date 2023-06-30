import pytorch_lightning as pl
from torch.utils.data import DataLoader, random_split


class LightningDataWrapper(pl.LightningDataModule):
    def __init__(
        self,
        dataset,
        batch_size,
        num_workers=None,
        valid_batch_size=None,
        valid_size=None,
    ):
        super().__init__()
        self.dataset = dataset
        self.train_batch_size = batch_size
        self.valid_batch_size = valid_batch_size
        self.train_size = None
        self.valid_size = valid_size
        self.train_dataset = None
        self.valid_dataset = None
        self.num_workers = num_workers
        self._compute_dataset_size()
        self._compute_valid_batch_size()

    def _compute_dataset_size(self):
        if self.valid_size < 1:  # ratio
            self.valid_size = int(len(self.dataset) * self.valid_size)
        elif self.valid_size >= 1 or isinstance(self.valid_size, int):
            pass  # DO NOTHING
        else:
            raise ValueError(f"valid_size의 값을 확인하세요. 현재 값 : {self.valid_size}")
        self.train_size = len(self.dataset) - self.valid_size

    def _compute_valid_batch_size(self):
        if self.valid_batch_size is None:
            self.valid_batch_size = self.train_batch_size

    def setup(self, stage=None):
        if stage == "fit" or stage is None:
            self.train_dataset = self.dataset
            _, self.valid_dataset = random_split(
                self.dataset, (self.train_size, self.valid_size)
            )

    def train_dataloader(self, shuffle=True):
        return DataLoader(
            self.train_dataset,
            batch_size=self.train_batch_size,
            shuffle=shuffle,
            num_workers=self.num_workers,
        )

    def val_dataloader(self, shuffle=False):
        return DataLoader(
            self.valid_dataset,
            batch_size=self.valid_batch_size,
            shuffle=shuffle,
            num_workers=self.num_workers,
        )
