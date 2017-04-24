from flask import render_template, redirect, request, url_for, flash ,current_app
from flask_login import login_user, logout_user, login_required,current_user
from . import tools
from .. import db
from .forms import OsuUserForm
from werkzeug.utils import secure_filename
from ..decorators import admin_required
import os,json,random,requests

@tools.route('/osu_user/<user>',methods=["GET","POST"])
@tools.route('/osu_user/<user>/<mode_id>',methods=["GET","POST"])
def query_osu_user(user,mode_id = 1,response = "html"):
    ''' get a osu! player 's information '''
    postdata={'k':current_app.config["OSU_API_TOKEN"],'u':user,'m':str(int(mode_id)-1)}
    request=requests.post("https://osu.ppy.sh/api/get_user",data=postdata)
    data=request.json()[0]

    if response == "html":
        #return render_template("osu/info.html", data=data, original_data = request.json())
        response = current_app.response_class(
                response = json.dumps(data,ensure_ascii=False),
                status = 200,
                mimetype = 'application/json; charset=utf-8',
            )
        return response
    if resonse == "json":
        response = current_app.response_class(
                response = json.dumps(data,ensure_ascii=False),
                status = 200,
                mimetype = 'application/json; charset=utf-8',
            )
        return response
    raise TypeError("No response type selected. >_<")

@tools.route('/osu_user',methods=["GET","POST"])
def osu_user():
    form = OsuUserForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            user = form.username.data
            mode = form.mode.data      
            return query_osu_user(user,mode,response = "html")
    return render_template("osu/query.html", form = form)

