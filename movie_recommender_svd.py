import pandas as pd
import numpy as np
from math import sqrt

def load_critic_ratings(pathname):
	critic_ratings={}

	for line in open(pathname):
		(user,movieid,rating,ts)=line.split('\t')
		critic_ratings.setdefault(user,{})
		critic_ratings[user][movieid]=float(rating)
	return critic_ratings


def read_file_2D_matrix(filename):
	df = pd.read_csv(filename, sep='\s+', header=None)
	df.columns = ['User','Item','ItemRating','Timestamp']
	#matrix=df.fillna(df.mean())
	#print matrix
	matrix=df.pivot(index='User', columns='Item', values='ItemRating')
	return matrix.fillna(matrix.mean())
	#print output_matrix
	#print matrix.mean()
	#return np.array(output_matrix)

#def process_matrix(ratings_matrix):


def matrix_svd(ratings_matrix,k):
	U, s, V = np.linalg.svd(ratings_matrix,full_matrices=False)
	s[k:] = 0
	new_ratings_matrix = np.dot(U, np.dot(np.diag(s), V))
	return new_ratings_matrix

def find_test_data_ratings(new_ratings_matrix,critic_ratings_test):
	sq_error=0
	number_of_ratings=0
	for critic in critic_ratings_test:
		for movieid in critic_ratings_test[critic]:
			#print new_ratings_matrix[critic,movieid]
			sq_error+=pow((new_ratings_matrix[int(critic)-1,int(movieid)-1]-critic_ratings_test[critic][movieid]),2)
			number_of_ratings+=1
	print sqrt(sq_error/number_of_ratings)


ratings_matrix=read_file_2D_matrix('ml-100k/ua.base')	
ratings_test=load_critic_ratings('ml-100k/ua.test')
new_ratings_matrix=matrix_svd(np.array(ratings_matrix),200)
print new_ratings_matrix.shape
find_test_data_ratings(new_ratings_matrix,ratings_test)
#find_ratings(new_ratings_matrix)

#print ratings_matrix
#process_matrix(ratings_matrix)
