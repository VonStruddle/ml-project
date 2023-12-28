import csv

from sentence_transformers import SentenceTransformer, util

from models import Article, Paraphrase

# load articles from csv
# https://www.kaggle.com/datasets/hsankesara/medium-articles
reader = csv.DictReader(open('./articles.csv'))

# initialize articles and sentences lists (for sentences, use title only for now but could be improved by adding text by concatenating the two)
articles = []
sentences = []
for row in reader:
    articles.append({
        'title': row['title'],
        'text': row['text'],
        'link': row['link'],
    })
    sentences.append(row['title'])

# populate database with articles (could be improved by not deleting articles every time)
Article.delete().execute()
Article.insert_many(articles).execute()

# remove duplicates from sentences
sentences = list(set(sentences))

# load model (faster one for great results, could be switched to a more accurate one)
model = SentenceTransformer('all-MiniLM-L6-v2')

# compute paraphrases for each title (could be improved by setting up a minimum score, top_k can also be changed to return more paraphrases, setting at 20 only to go fast for the demo)
paraphrases = util.paraphrase_mining(
    model, sentences, show_progress_bar=True, top_k=20)

# store paraphrases in database (could be improved by not deleting paraphrases every time. Also, could be improved by bulk inserting but would mean a higher memory usage)
Paraphrase.delete().execute()
for paraphrase in paraphrases:
    score, i, j = paraphrase
    # find article ids for each paraphrase
    article_i = Article.select().where(Article.title == sentences[i]).get()
    article_j = Article.select().where(Article.title == sentences[j]).get()
    Paraphrase.create(
        pair=[article_i.id, article_j.id],
        score=score,
    )
    print(f'Paraphrase: {sentences[i]} <=> {sentences[j]}')
