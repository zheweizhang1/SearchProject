from flask import Flask, redirect, render_template, request
import project as p
import extended_part1 as e1

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("home.html")

@app.route("/input",methods=["POST","GET"])
def index():
	md = p.mock_data[1:]
	if request.method=="GET":
		return render_template("inverted_index.html",result = md, lresult = str(len(md))+'/'+str(len(md))+' results')
	term = request.form['term']
	nresult = render_template("inverted_index.html",nresult = "No result for '"+term+"' please enter again.",lresult = '0/'+str(len(md))+' results')
	if not term.strip(): return nresult
	t = p.clean_text(term).split()
	result = e1.and_query(t)
	if result is None or not result: return nresult
 	return render_template("inverted_index.html", result = p.return_values(result), lresult = str(len(result))+'/'+str(len(md))+' results',dresult = 'Results for "'+term+'.')

@app.route("/input/narrow_search",methods=["POST","GET"])
def narrow():
	md = p.mock_data[1:]
	options = ['ID','Name','Gender','Nationality','Company']
	if request.method=="GET":
		return render_template("narrow_search.html",result = md, lresult = str(len(md))+'/'+str(len(md))+' results', options = options)
	term = request.form['term']
	option = request.form.get('options')
	exclude = request.form['exclude']
	nresult = render_template("narrow_search.html",nresult = "No result for '"+term+"' please enter again.",lresult = '0/'+str(len(md))+' results', options = options)
	if not term.strip(): 
		if not exclude.strip():
			return nresult
		e = e1.get_results(exclude.strip())
		result = e1.not_query(e1.get_data_id(),e)
		return render_template("narrow_search.html", result = p.return_values(result), lresult = str(len(result))+'/'+str(len(md))+' results', dresult = 'Results for "'+term+'" excluding "'+exclude+'".', options = options)
	result = e1.get_results(term.strip())
	if exclude.strip():
		e = e1.get_results(exclude.strip())
		result = e1.not_query(result,e)
	if result is None or not result: return nresult
	return render_template("narrow_search.html",result = p.return_values(result), lresult = str(len(result))+'/'+str(len(md))+' results', dresult ='Results for "'+term+'"excluding "'+exclude+'".', options = options)
	

app.run(debug=True,host="0.0.0.0",port=5000)
