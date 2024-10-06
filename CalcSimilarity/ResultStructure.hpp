#include <vector>

struct PieceSimilarityResult {
    double maxSimilarity;
};

struct SimilarityResult {
    std::vector<PieceSimilarityResult> maxSimilarities;
    double similarityMean;
};
