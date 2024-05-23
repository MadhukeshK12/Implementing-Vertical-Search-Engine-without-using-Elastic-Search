from flask import Flask, render_template, request
from query_processor import result
from jinja2 import Environment
env = Environment(autoescape=True)
env.globals.update(len=len)
import pandas as pd

app2 = Flask(__name__)

@app2.route('/', methods=['GET', 'POST'])
def index():
    
    query = ''
    if request.method == 'POST':
        query = request.form['query']
        df, sim = result(query)
        iterable = range(len(df))
        sim_values=list(sim.values())
        l = len(df)
        data = []
        for i in iterable:
            data.append(df.iloc[i])
        return  render_template('index.html', iterable = iterable, sim = sim_values,row=data,env=env,query=query,l=l)
    else:
        return render_template('index.html',iterable = False,env=env,query=query)

if __name__ == '__main__':
    app2.run(debug=True)