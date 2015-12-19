import math
import operator
from collections import OrderedDict
import itertools
from math import sqrt
import matplotlib.pyplot as plt

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

def find_nearest_critics(critic_based_ratings, movies_rated,top_n):
	distance_dict={}

	for critics1 in critic_based_ratings:
		temp_dict={}
		for critics2 in critic_based_ratings:	#itertools.combinations(critic_based_ratings,r=2):
			if(critics1!=critics2):
				similarity=find_euclidean_distance([critics1,critics2], critic_based_ratings, movies_rated)
				temp_dict[critics2]=similarity
		d=OrderedDict(sorted(temp_dict.items(), key=lambda kv: kv[1], reverse=True))
		distance_dict[critics1]=list(d.items())[:top_n]

	return distance_dict
				



#def find_rating(movie, critic, critic_based_ratings):




def find_euclidean_distance(pair, critic_based_ratings, movies_rated):
	sum_of_distances=0
	for movies in critic_based_ratings[pair[0]]:
		if movies in critic_based_ratings[pair[1]]:
			sum_of_distances+=(pow(critic_based_ratings[pair[0]][movies]-critic_based_ratings[pair[1]][movies],2)) 

	return 1/(1+sum_of_distances)








def find_test_data_ratings(distance_dict,movies_rated_train,critic_ratings_test):
	filter_ratings={}
	sq_error=0
	number_of_ratings=0
	for critic in critic_ratings_test:
		for movieid in critic_ratings_test[critic]:
			filter_ratings.setdefault(critic,{})
			filter_ratings[critic][movieid]=find_single_rating(critic, distance_dict, movieid,critic_ratings_train,movies_rated_train)
			sq_error+=pow((filter_ratings[critic][movieid]-critic_ratings_test[critic][movieid]),2)
			number_of_ratings+=1
			#print critic, movieid, critic_ratings_test[critic][movieid],filter_ratings[critic][movieid]
	#print filter_ratings
	print sqrt(sq_error/number_of_ratings)
	#print filter_ratings
	return sqrt(sq_error/number_of_ratings)		
		

def find_single_rating(critic, distance_dict,movieid,critic_ratings_train,movies_rated_train):
	total_rating=0
	similarity=0
	#print critic_ratings_train
	#print distance_dict
	for items in distance_dict[critic]:
		#print items[0],",",items[1]

		if movieid in movies_rated_train[items[0]]:
			#print "rating",critic_ratings_train[items[0]][movieid]			
			total_rating+=critic_ratings_train[items[0]][movieid]*items[1]
			similarity+=items[1]
	if(similarity!=0):
		return total_rating/similarity
	else:
		return 0

# critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
#       'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
#       'The Night Listener': 3.0},
#      'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
#       'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
#       'You, Me and Dupree': 3.5},
#      'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
#       'Superman Returns': 3.5, 'The Night Listener': 4.0},
#      'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
#       'The Night Listener': 4.5, 'Superman Returns': 4.0,
#       'You, Me and Dupree': 2.5},
#      'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
#       'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
#       'You, Me and Dupree': 2.0},
#      'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
#       'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
#      'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}


critic_ratings_train,movies_rated_train=load_critic_ratings('ml-100k/u1.base')
critic_ratings_test,movies_rated_test=load_critic_ratings('ml-100k/u1.test')
top_n_data=[]
rmse_data=[]


for top_n in xrange(10,1000,100):
	top_n_data.append(top_n)
	distance_dict=find_nearest_critics(critic_ratings_train, movies_rated_train,top_n)
	rmse=find_test_data_ratings(distance_dict,critic_ratings_train, critic_ratings_test)
	rmse_data.append(rmse)

print top_n_data
print rmse_data
X=[10, 110, 210, 310, 410, 510, 610, 710, 810, 910]
Y=[3.4497524812315365, 2.4497896241918093, 1.9306776390259754, 1.6047617383586397, 1.3866856313498583, 1.2351110096454858, 1.1377701691789786, 1.0801400497692355, 1.0476806508347307, 1.0347662916092135]
plt.plot(X,Y)
plt.show()







