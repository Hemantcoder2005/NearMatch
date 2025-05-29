from NearMatch import FuzzySearch
from  data_gen import  generate_mock_users

mock_data = generate_mock_users(10)

search = FuzzySearch(mock_data)
search.build_tree()

results = search.sentence_ranking("John Thomas",weightage='exp')
print(results)
