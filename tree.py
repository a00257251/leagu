from sklearn import tree
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
#from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

twenty_train = ['osama alghamdi','lulu soso','paries hele','sami alghahtani ','lulu alghamdi','ahmed alghamdi','kela soso','mickel hele','sami soso ','moa alghamdi','osama alghamdi','lulu soso','paries hele','sami alghahtani ','lulu alghamdi','ahmed alghamdi','kela soso','mickel hele','sami soso ','moa alghamdi','osama alghamdi','lulu soso','paries hele','sami alghahtani ','lulu alghamdi','ahmed alghamdi','kela soso','mickel hele','sami soso ','moa alghamdi','osama alghamdi','lulu soso','paries hele','sami alghahtani ','lulu alghamdi','ahmed alghamdi','kela soso','mickel hele','sami soso ','moa alghamdi','osama alghamdi','lulu soso','paries hele','sami alghahtani ','lulu alghamdi','ahmed alghamdi','kela soso','mickel hele','sami soso ','moa alghamdi']

twenty_target = ['male','female','female','male','female','male','female','male','male','female','male','female','female','male','female','male','female','male','male','female','male','female','female','female','female','male','female','male','male','female','male','female','male','male','female','male','female','male','male','female','male','female','female','male','female','male','female','male','male','female']

print twenty_train

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(twenty_train)
print X_train_counts.shape


tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)
print X_train_tf.shape

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
print X_train_tfidf.shape

clf = MultinomialNB().fit(X_train_tfidf, twenty_target)

clf2 = tree.DecisionTreeClassifier().fit(X_train_tfidf,twenty_target)



docs_new = ['alghamdi sai', 'khaled', 'hjd alghamdi',' dj5d alghamdi', 'osama', 'alghamdi','alghamdi']
X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)
predicted2 = clf2.predict(X_new_tfidf)

print predicted
print predicted2


for doc in zip(docs_new, predicted):
    print('%r => %s' % (doc, twenty_train))








X = [[121, 80, 44], [180, 70, 43], [166, 60, 38], [153, 54, 37],
     [174, 71, 40], [159, 52, 37], [171, 76, 42], [183, 85, 43]]

Y = ['male', 'male', 'female', 'female', 'male', 'male', 'female', 'female']

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=42)

clf = tree.DecisionTreeClassifier()
clf2 = tree.DecisionTreeRegressor()
clf3 = tree.ExtraTreeRegressor()



clf = clf.fit(X_train,y_train)

clf2 = clf.fit(X,Y)

clf3 = clf.fit(X,Y)

print clf.predict([[185,52,45]])
v = clf.predict(X_test)
print clf2.predict([[185,52,45]])
print clf3.predict([[185,52,45]])


print "Accuracy is ", accuracy_score(y_test,v)*100