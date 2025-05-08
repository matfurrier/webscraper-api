import pandas as pd
from app.db import get_all_data, ScrapedItemDB
from typing import List

def get_data_as_dataframe() -> pd.DataFrame:
    """Fetches all data and returns it as a Pandas DataFrame."""
    items: List[ScrapedItemDB] = get_all_data()
    
    # Convert list of Pydantic models to list of dicts, handling the _id field
    data_for_df = []
    for item in items:
        item_dict = item.model_dump(by_alias=True) # Use by_alias to get _id
        # Flatten the 'dados' dictionary
        if 'dados' in item_dict and isinstance(item_dict['dados'], dict):
            for key, value in item_dict['dados'].items():
                item_dict[f"dados_{key}"] = value
            del item_dict['dados'] # Remove original nested dict
        data_for_df.append(item_dict)
        
    df = pd.DataFrame(data_for_df)
    # Ensure _id is string, if it exists
    if "_id" in df.columns:
        df["_id"] = df["_id"].astype(str)
    return df

def export_to_json_str() -> str:
    """Exports all data to a JSON string."""
    df = get_data_as_dataframe()
    # Use records orientation for a list of JSON objects
    return df.to_json(orient="records", indent=4, date_format="iso")

def export_to_csv_str() -> str:
    """Exports all data to a CSV string."""
    df = get_data_as_dataframe()
    return df.to_csv(index=False) 