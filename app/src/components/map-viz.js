import React, { useMemo } from "react";
import { geoBounds, geoCentroid, geoConicEqualArea } from "d3-geo";
import { scaleThreshold } from "@visx/scale";
import Pie from "@visx/shape/lib/shapes/Pie";
import { scaleOrdinal } from "@visx/scale";
import { Group } from "@visx/group";

import { Tooltip, defaultStyles, useTooltip } from "@visx/tooltip";
import { LegendThreshold, LegendOrdinal } from "@visx/legend";
import styled from "styled-components";
import { makeStyles } from "@material-ui/core";
import { ColorSchemes, Colors } from "../utils/colorUtils";
import { round } from "../utils/statUtils";

const MapVizWrap = styled.div`
  flex-basis: 450px;
  flex-grow: 1;
  max-width: 650px;
  position: relative;
`;

const LegendWrap = styled.div`
  font-size: 9px;
  margin-top: 10px;
  display: flex;
  flex-direction: row;
  justify-content: center;
  width: 100%;
  height: 50px;
`;

const PolyLine = ({ coordinates, projection }) => (
  <polygon
    points={coordinates
      .map((coordinatePair) => projection(coordinatePair).toString())
      .join(" ")}
  />
);

const Polygon = ({ coordinateList, projection, name }) => (
  <g>
    {coordinateList.map((polygon, i) => (
      <PolyLine
        key={name + "-" + i}
        coordinates={polygon}
        projection={projection}
      />
    ))}
  </g>
);

const MultiPolygon = ({ polygonList, projection, name }) => (
  <g>
    {polygonList.map((polygon, i) => (
      <Polygon
        key={name + "-" + i}
        name={name + "-" + i}
        coordinateList={polygon}
        projection={projection}
      />
    ))}
  </g>
);

const useStyles = makeStyles({
  markLabel: {
    color: "white",
  },
});

const Coordinates = ({ type, name, projection, coordinates }) => {
  return useMemo(
    () =>
      type === "MultiPolygon" ? (
        <MultiPolygon
          name={name}
          polygonList={coordinates}
          projection={projection}
        />
      ) : (
        <Polygon
          name={name}
          coordinateList={coordinates}
          projection={projection}
        />
      ),
    []
  );
};

