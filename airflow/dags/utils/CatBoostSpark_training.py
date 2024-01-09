from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructField, StructType
from pyspark.sql.functions import col
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.regression import (
    AFTSurvivalRegression,
    GBTRegressor,
    GeneralizedLinearRegression,
    IsotonicRegression,
    LinearRegression,
    RandomForestRegressor,
    FMRegressor,
)
from Spark_preprocessing import spark_preprocessing


def prepare_vector(df: DataFrame, assembler):
    result_df = assembler.transform(df)
    return result_df


def training():
    spark = SparkSession.builder.master("local").appName("CatBoostSpark").getOrCreate()

    # Load Data
    df = spark_preprocessing(spark)

    TARGET_LABEL = "Price"

    evaluator = RegressionEvaluator(
        labelCol=TARGET_LABEL, predictionCol="prediction", metricName="rmse"
    )

    train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)

    features = [
        "TypeOfProperty_ohe",
        "SubtypeOfProperty_ohe",
        "StateOfBuilding_ohe",
        "PostalCode",
        "NumberOfRooms",
        "LivingArea",
        "EquippedKitchen",
        "Furnished",
        "OpenFire",
        "Terrace",
        "Garden",
        "Surface",
        "NumberOfFacades",
        "SwimmingPool",
    ]
    assembler = VectorAssembler(inputCols=features, outputCol="features")

    train = prepare_vector(
        train_df,
        assembler,
    )
    test = prepare_vector(
        test_df,
        assembler,
    )

    # LinearRegression
    regressor = AFTSurvivalRegression(labelCol=TARGET_LABEL, featuresCol="features")

    # train a model
    model = regressor.fit(train)

    predict = model.transform(test)
    print(f"Model RMSE: {evaluator.evaluate(predict)}")

    spark.stop()


training()
