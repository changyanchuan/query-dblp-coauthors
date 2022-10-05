# cyc @ 2022-10-04
import os
import time
import logging
from flask import Flask, request, render_template
from coauthor_dblp import get_dblp_coauthors, coauthors_dic_to_str
app = Flask(__name__)


@app.before_first_request
def before_first_request():
    log_level = logging.INFO

    for handler in app.logger.handlers:
        app.logger.removeHandler(handler)

    root = os.path.dirname(os.path.abspath(__file__))
    logdir = os.path.join(root, 'logs')
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    log_file = os.path.join(logdir, 'log-' + str(int(time.time())) + '.log')
    handler = logging.FileHandler(log_file)
    handler.setLevel(log_level)
    defaultFormatter = logging.Formatter('[%(levelname)s][%(asctime)s][%(module)s:%(funcName)s:%(lineno)d]: %(message)s')
    handler.setFormatter(defaultFormatter)

    app.logger.addHandler(handler)
    app.logger.setLevel(log_level)


@app.route('/')
def index():
    return render_template('index.html', start_year = 2020, min_papers = 1)


@app.route('/', methods=['POST'])
def get_dblp_coauthors_str():
    
    start_year = min_papers = 0
    try:
        assert len(request.form['pid']) > 0
        start_year = int(request.form['start_year'])
        min_papers = int(request.form['min_papers'])
    except (ValueError, AssertionError) as err:
        app.logger.info("ERR: pid={}, start_year={}, min_papers={}. Invalid inputs!".format(request.form['pid'], request.form['start_year'], request.form['min_papers']))
        return render_template('index.html', pid = request.form['pid'], start_year = request.form['start_year'],
                            min_papers = request.form['min_papers']) \
                            + "Invalid inputs!"

    coauthors_lst = get_dblp_coauthors(request.form['pid'], start_year, min_papers)
    if coauthors_lst != None:
        rtn = coauthors_dic_to_str(coauthors_lst, sep = '<br>')

        app.logger.info("RSP: pid={}, start_year={}, min_papers={}, rsp={}".format( \
                        request.form['pid'], request.form['start_year'], request.form['min_papers'], rtn))
        
        return render_template('index.html', pid = request.form['pid'], start_year = request.form['start_year'],
                            min_papers = request.form['min_papers']) \
                            + rtn
    else:
        app.logger.info("ERR: pid={}, start_year={}, min_papers={}. DBLP request failed.".format(request.form['pid'], request.form['start_year'], request.form['min_papers']))

        return render_template('index.html', pid = request.form['pid'], start_year = request.form['start_year'],
                            min_papers = request.form['min_papers']) \
                            + "DBLP request failed."