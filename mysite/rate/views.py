from django.shortcuts import render
from django.views import generic
from numpy import mean
from .models import Query, ScoreMovie, Score
from .crawler_api import mongodb
from .crawler_api.crawler import pre_art
from .model import KerasModel
import re
# Create your views here.


model_handler = KerasModel()


class HomeView(generic.TemplateView):
    template_name = 'rate/home.html'


class IndexView(generic.ListView):
    model = Query
    form_class = Query
    template_name = 'rate/index.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            temp, nlp = [[]], [[]]
            date_info = []
            example = []
            with mongodb.Mongodb(hash_check=False) as mgd:
                temp = mgd.search_title('articles', form.query['search'])
                if temp:
                    date_str = temp[len(temp) - 1]['date_added']
                    year, month = re.split('[-T]', date_str)[0:2]
                    year = int(year)
                    month = int(month)
                    for i in range(1, 7):
                        post_num = 0
                        for t in temp:
                            if int(t['date_added'][0:4]) == year and int(t['date_added'][5:7]) == month:
                                post_num += 1

                        date_info.append([year, month, post_num])
                        month = month - 1
                        if month == 0:
                            year = year - 1
                            month = 12

                    nlp = [t['encode'] for t in temp]
                    predict_result = model_handler.predict(nlp)
                    for ori, ft, cl, c2l in zip(temp, predict_result['fasttext'], predict_result['cnn_lstm'], predict_result['cnn_2lstm']):
                        ori['fasttext'] = ft
                        ori['cnn_lstm'] = cl
                        ori['cnn_2lstm'] = c2l
                    pos_articles = [t for t in temp if t['score'] > 3]
                    neu_articles = [t for t in temp if t['score'] == 3]
                    neg_articles = [t for t in temp if t['score'] < 3]
                    example.append(pre_art(temp))
                    example.append(pre_art(neu_articles))
                    example.append(pre_art(neg_articles))
                    temp = [t['score'] for t in temp]

            try:
                stat_score = (sum(temp) / len(temp)) * 21
                articles = len(temp)
                fasttext_score = int(mean(predict_result['fasttext']) * 100)
                cnn_lstm_score = int(mean(predict_result['cnn_lstm']) * 100)
                cnn2lstm_score = int(mean(predict_result['cnn_2lstm']) * 100)
            except ZeroDivisionError:
                return render(request, self.template_name, {
                    'form': form,
                    'error_message': '請輸入正確電影名稱，若沒輸入錯誤，就是該電影還未加入資料庫請見諒',
                })

            return render(request, self.template_name, {
                'form': form,
                'search_valid': True,
                'query': form.query['search'],
                'movie_score': int(stat_score),
                'total': articles,
                'pos': len(pos_articles),
                'neg': len(neg_articles),
                'neutral': len(neu_articles),
                'fast_text': fasttext_score,
                'cnn_lstm': cnn_lstm_score,
                'cnn_2lstm': cnn2lstm_score,
                'art': example,
                'date_info': date_info,
                'pos_articles': pos_articles,
                'neg_articles': neg_articles,
                'neu_articles': neu_articles
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
                mgd.update_modified(id1)

            return render(request, 'rate/forms.html')

        return render(request, 'rate/home.html', {'form': form, })
