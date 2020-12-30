import numpy as np
import pandas as pd
from sklearn.linear_model import LassoCV, Lasso
from sklearn.model_selection import train_test_split


def train_and_test(df):
    """
    """
    train, test = train_test_split(df, shuffle=True)
    lasso_cv = LassoCV(cv=10, random_state=0)
    lasso_cv.fit(train.drop('Price', axis=1), train.Price)

    model = Lasso(random_state=0, alpha=lasso_cv.alpha_)
    model.fit(train.drop('Price', axis=1), train.Price)

    r2_score = model.score(test.drop('Price', axis=1), test['Price'])
    return model, r2_score


def transformer(series, tr_type):
    """
    """
    if callable(tr_type):
        return tr_type(series)
    elif tr_type == "standardize":
        return (series - np.mean(series)) / np.std(series)
    elif tr_type == "center":
        return series.max() - series


def main(df, mileage_per_year):
    """
    """
    df = df.copy()
    df["Mileage_std"] = transformer(df.Mileage, "standardize")
    df["Mileage_log"] = transformer(df.Mileage, np.log2)
    df["Year_centered"] = transformer(df.Year, "center")

    df = pd.get_dummies(df, columns=["clean_trim"])
    print(df)
    trim_columns = [
        column for column in df.columns if column.startswith("clean_trim")
    ]
    trim_binary = [0 for col in trim_columns if col != "clean_trim_Other"]

    mileage = np.arange(0, 150000, mileage_per_year)
    year = mileage // mileage_per_year

    model1, score1 = train_and_test(
        df.drop(["Mileage", "Year", "Mileage_log", "clean_trim_Other"],
                axis=1))
    model2, score2 = train_and_test(
        df.drop(["Mileage", "Year", "Mileage_std", "clean_trim_Other"],
                axis=1))

    # If score2 is not significantly better than score1
    # favor model1
    margin = 0.1  #
    if score1 + margin > score2:
        transform = "std"
        mileage = (mileage - df.Mileage.mean()) / df.Mileage.std()
        model = model1
        score = score1
    else:
        transform = "log"
        mileage[0] = 1
        mileage = np.log2(mileage)
        model = model2
        score = score2
    mileage_year = list(zip(mileage, year))
    mileage_year_trim = [[m, yr, *trim_binary] for m, yr in mileage_year]
    predicted = model.predict(np.array(mileage_year_trim))
    return predicted.astype("int"), model, transform, score, trim_columns
