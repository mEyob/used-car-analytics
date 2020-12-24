import dask.dataframe as dd
import pandas as pd
import s3fs

# s3 = s3fs.S3FileSystem()
# s3.invalidate_cache()

df = dd.read_csv("s3://used-car-listing-prices/*/*.csv",
                 assume_missing=True,
                 dtype={
                     'Mileage': 'object',
                     'Price': 'object',
                     'Year': 'object'
                 })


def merge_models(model):
    if model == "ES":
        return "ES 350"
    elif model == "RX":
        return "RX 350"
    elif model == "GX":
        return "GX 460"
    else:
        return model


df["Model"] = df.Model.apply(merge_models)
df = df.drop_duplicates().compute()


def safe_to_number(x):
    try:
        return int(x)
    except:
        return None


df["Year"] = df.Year.apply(safe_to_number)
df["Mileage"] = df.Mileage.apply(safe_to_number)
df["Price"] = df.Price.apply(safe_to_number)

bins = [0, 1000, 20000, 40000, 70000, 100000, float('Inf')]
labels = ["<1k", "1k-20k", "20k-40k", "40k-70k", "70k-100k", ">100k"]

#df["Mileage_range"] = df["Mileage"].map_partitions(pd.cut, bins=bins, labels=labels)
df["Mileage_range"] = pd.cut(df["Mileage"], bins=bins, labels=labels)


def round_safe(x):
    try:
        return round(x)
    except:
        return x


def get_data(**kwargs):
    """
    """
    query = ' & '.join(
        [f"{key} == {repr(value)}" for key, value in kwargs.items()])
    return df.query(query).copy()


def get_grouped_data(make, model, year, **kwargs):
    """
    """
    if year:
        car = " ".join([str(year), make, model])
        filtered_df = df[(df["Make"] == make) & (df["Model"] == model) &
                         (df["Year"] == year)]
    else:
        car = " ".join([make, model])
        filtered_df = df[(df["Make"] == make) & (df["Model"] == model)]
    filtered_df = filtered_df.groupby(by="Mileage_range", as_index=False).agg(
        Count=("Price", "count"),
        Average_Price=("Price", "mean"),
        STD_Price=("Price", "std"))
    filtered_df = filtered_df.applymap(round_safe)
    filtered_df["MakeModel"] = car

    if kwargs:
        filtered_df2 = get_grouped_data(kwargs.get("make2"),
                                        kwargs.get("model2"),
                                        kwargs.get("year2"))
        filtered_df = pd.concat([filtered_df, filtered_df2], ignore_index=True)
    return filtered_df


def make_and_model():
    """
    """
    all_options = {}
    makes = df.Make.unique().tolist()

    for make in makes:
        models = df[df.Make == make].Model.unique().tolist()
        models.sort()
        all_options[make] = models
    return all_options


#print(make_and_model())
