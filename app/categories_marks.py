from pyspark.sql.window import Window
from pyspark.sql import functions as F

def calculate_votes_frequency(business_df, review_df):
    # Створюємо выкно та вказуємо параметри сортування
   windowSpec = Window.partitionBy("categories").orderBy(F.desc("repeating_count"))

    # Розраховуємо частоту голосів для кожної категорії ('cool', 'funny', 'useful')
   cool_frequency_df = review_df.filter(review_df['cool'] > 0) \
   .join(business_df, 'business_id', 'inner') \
   .groupBy('categories') \
   .agg(
      F.avg('cool').alias('cool_frequency'),
      F.count('cool').alias('repeating_count')
    ) \
   .withColumn('frequency_rank', F.rank().over(windowSpec)) \
   .orderBy(F.desc("repeating_count"))  

   funny_frequency_df = review_df.filter(review_df['funny'] > 0) \
   .join(business_df, 'business_id', 'inner') \
   .groupBy('categories') \
   .agg(
      F.avg('funny').alias('funny_frequency'),
      F.count('funny').alias('repeating_count')
    ) \
   .withColumn('frequency_rank', F.rank().over(windowSpec)) \
   .orderBy(F.desc("repeating_count"))  

   useful_frequency_df = review_df.filter(review_df['useful'] > 0) \
   .join(business_df, 'business_id', 'inner') \
   .groupBy('categories') \
   .agg(
      F.avg('useful').alias('useful_frequency'),
      F.count('useful').alias('repeating_count')
    ) \
   .withColumn('frequency_rank', F.rank().over(windowSpec)) \
   .orderBy(F.desc("repeating_count"))  

    # Виводимо результати
   print("Частота голосів 'cool' по категоріям:")
   cool_frequency_df.show(5)

   print("Частота голосів 'funny' по категоріям:")
   funny_frequency_df.show(5)

   print("Частота голосів 'useful' по категоріям:")
   useful_frequency_df.show(5)

    # Записуємо результати в CSV файли
   cool_frequency_df.write.csv("result/cool_frequency.csv", header=True, mode="overwrite")
   funny_frequency_df.write.csv("result/funny_frequency.csv", header=True, mode="overwrite")
   useful_frequency_df.write.csv("result/useful_frequency.csv", header=True, mode="overwrite")
