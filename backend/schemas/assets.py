from pydantic import BaseModel, ConfigDict

class AssetBase(BaseModel):
    owner : int
    title : str
    description : str
    longitude : float
    latitude : float

class AssetCreateResponse(BaseModel):
    id : int
    title : str
    description : str

    model_config = ConfigDict(
        from_attributes = True
    )
    
     