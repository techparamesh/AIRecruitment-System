from pp_algorithm import raw_data_df
from utils import collection_creation, records_insertion, records_deletion
import ast

# Create collection on Mongodb to store selected candidates
selected_candidates = collection_creation('Selected_Candidates')

# Delete previously stored candidates from MongoDB.
records_deletion(query={"_id": {"$gte": 0}}, collection=selected_candidates)

# Create list with the new candidates
selected_df = raw_data_df.loc[raw_data_df['selected'] == True][['display_name', 'email']]
candidates_list = []
candidate_id = 1
for index, row in selected_df.iterrows():
    row['_id'] = candidate_id
    file = row.to_json()
    dict_file = ast.literal_eval(file)
    candidates_list.append(dict_file)
    candidate_id += 1

# Insert new candidates into mongodb
records_insertion(candidates_list, selected_candidates)