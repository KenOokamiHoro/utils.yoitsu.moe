from flask import render_template, redirect, request, url_for, flash ,current_app,abort
from flask_login import login_user, logout_user, login_required,current_user
from . import irclog
from .. import db
from ..models import ChatLogMessage
from ..decorators import admin_required
import os,datetime,json,glob,random

@irclog.route("/")
def index():
    channels = { j:["Today"] for j in sorted([i.replace("/home/horo/.weechat/logs/freenode/","") for i in glob.glob("/home/horo/.weechat/logs/freenode/*")]) if "#" in j }
    for channel in channels:
        channels[channel].extend(sorted([i.replace("/home/horo/.weechat/logs/freenode/{}/".format(channel),"").replace(".log","") for i in glob.glob("/home/horo/.weechat/logs/freenode/{}/*".format(channel))]))
        try:
            channels[channel].remove(str(datetime.date.today()))
        except ValueError:
            channels[channel].remove('Today')
    return render_template("irclog/index.html",channels=channels)

@irclog.route('/<channel>',methods=["GET","POST"])
def view(channel):
    channel=channel.replace("$","#")
    try:
        log_files=[ open(i) for i in glob.glob("/home/horo/.weechat/logs/freenode/{}/*".format(channel))]
        if not log_files:
            raise FileNotFoundError
    except FileNotFoundError:
        abort(404)
    else:
        logs = []
        for logfile in log_files:
            logs.extend([j for j in [i.rstrip().split("\t") for i in logfile.readlines()] if j[1] != "--"])        
        return render_template("irclog/channel.html",channel=channel,logs=logs,full_timestamp=True)

@irclog.route('/<channel>/<day>',methods=["GET","POST"])
def view_day(channel,day):
    channel=channel.replace("$","#")
    try:
        if day.lower() == "today":
            log_file = open("/home/horo/.weechat/logs/freenode/{}/{}.log".format(channel,str(datetime.date.today())))
        else:
            log_file = open("/home/horo/.weechat/logs/freenode/{}/{}.log".format(channel,day))
        logs = [j for j in [i.rstrip().split("\t") for i in log_file.readlines()] if j[1] != "--"]
        for log in logs:
            log[0] = log[0][10:]
        return render_template("irclog/channel.html",channel=channel,logs=logs,full_timestamp=False,day=day)
    except FileNotFoundError:
        abort(404)    