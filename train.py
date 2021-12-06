from sklearn.metrics.pairwise import cosine_similarity as cs
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
import pandas as pd
import numpy as np
import random
import json
#from db_unk import unkq
#Run once
nltk.download('punkt')
nltk.download('averaged_perception_tagger')
nltk.download('wordnet')
nltk.download('stopwords')


def chatbot(wts):
    data = pd.read_json("intents.json")
    data.head

    jsonfile = open('intents.json', 'r')
    intents = json.load(jsonfile)

    words = []
    for i in data["intents"]:
        words.append([i["patterns"], i["tag"]])
    bog = []
    for i in words:
        bog.append([' '.join(i[0]), i[1]])

    df = pd.DataFrame(bog)

    df.loc[len(df.index)] = [wts, "USERINPUT"]

    final_data_q = df[[1, 0]]
    final_data_q = final_data_q.set_index(1)

    lemmatizer = WordNetLemmatizer()

    def prep_sentences(w):
        w = w.lower()
        w = nltk.word_tokenize(w)
        my_w = [lemmatizer.lemmatize(word,pos='v') for word in w if word not in stopwords.words('english')]
        #my_w = [lemmatizer.lemmatize(
        #    word) for word in w]

        f_w = ' '.join(my_w)
        f_w = f_w.replace("?", '')
        f_w = f_w.replace("!", '')
        f_w = f_w.replace(".", '')
        f_w = f_w.replace(",", '')
        return f_w

    final_data_q["keywords"] = final_data_q[0].apply(prep_sentences)

    tfidf = TfidfVectorizer()
    tfidf_keys = tfidf.fit_transform((final_data_q["keywords"]))
    feature_names = tfidf.get_feature_names_out()
    dense = tfidf_keys.todense()
    denselist = dense.tolist()

    df1 = pd.DataFrame(denselist, columns=feature_names)

    similarity = cs(tfidf_keys, tfidf_keys)

    indices = pd.Series(final_data_q.index)
    def chat(cos_sim = similarity):
        index = indices[indices == "USERINPUT"].index[0]
        ansindex = [];
        finalres = [];
        similarity_score = pd.Series(cos_sim[index]).sort_values(ascending = False)

        q_sim = list(similarity_score.iloc[1:2].index)
        res = [list(final_data_q.index)[i] for i in q_sim]
        xsim = similarity_score[q_sim[0]]
        if (xsim>0.15):
            finalres.append([res,xsim])
        else:
            finalres.append([['unk'],xsim])

        return  finalres

    def extract(w):
        for i in w[0][0]:
            return i

    def prob(fr):
        i = fr[0][1]
        return i

    def response(tag, i_json):

        loi = i_json['intents']
        for i in loi:
            if i['tag'] == tag:
                  result = random.choice(i['responses'])
                  break
            else:
                aq = pd.read_json("aq.json")
                loadaq = aq['intents']
                for i in loadaq:
                    if i['tag'] == 'unk':                        
                        result = random.choice(i['responses'])
                        break
        #if tag == 'unk':            
            #unkq(wts)                
        return result           

    res = response(extract(chat()), intents) 
    #+ "   % = " + str(prob(chat()))

    return res
