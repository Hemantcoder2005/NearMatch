from pybktree import BKTree
import numpy as np
class UserData:
    def __init__(self, username, firstname, lastname):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname

class FuzzySearch:
    @staticmethod
    def _run(str1: str, str2: str):
        m = len(str1)
        n = len(str2)
        prev_row = [j for j in range(n + 1)]
        curr_row = [0] * (n + 1)

        for i in range(1, m + 1):
            curr_row[0] = i
            for j in range(1, n + 1):
                if str1[i - 1] == str2[j - 1]:
                    curr_row[j] = prev_row[j - 1]
                else:
                    curr_row[j] = 1 + min(
                        curr_row[j - 1],
                        prev_row[j],
                        prev_row[j - 1]
                    )
            prev_row = curr_row.copy()
        return curr_row[n]

    @staticmethod
    def lev_username(a: UserData, b: UserData):
        return FuzzySearch._run(a.username, b.username)

    @staticmethod
    def lev_firstname(a: UserData, b: UserData):
        return FuzzySearch._run(a.firstname, b.firstname)

    @staticmethod
    def lev_lastname(a: UserData, b: UserData):
        return FuzzySearch._run(a.lastname, b.lastname)

    @staticmethod 
    def getScore(distance,search_str, found_str):
        """Improved scoring that considers prefix matching"""
        search_len = len(search_str)
        found_len = len(found_str)
        
        if search_len == 0 or found_len == 0:
            return 0
        
        max_len = max(search_len, found_len)
        base_score = 1 - (distance / max_len)
        
        prefix_bonus = 0
        if found_str.lower().startswith(search_str.lower()):
            prefix_bonus = 0.3
        elif search_str.lower()[0] == found_str.lower()[0]:
            prefix_bonus = 0.1
            
        contains_bonus = 0
        if search_str.lower() in found_str.lower():
            contains_bonus = 0.15
            
        return min(1.0, base_score + prefix_bonus + contains_bonus)
    def adaptive_distance(self, query_length):
        """Calculate appropriate distance threshold based on query length"""
        if query_length <= 2:
            return max(5, query_length + 3)
        elif query_length <= 4:
            return query_length + 2
        else:
            return max(2, query_length // 2)
    def __init__(self, user_data,threshold = 0.2):
        self.data = [UserData(u["username"], u["firstname"], u["lastname"]) for u in user_data]
        self.tree_username = None
        self.tree_firstname = None
        self.tree_lastname = None
        self.weights = np.array([0.5,0.3,0.2])
        self.weightage_types = ['exp','linear']
        self.weightage_type = None 
        self.threshold  = threshold

    def build_tree(self):
        self.tree_username = BKTree(self.lev_username, self.data)
        self.tree_firstname = BKTree(self.lev_firstname, self.data)
        self.tree_lastname = BKTree(self.lev_lastname, self.data)

    def search_by_username(self, s:str, distance=5):
        if self.tree_username is None:
            raise ValueError("Tree not built")
        return self.tree_username.find(UserData(s, "", ""), distance)

    def search_by_firstname(self, s:str, distance=5):
        if self.tree_firstname is None:
            raise ValueError("Tree not built")
        return self.tree_firstname.find(UserData("", s, ""), distance)

    def search_by_lastname(self, s, distance=5):
        if self.tree_lastname is None:
            raise ValueError("Tree not built")
        return self.tree_lastname.find(UserData("", "", s), distance)
    def getLossedScore(self,pos,score):
        if self.weightage_type == None:
            raise ValueError("Weightage type not set. You can set up  by calling the rank method")
        if self.weightage_type == 'linear':
            return score * (1/(1+pos))
        if self.weightage_type == 'exp':
            return score * (np.exp(-pos))
    def rank(self, string_to_search: str, distance=5):
        if not all([self.tree_username, self.tree_firstname, self.tree_lastname]):
            raise ValueError("Tree not built")
        results_username = sorted(self.search_by_username(string_to_search, distance), key=lambda p: p[0])
        results_firstname = sorted(self.search_by_firstname(string_to_search.lower(), distance), key=lambda p: p[0])
        results_lastname = sorted(self.search_by_lastname(string_to_search.lower(), distance), key=lambda p: p[0])
        ranking = {} # every username has a score
        search_String_len = len(string_to_search)
        for user in results_username:
            distance = user[0]
            user_info = user[1]
            username = user_info.username
            found = user_info.username
            found_len = len(found)
            score = self.getScore(distance,string_to_search,found) * self.weights[0]
            try:
                ranking[username] += score
            except KeyError:
                ranking[username] = score

        for user in results_firstname:
            distance = user[0]
            user_info = user[1]
            username = user_info.username
            found = user_info.firstname
            found_len = len(found)
            score = self.getScore(distance,string_to_search,found) * self.weights[1]
            try:
                ranking[username] += score
            except KeyError:
                ranking[username] = score

        for user in results_lastname:
            distance = user[0]
            user_info = user[1]
            username = user_info.username
            found = user_info.lastname
            found_len = len(found)
            score = self.getScore(distance,string_to_search,found) * self.weights[2]
            try:
                ranking[username] += score
            except KeyError:
                ranking[username] = score
        return ranking
    def sentence_ranking(self, string_to_search: str,weightage = 'exp') -> list:
        if weightage not in self.weightage_types:
            print(f" We have {self.weightage_types} weightage types. Please choose from them.")
            raise ValueError("Invalid weightage type")
        distance = self.adaptive_distance(len(string_to_search))
        self.weightage_type = weightage
        rank_score = {}
        words = string_to_search.split()
        for pos in range(len(words)):
            word = words[pos]
            d = self.rank(word, distance)
            for username, score in d.items():
                try:
                    rank_score[username] += self.getLossedScore(pos,score)
                except KeyError:
                    rank_score[username] = self.getLossedScore(pos,score)
        return sorted(
                [k for k, v in rank_score.items() if v > self.threshold],
                key=rank_score.get,
                reverse=True
            )


