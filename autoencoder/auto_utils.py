from autoencoder import TabularDataset, Autoencoder
from fastai.tabular.all import *
import pandas as pd
from torch import nn
from torch.utils.data import Dataset, DataLoader
import torch
from sklearn.preprocessing import LabelEncoder

def get_data_from_file(filename):
	'''
	filename: string with csv filename of ais data
	returns a pandas dataframe
	'''
	try: 
		data =  pd.read_csv(filename)
	except:
		data = pd.read_csv(filename, sep='\t')
	data['dt'] = pd.to_datetime(data['dt'], format='%Y-%m-%dT%H:%M:%S')
	return data

def aggregate_ais_data(data):
	'''
	data: dataframe with raw data
	returns dataframe with aggregates
	'''
	agg_dictionary = {
		'sog': ['mean', 'min', 'max', 'std'],
		'dt': 'count', 
		'length': 'mean',
		'width': 'mean', 
		'draft': 'mean'
	}

	aggs = data.groupby(['mmsi', pd.Grouper(key='dt', freq='H'), 'status', 'vesseltype']).agg(agg_dictionary)
	aggs.reset_index(inplace=True)

	aggs.columns = ['_'.join(col).strip() for col in aggs.columns.values]

	aggs.rename(columns={'mmsi_':'mmsi', 'dt_':'dt', 'status_': 'status', 'vesseltype_':'vesseltype', 
                     'dt_count':'count', 'length_mean':'length', 'width_mean':'width', 'draft_mean':'draft'}, 
            inplace=True)
	aggs['vesseltype'] = aggs['vesseltype'].astype(int)
	aggs.fillna(0, inplace=True)

	return aggs

def get_vessel_dictionary():
	'''
	utility function to give the name of the vessel based on number of vesseltype.
	There is room to improve this dictionary, but it works for now.
	'''
	return {
		    0:'na',
		    4:'other', 7:'other', 33:'other', 47:'other', 110:'other', 
		    1005:'other', 1010:'other', 1018:'other', 1020:'other', 1022:'other', 
		    30:'fishing', 1001:'fishing', 1002:'fishing', 
		    70:'cargo', 71:'cargo', 72:'cargo', 74:'cargo', 79:'cargo', 1003:'cargo', 1004:'cargo',
		    80:'tanker', 84:'tanker', 1024:'tanker',
		    1012:'passenger', 1013:'passenger',
		    1025:'tugtow'
		}

def make_sparse_matrix_for_vesseltype(aggs):
	'''
	aggs: dataframe of aggregates
	returns modified aggregate df with addition of one-hot encoding for status and vessel fields.
	'''
	try:
		if aggs['vessel'].any(): pass # if already there, move right along
	except :
		vessel_dictionary = get_vessel_dictionary()
		aggs['vessel'] = aggs['vesseltype'].map(vessel_dictionary)
	return pd.get_dummies(aggs, columns=['status', 'vessel'])
	
def make_model(one_hot):
	'''
	one_hot: the aggregated data with one-hot encoded status and vessel fields
	returns DataLoader and Autoencoder model ready to be trained
	'''
	categorical = ['mmsi', 'dt']
	continuous = list(set(one_hot.columns)-set(categorical))
	to = TabularPandas(one_hot, procs=[Categorify, Normalize], cat_names=categorical, 
		cont_names=continuous)
	dataset = TabularDataset(to.xs)
	BATCH_SIZE = 64 # don't love the hard coding of the constants but deal with this another time
	dls = DataLoader(dataset, batch_size=BATCH_SIZE)
	model = Autoencoder(to.xs.shape[1]) # That's the number of features
	return dls, model

def train_model(dls, model):
	'''
	MODEL IS UNTRAINED AT THE BEGINNING, RETURNS IN EVAL MODE 
	dls: DataLoader (batched data)
	model: untrained Autoencoder
	returns trained model
	'''
	LEARNING_RATE = 0.001 # again with the hard coded constant
	criterion = nn.MSELoss()
	optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

	model.float()
	model.train() # turn on training mode

	NUM_EPOCHS = 80
	for epoch in range(NUM_EPOCHS):
		running_loss = 0.0
		for batch in dls:
			# clear the optimizer of previous gradients
			optimizer.zero_grad()
			# forward --------------------------------------------
			output = model(batch[1]) # batch is a list of three vectors:
			# [y, cont_X, cat_X]. We already converted categorical to continuous,
			# so pass in batch[1]
			loss = criterion(output, batch[1])
			# backward -------------------------------------------
			loss.backward()
			optimizer.step()
			#keep a running total of loss for the batches in this epoch
			running_loss += loss.item()
			# log
			lossb = running_loss/len(dls)
			train_loss.append(lossb)
			print('epoch [{}/{}], loss:{:.4f}'.format(epoch+1, NUM_EPOCHS, loss.data), lossb)
	return model.eval()


def evaluate_data(aggs, model):
	'''
	FOR USE ON TRAINED MODEL
	aggs: assumed to be in aggregated form matching dataframe returned from aggregate_ais_data()
	model: the trained model IN EVAL MODE
	returns aggs augmented with losses for each record
	'''
	one_hot = make_sparse_matrix_for_vesseltype(aggs)
	categorical = ['mmsi', 'dt']
	continuous = list(set(one_hot.columns)-set(categorical))
	to = TabularPandas(one_hot, procs=[Categorify, Normalize], 
		cat_names=categorical, cont_names=continuous)
	dataset = TabularDataset(to.xs)
	evaluate = DataLoader(dataset, batch_size=1) # evaluate error for each record

	LEARNING_RATE = 0.001 # again with the hard coded constant
	criterion = nn.MSELoss()
	optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

	model.eval() # just for good measure
	item_losses = []
	for item in evaluate:
		# clear the optimizer of previous gradients
		optimizer.zero_grad()
		# forward ---------------------------------------------
		output = model(item[1]) # batch is a list of three vectors:
			# [y, cont_X, cat_X]. We already converted categorical to continuous,
			# so pass in batch[1]
		loss = criterion(output, item[1])
		# backward ---------------------------------------------
		loss.backward()
		optimizer.step()
		#append to the list of item losses
		item_losses.append(loss.item())
	aggs['losses'] = item_losses
	return aggs









