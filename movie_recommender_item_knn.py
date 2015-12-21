import math
import operator
from math import sqrt
from collections import OrderedDict
import itertools
import numpy


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

def find_similarity_matrix(critic_ratings_train,critic_averages,movies_rated,top_n):
	similarity_dict={}
	for movies1 in movies_rated:
		temp_dict={}
		for movies2 in movies_rated:
			if(movies1!=movies2):
				temp_dict[movies2]=find_cosine_similarity(movies1,movies2, movies_rated, critic_averages,critic_ratings_train)
		d=OrderedDict(sorted(temp_dict.items(), key=lambda kv: kv[1], reverse=True))
		similarity_dict[movies1]=list(d.items())[:top_n]
	print 'finish computing similaritymatrix'	
	return similarity_dict

def find_cosine_similarity(movies1,movies2,movies_rated, critic_averages,critic_ratings_train):
	cosine_similarity=0
	num_cosine_similarity=0
	den_cosine_similarity_movies1=0
	den_cosine_similarity_movies2=0
	for user in movies_rated[movies1]:
		if user in movies_rated[movies2]:
			num_cosine_similarity+=(critic_ratings_train[user][movies1]-critic_averages[user])*(critic_ratings_train[user][movies2]-critic_averages[user])
			den_cosine_similarity_movies1+=pow((critic_ratings_train[user][movies1]-critic_averages[user]),2)
			den_cosine_similarity_movies2+=pow((critic_ratings_train[user][movies2]-critic_averages[user]),2)
	if(den_cosine_similarity_movies1!=0 and den_cosine_similarity_movies2!=0):
		return round(num_cosine_similarity/sqrt(den_cosine_similarity_movies1*den_cosine_similarity_movies2),2)
	else:
		return 0


def find_test_data_ratings(similarity_dict,critic_ratings_train,critic_ratings_test,movies_rated_train,critic_averages):
	filter_ratings={}
	sq_error=0
	number_of_ratings=0
	for critic in critic_ratings_test:
		for movieid in critic_ratings_test[critic]:
			if movieid in similarity_dict:
				filter_ratings.setdefault(critic,{})
				filter_ratings[critic][movieid]=find_single_rating(critic, similarity_dict, movieid,critic_ratings_train,movies_rated_train)
				sq_error+=pow((filter_ratings[critic][movieid]-critic_ratings_test[critic][movieid]),2)
				number_of_ratings+=1
				#print filter_ratings
			#print critic, movieid, critic_ratings_test[critic][movieid],filter_ratings[critic][movieid]

	print sqrt(sq_error/number_of_ratings)
	#print filter_ratings
	return sqrt(sq_error/number_of_ratings)	




def find_single_rating(critic, similarity_dict,movieid,critic_ratings_train,movies_rated_train):
	total_rating=0
	similarity=0
	if movieid in similarity_dict:
		for movies in similarity_dict[movieid]:
	#	print critic, movies, movies[0],movies_rated_train[movies[0]]
			if critic in movies_rated_train[movies[0]]:		
				total_rating+=critic_ratings_train[critic][movies[0]]*movies[1]
				similarity+=abs(movies[1])
	if(similarity!=0):
		return total_rating/similarity
	else:
		return 0




critic_ratings_train,movies_rated_train=load_critic_ratings('ml-100k/ua.base')
#print movies_rated_train['1620']

critic_averages=find_critic_averages(critic_ratings_train)

similarity_dict=find_similarity_matrix(critic_ratings_train,critic_averages, movies_rated_train,725)
#print similarity_dict
#print critic_averages
#print similarity_dict['9']

critic_ratings_test,movies_rated_test=load_critic_ratings('ml-100k/ua.test')
rmse=find_test_data_ratings(similarity_dict,critic_ratings_train, critic_ratings_test,movies_rated_train,critic_averages)






			