import difflib

from nlp_utils import NlpUtils
from test_cskg import ppdb_phrase
from transformer_utils import TransformerUtils
from verb_utils import VerbUtils
from fitbert import FitBert


def main():
    ts = TransformerUtils(bert_threshold=0.01, window_size=5)
    vp = VerbUtils()
    # vp.get_class("kill")
    # tsv_data_file = 'datasets/trial/tsar2022_en_trial_none.tsv'
    tsv_data_file = 'datasets/test/verbnet_example.tsv'
    # out_data_file = 'datasets/trial/tsar2022_en_teamPN_1.tsv'
    # file_out = open(out_data_file,"w", encoding="utf8")
    # # tsv_data_file = 'datasets/trial/tsar2022_en_trial_none.tsv'
    s = NlpUtils()
    # single_verb_cases = 0
    total_verb_cases = 0
    correct = 0
    all_cases = 0
    # # fb = FitBert(model_name="C:/Users/p00770556/Projects/distilbert-base-uncased/", disable_gpu=True)
    fb = FitBert(model_name="C:/Users/p00770556/Projects/bert-large-uncased-whole-word-masking/", disable_gpu=True)
    with open(tsv_data_file, encoding="utf8") as f:
        for line in f:

            sentence, phrase, org_class = line.strip().split('\t')
            if len(sentence.split(" ")) < 3:
                continue
            # print("####################################################################")
            ts_p = ts.pred_transformer(sentence, phrase)
            pos_tag_phrase = s.get_pos(sentence, phrase)
            # print("POS: ", pos_tag_phrase)
            if not pos_tag_phrase == "VERB":
                continue
                # total_verb_cases += 1
            try:
                tense, ordn = vp.get_verb_form(phrase)
            except:
                continue
            ts_x = []
            for verb2 in ts_p:
                verb2 = vp.get_lemma_verb(verb2)
                x = vp.set_verb_form(verb2, tense, ordn)
                ts_x.append(x)
            vn_p = vp.get_class(phrase, ts_x)
            if not vn_p:
                masked_string = ts.get_vic(sentence, phrase).replace(phrase, "***mask***")
                vn_p = vp.get_class_2(phrase,masked_string,fb)
                # print("No out: ", line)
                # continue
            all_cases += 1
            # print("predicted: ",vn_p)
            # print("original: ",org_class)
            if (vn_p.split("-")[0] == org_class.split("-")[0]):
                correct += 1
            print(str(correct) + " / " + str(all_cases))
            # print(all_cases)
            # print("\n\n")


if __name__ == '__main__':
    main()
