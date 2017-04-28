from flask import render_template, redirect, request, url_for, flash ,current_app,abort
from flask_login import login_user, logout_user, login_required,current_user
from . import irclog
from .. import db
from ..models import ChatLogMessage
from ..decorators import admin_required
import os,datetime,json,glob,random

@irclog.route("/")
def index():
    channels = { j:["Today"] for j in sorted([i.replace("/home/horo/.weechat/logs/freenode/","").replace(".weechatlog","") for i in glob.glob("/home/horo/.weechat/logs/freenode/*.weechatlog")])}
    for channel in channels:
        channels[channel].extend(list(sorted(set([i.split("\t")[0][:10] for i in open("/home/horo/.weechat/logs/freenode/{}.weechatlog".format(channel))]))))

    return render_template("irclog/index.html",channels=channels)

@irclog.route('/<channel>',methods=["GET","POST"])
def view(channel):
    channels = sorted([i.replace("/home/horo/.weechat/logs/freenode/","").replace(".weechatlog","") for i in glob.glob ("/home/horo/.weechat/logs/freenode/*.weechatlog")])
    if "#"+channel in channels:
        channel = "#"+channel
        log_file = open("/home/horo/.weechat/logs/freenode/{}.weechatlog".format(channel))
        logs = [j for j in [i.rstrip().split("\t") for i in log_file.readlines()] if j[1] != "--"]
        return render_template("irclog/channel.html",channel=channel,logs=logs,full_timestamp=True)
    else:
        abort(404)

@irclog.route('/<channel>/<day>',methods=["GET","POST"])
def view_day(channel,day):
    if day.lower() == "today":
        day = str(datetime.date.today())
    print(day)
    channels = sorted([i.replace("/home/horo/.weechat/logs/freenode/","").replace(".weechatlog","") for i in glob.glob ("/home/horo/.weechat/logs/freenode/*.weechatlog")])
    if "#"+channel in channels:
        channel = "#"+channel
        log_file = open("/home/horo/.weechat/logs/freenode/{}.weechatlog".format(channel))
        logs = [j for j in [i.rstrip().split("\t") for i in log_file.readlines()] if j[1] != "--" and day in j[0]]
        for log in logs:
            log[0] = log[0][10:]
        return render_template("irclog/channel.html",channel=channel,logs=logs,full_timestamp=False,day=day)
    else:
        abort(404)    