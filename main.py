from flask import Flask, render_template, send_file
from markdown import markdown
from db import DB
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)
r = DB()

@app.route('/')
def home():
    return render_template("template.html", body=markdown(read_file("static/home.md")))

@app.route('/articles/<site>/')
def load_article(site):
    '''Capture a given article page and load it'''
    article = r.get_article(site)
    body = markdown(read_file(article["file"]))
    return render_template("articletemplate.html", body=body)

@app.route('/articles/<article>/img/<image>')
def get_article_images(article, image):
    '''Capture a url for an image in an article and return the file'''
    return send_file(f"static/articles/{article}/img/{image}", mimetype='image/png')

@app.route('/articles/')
def articles_page():
    '''Render the main articles page'''
    articles = sorted(r.get_all_articles(), reverse=True, key=lambda d: d['id'])
    html = ['<div class="article">']
    for article in articles:
        html.append(f'<a href="{article["url"]}"><h2>{article["title"]}</h2><p>{article["date"]}<br>{article["desc"]}</p>')
    html.append("</div>")
    return render_template("articletemplate.html", body="".join(html))

@app.route("/card")
def get_card():
    return send_file("static/business_card")

@app.route("/rss.xml")
@app.route("/rss")
def get_rss():
    return send_file("static/rss.xml")

@app.route('/css/<file>')
def get_css(file):
    return send_file(f"static/css/{file}", mimetype='text/css')

@app.route('/favicon.ico')
def get_favicon():
    return send_file("static/favicon.ico", mimetype='image/ico')

@app.route('/robots.txt')
def get_robots():
    return send_file("static/robots.txt", mimetype='text/text')

@app.route("/testpage")
def test_page():
    return render_template("template.html", body=read_file("static/testpage.html"))

@app.errorhandler(404)
@app.errorhandler(500)
def page_not_found(e):
    return render_template('template.html', body=markdown(read_file("static/404.md")))

def read_file(file):
    '''Read a given html file and return string'''
    file = open(file, "r")
    body = file.read()
    file.close()
    return body

if __name__ == "__main__":
    app.run(host="0.0.0.0")

