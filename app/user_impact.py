from pyspark.sql.window import Window
from pyspark.sql import functions as F

def user_impact(users):
   
   windowSpec = Window.orderBy(F.desc('fans'))
   
   ranked_users = users.withColumn('rank', F.row_number().over(windowSpec))
   
   top_users = ranked_users.filter(F.col('rank') <= 20)
   
   top_users = top_users.select(
      F.col("rank"),
      F.col("name"),
      F.col("average_stars"),
      F.col("review_count"),
      F.col("fans")
   )
   
   # показать топ 5
   print("Рейтинг користувачів")
   top_users.show(5)

   # записать в файл
   top_users.write.csv("result/top_users.csv", header=True, mode="overwrite")
   