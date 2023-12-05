def info_view(df):
   
   with open("result/main.txt", 'w') as txt_file:
      print(f"General information about the Dataframe: ")
   
      #df.printSchema()
      #df.show(5)
      num_rows = df.count()
      columns_df = df.columns
      num_columns = len(columns_df)
   
   
      txt_file.write(f"\n Number of rows: {num_rows}\n")
      txt_file.write(f"\n Number of columns: {num_columns}\n")
      txt_file.write(f"\n Columns: {columns_df}\n\n")
   

def read(spark, input_directory):
    df = spark.read.json(input_directory)
    return df
 

 