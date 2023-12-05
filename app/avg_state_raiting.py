from pyspark.sql import functions as f 
from pyspark.sql.window import Window
from pyspark.sql.functions import avg

def region_impact(df):
   #для початку я хочу знати лише про ті заклади в яких багато відгуків
   avg_review_count = df.agg(f.avg('review_count')).first()[0]
   popular_df = df.filter(df['review_count'] > avg_review_count)
   
   #групування по штатам
   heap_result = popular_df.groupBy('state').agg(f.avg('stars').alias('avg_stars'))
   
   #впорядкувати по рейтингу (від більшого до меншого)
   result = heap_result.orderBy(f.desc('avg_stars'))

   #показати
   print("П'ять штатів з найкращим рейтингом")
   result.show(5)
   
   result_dt = result.limit(5)
   # записати результат у CSV файл
   result_dt.write.csv("result/avg_state_raiting_v1.csv", header=True, mode="overwrite")
   