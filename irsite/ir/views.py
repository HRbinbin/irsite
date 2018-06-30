from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from ir.models import Abstract
from ir.models import Keyword
import Jcore
import matplotlib.pyplot as plt
import numpy as np

# Create your views here.


class Ir:

    def __init__(self):
        self.keyword = ''
        self.result_list = []
        self.tp = {'T': []}
        self.fp = {'T': []}
        self.fn = {'T': []}
        self.tn = {'T': []}

    def index(self, request):
        return render(request, 'index.html')

    def search(self, request):
        self.tp = {'T': []}
        self.fp = {'T': []}
        self.fn = {'T': []}
        self.tn = {'T': []}
        if 'keywords' in request.GET:
            self.keyword = request.GET['keywords']
            self.result_list = Jcore.search(self.keyword)
            # print(kw_split.strip())
            result = {
                'keyword': request.GET['keywords'],
                'length': len(self.result_list) - 1,
                'check_words': 0,
                'results': []
            }
            check_words = Keyword.objects.filter(keyword=request.GET['keywords'])
            if len(check_words) > 0:
                result['check_words'] = 1

            for item in self.result_list:
                if item[0] == '':
                    continue

                result_item = {
                    'doc_id': item[0],
                    'score': item[1]
                }
                text = Abstract.objects.all().get(id=item[0]).abstract
                result_item['line'] = text.replace(self.keyword, '<strong style="color: 46a3ff;">' + self.keyword + '</strong>')
                result['results'].append(result_item)
        else:
            result = {
                'keyword': request.GET['keywords'],
                'length': 0,
                'results': []
            }
        # return HttpResponse(message)
        return render(request, 'result.html', result)

    def detail(self, request, doc_id):
        item = Abstract.objects.all().get(id=doc_id)
        results = {
            'Document_id': doc_id,
            'title': item.title,
            'author': item.author,
            'publisher': item.publisher,
            'content': item.abstract,
        }
        return render(request, 'news.html', results)

    def accuracy(self, request, keyword):
        self.result_list = Jcore.search(keyword)  # 检索结果
        result = {
            'keyword': keyword,
            'tp': 0,  # 返回相关
            'fn': 0,  # 未返回相关
            'fp': 0,  # 返回不相关
            'tn': 0,  # 未返回不相关
            'precise': 0,
            'recall': 0,
            'f': 0,
            'T': [],
            'rank': 0,  # there
            'pr': [],  # there
            'pmax': 0,  # there
            'pmin': 0,  # there
            'rmax': 0,  # there
            'rmin': 0  # there
        }
        id_list = []
        rank_index = 1  # there
        rank = []  # there
        tp_id_list = []
        # 被检索到
        objs = Abstract.objects.all()
        for item in self.result_list:
            if item[0] == '':
                continue
            id_list.append(int(item[0]))
            obj = objs.get(id=int(item[0].strip()))
            origin_words = [j.keyword for j in obj.keywords.all()]
            # 检索且相关
            if keyword in origin_words:
                # print(origin_words)
                # print(item[0])
                result['tp'] += 1
                self.tp['T'].append({
                    'id': item[0],
                    'rank': self.result_list.index(item) + 1,
                    'title': obj.title,
                    'abstract': obj.abstract.replace(keyword, '<strong>' + keyword + '</strong>'),
                    'tags': str(origin_words).replace('\'', '').replace('[', '').replace(']', '')
                })
                tp_id_list.append(item[0])
                rank.append(rank_index)  # there
            # 检索到但不相关
            else:
                result['fp'] += 1
                self.fp['T'].append({
                    'id': item[0],
                    'rank': self.result_list.index(item) + 1,
                    'title': obj.title,
                    'abstract': obj.abstract.replace(keyword, '<strong>' + keyword + '</strong>'),
                    'tags': str(origin_words).replace('\'', '').replace('[', '').replace(']', '')
                })
            rank_index += 1  # there
        total_item_numb = len(objs)

        # 未被检索到
        for index in list(set(list(range(0, total_item_numb))) - set(id_list)):
            obj = objs.get(id=index)
            origin_words = [j.keyword for j in obj.keywords.all()]
            # 未被检索到但相关
            if keyword in origin_words:
                # print(origin_words)
                result['fn'] += 1
                self.fn['T'].append({
                    'id': index,
                    'rank': None,
                    'title': obj.title,
                    'abstract': obj.abstract.replace(keyword, '<strong>' + keyword + '</strong>'),
                    'tags': str(origin_words).replace('\'', '').replace('[', '').replace(']', '')
                })
            # 未被检索到且不相关
            else:
                result['tn'] += 1
                self.tn['T'].append({
                    'id': index,
                    'rank': None,
                    'title': obj.title,
                    'abstract': obj.abstract.replace(keyword, '<strong>' + keyword + '</strong>'),
                    'tags': str(origin_words).replace('\'', '').replace('[', '').replace(']', '')
                })

        # 计算p-r曲线
        tp = 0  # there
        fp = 0  # there
        p = []
        r = []
        for item in self.result_list:  # 被检索到
            if item[0] == '':
                continue
            if item[0] in tp_id_list:  # 检索且相关
                tp += 1  # there
            else:  # 检索到但不相关
                fp += 1
            result['pr'].append([float(tp) / (tp + result['fn']), float(tp) / (tp + fp)])  # there
            p.append(float(tp) / (tp + fp))
            r.append(float(tp) / (tp + result['fn']))

        result['precise'] = result['tp'] / (result['tp'] + result['fp'])
        result['recall'] = result['tp'] / (result['tp'] + result['fn'])
        result['f'] = str(2 * result['precise'] * result['recall'] / (result['precise'] + result['recall']))[:5]
        result['precise'] = str(result['precise'])[:5]
        result['recall'] = str(result['recall'])[:5]
        for i in range(len(rank)):  # there
            result['rank'] += (i + 1) / rank[i]  # 计算AP
        result['rank'] = (result['rank'] / len(rank))  # there
        result['pmax'] = float(str(max(p))[:4])
        if result['pmax'] + 0.01 <= 1:
            result['pmax'] += 0.01
        result['pmax'] = str(result['pmax'])[:4]
        result['rmax'] = max(r)
        if result['rmax'] + 0.01 <= 1:
            result['rmax'] += 0.01
        result['rmax'] = str(result['rmax'])[:4]
        result['pmin'] = min(p)
        if result['pmin'] - 0.01 >= 0:
            result['pmin'] -= 0.01
        result['pmin'] = str(result['pmin'])[:4]
        result['rmin'] = min(r)
        if result['rmin'] - 0.01 >= 0:
            result['rmin'] -= 0.01
        result['rmin'] = str(result['rmin'])[:4]

        return render(request, 'accuracy.html', result)

    def list_tp(self, request, keyword):
        return render(request, 'list.html', self.tp)

    def list_fp(self, request, keyword):
        return render(request, 'list.html', self.fp)

    def list_fn(self, request, keyword):
        return render(request, 'list.html', self.fn)

    def list_tn(self, request, keyword):
        return render(request, 'list.html', self.tn)
