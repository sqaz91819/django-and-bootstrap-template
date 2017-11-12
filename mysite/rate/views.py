from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Query
from .crawler_api import mongodb
from .model import KerasModel

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
            with mongodb.Mongodb(hash_check=False) as mgd:
                temp = mgd.search_title('articles', form.query['search'])
                nlp = mgd.search_encode('jie_ba_Articles', form.query['search'])
                nlp = [a['encode'] for a in nlp]
                pos_articles = [[t['title'], t['url']] for t in temp if t['score'] > 3]
                pos = [t['score'] for t in temp if t['score'] > 3]
                neg = [t['score'] for t in temp if t['score'] == 3]
                temp = [t['score'] for t in temp if t['score'] > 0]
                neutral = len(temp) - len(pos) - len(neg)

            if len(pos_articles) > 0:
                about = True
            else:
                about = False

            try:
                score = (sum(temp) / len(temp)) * 21
                articles = len(temp)
                fasttext_score = int(sum(model.predict(nlp)) / len(temp) * 100)
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
            })

        return render(request, self.template_name, {
            'form': form,
            'error_message': 'Please enter movie name',
        })
