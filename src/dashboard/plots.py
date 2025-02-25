from plotnine import ggplot, aes, theme_light, geom_point, labs, stat_smooth


def scatter_plot(df, x, y, trend_line=False):
    df_pl = df

    plot = (
        ggplot(df_pl, aes(x=x, y=y))
        + geom_point(aes(fill="factor(Label)"), size=3, alpha=0.5)
        + labs(fill="KMeans Groups")
        + theme_light()
    )

    if trend_line:
        plot = plot + stat_smooth()

    return plot
