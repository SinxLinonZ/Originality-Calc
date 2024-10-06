void write_file(std::string filename, std::string data);
void output_result(SimilarityResult result, std::string filename);
std::vector<std::set<Point>> read_points_from_file(std::ifstream& file);
