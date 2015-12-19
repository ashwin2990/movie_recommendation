import math
import operator
from math import sqrt
from collections import OrderedDict
import itertools
import numpy

critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
      'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
      'The Night Listener': 3.0},
     'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
      'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
      'You, Me and Dupree': 3.5},
     'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
      'Superman Returns': 3.5, 'The Night Listener': 4.0},
     'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
      'The Night Listener': 4.5, 'Superman Returns': 4.0,
      'You, Me and Dupree': 2.5},
     'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
      'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
      'You, Me and Dupree': 2.0},
     'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
      'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
     'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

def load_critic_ratings(pathname):
	critic_ratings={}
	movies_rated={}

	for line in open(pathname):
		(user,movieid,rating,ts)=line.split('\t')
		critic_ratings.setdefault(user,{})
		movies_rated.setdefault(movieid,[])
		movies_rated[movieid].append(user)
		critic_ratings[user][movieid]=float(rating)
	return critic_ratings,movies_rated

def find_critic_averages(critic_ratings_train):
	critic_averages={}
	for user in critic_ratings_train:
		total_ratings=0
		for v in critic_ratings_train[user]:
			total_ratings+=critic_ratings_train[user][v]
		critic_averages[user] = total_ratings/ len(critic_ratings_train[user])
	return critic_averages

def find_similarity_matrix(critic_ratings_train,critic_averages,movies_rated):
	similarity_dict={}
	for movies1 in movies_rated:
		temp_dict={}
		for movies2 in movies_rated:
			if(movies1!=movies2):
				temp_dict[movies2]=find_cosine_similarity(movies1,movies2, movies_rated, critic_averages,critic_ratings_train)
		similarity_dict[movies1]=temp_dict
	print similarity_dict

def find_cosine_similarity(movies1,movies2,movies_rated, critic_averages,critic_ratings_train):
	cosine_similarity=0.0
	num_cosine_similarity=0.0
	den_cosine_similarity_movies1=0.0
	den_cosine_similarity_movies2=0.0
	for user in movies_rated[movies1]:
		if user in movies_rated[movies2]:
			num_cosine_similarity+=(critic_ratings_train[user][movies1]-critic_averages[user])*(critic_ratings_train[user][movies2]-critic_averages[user])
			den_cosine_similarity_movies1+=pow((critic_ratings_train[user][movies1]-critic_averages[user]),2)
			den_cosine_similarity_movies2+=pow((critic_ratings_train[user][movies2]-critic_averages[user]),2)
	if(den_cosine_similarity_movies1!=0 and den_cosine_similarity_movies2!=0):
		return num_cosine_similarity/sqrt(den_cosine_similarity_movies1*den_cosine_similarity_movies2)
	else:
		return 0




critic_ratings_train,movies_rated_train=load_critic_ratings('ml-100k/u1.base')

critic_averages=find_critic_averages(critic_ratings_train)

find_similarity_matrix(critic_ratings_train,critic_averages, movies_rated_train)




			