class Point {
public:
    int x, y;
    Point(int _x, int _y) : x(_x), y(_y) {}

    bool operator== (const Point p) const {
        return x == p.x && y == p.y;
    }
    Point operator+ (const Point p) const {
        return Point(x + p.x, y + p.y);
    }
    Point operator- (const Point p) const {
        return Point(x - p.x, y - p.y);
    }

    bool operator< (const Point p) const {
        return p.x * 100 + p.y < x * 100 + y;
    }
};

struct PointHash {
    std::size_t operator()(const Point& p) const {
        return std::hash<int>()(p.x) ^ std::hash<int>()(p.y);
    }
};

struct PointEqual {
    bool operator()(const Point& p1, const Point& p2) const {
        return p1 == p2;
    }
};