#include <iostream>
#include <fstream>

#include <vector>
#include <set>
#include <unordered_map>
#include <cmath>
#include <numeric>

#include "json/json.hpp"
#include "Point.hpp"
#include "ResultStructure.hpp"
#include "FileIO.hpp"


SimilarityResult CalcSimilarity(
    std::vector<std::set<Point>> targetPieces,
    std::vector<std::set<Point>> originPieces
);

std::string getFileBasename(std::string filepath);


int main(int argc, char* argv[]) {

    // Check arguments
    if (argc < 3) {
        std::cout << "Usage: " << argv[0] << " <target_point_file> <origin_point_file1> ..." << std::endl;
        return 1;
    }

    // Read target file
    std::ifstream targetPointFile(argv[1]);
    std::vector<std::set<Point>> targetPieces = read_points_from_file(targetPointFile);

    // Read origin files
    std::vector<std::set<Point>> originPieces;
    for (int i = 2; i < argc; i++) {
        std::ifstream originPointFile(argv[i]);
        std::vector<std::set<Point>> p = read_points_from_file(originPointFile);
        originPieces.insert(originPieces.end(), p.begin(), p.end());
    }

    // Calculate similarity
    std::string outputFilename = getFileBasename(std::string(argv[1]));
    SimilarityResult result = CalcSimilarity(targetPieces, originPieces);
    output_result(result, outputFilename);
    return 0;
}


SimilarityResult CalcSimilarity(
    std::vector<std::set<Point>> targetPieces,
    std::vector<std::set<Point>> originPieces
) {

    SimilarityResult result;
    std::vector<double> similarities;

    for (size_t i = 0; i < targetPieces.size(); i++) {
        PieceSimilarityResult pieceResult;
        std::vector<double> _similarities;

        for (size_t j = 0; j < originPieces.size(); j++) {
            std::unordered_map<Point, int, PointHash, PointEqual> transformVectors;

            auto& targetPiece = targetPieces[i];
            auto& originPiece = originPieces[j];

            // Count transform vectors
            for (const auto& targetPoint : targetPiece) {
                for (const auto& originPoint : originPiece) {
                    Point transform = originPoint - targetPoint;
                    transformVectors[transform]++;
                }
            }

            // Get max count transform vector
            int _max = 0;
            Point _maxTransform(0, 0);
            for (const auto& countData : transformVectors) {
                if (countData.second > _max) {
                    _max = countData.second;
                    _maxTransform.x = countData.first.x;
                    _maxTransform.y = countData.first.y;
                }
            }

            // Calculate targetPiece-originPiece similarity
            double _maxSimilarity = (double)_max / std::max(targetPiece.size(), originPiece.size());
            _similarities.push_back(_maxSimilarity);
        }

        // Get max similarity among all targetPiece-originPiece similarity
        double _maxSimilarity = *std::max_element(_similarities.begin(), _similarities.end());
        std::cout << "[" << i << " / " << targetPieces.size() << "] " << _maxSimilarity << std::endl;

        pieceResult.maxSimilarity = _maxSimilarity;
        result.maxSimilarities.push_back(pieceResult);
        similarities.push_back(_maxSimilarity);
    }

    // Calculate mean similarity
    double sum = 0;
    for (const auto& similarity : similarities) {
        sum += similarity;
    }
    double mean = sum / similarities.size();
    std::cout << "Mean: " << mean << std::endl;
    result.similarityMean = mean;

    return result;
}

std::string getFileBasename(std::string filepath) {
    std::string base_filename = filepath.substr(filepath.find_last_of("/\\") + 1);
    std::string::size_type const p(base_filename.find_last_of('.'));
    return base_filename.substr(0, p);
}
