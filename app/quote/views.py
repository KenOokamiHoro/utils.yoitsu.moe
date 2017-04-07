from flask import render_template, redirect, request, url_for, flash ,current_app
from flask_login import login_user, logout_user, login_required,current_user
from . import quote
from .. import db
from ..models import Quote
from .forms import AddQuoteForm, MassQuoteForm
from werkzeug.utils import secure_filename
from ..decorators import admin_required
import os,json,random

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@quote.route('/add',methods=["GET","POST"])
@admin_required
def add():
    form = AddQuoteForm()
    if form.validate_on_submit():
        new_quote = Quote(content = form.content.data,
                          author = form.author.data,
                          source = form.source.data,
                          link = form.link.data,
                          comment = form.comment.data)
        db.session.add(new_quote)
        flash('😋')
        return redirect(url_for('quote.all'))
    return render_template("quote/add.html", form = form)

@quote.route('/edit/<id>',methods=["GET","POST"])
@admin_required
def edit(id):
    form = AddQuoteForm()
    current_quote = Quote.query.filter_by(id = id).first_or_404()
    if form.validate_on_submit():
        current_quote.content = form.content.data
        current_quote.author = form.author.data
        current_quote.source = form.source.data
        current_quote.link = form.link.data
        current_quote.comment = form.comment.data
        db.session.add(current_quote)
        flash('😋')
        return redirect(url_for('quote.view',id = id))
    form.content.data = current_quote.content
    form.author.data = current_quote.author
    form.source.data = current_quote.source
    form.link.data = current_quote.link
    form.comment.data = current_quote.comment
    return render_template("quote/add.html", form = form)

@quote.route('/massadd',methods=["GET","POST"])
@admin_required
def massadd():
    form = MassQuoteForm()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            json_quotes = json.load(file)
            for item in json_quotes:
                new_quote = Quote(content = item.get("content",None),
                                    author = item.get("author",None),
                                    source = item.get("source",None),
                                    link = item.get("link",None),
                                    comment = item.get("comment",None))
                if new_quote.content:
                    db.session.add(new_quote)
            flash('😋')
            return redirect(url_for('main.index'))
    return render_template("quote/add.html", form = form)
    
@quote.route('/view/<id>')
def view(id):
    current_quote = Quote.query.filter_by(id = id).first_or_404()
    return render_template("quote/view.html", quote = current_quote)

@quote.route('/view/random')
def view_random():
    current_quote = random.choice(Quote.query.all())
    return view(current_quote.id)

@quote.route('/view/all')
def all():
    quotes = Quote.query.all()
    return render_template("quote/all.html", quotes = quotes)

@quote.route('/delete/<id>')
def delete(id):
    current_quote = Quote.query.filter_by(id = id).first_or_404()
    db.session.delete(current_quote)
    flash('😋')
    return redirect(url_for('quote.all'))

@quote.route('/jsonify/<id>')
def jsonify(id):
    current_quote = Quote.query.filter_by(id = id).first_or_404()
    response = current_app.response_class(
        response = json.dumps(current_quote.jsonify(),ensure_ascii=False),
        status = 200,
        mimetype = 'application/json; charset=utf-8',
    )
    return response

@quote.route('/jsonify/random')
def jsonify_random():
    current_quote = random.choice(Quote.query.all())
    return jsonify(current_quote.id)

@quote.route('/')
def index():
    current_quote = random.choice(Quote.query.all())
    return render_template("quote/index.html", quote = current_quote)