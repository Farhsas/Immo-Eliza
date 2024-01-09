from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, when
from pyspark.sql.types import IntegerType
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.ml import Pipeline


def spark_preprocessing(spark):
    # Load your data
    df = spark.read.csv(
        "airflow/dags/datasets/houses_data_copy.csv",
        header=True,
        inferSchema=True,
    )

    # Fill the missing values with 0
    df = df.fillna(0)

    # Filter the Postal Code with regex
    df = df.filter(df["PostalCode"].rlike("^[0-9]{4}$"))

    # Convert the Postal Code to integer
    df = df.withColumn("PostalCode", df["PostalCode"].cast(IntegerType()))

    # One-hot encode the categorical columns
    categorical_columns = [
        "TypeOfProperty",
        "SubtypeOfProperty",
        "StateOfBuilding",
        "TypeOfSale",
    ]
    indexers = [
        StringIndexer(
            inputCol=column, outputCol=column + "_index", handleInvalid="keep"
        ).fit(df)
        for column in categorical_columns
    ]
    encoder = OneHotEncoder(
        inputCols=[indexer.getOutputCol() for indexer in indexers],
        outputCols=[column + "_ohe" for column in categorical_columns],
    )

    # Define the pipeline
    pipeline = Pipeline(stages=indexers + [encoder])

    # Fit and transform the data
    df = pipeline.fit(df).transform(df)

    df.show()

    # Drop the original and indexed categorical columns
    df = df.drop(*categorical_columns)
    df = df.drop(*[column + "_index" for column in categorical_columns])

    return df
