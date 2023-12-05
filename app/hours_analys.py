from pyspark.sql import functions as F
from pyspark.sql.window import Window

def hour_raiting(df):
   
   # для початку я хочу знати лише про ті заклади в яких багато відгуків
   avg_review_count = df.agg(F.avg('review_count')).first()[0]
   popular_df = df.filter(df['review_count'] > avg_review_count)
   
   #обираємо лише потрібні колонки
   cutted_df = popular_df.select(
      F.col("hours.Friday"),
      F.col("hours.Saturday"),
      F.col("hours.Sunday"),
      F.col("stars")
   )  

   # створюємо вікно та рахуємо середнє по 3 колонкам
   window_spec = Window().partitionBy("Friday", "Saturday", "Sunday")
   grouped_df = cutted_df.withColumn("average_stars", F.avg("stars").over(window_spec))


   #чистимо датафрейм для гарних результатів
   grouped_df = grouped_df.drop("stars")
   result_df = grouped_df.dropDuplicates()
   
   #сортуємо
   result_df = result_df.orderBy("average_stars", ascending=False)

   # показати топ 5
   print("Рейтинг по годинам")
   result_df.show(5)

   # запис у файл
   result = result_df.limit(10)
   result.write.csv("result/hour_raiting.csv", header=True, mode="overwrite")


