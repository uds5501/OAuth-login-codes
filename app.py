from flask import Flask,redirect,url_for
from flask_dance.contrib.twitter import make_twitter_blueprint,twitter
from flask_dance.contrib.github import make_github_blueprint,github
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin


app=Flask(__name__)
app.config['SECRET_KEY']='somethingsecret'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:/'
#making blueprints
twitter_blueprint=make_twitter_blueprint(api_key='7ul58pXpUO9bDKvyVPVZGDL3F',api_secret='7OguVMaMr7P62dL51yDBtAFj0sns4wNXyjRAYHLiMkHSH6vmol')
github_blueprint=make_github_blueprint(client_id='a607b8394d9f07a317e6',client_secret='65e8c2f50cd9f633d8fa0b0308077f90d370c4e7')


#registering blueprints
app.register_blueprint(twitter_blueprint,url_prefix='/twitter_login')
app.register_blueprint(github_blueprint,url_prefix='/github_login')

@app.route('/')
def home():
    return ('You are at home')

@app.route('/twitter')
def twitter_login():
    if not twitter.authorized:
        return redirect(url_for('twitter.login'))

    account_info = twitter.get('account/settings.json')

    if account_info.ok:
        account_info_json=account_info.json()
        print('\n Response is :',account_info_json)
        return '<h1>Your Twitter name is @{}</h1>'.format(account_info_json['screen_name'])

    return '<h1>Request Failed!</h1>'

@app.route('/github')
def github_login():
    if not github.authorized:
        return redirect(url_for('github.login'))
    
    account_info=github.get('/user')
    if account_info.ok:
        account_info_json=account_info.json()
        return '<h1> Your Github name is {}'.format(account_info_json['login'])

    return '<h1>Request failed!</h1>'

if __name__=='__main__':
    app.run(debug=True)
