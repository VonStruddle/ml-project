from os import getenv
from flask import Flask, jsonify, request
from dotenv import load_dotenv

from models import Article, Paraphrase

load_dotenv()

app = Flask(__name__)


# return related articles for a given article id
@app.route(('/get_related_articles/<article_id>'))
def get_related_articles(article_id):
    # get max number of related articles to return
    max_articles = request.args.get('max_articles', default=5, type=int)

    # find paraphrases for the given article id
    paraphrases = Paraphrase.select()\
        .where(Paraphrase.pair.contains([article_id]))\
        .order_by(Paraphrase.score.desc())[:max_articles]

    # find related articles for each paraphrase
    related_articles = []
    for paraphrase in paraphrases:
        related_article_id = paraphrase.pair[0] if paraphrase.pair[0] != article_id else paraphrase.pair[1]
        related_articles.append(Article.select().where(
            Article.id == related_article_id).get())

    # return related articles
    response_body = {
        'data': [{
            'title': el.title,
            'link': el.link,
        } for el in related_articles],
        'message': 'success',
        'length': len(related_articles),
    }
    return jsonify(response_body)


if __name__ == '__main__':
    app.run(debug=getenv('DEBUG', False))
