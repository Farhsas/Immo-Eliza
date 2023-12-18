import pickle
from typing import Optional
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from predict.prediction import prediction
import catboost

app = FastAPI()


class Estate(BaseModel):
    """
    Pydantic model representing the input data for property prediction.

    Attributes:
        Url (Optional[str]): URL of the property listing.
        Openfire (Optional[bool]): Indicates if the property has an open fire.
        Furnished (Optional[bool]): Indicates if the property is furnished.
        Terrace (Optional[bool]): Indicates if the property has a terrace.
        Garden (Optional[bool]): Indicates if the property has a garden.
        PropertyId (Optional[int]): Identifier for the property.
        TypeOfProperty (Optional[str]): Type of the property.
        PostalCode (int): Postal code of the property (required).
        SubtypeOfProperty (Optional[str]): Subtype of the property.
        TypeOfSale (Optional[int]): Type of sale for the property.
        Kitchen (Optional[str]): Type of kitchen in the property.
        StateOfBuilding (Optional[str]): State of the building.
        Heating (Optional[str]): Type of heating in the property.
        Bedrooms (int): Number of bedrooms in the property (required).
        SurfaceOfGood (Optional[int]): Surface area of the property.
        SwimmingPool (Optional[bool]): Indicates if the property has a swimming pool.
        NumberOfFacades (Optional[int]): Number of facades of the property.
        LivingArea (int): Total living area of the property (required).
        ConstructionYear (Optional[int]): Year of construction of the property.
        GardenArea (Optional[int]): Area of the garden in the property.
    """

    Url: Optional[str] = None
    Openfire: Optional[bool] = None
    Furnished: Optional[bool] = None
    Terrace: Optional[bool] = None
    Garden: Optional[bool] = None
    PropertyId: Optional[int] = None
    TypeOfProperty: Optional[str] = None
    PostalCode: int
    SubtypeOfProperty: Optional[str] = None
    TypeOfSale: Optional[int] = None
    Kitchen: Optional[str] = None
    StateOfBuilding: Optional[str] = None
    Heating: Optional[str] = None
    Bedrooms: int
    SurfaceOfGood: Optional[int] = None
    SwimmingPool: Optional[bool] = None
    NumberOfFacades: Optional[int] = None
    LivingArea: int
    ConstructionYear: Optional[int] = None
    GardenArea: Optional[int] = None


@app.get("/")
async def home():
    """
    Endpoint to test the API's availability.

    Returns:
        str: A simple message indicating the API is still running.
    """
    return "I'm still standing"


@app.post("/predict/")
async def predict(data: Estate):
    """
    Endpoint to make property price predictions based on input data.

    Args:
        data (Estate): Input data for property prediction.

    Returns:
        dict: A dictionary containing the prediction result.
    Raises:
        HTTPException: If required fields (LivingArea, Bedrooms, or PostalCode) are missing or set to 0.
    """
    if data.LivingArea == 0:
        raise HTTPException(
            status_code=422, detail="You must provide the LivingArea of the property"
        )
    elif data.Bedrooms == 0:
        raise HTTPException(
            status_code=422,
            detail="You must provide the number of Bedrooms of the property",
        )
    elif data.PostalCode == 0:
        raise HTTPException(
            status_code=422, detail="You must provide the PostalCode of the property"
        )

    df = pd.DataFrame(data.dict(), index=[0])
    pred = prediction(df)
    pred_dict = {"Prediction": pred[0]}
    print(pred_dict)

    return pred_dict


@app.get("/predict")
async def get_predict():
    """
    Endpoint to retrieve an example data structure for property prediction.

    Returns:
        str: A JSON-like string representing an example data structure for property prediction.
    """
    data = {
        "Url": Optional[str],
        "Openfire": Optional[bool],
        "Furnished": Optional[bool],
        "Terrace": Optional[bool],
        "Garden": Optional[bool],
        "PropertyId": Optional[int],
        "TypeOfProperty": Optional[str],
        "PostalCode": int,
        "SubtypeOfProperty": Optional[str],
        "TypeOfSale": Optional[int],
        "Kitchen": Optional[str],
        "StateOfBuilding": Optional[str],
        "Heating": Optional[str],
        "Bedrooms": int,
        "SurfaceOfGood": Optional[int],
        "SwimmingPool": Optional[bool],
        "NumberOfFacades": Optional[int],
        "LivingArea": int,
        "ConstructionYear": Optional[int],
        "GardenArea": Optional[int],
    }
    return str(data)
