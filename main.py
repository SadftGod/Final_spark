from pyspark import SparkConf
from pyspark.sql import SparkSession, Window
import pyspark.sql.types as t


from app.default import info_view , read

from app.avg_state_raiting import region_impact 
from app.the_best_tip import best_tips
from app.hours_analys import hour_raiting
from app.categories_marks import calculate_votes_frequency
from app.user_impact import user_impact
from app.popular_favorite import analyze_favorite_businesses

def main():
   spark_session = (SparkSession.builder
                                 .master("local")
                                 .appName("Yelp Analisys")
                                 .config(conf=SparkConf())
                                 .getOrCreate())
   path = "/yelp_data/"
    
   business_df = read(spark_session, f"{path}/yelp_academic_dataset_business.json")
   review_df = read(spark_session, f"{path}/yelp_academic_dataset_review.json")
   tip_df = read(spark_session, f"{path}/yelp_academic_dataset_tip.json")
   user_df = read(spark_session, f"{path}/yelp_academic_dataset_user.json")

   info_view(business_df)
   info_view(review_df)
   info_view(tip_df)
   info_view(user_df)
   
   region_impact(business_df)
   best_tips_result = best_tips(tip_df, business_df).limit(5)
   best_tips_result.write.csv("result/best_tips.csv", header=True, mode="overwrite")
   hour_raiting(business_df)  
   user_impact(user_df)
   calculate_votes_frequency(business_df,review_df)
   analyze_favorite_businesses(review_df , business_df,user_df)
   
main()