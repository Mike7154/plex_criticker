import json
from datetime import datetime
import re
import urllib.parse
import ruamel.yaml
import numpy as np
# -------------------------------------------------------------------------


class User:
    def __init__(self, username, gender, dob, age, playlist):
        self.username = username
        self.gender = gender
        self.dob = dob
        self.age = age
        self.playlist = playlist
# -------------------------------------------------------------------------
def string_to_date(string):
    return datetime.strptime(string, '%Y-%m-%d').date()
def date_to_string(date):
    return date.strftime('%Y-%m-%d')
def combine_unique(list1, list2):
    list = list1
    list.extend(list2)
    newlist = []
    for x in list:
        if x not in newlist:
            newlist.append(x)
    return newlist

def build_filter(text, labels):
    if text == '':
        filter = {'label': labels}
    else:
        text = urllib.parse.unquote(text)
        text = re.split(r'[&|]', text)
        filter = {}
        i = text[0]
        for i in text:
            pair = i.split("=")
            filter.update({pair[0]:pair[1].split(",")})
        label_filter = filter.get("label")
        if label_filter is None:
            label_filter = labels
        else:
            label_filter = combine_unique(label_filter, labels)
        filter.update({"label":label_filter})
    return filter

def str_to_date(str):
    return datetime.strptime(str, '%Y-%m-%d').date()


def get_age(date):
    age = datetime.now().date()-date
    age = age.total_seconds()
    age = age/3600
    age = age/24
    age = age/365
    return age


def difference(list1, list2):
    list_dif = [i for i in list1 if i not in list2]
    return list_dif

def reorder_list(list1, orderby):
    array = np.array(orderby)
    temp = array.argsort()
    ranks = np.empty_like(temp)
    ranks[temp] = np.arange(len(array))
    ranks = list(ranks)
    new_order = []
    for k in range(0,len(ranks)):
        new_order.extend([i for i in range(len(ranks)) if ranks[i] == k])
    return [list1[i] for i in new_order]
from random import random
from bisect import bisect_right
import numpy as np

def weighted_shuffle(a,w):
    r = np.empty_like(a)
    cumWeights = np.cumsum(w)
    for i in range(len(a)):
        rnd = random() * cumWeights[-1]
        j = bisect_right(cumWeights,rnd)
        #j = np.searchsorted(cumWeights, rnd, side='right')
        r[i] = a[j]
        cumWeights[j:] -= w[j]
    return r
def test_weighted(a,w, n = 100):
    tmean = []
    tmin = []
    tmid = []
    for i in range(1,n):
        ws = weighted_shuffle(a,w)
        nw = ws[0:round(len(w)*.05)+6]
        tmean.append(sum(nw)/len(nw))
        tmin.append(min(nw))
        tmid.append(median(nw))

    print(sum(tmean)/len(tmean))
    print(sum(tmin)/len(tmin))
    print(sum(tmid)/len(tmid))

def median(numbers):
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    if n % 2 == 0:
        median_value = (sorted_numbers[n//2 - 1] + sorted_numbers[n//2]) / 2
    else:
        median_value = sorted_numbers[n//2]
    return median_value