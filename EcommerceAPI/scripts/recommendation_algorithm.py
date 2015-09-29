__author__ = 'Duy'

import goodreads_api as gr_api
import word_similarity_algorithm as similar_alg
import time

def resem(source_book_id, candidate_book_id):
    sb_shelves = gr_api.get_shelves_of_book_on_cloud(source_book_id)
    cb_shelves = gr_api.get_shelves_of_book_on_cloud(candidate_book_id)

    total_min = 0
    for sb in sb_shelves:
        total_similar = 0
        for cb in cb_shelves:
            total_similar += similar_alg.similarity_measure(sb, cb)
            # sim = similar_alg.similarity_measure(sb, cb)
            # total_similar += sim
            # print "sim between %s and %s : %s" %(sb, cb, sim)
        total_min += min(total_similar, 1)
        # print "min : %s" % min(total_similar, 1)

    return total_min


def close(sb_gr_shelves, gr_friend_id):
    # sb_gr_shelves = gr_api.get_user_book_shelves(gr_api.get_auth_user_id(), source_book_id)
    print "sb_gr : %s" %sb_gr_shelves
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


def select_candidate_set():

    return [{"book_id" : 1234, "friend_id" : 4567}]


def recommend_book(list_book_in_profile, candidate_set):
    list_recommended_book = []
    ranking_for_each_book = []

    for user_book in list_book_in_profile:
        ranking_for_book = []
        for candidate in candidate_set:
            resem_degree = resem(user_book, candidate.get("book_id"))
            interest_degree = close(user_book.get("list_shelf"), candidate.get("friend_id"))
            rank_point = resem_degree * interest_degree
            ranking_for_book.append({"book_id" : candidate.get("book_id"), "rank_point" : rank_point})
        ranking_for_book.append({"book_in_profile_id" : user_book, "candidate_rank_point" : ranking_for_book})

    return list_recommended_book


start = time.clock()
# print(resem(23435542, 148050))
# print close(gr_api.get_user_books(gr_api.get_auth_user_id())[0].get("list_shelf"), 46109817)
print "Spending time : %s" % (time.clock() - start)