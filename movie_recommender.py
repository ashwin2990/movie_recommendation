import math
import operator
from collections import OrderedDict
import itertools
from math import sqrt

def load_data_names(pathname):
	movie_names={}


	with open(pathname+'/u.item','r') as f:
		for line in f:
			(id, movie)=line.split('|')[0:2]
			movie_names[int(id)]=movie
	return movie_names

def load_data_genre(pathname):
	movie_genre={}
	genre=[]
	with open(pathname+'/u.item','r') as f:
		for line in f:
			(id, genre)=(line.split('|')[0],line.split('|')[5:23])
			genre.extend(line.split('|')[23].rsplit())	
			movie_genre[int(id)]=genre
	return movie_genre

def load_data_ratings(pathname):
	movie_ratings={}
	for line in open(pathname+'/u.data'):
		(user,movieid,rating,ts)=line.split('\t')
		movie_ratings.setdefault(user,{})
		movie_ratings[user][movieid]=float(rating)
	return movie_ratings

def dot_product(vec1,vec2):
	dot_product=0
	for i in range(len(vec1)):
		dot_product+=(vec1[i]*vec2[i])
	cosine_val=dot_product/((math.sqrt(vec1.count(1)))*(math.sqrt(vec2.count(1))))
	return cosine_val	

def genre_vector_int(movie_genre):
	movie_genre_int={}
	for id in movie_genre:
		genre=[]
		for elem in movie_genre[id]:
			genre+=[int(elem)]
		movie_genre_int[id]=genre	
	return movie_genre_int	

def find_item_similarities(movie_genre_int):
	movie_similarity={}
	for id in movie_genre_int:
		movie_similarity[id]={}
		for elem2 in movie_genre_int:
			if(elem2!=id):
				movie_similarity[id][elem2]=dot_product(movie_genre_int[id],movie_genre_int[elem2])	
	return movie_similarity		

def transform_dictionary(ratings):
	result={}
	for person in ratings:
		result[ratings[person]]=person
	return result	

movie_names=load_data_names('ml-100k')
movie_genre=load_data_genre('ml-100k')
movie_genre_int=genre_vector_int(movie_genre)
movie_similarity_matrix=find_item_similarities(movie_genre_int)
movie_similarity_matrix_5_elems={}
for id in movie_similarity_matrix:
	d=OrderedDict(sorted(movie_similarity_matrix[id].items(), key=lambda kv: kv[1], reverse=True))
	x = itertools.islice(d.items(), 0, 4)
	temp=[]
	for key in x:
		temp+=[key[0]]
	movie_similarity_matrix_5_elems[id]=temp

#print movie_similarity_matrix_5_elems  

def get_input(movie_names):
	user_list={}
	for i in range(8):
		movie=raw_input('Enter the name of the movie:')
		# while movie not in movie_names.values():
		# 	movie=input('Enter the name of the movie again:') 
		rating=raw_input('Enter the movie rating')
		movie_names_inv=transform_dictionary(movie_names)
		user_list[int(movie_names_inv[movie])]=int(rating)
	return user_list
			

for items in movie_names:
	print movie_names[items]
user_list=get_input(movie_names)#{472: 1.0, 356: 3.0, 470: 5.0, 471: 4.0, 688: 1.0, 474: 5.0, 475: 1.0, 479: 4.0, 680: 3.0, 358: 1.0}	
movie_genre_array=[]

for items in user_list:
	movie_genre_array+=movie_similarity_matrix_5_elems[items]
	


movie_genre_array=list(OrderedDict.fromkeys(movie_genre_array))	
#print movie_genre_array

for items in movie_genre_array:
	if(items in user_list):
		movie_genre_array.remove(items)

#print movie_genre_array







def find_critic_reviews(movie_genre_array,movie_critic_list,critic_based_ratings):
	critic_based_ratings_for_new_movies={}
	for movies in movie_genre_array:
		no_of_ratings=0
		sum_ratings=0
		sum_similarities=0.0
		for critics in movie_critic_list:
			r=critic_based_ratings[critics].get(str(movies))
			if(r!=None):
				no_of_ratings+=1
				sum_ratings+=movie_critic_list[critics]*critic_based_ratings[critics][str(movies)]
				sum_similarities+=movie_critic_list[critics]
		if(no_of_ratings!=0):
			critic_based_ratings_for_new_movies[movies]=sum_ratings/sum_similarities

	return critic_based_ratings_for_new_movies	




def find_critics(user_list,critic_based_ratings):
	distance_array={}

	for critic in critic_based_ratings:
		distance_array[critic]=find_distance(user_list, critic, critic_based_ratings)
	d=OrderedDict(sorted(distance_array.items(), key=lambda kv: kv[1], reverse=True))
	x=itertools.islice(d.items(), 0, 10)
	distance_array.clear()
	for key in x:
		distance_array[key[0]]=d[key[0]]
	return distance_array	

def find_distance(user_list, critic,critic_based_ratings):
	common_items={}
	sum_of_distances=0
	for movies in user_list:
		if str(movies) in critic_based_ratings[critic]:
			common_items[movies]=1
	if (len(common_items)==0):
		return 0

	for movies in user_list:
		if str(movies) in critic_based_ratings[critic]:
			sum_of_distances+=(pow(user_list[movies]-critic_based_ratings[critic][str(movies)],2))

	return 1/(1+sum_of_distances)                          		


		

critic_based_ratings=load_data_ratings('ml-100k')

movie_critic_list=find_critics(user_list,critic_based_ratings)
#print movie_critic_list			

print 'input='
for items in user_list:
	print movie_names[items]

#critic_based_ratings_inv=transform_dictionary(critic_based_ratings)
#print critic_based_ratings
print '\n'
final_list = find_critic_reviews(movie_genre_array,movie_critic_list,critic_based_ratings)
d=OrderedDict(sorted(final_list.items(), key=lambda kv: kv[1], reverse=True))
x=itertools.islice(d.items(), 0, 5)
print "Recommended Movies:"
for items,values in x:
	print movie_names[items]










	



	






	

