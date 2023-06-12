import plex_functions
import csv
import urllib.parse
import general_functions
import mlfiles
import xmltodict
import requests
import mlscraping
from scipy.stats import percentileofscore
from tqdm import tqdm
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta

class criticker_item:
    def __init__(self, imdb, guid = None, url = None, rating = None, psi = None, rating_date = None, import_date = None, psi_date = None):
        self.imdb = imdb
        self.guid = guid
        self.rating = rating
        self.psi = psi
        self.url = url
        self.rating_date = rating_date
        self.import_date = import_date
        self.psi_date = psi_date
def criticker_to_dict(criticker):
    c = criticker
    if c.rating_date is None:
        rating_date = None
    else:
        rating_date = general_functions.date_to_string(c.rating_date)
    if c.import_date is None:
        import_date = None
    else:
        import_date = general_functions.date_to_string(c.import_date)
    if c.psi_date is None:
        psi_date = None
    else:
        psi_date = general_functions.date_to_string(c.psi_date)
    dict = {'url':c.url, 'guid':c.guid, 'rating':c.rating, 'psi':c.psi, 'rating_date':rating_date, 'import_date':import_date, 'psi_date':psi_date}
    return dict

def dict_to_criticker(dictionary, imdb):
    dict = check_dict(dictionary, imdb)
    if dict.get('rating_date') is None:
        rating_date = None
    else:
        rating_date = general_functions.string_to_date(dict.get('rating_date'))
    if dict.get('import_date') is None:
        import_date = None
    else:
        import_date = general_functions.string_to_date(dict.get('import_date'))
    if dict.get('psi_date') is None:
        psi_date = None
    else:
        psi_date = general_functions.string_to_date(dict.get('psi_date'))
    return criticker_item(imdb,dict.get('guid'), dict.get('url'), dict.get('rating'), dict.get('psi'), rating_date, import_date, psi_date)

def cstr_to_date(string):
    return datetime.strptime(string,'%b %d %Y, %H:%M').date()

def check_dict(dict, id):
    if id not in dict:
        dict.update({id: {}})
    return dict.get(id)


def save_crit_dict(crit_list, dict_file):
    mlfiles.create_json(dict_file)
    dictionary = mlfiles.load_dict(dict_file)
    for crit in crit_list:
        new_dict = criticker_to_dict(crit)
        dictionary.update({crit.imdb: new_dict})
    mlfiles.write_dict(dict_file, dictionary)
    return dictionary

def load_crit_dict(dictionary_file):
    mlfiles.create_json(dictionary_file)
    dict = mlfiles.load_dict(dictionary_file)
    crit_list = []
    for imdb in dict.keys():
        crit = dict_to_criticker(dict, imdb)
        crit_list.append(crit)
    return crit_list


def load_criticker_from_file(ratings_file = "ratings.csv", dict_file = "ratings.json"):
    mlfiles.create_json(dict_file)
    ratings_dict = mlfiles.load_dict(dict_file)
    ratings = csv.DictReader(open(ratings_file))
    crit_list = []
    for rating in ratings:
        imdb = rating.get(' IMDB ID')
        crit = dict_to_criticker(ratings_dict, imdb)
        crit.rating_date = cstr_to_date(rating.get(' Date Rated'))
        crit.url = rating.get(" URL")
        crit.rating = int(rating.get('Score'))
        crit_list.append(crit)
    return crit_list

def load_criticker_from_xml(url, dict_file = "ratings.json"):
        mlfiles.create_json(dict_file)
        ratings_dict = mlfiles.load_dict(dict_file)
        page = requests.get(url)
        recent_ratings=xmltodict.parse(page.text)
        recent_ratings = recent_ratings.get("recentratings")
        films = recent_ratings.get("film")
        crit_list = []
        for film in films:
            imdb = film.get('imdbid')
            crit = dict_to_criticker(ratings_dict, imdb)
            crit.rating = int(film.get('score'))
            crit.rating_date = cstr_to_date(film.get('reviewdate'))
            crit.url = film.get('filmlink')
            crit_list.append(crit)
        return crit_list

def import_criticker_collection(plex, crit_list, collection, libraries = ["Movies", "TV Shows"], rating_cutoff = 60, metric = 'rating', u_metric = 'rating_date'):
    for library in libraries:
        lib = plex.library.section(library)
        print(library)
        a_items = []
        a_ratings = []
        a_updated = [general_functions.string_to_date("1900-01-01")]
        for crit in crit_list:
            score = getattr(crit, metric)
            updated = getattr(crit, u_metric)
            #print(score)
            try:
                if score >= rating_cutoff:
                    #print(crit.guid)
                    item = lib.getGuid(crit.guid)
                    a_items.append(item)
                    a_ratings.append(100-score)
                    a_updated.append(updated)
                    #print(item)
            except:
                next
                #print("next")
        if collection is not None:
            if plex_functions.collection_exists(collection, lib) == False:
                i = lib.all()[0]
                col = lib.createCollection(collection, i, sort = "custom")
                col.removeItems(i)
            col = lib.collection(collection)
            print(str(len(a_items)) + " movies meet import criteria")
            if col.updatedAt.date() <= max(a_updated): #if collection is older than the newest rating
                print("importing and reordering plex collection")
                items = general_functions.reorder_list(a_items, a_ratings)
                plex_functions.add_ordered_collection(col, items)
def import_criticker_rating(plex, crit_list, libraries):
    for library in libraries:
        lib = plex.library.section(library)
        for crit in crit_list:
            if crit.guid is None:
                id = 'imdb://'+ crit.imdb
            else:
                id = crit.guid
            if crit.import_date is None:
                crit.import_date = general_functions.string_to_date("1900-01-01")
            try:
                if crit.rating_date >= crit.import_date:
                    item = lib.getGuid(id)
                    crit.guid = item.guid
                    item.rate(crit.rating/10)
                    crit.import_date = datetime.now().date()
                    print("rating " + id + " " + item.title + " " + str(crit.rating))
            except:
                next


