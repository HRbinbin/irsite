from django.test import TestCase
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "irsite.settings")
django.setup()
from ir import models

# Create your tests here.
file = open('C:/Users/Ruibin/Downloads/cutIdData.txt', 'r', encoding='utf-8')
lines = file.readlines()
file.close()

models.Abstract.objects.all().delete()
for i in lines:
    row = models.Abstract(
        id=i.replace('\n', '').split('\u0001')[0].replace(' ', ''),
        title=i.replace('\n', '').split('\u0001')[1].replace(' ', ''),
        author=i.replace('\n', '').split('\u0001')[2].strip().replace(' ', ';'),
        publisher=i.replace('\n', '').split('\u0001')[3].replace(' ', ';'),
        abstract=i.replace('\n', '').split('\u0001')[4].replace(' ', ''),
    )
    row.save()
    for keyword in i.replace('\n', '').split('\u0001')[5].strip().split(' '):
        try:
            row.keywords.add(models.Keyword.objects.all().get(keyword=keyword))
        except:
            print(keyword)
            continue
    # break
    print(i.replace('\n', '').split('\u0001')[1].replace(' ', ''))
