def isPointinPolygon(point, rangelist):
    # Judge whether the point is within the outsourcing rectangle. If not, return false
    lnglist, latlist = [], []
    for i in range(len(rangelist)-1):
        lnglist.append(rangelist[i][0])
        latlist.append(rangelist[i][1])
    maxlng, minlng = max(lnglist), min(lnglist)
    maxlat, minlat = max(latlist), min(latlist)
    if point[0] > maxlng or point[0] < minlng or point[1] > maxlat or point[1] < minlat:
        return False
    count = 0
    point1 = rangelist[0]
    for i in range(1, len(rangelist)):
        point2 = rangelist[i]
        # Point coincides with polygon vertex
        if (point[0] == point1[0] and point[1] == point1[1]) or (point[0] == point2[0] and point[1] == point2[1]):
            print("on vertex")
            return False
        # Judge whether the two ends of the line segment are on both sides of the ray.
        # If not, they will not intersect（-∞，lat）（lng,lat）
        if (point1[1] < point[1] <= point2[1]) or (point1[1] >= point[1] > point2[1]):
            # Find the intersection of line segment and ray, and then compare with lat
            point12lng = point2[0] - (point2[1] - point[1]) * (point2[0] - point1[0])/(point2[1] - point1[1])
            # Point on polygon edge
            if point12lng == point[0]:
                print("Point on polygon edge")
                return False
            if point12lng < point[0]:
                count += 1
        point1 = point2
    if count % 2 == 0:
        return False
    else:
        return True

if __name__ == '__main__':
    test_point1 = [1.3, 1.2]
    test_polygonlist = [[0, 0], [2, 0], [2, 2], [1, 1], [0, 2], [0, 0]]
    print(isPointinPolygon(test_point1, test_polygonlist))
