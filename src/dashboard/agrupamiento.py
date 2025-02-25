import polars as pl
import sklearn.cluster
import sklearn.feature_selection
import sklearn.linear_model
import sklearn.preprocessing
import sklearn.model_selection


def labeled_df(pl_df, grupos=3, remove_columns=0):
    # https://docs.pola.rs/api/python/dev/reference/expressions/api/polars.exclude.html
    filtered_data = pl_df.select(pl.exclude(pl.String)).select(pl.exclude("Year"))

    # https://how.dev/answers/how-to-scale-and-normalize-data-in-python-using-polars
    normalized_data = filtered_data.select(
        (pl.all() - pl.all().mean()) / pl.all().std()
    )

    agrupador = sklearn.cluster.KMeans(grupos, random_state=0)
    agrupador.fit(normalized_data)

    # https://sparkbyexamples.com/polars/convert-polars-cast-int-to-string/#:~:text=The%20cast(pl.,rename%20the%20column%20after%20casting.
    label_serie = pl.Series(
        "Label", agrupador.labels_
    )  # .with_columns(pl.col("Label").cast(pl.String).alias("Label"))

    # https://docs.pola.rs/api/python/stable/reference/dataframe/api/polars.DataFrame.join.html
    # pl_df.insert_column(-1, label_serie)
    return pl_df.with_columns(label_serie)


def column_ranking(pl_df, col, axis_x, axis_y):
    # We exclude the following items:
    # - Any String field as it's not suitable to be in a scatter and it would cause noise
    # - The year column becacuse it contains None values
    # - The X and Y axis in our Dashboard, since we need it to plot the results,
    #   so we exclude them in order to avoid being filtered out. Note that we won't exclude them
    #   if it's the same as the "col" value, since it will be our class ("y") attribute.

    filtered_data = pl_df.select(pl.exclude(pl.String)).select(pl.exclude("Year"))
    if col not in axis_x:
        filtered_data = filtered_data.select(pl.exclude(axis_x))
    if col not in axis_y:
        filtered_data = filtered_data.select(pl.exclude(axis_y))

    X = filtered_data.select(pl.exclude(col))
    y = filtered_data.select(col)
    scaler = sklearn.preprocessing.StandardScaler().fit(X)
    X_scaled = scaler.transform(X)
    selector_RFE = sklearn.feature_selection.RFE(
        sklearn.linear_model.LinearRegression(), n_features_to_select=1
    )
    selector_RFE.fit(X_scaled, y)
    ranking_X = selector_RFE.ranking_

    posiciones_atributos = list(zip(ranking_X, list(X.columns)))
    posiciones_atributos.sort()
    return [a for _, a in posiciones_atributos]
