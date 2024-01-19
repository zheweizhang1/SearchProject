import project

#adding AND query
def and_query(keywords):
	if project.is_key(keywords[0]):
		result = []
		for k in project.get_key(keywords[0]):
			result.extend(project.mock_data_company[k])
		result = list(set(result))
	else: return None
	if len(keywords)>1:
		for i in keywords[1:]:
			if not project.is_key(i):return None
			r=[]
			for j in project.get_key(i):
				r.extend(project.mock_data_company[j])
			r = list(set(r))
			result = [a for a in result if a in r]
	return result

#adding OR query
def or_query(result1,result2):
	if result2 is None: return result1
	r = [i for i in result1]
	for j in result2:
		if j not in r: r.append(j)
	return r

#adding NOT query
def not_query(result1,result2):
	if result2 is None: return result1
	r = [i for i in result1]
	for i in result2:
		if i in r: r.remove(i)
	return r

def get_data_id():
	return [i[0] for i in project.mock_data[1:]]

def get_data(data):
	if data == "Name": return project.mock_data_name
	if data == "Gender": return project.mock_data_gender
	if data == "Nationality": return project.mock_data_nationality
	if data == "Company":return project.mock_data_company

def get_results(keywords):
	k = keywords.lower().split("or")
	if len(k) == 1: return and_query(project.clean_text(k[0]).split())
	result=[]
	for i in k:
		result = or_query(result,and_query(project.clean_text(i).split()))
	return result
