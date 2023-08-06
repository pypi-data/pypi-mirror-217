## Usage of PostProcessingService 

You can access following functions:


The provided package is a collection of functions for text preprocessing and cleaning. Here is a brief explanation of each function:

jaccard_similarity: To calculate jaccard similarity

levenshtein_distance: To calculate levenshtein distance

score: To calculate combined score

Function signature : score(score1, w1, score2, w2) where  score1,score2 is jaccard_similarity,levenshtein_distance & w1,w2 is weightage of score1, score2 resp. 

## Example usage:
>>  pip install postProcessingGEP==1.0.0

import postProcessingGEP

print(postProcessingGEP.PostProcessingService.jaccard_similarity(inputText1,inputText2))

