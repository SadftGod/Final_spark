from pyspark.sql import functions as f  
from pyspark.sql.window import Window

def best_tips(tips,business):
   windowSpec = Window.orderBy(f.desc("compliment_count"))
   best_tips = (
      tips
      .join(business.select("business_id", "name"), on="business_id", how="left_outer")
      .withColumn("row_number", f.row_number().over(windowSpec))
      .filter(f.col("row_number") <= 5)  
      .select("text", "compliment_count", "name")
   )
    
   print("Найкращі поради")
   best_tips.show(5)
   
   return best_tips