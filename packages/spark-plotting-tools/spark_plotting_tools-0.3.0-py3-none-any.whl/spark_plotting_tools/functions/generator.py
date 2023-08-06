def plot_generated_null_column(spark=None,
                               df=None,
                               col_name=None):
    from pyspark.sql import functions as func
    from pyspark.sql import Row
    column_names = []
    df = df.select(func.col(col_name))
    total_count = df.count()
    for col_name, dtype in df.dtypes:
        null_count = df.select(func.col(col_name)).filter(func.col(col_name).isNull()).count()
        if null_count > 0:
            percent = round((null_count / total_count) * 100, 4)
            rows = Row(NAME=col_name,
                       DTYPE=dtype,
                       TOTAL=null_count,
                       PERCENTAJE_NULL=percent)
            column_names.append(rows)
    if len(column_names) > 0:
        df2 = spark.createDataFrame(column_names)
        return df2.show2(500)
    else:
        print("Not exist missing values")
    del df


def plot_generated_histogram(df=None, col=None, bins=10):
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set_style("whitegrid")
    sns.set_palette("Set2")

    vals2 = df.select(col).rdd.flatMap(lambda x: x).histogram(bins)
    width = vals2[0][1] - vals2[0][0]
    loc = [vals2[0][0] + (i + 1) * width for i in range(len(vals2[1]))]

    fig = plt.figure()
    plt.bar(loc, vals2[1], width=width)
    fig.suptitle(f'Validation Data column {col}')
    plt.xlabel(col)
    plt.ylabel(f"Number of {col}")
    plt.show()

    vals2 = df.select(col).fillna(-999).rdd.flatMap(lambda x: x).collect()
    fig = plt.figure()
    plt.boxplot(vals2, showfliers=False)
    fig.suptitle(f'Validation Data column {col}')
    plt.xlabel(col)
    plt.ylabel(f"Number of {col}")
    plt.show()

    del vals2, df


def plot_generated_barplot(df=None, col=None, limit=10):
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set_style("whitegrid")
    sns.set_palette("Set2")

    df = df.select(col).fillna("VACIO") \
        .groupBy(col).count() \
        .orderBy('count', ascending=False).limit(limit)
    df = df.select([cols for cols in df.columns])

    names = df.select(col).rdd.flatMap(lambda x: x).collect()
    values = df.select("count").rdd.flatMap(lambda x: x).collect()

    def addlabels(x, y):
        for i in range(len(x)):
            plt.text(i, y[i] // 2, y[i], ha='center')

    fig = plt.figure()
    plt.bar(names, values, alpha=0.7)
    addlabels(names, values)
    plt.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='x', alpha=0.7)
    fig.suptitle(f'Validation Data column {col}')
    plt.xlabel(col)
    plt.ylabel(f"Number of {col}")
    plt.show()

    fig1, ax1 = plt.subplots()
    ax1.pie(values, labels=names, autopct='%1.2f%%')
    ax1.axis('equal')
    plt.show()

    del df


def plot_generated_lineplot(spark=None, path=None, col=None, months="{01}", years="{2023}", agg_func="count"):
    import matplotlib.pyplot as plt
    from spark_plotting_tools.utils.color import get_color_b
    from pyspark.sql import functions as func
    import seaborn as sns
    import os
    import sys

    sns.set_style("whitegrid")
    sns.set_palette("Set2")
    is_windows = sys.platform.startswith('win')
    days = "{01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31}"
    cutoff_date = f"{years}-{months}-{days}"
    path_master = os.path.join(path, f"cutoff_date={cutoff_date}")
    if is_windows:
        path_master = path_master.replace("\\", "/")

    df = spark.read.parquet(path_master)
    df = df.withColumn('date_col', func.regexp_extract(func.input_file_name(), r'(\d{4})-(\d{2})-(\d{2})', 0))

    df = df.select("date_col", col)
    df2 = df.withColumn("date_col", func.col("date_col").cast("date")) \
        .withColumn("DAY", func.format_string("%02d", func.dayofmonth("date_col"))) \
        .withColumn("YEAR_MONTH", func.concat(func.year("date_col"),
                                              func.lit("-"),
                                              func.format_string("%02d", func.month("date_col"))))
    df2 = df2.groupBy("YEAR_MONTH", "DAY").agg(func.mean(col).alias("mean"),
                                               func.count(col).alias("count"))
    df2 = df2.withColumn("YEAR", func.substring("YEAR_MONTH", 1, 4)) \
        .withColumn("MONTH", func.substring("YEAR_MONTH", 6, 7))
    year_list = [col[0] for col in df2.select("YEAR").distinct().orderBy(func.col("YEAR").desc()).limit(2).collect()]
    df2 = df2.filter(func.col("YEAR").isin(year_list)) \
        .orderBy(func.col("YEAR_MONTH").desc(), func.col("DAY").asc())
    df3 = df2.toPandas()

    print(get_color_b(":::::DAILY:::::::"))
    plt.figure().set_figwidth(15)
    sns.lineplot(data=df3.sort_values("DAY"), x="DAY", y=agg_func, hue="MONTH", markers=True, dashes=False)
    plt.show()

    plt.figure().set_figwidth(15)
    sns.lineplot(data=df3.sort_values("DAY"), x="DAY", y=agg_func, hue="YEAR", markers=True, dashes=False)
    plt.show()

    plt.figure().set_figwidth(15)
    sns.lineplot(data=df3, x="DAY", y=agg_func, hue="YEAR_MONTH", style="YEAR_MONTH", markers=True, dashes=False)
    plt.show()

    print(get_color_b(":::::MONTHLY:::::::"))
    plt.figure().set_figwidth(15)
    sns.lineplot(data=df3.sort_values("MONTH"), x="MONTH", y=agg_func, hue="YEAR", markers=True, dashes=False)
    plt.show()

    plt.figure().set_figwidth(15)
    sns.lineplot(data=df3.sort_values("YEAR_MONTH"), x="YEAR_MONTH", y=agg_func, hue="MONTH", markers=True, dashes=False)
    plt.show()

    print(get_color_b(":::PARTITION MONTHLY:::"))
    sns.relplot(data=df3.sort_values("DAY"), x="DAY", y=agg_func, col="YEAR_MONTH", hue="YEAR_MONTH", kind="line")
    plt.show()

    sns.relplot(data=df3.sort_values("DAY"), x="DAY", y=agg_func, col="YEAR", hue="YEAR_MONTH", kind="line")
    plt.show()

    sns.relplot(data=df3.sort_values("MONTH"), x="MONTH", y=agg_func, col="YEAR", hue="YEAR", kind="line")
    plt.show()
    del df, df2, df3
