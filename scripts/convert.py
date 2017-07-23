import pandas as pd
import numpy as np
import sys,csv
import time
from heapq import nlargest
import dill

curr_time=time.time()
ADID_LIMIT = 2922042

converter={'user_id':np.int64,'ad_id':np.int64}
# 'images_count':np.int64,'ad_impressions':np.int64,'ad_views':np.int64,'ad_messages':np.int64}
ud=pd.read_csv('data/user_data.csv',dtype=converter).fillna(0)
ad=pd.read_csv('data/ads_data.csv',dtype=converter).fillna(0)
umt=pd.read_csv('data/user_messages_test.csv').fillna(0)
um=pd.read_csv('data/user_messages.csv').fillna(0)

print('pds loaded', time.time()-curr_time)
curr_time=time.time()

a2c = [-1]*ADID_LIMIT
for i,row in ad_data.iterrows():
	ad_id,c_id=row['ad_id'],row['category_id']
	a2c[ad_id]=c_id
# for x in ud.columns:
# 	y=np.array(ud[x].unique())
# 	print(x,y,len(y))

# print('-----------------------------------------------------------------------------------')
# for x in ad.columns:
# 	y=np.array(ad[x].unique())
# 	print(x,y,len(y))

category_ids=[800,815,806,859,811,853,881,888,887,362]


def create_submission(values,user_messages,name):
	submission = user_messages.assign(ads=pd.Series(values))
	submission.to_csv('submissions/'+name)


def popularity_based(user_data,ad_data,user_messages):	
	frequency = [0]*ADID_LIMIT
	for i,row in user_data.iterrows():
		ad_id,ad_views=row['ad_id'],row['ad_views']	
		frequency[ad_id] = max(ad_views,frequency[ad_id])

	categories={x:[] for x in category_ids}
	for i,row in ad_data.iterrows():
		ad_id,c_id=row['ad_id'],row['category_id']
		a2c[ad_id]=c_id
		categories[c_id].append(ad_id)

	for x in category_ids:
		categories[x] = nlargest(10, categories[x],key=lambda y: frequency[y])

	values=[[] for i in range(10)]
	for i,row in user_messages.iterrows():
		u_id,c_id=row['user_id'],row['category_id']
		for x in range(1,10):
			if c_id not in category_ids:
				values[x].append( '[]' )
			else:
				values[x].append( str(categories[c_id][:x]) )
	for x in range(1,10):
		create_submission(values[x],umt,str(x)+'.csv')

# curr_time=time.time()
# popularity_based(ud[:100],ad,umt)
# print('popularity_based done', time.time()-curr_time)

# curr_time=time.time()
# table={}
# cc=0
# for i,x in um.iterrows():
# 	dt=(x['user_id'],x['category_id'])
# 	table[dt]=1+(table[dt] if dt in table else 0)
# for i,x in umt.iterrows():
# 	dt=(x['user_id'],x['category_id'])
# 	if dt in table:
# 		cc+=1

# print('stats',cc,len(um),len(umt))
# print('stats done', time.time()-curr_time)


def item_item_collaborative(user_data,ad_data,user_messages):	
	
	for i,row in user_data.iterrows():
		ad_id,ad_views=row['ad_id'],row['ad_views']	
		frequency[ad_id] = max(ad_views,frequency[ad_id])


	values=[[] for i in range(10)]
	for i,row in user_messages.iterrows():
		u_id,c_id=row['user_id'],row['category_id']
		for x in range(1,10):
			if c_id not in category_ids:
				values[x].append( '[]' )
			else:
				values[x].append( str(categories[c_id][:x]) )
	for x in range(1,10):
		create_submission(values[x],umt,str(x)+'.csv')
