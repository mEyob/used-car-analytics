import numpy as np
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

    mileage = np.arange(0, 150000, mileage_per_year)
    year = mileage // mileage_per_year

    model1, score1 = train_and_test(
        df[["Mileage_std", "Year_centered", "Price"]])
    model2, score2 = train_and_test(
        df[["Mileage_log", "Year_centered", "Price"]])

    # If score2 is not significantly better than score1
    # favor model1
    margin = 0.03  #
    if score1 + margin > score2:
        transform = "std"
        mileage = (mileage - df.Mileage.mean()) / df.Mileage.std()
        predicted = model1.predict(
            np.array(list(zip(mileage, year))).reshape(-1, 2))
        model = model1
        score = score1
    else:
        transform = "log"
        mileage[0] = 1
        mileage = np.log2(mileage)
        predicted = model2.predict(
            np.array(list(zip(mileage, year))).reshape(-1, 2))
        model = model2
        score = score2
    return predicted, model, transform, score
