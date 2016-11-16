import pandas as pd
import numpy as np
import feature_helpers
import random
from collections import defaultdict 

"""
Add code for feature generation to this file
Example:
Suppose your new feature is called 'area' and you have specified in the yml file to include 'length' and 'width'
Then your function should look as follows:

def area_feature(df):
	return df.apply(lambda x: x.length * x.width, 1)	
"""

def alph_term_feature(df):
	return df.Term.apply(feature_helpers.get_sortable_term)

def running_gpa_feature(df):
	dict_vals = {}
	
	gr_sum = df.groupby(['ID','alph_term']).sum().grade
	sub_df = df.groupby(['ID','alph_term']).count()
	sub_df['sumgrade'] = gr_sum
	
	old_id = ''
	gr_sum_running = 0
	course_count_running = 0
	
	for i,row in sub_df.iterrows():
		if i[0] == old_id:
			dict_vals[i] = gr_sum_running/course_count_running
			gr_sum_running = gr_sum_running+row.sumgrade
			course_count_running = course_count_running+row.grade
		else:
			gr_sum_running = row.sumgrade
			course_count_running = row.grade
			dict_vals[i] = -1
			old_id = i[0]
			
	return df.apply(lambda x: dict_vals[(x.ID, x.alph_term)], axis='columns')
	
def gpa_last_quarter_feature(df):
	dict_vals = {}
	
	sub_df = df.groupby(['ID','alph_term']).mean()
	
	old_id = ''
	gr_last = 0
	
	for i,row in sub_df.iterrows():
		if i[0] == old_id:
			dict_vals[i] = gr_last
			gr_last = row.grade
		else:
			gr_last = row.grade
			dict_vals[i] = -1
			old_id = i[0]
			
	return df.apply(lambda x: dict_vals[(x.ID, x.alph_term)], axis='columns')
	
def last_quarter_feature(df):
	dict_vals = {}
	
	sub_df = df.groupby(['ID','alph_term']).count()
	
	old_id = ''
	term_last = ''

	for i,row in sub_df.iterrows():
		if i[0] == old_id:
			dict_vals[i] = term_last
			term_last = i[1]
		else:
			term_last = i[1]
			dict_vals[i] = -1
			old_id = i[0]	
	
	return df.apply(lambda x: dict_vals[(x.ID, x.alph_term)], axis='columns')
		
		
		
def course_level_feature(df):
	return df.course.apply(feature_helpers.get_course_level)

def math_units_feature(df):
	return df.apply(feature_helpers.get_math_units, axis = 'columns')
	
def terms_so_far_feature(df):
	dict_index = {}
	gb_id = df.groupby('ID')
	for name,group in gb_id:
		group = group.sort('alph_term')
		gb_term = group.groupby('alph_term')
		count = 0
		for name2, group2 in gb_term:
			dict_index[str(name)+str(name2)] = count
			count+=1
			
	return df.apply(lambda x: dict_index[str(x.ID)+str(x.alph_term)], axis = 'columns')
	
def avg_rank_last_quarter_feature(df):
	"""
	not working yet!
	"""
	dict_stats = {}
	gb_term_course = df.groupby(['alph_term','course'])
	l = len(gb_term_course)
	for name,group in gb_term_course:
		mu = group.grade.mean()
		stdev = group.grade.std()
		group['rank'] = group.grade.apply(lambda x: (x-mu)/stdev if stdev != 0 else -1)
		group['term'] = name[0]*len(group)
		group['course'] = name[1]*len(group)
		dict_stats = group.set_index(['ID','term','course'])['rank'].to_dict()
		
	
	raise SystemExit
	
	rk_list = []
	for i,row in df.iterrows():
		stats = dict_stats[(row.last_quarter, row.course)]
		

def actual_grade_feature(df):
	return df.grade.apply(feature_helpers.get_actual_grade)

def previous_gpa_feature(df):
	students = list(set(df['ID'].values.tolist()))

	dct = defaultdict(list)
	grades_dct = {}
	for index, row in df.iterrows():
		dct[row['ID'] + "-" + str(row['alph_term'])].append(row['grade'])

	for index, row in df.iterrows(): 
		previous_term = row['alph_term'] - 0.25
		grades_list = []
		count = 0 

		while (count < 20): 
			grades_list.extend(dct[row['ID'] + '-' + str(previous_term)])
			count = count + 1
			previous_term = previous_term - 0.25

		grade_units = [grade * 4 for grade in grades_list]
		if len(grade_units) > 0: 
			previous_gpa = sum(grade_units)/float(len(grade_units)*4) 
		else:
			previous_gpa = 0 

		grades_dct[(row['ID'], row['alph_term'])] = previous_gpa

	return df.apply(lambda x: grades_dct[(x.ID, x.alph_term)], axis = 'columns')


def recieved_A_plus_feature(df):
	return df.grade.apply(feature_helpers.get_boolean_A_plus)
	
def dummy_label_feature(df):
	dummy_list = []
	for i in range(len(df)):
		r = random.random()
		if r <= 0.5:
			dummy_list.append(0)
		else:
			dummy_list.append(1)
	return dummy_list


