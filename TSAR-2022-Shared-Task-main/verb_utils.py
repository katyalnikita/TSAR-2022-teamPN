from pattern.en import conjugate, lemma, lexeme, SG, PL, PRESENT, PAST, FUTURE
from nltk.corpus import verbnet


class VerbUtils:
    def __init__(self, init_verb="test"):
        self.init_verb = init_verb
        self.get_verb_form(init_verb)

    def myfunc(self):
        print("Hello my name is " + self.name)

    def get_verb_form(self, verb):
        try:
            if verb == conjugate(verb=verb, tense=FUTURE, number=SG):
                return FUTURE, SG
            elif verb == conjugate(verb=verb, tense=PRESENT, number=SG):
                return PRESENT, SG
            elif verb == conjugate(verb=verb, tense=PAST, number=SG):
                return PAST, SG
            elif verb == conjugate(verb=verb, tense=FUTURE, number=PL):
                return FUTURE, PL
            elif verb == conjugate(verb=verb, tense=PRESENT, number=PL):
                return PRESENT, PL
            elif verb == conjugate(verb=verb, tense=PAST, number=PL):
                return PAST, PL
            return None
        except:
            pass

    def set_verb_form(self, verb, tense, number):
        try:
            return conjugate(verb=verb, tense=tense, number=number)
        except:
            pass

    def get_lemma_verb(self, verb):
        return self.set_verb_form(verb, PRESENT, PL)

    def get_possible_classes(self, verb):
        return verbnet.classids(lemma=verb)

    def get_verb_members(self, classid, tense, ordn):
        poss_members = verbnet.pprint_members(classid).strip().replace("\n", "").split(" ")
        str_list = list(filter(None, poss_members))[1:]
        final_list = []
        for root_v in str_list:
            final_list.append(self.set_verb_form(root_v, tense, ordn))
        return final_list

    def get_alternate_verbs(self, verb, ts_predicted_verb_list):
        try:
            tense, ordn = self.get_verb_form(verb)
            verb = self.get_lemma_verb(verb)
            possible_classes = self.get_possible_classes(verb)
            if len(possible_classes) == 1:
                return self.get_verb_members(possible_classes[0], tense, ordn)
            else:
                # print("MC Verbcase", possible_classes, verb,ts_predicted_verb_list)
                len_max = 0
                max_len_class = ""
                for i in possible_classes:
                    local_mem = self.get_verb_members(i, tense, ordn)
                    common = len(list(set(local_mem) & set(ts_predicted_verb_list)))
                    # print("localMem",local_mem)
                    # print(common ,len_max, i)
                    if common > len_max:
                        len_max = common
                        max_len_class = i
                # print("Multiclass: ", max_len_class)
                return (self.get_verb_members(max_len_class, tense, ordn))
        except:
            return ([])

    def get_class(self, verb, ts_predicted_verb_list):
        tense, ordn = self.get_verb_form(verb)
        verb = self.get_lemma_verb(verb)
        possible_classes = self.get_possible_classes(verb)
        if len(possible_classes) == 1:
            return possible_classes[0]
        else:
            len_max = 0
            max_len_class = ""
            for i in possible_classes:
                local_mem = self.get_verb_members(i, tense, ordn)
                common = len(list(set(local_mem) & set(ts_predicted_verb_list)))
                # print("localMem",local_mem)
                # print(common ,len_max, i)
                if common > len_max:
                    len_max = common
                    max_len_class = i
            # print("Multiclass: ", max_len_class)
        return max_len_class

    def get_class_2(self, verb, masked_string, fb):
        tense, ordn = self.get_verb_form(verb)
        verb = self.get_lemma_verb(verb)
        possible_classes = self.get_possible_classes(verb)
        possible_vers = []
        for i in possible_classes:
            local_mem = self.get_verb_members(i, tense, ordn)
            possible_vers = possible_vers + local_mem
        ranked_vn_and_trans = fb.rank(masked_string, options=possible_vers)[:5]
        len_max = 0
        max_len_class = ""
        for i in possible_classes:
            local_mem = self.get_verb_members(i, tense, ordn)
            common = len(list(set(local_mem) & set(ranked_vn_and_trans)))
            if common > len_max:
                len_max = common
                max_len_class = i
        return max_len_class


def main():
    vs = VerbUtils()
    # tense, form = vs.get_verb_form("indicated")
    # print(tense, form)
    print(vs.get_lemma_verb("establish"))
    print(vs.get_lemma_verb("indicated"))


if __name__ == '__main__':
    main()
