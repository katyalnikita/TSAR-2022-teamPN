import difflib

from nlp_utils import NlpUtils
from test_cskg import ppdb_phrase
from verb_utils import VerbUtils
from fitbert import FitBert


class SM(difflib.SequenceMatcher):
    def __init__(self, a):
        super().__init__(a=a)

    def __call__(self, b):
        self.set_seq2(b)
        return self.ratio()


from transformers import pipeline

THRESHOLD_BERT = 0.02 #run1
# THRESHOLD_BERT = 0.03 #run2
# THRESHOLD_BERT = 0.01 #run3
# THRESHOLD_BERT = 0.02 #run4
# THRESHOLD_BERT = 0.02 #run5
WINDOW_SIZE = 9 #run1
# WINDOW_SIZE = 9 #run2
# WINDOW_SIZE = 9 #run3
# WINDOW_SIZE = 15 #run4
# WINDOW_SIZE = 5 #run4
# unmasker = pipeline('fill-mask', model='C:/Users/p00770556/Projects/distilbert-base-uncased/')
unmasker = pipeline('fill-mask', model='C:/Users/p00770556/Projects/bert-large-uncased-whole-word-masking/')

####KG####
file_kg = open("KG_defs.txt", "r")
kg_def = {}
for line in file_kg.readlines():
    line_list = line.strip().split("\t")
    tem_def = []
    for k in line_list[1:]:
        if len(k.split("_")) == 1 and "-" not in k and len(k) > 3:
            tem_def.append(k.lower())
    kg_def[line_list[0]] = tem_def


class TransformerUtils:
    def __init__(self, bert_threshold=THRESHOLD_BERT, window_size=WINDOW_SIZE):
        self.THRESHOLD_BERT = bert_threshold
        self.WINDOW_SIZE = window_size

    def get_vic(self, sentence, word):
        words = sentence.split(" ")
        water = SM(word)
        best = max(words, key=water)
        index_1 = words.index(best)
        strt_idx = index_1 - self.WINDOW_SIZE
        end_idx = index_1 + self.WINDOW_SIZE
        if strt_idx < 0:
            strt_idx = 0
        if end_idx > len(words) - 1:
            end_idx = len(words) - 1
        return " ".join(words[strt_idx: end_idx + 1])

    def pred_transformer(self, sent, word):
        window_masked_sent = self.get_vic(sent, word).replace(word, "[MASK]")
        predicted_words_window = [(d["token_str"]) for d in unmasker(window_masked_sent) if
                                  d["score"] > self.THRESHOLD_BERT]
        return predicted_words_window


def main():
    ts = TransformerUtils()
    vp = VerbUtils()
    tsv_data_file = 'datasets/trial/tsar2022_en_trial_none.tsv'
    out_data_file = 'datasets/trial/tsar2022_en_teamPN_1.tsv'
    file_out = open(out_data_file,"w", encoding="utf8")
    # tsv_data_file = 'datasets/trial/tsar2022_en_trial_none.tsv'
    s = NlpUtils()
    single_verb_cases = 0
    total_verb_cases = 0
    all_cases = 0
    # fb = FitBert(model_name="C:/Users/p00770556/Projects/distilbert-base-uncased/", disable_gpu=True)
    fb = FitBert(model_name="C:/Users/p00770556/Projects/bert-large-uncased-whole-word-masking/", disable_gpu=True)
    with open(tsv_data_file, encoding="utf8") as f:
        for line in f:
            all_cases += 1
            sentence, phrase = line.strip().split('\t')
            print("####################################################################")
            # print(sentence)
            # print(phrase)
            vn_p = []
            ts_p = ts.pred_transformer(sentence, phrase)
            pos_tag_phrase = s.get_pos(sentence, phrase)
            print("POS: ", pos_tag_phrase)
            if pos_tag_phrase == "VERB":
                total_verb_cases += 1
                try:
                    tense, ordn = vp.get_verb_form(phrase)
                    for verb2 in ts_p:
                        verb2 = vp.get_lemma_verb(verb2)
                        temp.append(vp.set_verb_form(verb2, tense, ordn))
                    ts_p = temp

                except:
                    pass
                vn_p = vp.get_alternate_verbs(phrase, ts_p)
                # print("VN: ", vn_p)
                temp = []
                # print("TS(no inflexion) : ", ts_p)
            try:
                kg_p = kg_def[phrase]
            except:
                kg_p = []

            pp_p = []
            pp_temp = []
            if pos_tag_phrase == "NOUN" or pos_tag_phrase == "ADJ":
                singular_phrase = s.set_noun_quantity(noun=phrase, quantity="singular")
                multiple_phrase = s.set_noun_quantity(noun=phrase, quantity="plural")
                single_pp, plu_pp, def_pp = ppdb_phrase(singular_phrase), ppdb_phrase(multiple_phrase), ppdb_phrase(
                    phrase)
                # if pos_tag_phrase == "NOUN":
                #     pp_temp = single_pp + plu_pp + def_pp+kg_p
                # else:
                pp_temp = single_pp + plu_pp + def_pp

                print("PPD_Stats: ", len(single_pp), len(plu_pp), len(def_pp))
                pp_temp = list(set(pp_temp))
                phrase_quantity = s.get_noun_quantity(phrase)
                if phrase_quantity:
                    for k in pp_temp:
                        pp_p.append(s.set_noun_quantity(k, phrase_quantity))
                else:
                    pp_p = pp_temp
            else:
                pp_p = ppdb_phrase(phrase)
            # print("PB: ", pp_p)
            masked_string = ts.get_vic(sentence, phrase).replace(phrase, "***mask***")
            # old full sent
            # masked_string = sentence.replace(phrase, "***mask***")
            ranked_pp_p = fb.rank(masked_string, options=pp_p)
            if pos_tag_phrase=="NOUN":
                kg_done= []
                phrase_quantity = s.get_noun_quantity(phrase)
                if phrase_quantity:
                    for k in kg_p:
                        kg_done.append(s.set_noun_quantity(k, phrase_quantity))
                else:
                    kg_done = kg_p
                ranked_vn_and_trans = fb.rank(masked_string, options=vn_p + ts_p + kg_done)
                # ranked_vn_and_trans = fb.rank(masked_string, options=vn_p + ts_p )
            else:
                ranked_vn_and_trans = fb.rank(masked_string, options=vn_p + ts_p)

            post_process_result = []
            for i in ranked_vn_and_trans:
                if len(i)>3 and i!=phrase:
                    post_process_result.append(i)
            ranked_options = ranked_pp_p + post_process_result[:5]
            file_out.write(sentence+"\t"+phrase+"\t"+"\t".join( ranked_options[:5])+"\n")
            # print("KG_def: ", kg_p)
            # print("####################################################################\n\n")
    file_out.close()
    print(total_verb_cases)

if __name__ == '__main__':
    main()
