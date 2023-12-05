from pyspark.sql.functions import col, avg

def analyze_favorite_businesses(review_df, business_df, user_df):
    # створення великого датасету
    joined_df = review_df.join(business_df, review_df.business_id == business_df.business_id) \
                        .join(user_df, review_df.user_id == user_df.user_id)

    # Фільтрация популярних користувачів
    popular_users_df = joined_df.filter(col("fans") > 150)

    # По категоріям
    result_df = popular_users_df.groupBy(
        business_df["business_id"].alias("business_id"), 
        user_df["name"].alias("user_name"), 
        business_df["categories"].alias("business_categories")
    ).agg(
        avg(review_df["stars"]).alias("average_stars"),
        avg(business_df["review_count"]).alias("average_review_count"),
        avg(user_df["fans"]).alias("average_fans")
    )

    # Сортування результатів по середньому рейтингу в порядку зменшення
    result_df = result_df.orderBy(col("average_stars").desc())

    result = result_df.select(
        col("user_name").alias("name"),
        col("business_categories").alias("categories"),
        col("average_stars"),
        col("average_review_count"),
        col("average_fans"),
    )

    # Показать
    print("Топ 10 закладів у популярних користувачів:")
    result.show(10, truncate=False)

    # Записать
    result.write.csv("result/favorite_businesses.csv", header=True, mode="overwrite")
