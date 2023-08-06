import Levenshtein

class PostProcessingService:
    def jaccard_similarity(str1, str2):
        set1 = set(str1.lower()) 
        set2 = set(str2.lower()) 
        
        intersection = set1.intersection(set2) 
        union = set1.union(set2) 
        
        similarity = len(intersection) / len(union)  
        
        return similarity
    
    def levenshtein_distance(str1, str2):
        distance = Levenshtein.distance(str1, str2)
        return distance
    
    def score(score1, w1, score2, w2):
        return float(round(((score1 * w1) + (score2 * w2)) * 100))