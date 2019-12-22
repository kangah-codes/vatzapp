from flask import Flask, redirect, render_template, request
from functions import *

app = Flask(__name__)

@app.route('/')
@app.route('/chart')
def chart():
	data = {
		"most": most_messages,
		"percent":most_percent,
		"dates_msg": [x[1] for x in zip(dates, date_messages)],
		"dates":[x[0] for x in zip(dates, date_messages)],
		"p1_data":p1_final_data,
		"p2_data":p2_final_data,
		"people":people,
		"messages":len(messages),
		'two_graph':dates

	}
	print(data['p1_data'])
	return render_template('index.html', **data)


app.run(debug=True)