from django.test import TestCase
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "irsite.settings")
django.setup()
from ir import models
import Jcore
import matplotlib.pyplot as plt
import numpy as np


def check(keyword):
    result_list = Jcore.search(keyword)
    result = {
        'keyword': keyword,
        'tp': 0,  # 返回相关
        'fn': 0,  # 未返回相关
        'fp': 0,  # 返回不相关
        'tn': 0,  # 未返回不相关
        'precision': 0,
        'recall': 0,
        'f': 0,
        'ap': 0,  # there
        'p': [],  # there
        'r': []  # there
    }
    id_list = []
    rank_index = 1  # there
    rank = []  # there
    # print(result_list)
    for item in result_list:  # 被检索到
        # print(item)
        if item[0] == '':
            continue
        id_list.append(int(item[0]))
        obj = models.Abstract.objects.all().get(id=int(item[0].strip()))
        origin_words = [j.keyword for j in obj.keywords.all()]
        # print(keyword in origin_words)
        if keyword in origin_words:  # 检索且相关
            # print(origin_words)
            # print(item[0])
            result['tp'] += 1
            rank.append(rank_index)  # there
        else:  # 检索到但不相关
            result['fp'] += 1
        rank_index += 1  # there
    total_item_numb = len(models.Abstract.objects.all())

    for index in list(set(list(range(0, total_item_numb))) - set(id_list)):  # 未被检索到
        obj = models.Abstract.objects.all().get(id=index)
        origin_words = [j.keyword for j in obj.keywords.all()]
        if keyword in origin_words:  # 未被检索到但相关
            # print(origin_words)
            result['fn'] += 1
        else:  # 未被检索到且不相关
            result['tn'] += 1

    # 计算p-r曲线
    # tp = 0  # there
    # fp = 0  # there
    # for item in result_list:  # 被检索到
    #     if item[0] == '':
    #         continue
    #     id_list.append(int(item[0]))
    #     obj = models.Abstract.objects.all().get(id=int(item[0].strip()))
    #     origin_words = [j.keyword for j in obj.keywords.all()]
    #     if keyword in origin_words:  # 检索且相关
    #         # print(origin_words)
    #         # print(item[0])
    #         tp += 1  # there
    #     else:  # 检索到但不相关
    #         fp += 1
        # result['p'].append(float(tp) / (tp + fp))  # there
        # print('tp:' + str(tp) + ' ' + 'fp:' + str(fp))
        # result['r'].append(float(tp) / (tp + result['fn']))  # there

    result['precision'] = float(result['tp']) / (result['tp'] + result['fp'])
    result['recall'] = float(result['tp']) / (result['tp'] + result['fn'])
    result['f'] = 2.0 * result['precision'] * result['recall'] / (result['precision'] + result['recall'])
    for i in rank:  # there
        result['ap'] += float(rank.index(i) + 1)/i  # there
    result['ap'] = result['ap'] / len(rank)  # there
    return result


if __name__ == '__main__':
    file = open('C:/Users/Ruibin/Desktop/reference.csv', 'r', encoding='utf-8')
    lines = file.readlines()
    file.close()
    #
    # for line in lines:
    #     keyword = line.replace('\n', '').strip().split(',')
    #     if int(keyword[1]) > 10:
    #         # print(check(keyword[0]))
    #         try:
    #             string = ''
    #             check_result = check(keyword[0])
    #             for i in check_result:
    #                 string = string + str(check_result[i]) + ','
    #             print(string[:-1])
    #         except:
    #             print('-----------------------------------')
    #             print('Wrong: ' + keyword[0])
    #             print('-----------------------------------')
    # sheng = len(lines)
    # for line in lines:
    #     row = line.replace('\n', '').strip().split(',')
    #     if int(row[1]) > 10 and lines.index(line) > 89:
    #         keyword = row[0]
    #         try:
    #             result = check(keyword)
    #             p = np.array(result['p'])
    #             r = np.array(result['r'])
    #
    #             plt.figure(figsize=(10, 5))
    #
    #             # 画图
    #             plt.plot(r, p)  # 默认
    #
    #             # 所有绘图对象
    #
    #             plt.savefig('E:/IrAssignment/irsite/templates/static/images/' + keyword + '.png')
    #             sheng -= 1
    #             print('画完' + keyword + ', 还剩' + str(sheng))
    #             plt.close()
    #             # plt.show()
    #         except:
    #             print('=====================')
    #             print(keyword)
    #             print('=====================')

    count = 0
    total = 0
    for line in lines:
        row = line.replace('\n', '').strip()
        keyword = row.replace('\ufeff', '')
        # print(keyword)
        # count += 1
        try:
            # result = {
            #     'keyword': keyword,
            #     'tp': 0,  # 返回相关
            #     'fn': 0,  # 未返回相关
            #     'fp': 0,  # 返回不相关
            #     'tn': 0,  # 未返回不相关
            #     'precision': 0,
            #     'recall': 0,
            #     'f': 0,
            #     'ap': 0,  # there
            #     'p': [],  # there
            #     'r': []  # there
            # }
            result = check(keyword)
            print(result['keyword'] + ',' + str(result['tp']) + ',' + str(result['fn']) + ',' + str(
                result['fp']) + ',' + str(result[
                                              'tn']) + ',' + str(result['precision']) + ',' + str(
                result['recall']) + ',' + str(result['f']) + ',' + str(result['ap']))
        except:
            print(keyword + ',0,0,0,0,0,0,0,0')



