from django.shortcuts import render
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def list(request):
    if request.method == "POST":
        content = request.POST.get('content', None)
        message = lstm_predict(content)
        return render(request, 'analyse/sentiment.html', {"message": message, "content": content})
    return render(request, 'analyse/sentiment.html')


def create_dictionaries(model=None, combined=None):
    from keras.preprocessing import sequence
    from gensim.corpora.dictionary import Dictionary
    maxlen = 100
    gensim_dict = Dictionary()
    gensim_dict.doc2bow(model.wv.vocab.keys(), allow_update=True)
    w2indx = {v: k+1 for k, v in gensim_dict.items()}
    w2vec = {word: model[word] for word in w2indx.keys()}
    data = []
    for sentence in combined:
        new_txt = []
        for word in sentence:
            try:
                new_txt.append(w2indx[word])
            except:
                new_txt.append(0)
        data.append(new_txt)
    combined = sequence.pad_sequences(data, maxlen=maxlen)
    return w2indx, w2vec, combined

def input_transform(string):
    import jieba
    import numpy as np
    from gensim.models.word2vec import Word2Vec
    words = jieba.lcut(string)
    words = np.array(words).reshape(1, -1)
    model = Word2Vec.load(os.path.join(BASE_DIR, 'model/Word2vec_model.pkl'))
    _,_,combined = create_dictionaries(model, words)
    return combined

def lstm_predict(string):
    from keras.models import load_model
    from keras import backend as K
    model = load_model(os.path.join(BASE_DIR, 'model/lstm.h5'))
    model.compile(loss='categorical_crossentropy', optimizer='adam',metrics=['accuracy'])
    data = input_transform(string)
    result = model.predict_classes(data.reshape(1, -1))
    K.clear_session()
    if result[0] == 1:
        return '满意'
    elif result[0] == 2:
        return '不满意'
    else:
        return '一般'

