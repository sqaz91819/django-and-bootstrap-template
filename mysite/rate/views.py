from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from numpy import mean
from .models import Query, ScoreMovie, Score
from .crawler_api import mongodb
from .model import KerasModel
from random import randrange
import re

# Create your views here.
model = KerasModel("model")


class HomeView(generic.TemplateView):
    template_name = 'rate/home.html'


class IndexView(generic.ListView):
    # fasttext = copy(fasttext_model)
    model = Query
    form_class = Query
    template_name = 'rate/index.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            temp, nlp = [[]], [[]]
            date_info = []
            example = {}
            articles_list = []
            with mongodb.Mongodb(hash_check=False) as mgd:
                temp = mgd.search_title('articles', form.query['search'])
                nlp = mgd.search_encode('jie_ba_Articles', form.query['search'])
                if temp:
                    date_str = temp[len(temp) - 1]['date_added']
                    year, month = re.split('[-T]', date_str)[0:2]
                    year = int(year)
                    month = int(month)
                    for i in range(1, 7):
                        post_num = mgd.search_date('articles001', month, year, form.query['search'])
                        date_info.append([year, month, post_num])
                        month = month - 1
                        if month == 0:
                            year = year - 1
                            month = 12
                    articles_list = temp
                    example = temp[randrange(0, len(temp))]

                nlp = [a['encode'] for a in nlp]
                pos_articles = [[t['title'], t['url']] for t in temp if t['score'] > 3]
                pos = [t['score'] for t in temp if t['score'] > 3]
                neg = [t['score'] for t in temp if 0 < t['score'] < 3]
                temp = [t['score'] for t in temp if t['score'] > 0]
                neutral = len(temp) - len(pos) - len(neg)
                if len(pos_articles) > 0:
                    about = True
                else:
                    about = False

                if len(example['content']) > 208:
                    example['content'] = example['content'][0:208]

            try:
                score = (sum(temp) / len(temp)) * 21
                articles = len(temp)
                predict_result = model.predict(nlp)
                fasttext_score = int(mean(predict_result) * 100)
            except ZeroDivisionError:
                return render(request, self.template_name, {
                    'form': form,
                    'error_message': '請輸入正確電影名稱，若沒輸入錯誤，就是該電影還未加入資料庫請見諒',
                })

            return render(request, self.template_name, {
                'form': form,
                'search_valid': True,
                'about': about,
                'query': form.query['search'],
                'movie_score': int(score),
                'articles': articles,
                'pos': len(pos),
                'neg': len(neg),
                'neutral': neutral,
                'pos_articles': pos_articles,
                'fast_text': fasttext_score,
                'art': example,
                'date_info': date_info,
                'articles_list': articles_list
            })

        return render(request, self.template_name, {
            'form': form,
            'error_message': 'Please enter movie name',
        })


class FormsView(generic.TemplateView):
    template_name = 'rate/forms.html'


class ModifyView(generic.ListView):
    model = ScoreMovie
    form_class = ScoreMovie
    template_name = 'rate/modify.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            score = form.score['score2']
            movie = form.score['movie2']
            with mongodb.Mongodb(hash_check=False) as mgd:
                article = mgd.search_dual('articles', 'title', movie, 'score', int(score))
            try:
                article['content'] = article['content'].replace(' ', '\n')
                article['id0'] = article['_id']
                return render(request, self.template_name, article)
            except IndexError:
                return render(request, 'rate/labelfix.html', {'error_message': '資料庫無此電影或沒有該範圍分數的文章'})
            except TypeError:
                return render(request, 'rate/labelfix.html', {'error_message': '資料庫無此電影或沒有該範圍分數的文章'})

        return render(request, 'rate/labelfix.html', {'error_message': 'Not valid input.'})


def score(request):
    if request.method == 'POST':
        form = Score(request.POST)

        if form.is_valid():
            id1 = form.id1['id1']
            get_score = form.id1['score1']

            with mongodb.Mongodb(hash_check=False) as mgd:
                mgd.update_score('articles', id1, int(get_score))
                # mgd.update_score('jie_ba_Articles', _id, get_score)
                mgd.update_modified(id1)

            return render(request, 'rate/forms.html')

        return render(request, 'rate/home.html', {'form': form, })
