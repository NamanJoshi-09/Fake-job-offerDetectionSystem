import pandas as pd
import pickle 
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
import os


def explain_prediction(text, model, vectorizer, top_n=5):
    vec = vectorizer.transform([text])
    
    prediction = model.predict(vec)[0]
    prob = model.predict_proba(vec)[0][1]  

    feature_names = vectorizer.get_feature_names_out()
    weights = model.coef_[0]

    word_scores = []

    for idx in vec.nonzero()[1]:
       label = "FAKE" if weights[idx] > 0 else "REAL"
       word_scores.append((feature_names[idx], weights[idx], label))
    
    word_scores = sorted(word_scores, key=lambda x: abs(x[1]), reverse=True)

    return prediction, prob, word_scores[:top_n]

if __name__ == "__main__":
    print("Loading dataset...")
    # Handle path smoothly whether run from root or model/
    data_path = "data/jobs.csv" if os.path.exists("data/jobs.csv") else "../data/jobs.csv"
    df = pd.read_csv(data_path)

    # Combine text columns
    text_columns = ['title','company_profile','description','requirements','benefits']
    df[text_columns] = df[text_columns].fillna("")

    df['text'] = (
        df['title'] + " " +
        df["company_profile"] + " " +
        df["description"] + " " +
        df["requirements"] + " " +
        df["benefits"]
    )

    X = df['text']
    y = df['fraudulent']

    print("Splitting...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Vectorizing...")
    vectorizer = TfidfVectorizer(
        stop_words='english',
        max_features=10000,
        ngram_range=(1,2),
        max_df=0.7
    )

    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec  = vectorizer.transform(X_test)

    print("Training model...")
    model = LogisticRegression(max_iter=1000, class_weight='balanced')
    model.fit(X_train_vec, y_train)

    y_pred = model.predict(X_test_vec)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    print("Saving model files...")
    model_path = "model.pkl" if os.path.exists("data") else "../model.pkl"
    vec_path = "vectorizer.pkl" if os.path.exists("data") else "../vectorizer.pkl"
    pickle.dump(model, open(model_path,"wb"))
    pickle.dump(vectorizer, open(vec_path,"wb"))
    print("Success!")

