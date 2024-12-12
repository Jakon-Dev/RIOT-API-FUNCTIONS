import os
import sys
from httpx import delete
import pandas as pd
import supabase
from supabase import create_client
import json
import SECRET_DATA as SECRETS
import utils



class GLOBALS:
    TABLES = [
        "Riot-Users"
    ]

    FILES = [
        "VALORANT/Data_Base/Riot-Users.csv"
    ]

    SUPABASE_KEY = SECRETS.SUPABASE_KEY
    SUPABASE_URL = SECRETS.SUPABASE_URL

supabase = create_client(GLOBALS.SUPABASE_URL, GLOBALS.SUPABASE_KEY)


class RIOT_USERS:
    
    TABLE = GLOBALS.TABLES[0]
    FILE = GLOBALS.FILES[0]
    
    def update() -> None:
        '''
            1. Updates the CSV file with the information from the table.
            2. Performs an upsert for each row in the table using 'puuid' as the key.
            3. Converts 'infoJson' to a text format suitable for CSV storage.
        '''
        
        table = fetchTable(RIOT_USERS.TABLE)
        file_path = RIOT_USERS.FILE
        
        if os.path.exists(file_path):
            existing_df = pd.read_csv(file_path)
        else:
            existing_df = pd.DataFrame(columns=['puuid', 'fullName', 'infoJson'])
        
        if table.data:
            new_data = pd.DataFrame(table.data)
            new_data['infoJson'] = new_data['infoJson'].apply(lambda x: json.dumps(x))
            
            if not existing_df.empty:
                existing_df = existing_df[~existing_df['puuid'].isin(new_data['puuid'])]  
            
            updated_df = pd.concat([existing_df, new_data], ignore_index=True)
            updated_df.to_csv(file_path, index=False)
    
    def search(value: str, search: str = "puuid") -> json:
        """
        Searches a CSV file for a specific entry based on the given search parameter.

        Args:
        - value (str): The value to search for. 
            - If `search` is "puuid", `value` must match the PUUID format.
            - If `search` is "fullName", `value` must match the full name format.
        - search (str): The type of search to perform. Valid options are:
            - "puuid": Search for a Player UUID.
            - "fullName": Search for a player's full name.
            - Default is "puuid".

        Raises:
            - ValueError: If `search` is not one of the valid options ("puuid", "fullName").
            - ValueError: If `value` does not match the expected format for the specified `search` parameter.

        Notes:
        - This function relies on external utility functions:
            - `utils.FUNCTIONS.isPuuidFormat(value)`: Validates the PUUID format.
            - `utils.FUNCTIONS.isFullName(value)`: Validates the full name format.
        """
        
        if search != "puuid" and search != "fullName":
            raise ValueError(f"Not valid search parameter '{search}', only 'puuid' and 'fullName' are valid.")
        if search == "puuid" and not utils.FUNCTIONS.isPuuidFormat(value):
            raise ValueError(f"Invalid puuid format for {value}")
        if search == "fullName" and not utils.FUNCTIONS.isFullName(value):
            raise ValueError(f"Invalid full name format for {value}")
        
        
        file_path = RIOT_USERS.FILE 
        if os.path.exists(file_path):
            existing_df = pd.read_csv(file_path)
            for index, row in existing_df.iterrows():
                puuid = row['puuid']
                fullName = row['fullName']
                infoJson = json.loads(row['infoJson'])
                if search == "puuid" and puuid == value:
                    return infoJson
                if search == "fullName" and fullName == value:
                    return infoJson
                else:
                    return None
        else:
            return None
                
    def upload() -> None:
        '''
        1. Reads the CSV file containing the data.
        2. Converts the 'infoJson' column back from text to JSON.
        3. Uploads each row to the API using the 'upsertToTable' function.
        '''

        file_path = RIOT_USERS.FILE  # Path to the CSV file

        if not os.path.exists(file_path):
            print("CSV file not found. No data to upload.")
            return

        # Read the CSV file into a DataFrame
        data_df = pd.read_csv(file_path)

        if data_df.empty:
            print("CSV file is empty. No data to upload.")
            return

        # Convert 'infoJson' column back from text to JSON
        data_df['infoJson'] = data_df['infoJson'].apply(lambda x: json.loads(x))

        # Convert DataFrame to a list of dictionaries for API upload
        data_to_upload = data_df.to_dict(orient='records')

        # Upload each record to the API
        for record in data_to_upload:
            upsertToTable(RIOT_USERS.TABLE, record)

        print("Data uploaded successfully.")
    
    def upsert(puuid: str, fullName: str, infoJson: json) -> None:
        """
        Inserts or updates a row in a CSV file based on the puuid.

        Args:
            puuid (str): The unique identifier for the record.
            fullName (str): The full name associated with the record.
            infoJson (json): A JSON object containing additional information.

        """
        file_path = RIOT_USERS.FILE 

        new_row = pd.DataFrame({
            'puuid': [puuid],
            'fullName': [fullName],
            'infoJson': [json.dumps(infoJson)]
        })

        try:
            data = pd.read_csv(file_path)
        except FileNotFoundError:
            new_row.to_csv(file_path, index=False)
            return

        if puuid in data['puuid'].values:
            data.loc[data['puuid'] == puuid, ['fullName', 'infoJson']] = [fullName, json.dumps(infoJson)]
        else:
            data = pd.concat([data, new_row], ignore_index=True)

        data.to_csv(file_path, index=False)
    
    def delete():
        file = RIOT_USERS.FILE
        if os.path.exists(file):
            os.remove(file)

        
        

def fetchTable(tableName: str) -> json:
    return supabase.table(tableName).select("*").execute()

def upsertToTable(tableName: str, data: json) -> None:
    supabase.table(tableName).upsert(data).execute()

def delete_all(tableName: str) -> json:
    return supabase.table(tableName).delete("*").execute()