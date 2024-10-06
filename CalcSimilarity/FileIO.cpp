#include <iostream>
#include <fstream>
#include <set>
#include <vector>

#include "json/json.hpp"
#include "Point.hpp"
#include "ResultStructure.hpp"

void write_file(std::string filename, std::string data) {
    std::ofstream file(filename);
    file << data;
    file.close();
}

void output_result(SimilarityResult result, std::string filename) {
    nlohmann::json j;
    j["maxSimilarities"] = nlohmann::json::array();
    for (const auto& pieceResult : result.maxSimilarities) {
        nlohmann::json piece;
        piece["maxSimilarity"] = pieceResult.maxSimilarity;
        j["maxSimilarities"].push_back(piece);
    }
    j["similarityMean"] = result.similarityMean;
    write_file("output\\" + filename + ".json", j.dump());
}

std::vector<std::set<Point>> read_points_from_file(std::ifstream& file) {
    std::vector<std::set<Point>> result;

    int listLength;
    if (file.is_open()) {
        std::cin.rdbuf(file.rdbuf());
        std::cin >> listLength;

        for (int i = 0; i < listLength; i++) {
            int pieceLength;
            std::cin >> pieceLength;
            std::set<Point> piece;
            for (int j = 0; j < pieceLength; j++) {
                int x, y;
                std::cin >> x >> y;
                piece.insert(Point(x, y));
            }
            result.push_back(piece);
        }
    }

    return result;
}
