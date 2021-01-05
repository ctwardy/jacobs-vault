"""
Autoencoding for tabular data
"""
from fastai.tabular.all import *
import pandas as pd
from torch import nn
from torch.utils.data import Dataset, DataLoader
import torch
from typing import List

class TabularDataset(Dataset):
	def __init__(self, data: pd, cat_cols: List[str]=None, output_col: List[str]=None):
		"""
		Characterize a dataset for PyTorch
		:param data: pandas data frame
		The data frame object for the input data. It must contain all the 
		continuous, categorical, and output columns to be used.
		
		:param cat_cols: List of strings
		The names of the categorical columns in the data. These columns will be
		passed through the embedding layers in the model. These columns must be
		numerically encoded beforehand.
		
		:param output_col: string
		The name of the output variable column in the data (if there is one)...
		and if there is, it should be numerical
		"""
		self.n = data.shape[0] # number of rows

		if output_col:
			self.y = data[output_col].astype(np.float32).values.reshape(-1, 1)
		else:
			self.y = np.zeros((self.n, 1))
		
		self.cat_cols = cat_cols if cat_cols else []
		self.cont_cols = [col for col in data.columns 
					if col not in self.cat_cols + [output_col]]

		if self.cont_cols:
			self.cont_X = data[self.cont_cols].astype(np.float32).values
		else:
			self.cont_X = np.zeros((self.n, 1))

		if self.cat_cols:
			self.cat_X = data[cat_cols].astype(np.float32).values
		else:
			self.cat_X = np.zeros((self.n, 1))

	def __len__(self) -> int:
		"""
		Denote the number of records.
		"""
		return self.n

	def __getitem__(self, idx) -> List[np.ndarray]:
		"""
		Generate one sample of data at index idx
		"""
		return [self.y[idx], self.cont_X[idx], self.cat_X[idx]]

class Autoencoder(nn.Module):
	"""
	Instantiate the autoencoder...note the hard coded bottleneck. This is not ideal.

	:arg dim: dimension, or number of features, of the data set.

	:param encoder: sequential nn, uses dim to determine number of hyper-
	parameters in the bottleneck

	:param decoder: sequential nn, increase the number of hyperparameters back
	to original dimension
		"""
	def __init__(self, dimension):
		super(Autoencoder, self).__init__()
		self.dim = dimension # number of features ... could bottleneck further, depending on number of features
                             #    but good enough for now
		self.encoder = nn.Sequential(nn.Linear(self.dim, self.dim//2),
					nn.ReLU(True), nn.Linear(self.dim//2, self.dim//4))
		self.decoder = nn.Sequential(nn.Linear(self.dim//4, self.dim//2),
					nn.ReLU(True), nn.Linear(self.dim//2, self.dim))

	def encode(self, x: torch.Tensor) -> torch.Tensor: return self.encoder(x)

	def decode(self, x: torch.Tensor) -> torch.Tensor: return self.decoder(x)

	def forward(self, x: torch.Tensor) -> torch.Tensor:
		encoded = self.encoder(x)
		decoded = self.decoder(encoded)
		return decoded

def get_device() -> str:
	"""
	Use to detrmine if gpu is available
	"""
	if torch.cuda.is_available():
		device = 'cuda:0'
	else:
		device = 'cpu'
	return device
