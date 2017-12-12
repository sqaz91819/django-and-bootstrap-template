from django.shortcuts import render
from django.views import generic
from numpy import mean
from .models import Query, ScoreMovie, Score
from .crawler_api import mongodb
from .crawler_api.crawler import pre_art
from .model import KerasModel
import re
from datetime import datetime
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
            pos_articles, neu_articles, neg_articles = [], [], []
            labeled_score = []
            date_info = []
            example = []
            with mongodb.Mongodb(hash_check=False) as mgd:
                old_articles = mgd.search_title('articles', ''.join(form.query['search'].split()))
                new_articles = mgd.search_title('new_articles', ''.join(form.query['search'].split()))
                total = old_articles + new_articles
                split = len(old_articles)
                if total:
                    date_str = total[len(total) - 1]['date_added']
                    year, month = re.split('[-T]', date_str)[0:2]
                    year = int(year)
                    month = int(month)
                    for i in range(1, 7):
                        post_num = 0
                        for t in total:
                            if int(t['date_added'][0:4]) == year and int(t['date_added'][5:7]) == month:
                                post_num += 1

                        date_info.append([year, month, post_num])
                        month = month - 1
                        if month == 0:
                            year = year - 1
                            month = 12

                    nlp = [t['encode'] for t in total]
                    predict_result = model_handler.predict(nlp)
                    for ori, ft, cl, c2l in zip(total, predict_result['fasttext'], predict_result['cnn_lstm'], predict_result['cnn_2lstm']):
                        ori['fasttext'] = ft
                        ori['cnn_lstm'] = cl
                        ori['cnn_2lstm'] = c2l
                    pos_articles = [t for t in total if t['score'] > 3]
                    neu_articles = [t for t in total if t['score'] == 3]
                    neg_articles = [t for t in total if t['score'] < 3]
                    example.append(pre_art(pos_articles))
                    example.append(pre_art(neu_articles))
                    example.append(pre_art(neg_articles))
                    labeled_score = [t['score'] for t in total]

            try:
                st = datetime.now()
                stat_score = int((sum(labeled_score) / len(labeled_score)) * 21)
                stat_score_time = datetime.now() - st
                articles = len(labeled_score)
                fasttext_score = int(mean(predict_result['fasttext']) * 100)
                fasttext_time = predict_result['fasttext_time']
                cnn_lstm_score = int(mean(predict_result['cnn_lstm']) * 100)
                cnn_lstm_time = predict_result['cnn_lstm_time']
                cnn2lstm_score = int(mean(predict_result['cnn_2lstm']) * 100)
                cnn2lstm_time = predict_result['cnn_2lstm_time']

                if old_articles:
                    old_stat_score = int((sum(labeled_score[:split]) / len(labeled_score[:split])) * 21)
                    old_articles = len(labeled_score[:split])
                    old_fasttext_score = int(mean(predict_result['fasttext'][:split]) * 100)
                    old_cnn_lstm_score = int(mean(predict_result['cnn_lstm'][:split]) * 100)
                    old_cnn2lstm_score = int(mean(predict_result['cnn_2lstm'][:split]) * 100)
                else:
                    old_stat_score = 0
                    old_articles = 0
                    old_fasttext_score = 0
                    old_cnn_lstm_score = 0
                    old_cnn2lstm_score = 0

                if new_articles:
                    new_stat_score = int((sum(labeled_score[split:]) / len(labeled_score[split:])) * 21)
                    new_articles = len(labeled_score[split:])
                    new_fasttext_score = int(mean(predict_result['fasttext'][split:]) * 100)
                    new_cnn_lstm_score = int(mean(predict_result['cnn_lstm'][split:]) * 100)
                    new_cnn2lstm_score = int(mean(predict_result['cnn_2lstm'][split:]) * 100)
                else:
                    new_stat_score = 0
                    new_articles = 0
                    new_fasttext_score = 0
                    new_cnn_lstm_score = 0
                    new_cnn2lstm_score = 0
            except ZeroDivisionError:
                return render(request, self.template_name, {
                    'form': form,
                    'error_message': '請輸入正確電影名稱，若沒輸入錯誤，就是該電影還未加入資料庫請見諒',
                })

            return render(request, self.template_name, {
                'form': form,
                'search_valid': True,
                'query': form.query['search'],

                'old_movie_score': old_stat_score,
                'old_total': old_articles,
                'old_fast_text': old_fasttext_score,
                'old_cnn_lstm': old_cnn_lstm_score,
                'old_cnn_2lstm': old_cnn2lstm_score,

                'mean_dl_score': int(mean([fasttext_score, cnn_lstm_score, cnn2lstm_score])),
                'movie_score': stat_score,
                'total': articles,
                'fast_text': fasttext_score,
                'cnn_lstm': cnn_lstm_score,
                'cnn_2lstm': cnn2lstm_score,

                'new_movie_score': new_stat_score,
                'new_total': new_articles,
                'new_fast_text': new_fasttext_score,
                'new_cnn_lstm': new_cnn_lstm_score,
                'new_cnn_2lstm': new_cnn2lstm_score,

                'total_time': '{:05.2f} sec'.format(stat_score_time.total_seconds()),
                'fast_text_time': '{:05.2f} sec'.format(fasttext_time.total_seconds()),
                'cnn_lstm_time': '{:05.2f} sec'.format(cnn_lstm_time.total_seconds()),
                'cnn_2lstm_time': '{:05.2f} sec'.format(cnn2lstm_time.total_seconds()),

                'pos': len(pos_articles),
                'neg': len(neg_articles),
                'neutral': len(neu_articles),
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


class CompareView(generic.TemplateView):
    template_name = 'rate/compare.html'


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


def vote(request, month):
    with mongodb.Mongodb(hash_check=False) as mgd:
        lst = mgd.search_month('movie_by_month', '2017/' + month)

    return render(request, 'rate/compare.html', {'test': lst})
