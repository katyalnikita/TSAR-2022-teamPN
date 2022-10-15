cskg_file = open("C:/Users/p00770556/Downloads/cskg/cskg.tsv", "r", encoding="utf8")
head_count = 0
unique_rels = []
final_dic = {}

import ppdb


ppdb_path = "C:/Users/p00770556/Downloads/ppdb-2.0-s-lexical"
ppdb_rules = ppdb.load_ppdb(ppdb_path)


def ppdb_phrase(word):
    try:
        a = list(ppdb_rules[word][0])
        return [i[0] for i in a]
    except:
        return []


# print(rhs)


#
# for line in cskg_file.readlines():
#     if head_count == 0:
#         head_count += 1
#         continue
#     all_r = line.strip().split("\t")
#     if len(all_r) == 10:
#         # print("SAHI")
#         id, node1, relation, node2, node1_label, node2_label, relation_label, relation_dimension, source, sentence = all_r
#     else:
#         id, node1, relation, node2, node1_label, node2_label, relation_label, relation_dimension, source = all_r
#     unique_rels.append(relation_label)
#     if node1 in final_dic:
#         temp = final_dic[node1]
#         temp = temp + [node2, relation_label]
#         final_dic[node1] = temp
#     else:
#         final_dic[node1] = [node2, relation_label]
# print("DONE")

#
# from nltk.corpus import verbnet
#
# all_possible_classes = verbnet.classids(lemma='add')
#
# verbnet.pprint_members('put-9.1.xml')
# # print(x)
