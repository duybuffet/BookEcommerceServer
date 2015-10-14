__author__ = 'Duy'

import goodreads_api as gr_api
import word_similarity_algorithm as similar_alg
import time
import operator

def resem(source_book_id, candidate_book_id):
    # can improve get_shelves_of_book_on_cloud by insert shelves to the local db
    sb_shelves = gr_api.get_shelves_of_book_on_cloud(source_book_id)
    # print "sb_shelves : %s"%sb_shelves
    cb_shelves = gr_api.get_shelves_of_book_on_cloud(candidate_book_id)
    # print "cb_shelves: %s"%cb_shelves

    total_min = 0
    for sb in sb_shelves:
        total_similar = 0
        for cb in cb_shelves:
            # total_similar += similar_alg.similarity_measure(sb, cb)
            if sb == cb:
                sim = 1
            else:
                sim = similar_alg.similarity_measure(sb, cb)
            total_similar += sim
            print "sim between %s and %s : %s" %(sb, cb, sim)
        total_min += min(total_similar, 1)
    return total_min


def close(sb_gr_shelves, gr_friend_id):
    # sb_gr_shelves = gr_api.get_user_book_shelves(gr_api.get_auth_user_id(), source_book_id)
    print "sb_gr : %s" % sb_gr_shelves
    gr_friend_shelves = gr_api.get_shelves_of_user(gr_friend_id)

    total_min = 0
    for sb in sb_gr_shelves:
        total_similar = 0
        for gr in gr_friend_shelves:
            # total_similar += similar_alg.similarity_measure(sb, gr)
            sim = similar_alg.similarity_measure(sb, gr)
            total_similar += sim
            print "sim between shelf %s and friend_%s : %s" %(sb, gr, sim)
        total_min += min(total_similar, 1)
        print "min : %s" % min(total_similar, 1)
    return total_min


def select_candidate_set(auth_user_id):
    auth_user_shelves = set(gr_api.get_shelves_of_user(auth_user_id))
    auth_user_friends = gr_api.get_user_friends(auth_user_id)
    auth_user_friends_with_shelves = []
    result_with_len = []
    candidate = []

    for frd in auth_user_friends:
        auth_user_friends_with_shelves.append({"friend_id": frd, "list_shelves": gr_api.get_shelves_of_user(frd)})

    for friends_shelves in auth_user_friends_with_shelves:
        length_friend_shelves = len(set(friends_shelves["list_shelves"]))
        if length_friend_shelves > 0:
            intersect_length = len(auth_user_shelves.intersection(set(friends_shelves["list_shelves"])))

            if (intersect_length > 0):
                ratio = float(intersect_length) / length_friend_shelves
                result = {"ratio": ratio,
                    "friend_id": friends_shelves["friend_id"]}
                print "ratio : %s"%ratio
                result_with_len.append(result)
            else:
                continue
        else:
            continue
    result_with_len.sort(key=operator.itemgetter('ratio'), reverse=True)

    if len(result_with_len) > 10:
        for res in result_with_len[0:10]:
            candidate.append({"friend_id": res["friend_id"], "book_ids": gr_api.get_user_books(res["friend_id"])})
    else:
        for res in result_with_len:
            candidate.append({"friend_id": res["friend_id"], "book_ids": gr_api.get_user_books(res["friend_id"])})

    # return [{"book_id" : 1234, "friend_id" : 4567}]
    return candidate


def recommend_book(list_book_in_profile, candidate_set):
    list_recommended_book = []
    ranking_for_each_book = []

    for user_book in list_book_in_profile:
        for candidate in candidate_set:
            interest_degree = close(user_book.get("list_shelf"), candidate.get("friend_id"))
            for book in candidate.get("book_ids"):
                resem_degree = resem(user_book, book.get("book_id"))
                rank_point = resem_degree * interest_degree
                ranking_for_each_book.append({"book_id": book, "rank_point": rank_point})

    ranking_for_each_book.sort(key=operator.itemgetter('rank_point'), reverse=True)
    if len(ranking_for_each_book) > 10:
        for res in ranking_for_each_book[0:10]:
            list_recommended_book.append(res["book_id"])
    else:
        for res in ranking_for_each_book:
            list_recommended_book.append(res["book_id"])
    return list_recommended_book


start = time.clock()
# print(resem(50, 50))
# print close(gr_api.get_user_books(gr_api.get_auth_user_id())[0].get("list_shelf"), 46109817)
# print select_candidate_set(gr_api.get_auth_user_id())
id = gr_api.get_auth_user_id()
print "list recommend : %s"% recommend_book(gr_api.get_user_books(id), select_candidate_set(id))
print "Spending time : %s" % (time.clock() - start)