#This code demonstartes how to evaluate the semantic similarity between two sentences using the SentenceTransformer library.
from llama_index.core.evaluation import SemanticSimilarityEvaluator

#create instance of the SemanticSimilarityEvaluator
evaluator=SemanticSimilarityEvaluator()

# Define function to evaluate semantic similarity between two sentences
def evaluate_similarity():
    response ="""cat is on the table
                 mat is on the floor"""
    reference="""table is occupied by cat
                 floor is occupied by mat"""

#evaluate function returns a dictionary with the the score and passing key value
    result=evaluator.evaluate(response=response,reference=reference)
    print("score:",result.score)
    print("pass:",result.passing)#default threshold is 0.8.

#the following function is used to run the the async function
def main():
    evaluate_similarity()

if __name__ == "__main__":
    main()