def import_psi(plex, rating_dict, rating_dict_file, libraries):
    login_post_url = "https://www.criticker.com/authenticate.php"
    cred = mlfiles.hash("criticker_user","Criticker","criticker_password","Criticker","chash","Misc")
    form_data = {'si_username': cred.u, 'si_password': cred.p}
    sesh = mlscraping.login_session(login_post_url, form_data)
    search_prefix = mlfiles.load_setting("Criticker", "search_prefix")
    search_suffix = mlfiles.load_setting("Criticker","search_suffix")
    search_matches = mlfiles.load_setting("Criticker","url_type")
    ratings_dict = mlfiles.load_dict(rating_dict_file)
    psi_url = mlfiles.load_setting("Criticker","psi_url")
    psi_interval = mlfiles.load_setting("Criticker","psi_interval")
    crit_list = []
    for library in libraries:
        lib = plex.library.section(library)
        all_items = lib.all()
        lib_type = lib.type
        if lib_type == 'movie':
            search_match = search_matches[0]
        elif lib_type == 'show':
            search_match = search_matches[1]
        else:
            next
        i = 0
        for item in all_items:
            skip = False
            i_title = item.title
            imdb = plex_functions.get_imdb(item)
            if imdb is None:
                skip = True
            crit = dict_to_criticker(ratings_dict, imdb)
            crit.guid = item.guid
            if crit.psi_date is not None:
                if crit.psi_date + timedelta(days = psi_interval) >= datetime.now().date():
                    skip = True
            if skip == False:
                #search_text = 'data-id="'+imdb+'"'
                search_text = imdb
                search_url = search_prefix + i_title + search_suffix
                if crit.url is None:
                    page = mlscraping.pages_search(sesh, search_url, search_text, search_match)
                else:
                    page = sesh.get(crit.url)
                crit = get_psi(sesh, crit, page, psi_url)
                print(i_title + " has a PSI of " + str(crit.psi))
                crit_list.append(crit)
                i = i + 1
                if i % 15 == 0:
                    ratings_dict = save_crit_dict(crit_list, rating_dict_file)
                    print("saving dictionary")
    return crit_list

def get_psi(sesh, crit, page = None, psi_url = 'https://www.criticker.com/psi/'):
    crit.psi_date = datetime.now().date()
    if crit.url is None and page is not None:
        crit.url = page.url
    if page is None and crit.url is None:
        print("could not find a match for " + crit.imdb)
        return crit
    if page is None:
        page = sesh.get(crit.url)
    psi_urls = mlscraping.get_matching_urls(page, psi_url)
    if len(psi_urls) ==0:
        return crit
    page = sesh.get(psi_urls[0])
    soup = BeautifulSoup(page.content, "html.parser")
    psi = mlscraping.cl_search_txt(soup, "div[class^=psi_div]")
    try:
        crit.psi = int(psi)
    except:
        crit.psi = None
    return crit

def import_ratings_shuffle(plex, crit_list, libraries, collection):
    for library in libraries:
        lib = plex.library.section(library)
        crit = crit_list[100]
        guids = []
        ratings = []
        a_ratings = []
        c_ratings = []
        psis = []
        dur_scores = []
        for crit in tqdm(crit_list):
            if crit.guid is not None:
                try:
                    item = lib.getGuid(crit.guid)
                    guids.append(crit.guid)
                    c_ratings.append(item.rating)
                    ratings.append(crit.rating)
                    a_ratings.append(item.audienceRating)
                    psis.append(crit.psi)
                    d = item.duration/(60*1000)
                    if 90 <= d <= 120:
                        dur_scores.append(100)
                    else:
                        dur_scores.append(100-min(abs(120-d), abs(90-d)))
                except:
                    next
        final_scores = []
        for i in tqdm(range(0,len(guids))):
            guid = guids[i]
            rating = ratings[i]
            weight = [10,5,3,7,2]
            d_score = percentileofscore([d for d in dur_scores if d < 100], dur_scores[i])
            if rating == None:
                rating = 0
                weight[0] = 1
                weight[3] = 10
            else:
                rating = percentileofscore([d for d in ratings if d is not None], rating)
            if a_ratings[i] is None:
                a_rating = 0
                weight[1] = 1
            else:
                a_rating = percentileofscore([d for d in a_ratings if d is not None] , a_ratings[i])
            if c_ratings[i] is None:
                c_rating = 0
                weight[2] = 1
            else:
                c_rating = percentileofscore([d for d in a_ratings if d is not None] , c_ratings[i])
            if psis[i] is None:
                psi = 0
                weight[3] = 1
            else:
                psi = percentileofscore([d for d in psis if d is not None] , psis[i])
            scores = [rating, a_rating, c_rating, psi, d_score]
            scores
            weight = [weight[l] for l in range(0,len(weight)) if scores[l] is not None]
            scores = [scores[l] for l in range(0,len(scores)) if scores[l] is not None]
            product = []
            for x, y in zip(weight, scores):
                product.append(x*y)
            final_score = sum(product)/sum(weight)
            final_scores.append(final_score)
        percentile = []
        for s in final_scores:
            percentile.append(percentileofscore(final_scores, s))
        p2 = [p ** 1.54 for p in percentile]
        new_list = general_functions.weighted_shuffle(guids, p2)
        new_list = new_list.tolist()
        new_list = new_list[0:round(len(new_list)*.05)+6]
        items = []
        for guid in tqdm(new_list):
            item = lib.getGuid(guid)
            items.append(item)
        plex_functions.create_ordered_collection(lib, collection, items)
