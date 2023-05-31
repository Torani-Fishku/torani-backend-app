const express = require("express");
const app = express();
const axios = require("axios");

const polygons = require("./polygon.json");

// Parse URL-encoded bodies (as sent by the client)
app.use(express.urlencoded({ extended: true }));

// Define the route to handle location properties retrieval
app.get("/location", (req, res) => {
  // Extract the longitude and latitude from the query parameters
  const longitude = parseFloat(req.query.longitude);
  const latitude = parseFloat(req.query.latitude);
  console.log(longitude, latitude);

  // Initialize variables for tracking the closest polygon
  let closestPolygon,
    closestDistance = Infinity;
  let targetCode, targetName, targetURI;

  // Iterate through all polygons
  polygons.features.forEach((polygon) => {
    const polygonCoordinates = polygon.geometry.coordinates;
    const isInside = isInsidePolygon([longitude, latitude], polygonCoordinates);

    if (isInside) {
      // Point is inside the polygon, return the polygon properties
      res.json(polygon.properties);
      targetCode = polygon.properties.WP_1;
      targetName = polygon.properties.WP_IMM;
      targetURI = `https://peta-maritim.bmkg.go.id/public_api/perairan/${targetCode}_${targetName}.json`;
      // Call the BMKG Perairan API
      axios
        .get(targetURI)
        .then((response) => {
          res.json(response.data.data);
        })
        .catch((error) => {
          console.log(error);
        });
      return;
    } else {
      // Calculate the distance between the point and the polygon
      const distance = calculateDistance(
        [longitude, latitude],
        polygonCoordinates
      );

      // Update the closest polygon if the current distance is smaller
      if (distance < closestDistance) {
        closestDistance = distance;
        closestPolygon = polygon;
      }
    }
  });

  if (closestPolygon) {
    // Return the properties of the closest polygon
    targetCode = closestPolygon.properties.WP_1;
    targetName = closestPolygon.properties.WP_IMM;
    targetURI = `https://peta-maritim.bmkg.go.id/public_api/perairan/${targetCode}_${targetName}.json`;
    // Call the BMKG API
    axios
      .get(targetURI)
      .then((response) => {
        res.json(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  } else {
    res.json({ message: "Location not found." });
  }
});

// Function to check if a point is inside a polygon
function isInsidePolygon(point, polygonCoordinates) {
  const [x, y] = point;
  let isInside = false;

  for (
    let i = 0, j = polygonCoordinates.length - 1;
    i < polygonCoordinates.length;
    j = i++
  ) {
    const xi = polygonCoordinates[i][0];
    const yi = polygonCoordinates[i][1];
    const xj = polygonCoordinates[j][0];
    const yj = polygonCoordinates[j][1];

    const intersect =
      yi > y !== yj > y && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi;

    if (intersect) {
      isInside = !isInside;
    }
  }

  return isInside;
}

// Function to calculate the distance between a point and a polygon
function calculateDistance(point, polygonCoordinates) {
  let closestDistance = Infinity;

  // Iterate through all polygon edges
  for (let i = 0; i < polygonCoordinates.length; i++) {
    const polygonEdge = polygonCoordinates[i];

    // Iterate through all points of the polygon edge
    for (let j = 0; j < polygonEdge.length - 1; j++) {
      const pointA = polygonEdge[j];
      const pointB = polygonEdge[j + 1];

      const distance = calculateDistanceToSegment(point, pointA, pointB);

      // Update the closest distance if the current distance is smaller
      if (distance < closestDistance) {
        closestDistance = distance;
      }
    }
  }

  return closestDistance;
}

// Function to calculate the distance between a point and a line segment
function calculateDistanceToSegment(point, segmentStart, segmentEnd) {
  const [px, py] = point;
  const [x1, y1] = segmentStart;
  const [x2, y2] = segmentEnd;

  const dx = x2 - x1;
  const dy = y2 - y1;

  const t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy);

  if (t <= 0) {
    return getPointDistance([px, py], [x1, y1]);
  } else if (t >= 1) {
    return getPointDistance([px, py], [x2, y2]);
  } else {
    const nearestX = x1 + t * dx;
    const nearestY = y1 + t * dy;
    return getPointDistance([px, py], [nearestX, nearestY]);
  }
}

// Function to calculate the distance between two points
function getPointDistance(point1, point2) {
  const [x1, y1] = point1;
  const [x2, y2] = point2;

  return Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
}

// Start the server
app.listen(3000, () => {
  console.log("Server running on http://localhost:3000");
});
