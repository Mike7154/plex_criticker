import criticker_functions
import plex_functions
import mlfiles
import sys
import general_functions
import mlscraping
# from importlib import reload
# reload(criticker_functions)
# reload(plex_functions)
# reload(mlfiles)
#reload(mlscraping)
#reload(general_functions)

print("Arguments include -f for file-read, -x for xml read, -i for import ratings, -c for collection build, -p for creating a collection sorted by PSI")
plex = plex_functions.return_plex_from_settings()
library = plex.library.section("TV Shows")
rating_dict_file = mlfiles.load_setting("Criticker", "ratings_json")
libraries = mlfiles.load_setting("Login","libraries")

if "-f" in sys.argv:
    ratings_file = mlfiles.load_setting("Criticker", "ratings_file")
    crit_list = criticker_functions.load_criticker_from_file(ratings_file, rating_dict_file)
    criticker_functions.save_crit_dict(crit_list, rating_dict_file)

if "-x" in sys.argv:
    url = mlfiles.load_setting("Criticker", "xml")
    crit_list = criticker_functions.load_criticker_from_xml(url, rating_dict_file)
    criticker_functions.save_crit_dict(crit_list, rating_dict_file)

#library = libraries[0]
if "-i" in sys.argv:
    crit_list = criticker_functions.load_crit_dict(rating_dict_file)
    criticker_functions.import_criticker_rating(plex, crit_list, libraries)
    criticker_functions.save_crit_dict(crit_list, rating_dict_file)

if "-c" in sys.argv:
    libraries = mlfiles.load_setting("Login","libraries")
    collection = mlfiles.load_setting("Criticker", "collection")
    rating_cutoff = mlfiles.load_setting("Criticker","rating_cutoff")
    crit_list = criticker_functions.load_crit_dict(rating_dict_file)
    criticker_functions.import_criticker_collection(plex, crit_list, collection, libraries, rating_cutoff, 'rating', 'rating_date')

if "-p" in sys.argv:
    rating_dict = mlfiles.load_dict(rating_dict_file)
    rating_cutoff = mlfiles.load_setting("Criticker","rating_cutoff")
    collection = mlfiles.load_setting("Criticker","psi_collection")
    crit_list = criticker_functions.import_psi(plex, rating_dict, rating_dict_file, libraries)
    rating_dict = criticker_functions.save_crit_dict(crit_list, rating_dict_file)
    crit_list = criticker_functions.load_crit_dict(rating_dict_file)
    new_crit_list = []
    for crit in crit_list:
        if crit.rating is  None:
            new_crit_list.append(crit)
        else:
            if crit.rating >= rating_cutoff:
                new_crit_list.append(crit)
    crit_list = new_crit_list
    criticker_functions.import_criticker_collection(plex, crit_list, collection, libraries, rating_cutoff+3, 'psi', 'psi_date')


if "-test" in sys.argv:
    from scipy.stats import percentileofscore
    from tqdm import tqdm
    collection = mlfiles.load_setting("Misc", "weighted_collection")
    crit_list = criticker_functions.load_crit_dict(rating_dict_file)
    criticker_functions.import_ratings_shuffle(plex, crit_list, libraries, collection)

print("END OF SCRIPT")