const MapViz = ({ geoJson, selectedDataSource, metaData, year }) => {
  const measure = selectedDataSource.key;
  const [long, lat] = useMemo(() => geoCentroid(geoJson), []);
  const [[left, bottom], [right, top]] = useMemo(() => geoBounds(geoJson), []);

  const {
    showTooltip,
    hideTooltip,
    tooltipOpen,
    tooltipData,
    tooltipLeft,
    tooltipTop,
  } = useTooltip();

  const projection = geoConicEqualArea()
    .parallels([bottom, top])
    .scale(3500)
    .rotate([-8, 0])
    .center([left, lat]);

  useMemo(
    () =>
      geoJson.features.forEach((feature) => {
        feature.properties.centroid = projection(geoCentroid(feature));
      }),
    []
  );

  const [minX, minY] = projection([left, top]);
  const [maxX, maxY] = projection([right, bottom]);
  const padding = 20;

  const thresholds = selectedDataSource.thresholds;
  const colorScale = scaleThreshold()
    .domain(thresholds)
    .range(ColorSchemes[selectedDataSource.colorScheme][thresholds.length + 1]);

  const tooltipStyles = {
    ...defaultStyles,
    width: 130,
    textOverflow: "ellipsis",
  };
  let tooltipTimeout;

  const votesMetaData = metaData.filter(
    (source) => source.dataTopic === "votes"
  );
  const partiesScale = scaleOrdinal({
    domain: votesMetaData.map((source) => source.key),
    range: votesMetaData.map((source) => Colors[source.colorScheme]),
  });

  return (
    <MapVizWrap>
      {tooltipOpen && tooltipData && (
        <Tooltip top={tooltipTop} left={tooltipLeft} style={tooltipStyles}>
          <div>
            <strong>{tooltipData.title}</strong>
          </div>
          <div>
            {round(
              selectedDataSource.hasMultipleYears
                ? tooltipData[measure][year]
                : tooltipData[measure]
            ) + "%"}
          </div>
          <div
            style={{
              padding: 5,
              width: 130,
              display: "flex",
              justifyContent: "space-between",
            }}
          >
            <div
              style={{
                display: "flex",
                justifyContent: "center",
                flexDirection: "column",
              }}
            >
              <svg width={70} height={70}>
                <Group opacity={0.9} top={35} left={35}>
                  <Pie
                    data={votesMetaData.map((source) => ({
                      ...source,
                      value: tooltipData[source.key],
                    }))}
                    pieValue={(datum) => datum.value}
                    pieSortValues={null}
                    outerRadius={35}
                    fill={(datum) => partiesScale(datum.data.key)}
                    centroid={([x, y], datum) =>
                      datum.value > 10 ? (
                        <text
                          x={x - 5}
                          y={y}
                          style={{ fontSize: 4 }}
                          fill={"white"}
                        >
                          {round(datum.value) + "%"}
                        </text>
                      ) : null
                    }
                  />
                </Group>
              </svg>
            </div>
            <LegendOrdinal
              scale={partiesScale}
              direction="column"
              shape={"circle"}
              style={{ fontSize: 5 }}
              labelMargin="0 0 0 1px"
              itemDirection="row"
              shapeWidth={8}
              shapeHeight={8}
              shapeMargin={"0"}
            />
          </div>
        </Tooltip>
      )}
      <svg
        width={"100%"}
        height={"600px"}
        viewBox={`${minX - padding - 15} ${minY - padding} ${
          maxX - minX + 2 * padding
        } ${maxY - minY + 2 * padding}`}
      >
        {useMemo(
          () =>
            [
              ...geoJson.features.filter(
                (feature) => feature.properties.AGS !== tooltipData?.id
              ),
              geoJson.features.find(
                (feature) => feature.properties.AGS === tooltipData?.id
              ),
            ].map((feature) => {
              if (!feature) return null;
              const { GEN, AGS, centroid } = feature.properties;
              const value = selectedDataSource.hasMultipleYears
                ? feature.data[measure][year]
                : feature.data[measure];
              const { type, coordinates } = feature.geometry;
              const [centroidLeft, centroidTop] = centroid;
              return (
                <g
                  key={AGS}
                  fill={colorScale(value)}
                  onMouseLeave={() => {
                    tooltipTimeout = window.setTimeout(hideTooltip, 300);
                  }}
                  onMouseMove={() => {
                    if (tooltipTimeout) clearTimeout(tooltipTimeout);
                    showTooltip({
                      tooltipData: { ...feature.data, title: GEN, id: AGS },
                      tooltipTop: centroidTop - padding,
                      tooltipLeft: centroidLeft - minX + padding * 4,
                    });
                  }}
                  onClick={() => {
                    if (tooltipTimeout) clearTimeout(tooltipTimeout);
                    showTooltip({
                      tooltipData: { ...feature.data, title: GEN, id: AGS },
                      tooltipTop: centroidTop - padding,
                      tooltipLeft: centroidLeft - minX + padding * 4,
                    });
                  }}
                  stroke={
                    tooltipData?.id === AGS
                      ? "rgba(80,80,80,0.9)"
                      : "rgba(255,255,255,0.9)"
                  }
                  strokeWidth={tooltipData?.id === AGS ? "0.6px" : "0.2px"}
                  id={GEN}
                >
                  <Coordinates
                    type={type}
                    name={AGS}
                    coordinates={coordinates}
                    projection={projection}
                  />
                </g>
              );
            }),
          [tooltipData?.id, measure, year]
        )}
      </svg>
      <LegendWrap>
        <LegendThreshold
          scale={colorScale}
          direction="row"
          labelMargin="3px 0 0 0"
          itemDirection="column"
          shapeWidth={"60px"}
          labelDelimiter={"-"}
          shapeMargin={"0"}
          labelLower={"<"}
          labelUpper={">"}
        />
      </LegendWrap>
    </MapVizWrap>
  );
};

export default MapViz;
