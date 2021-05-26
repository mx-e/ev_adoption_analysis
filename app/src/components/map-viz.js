import React, { useMemo, useState } from "react";
import { geoBounds, geoCentroid, geoConicEqualArea } from "d3-geo";
import { scaleThreshold } from "@visx/scale";
import { schemeRdPu } from "d3-scale-chromatic";
import { LegendThreshold } from "@visx/legend";
import styled from "styled-components";
import { Slider } from "@material-ui/core";
import { makeStyles } from "@material-ui/core";

const MapVizWrap = styled.div`
  flex-basis: 450px;
  flex-grow: 1;
  max-width: 650px;
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

const SliderWrap = styled.div`
  width: 80%;
  margin-left: auto;
  margin-right: auto;
  font-family: "Quicksand", "sans-serif";
`;

const PolyLine = ({ coordinates, projection, color }) => (
  <polygon
    stroke={"rgba(255,255,255,0.9)"}
    strokeWidth={"0.2px"}
    points={coordinates
      .map((coordinatePair) => projection(coordinatePair).toString())
      .join(" ")}
  />
);

const Polygon = ({ coordinateList, projection, name, color }) => (
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

const MultiPolygon = ({ polygonList, projection, name, color }) => (
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

const getYearsFromMeasure = (geoJson, measure) =>
  Object.keys(geoJson.features[0].data[measure]);

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
    [name]
  );
};

const MapViz = ({ geoJson, dataProperty }) => {
  const measure = dataProperty;
  const [long, lat] = useMemo(() => geoCentroid(geoJson), []);
  const [[left, bottom], [right, top]] = useMemo(() => geoBounds(geoJson), []);
  const yearsAvailable = getYearsFromMeasure(geoJson, measure);
  const [year, setYear] = useState(yearsAvailable.slice(-1)[0]);

  const projection = geoConicEqualArea()
    .parallels([bottom, top])
    .scale(3500)
    .rotate([-8, 0])
    .center([left, lat]);

  const [minX, minY] = projection([left, top]);
  const [maxX, maxY] = projection([right, bottom]);
  const padding = 20;

  const thresholds = [100, 200, 400, 800, 1600, 3200, 6400];
  const colorScale = scaleThreshold()
    .domain(thresholds)
    .range(schemeRdPu[thresholds.length + 1]);

  return (
    <MapVizWrap>
      <svg
        width={"100%"}
        height={"600px"}
        viewBox={`${minX - padding - 15} ${minY - padding} ${
          maxX - minX + 2 * padding
        } ${maxY - minY + 2 * padding}`}
      >
        {geoJson.features.map((feature) => {
          const { GEN, AGS } = feature.properties;
          const value = feature.data[measure][year];
          const { type, coordinates } = feature.geometry;
          return (
            <g fill={colorScale(value)}>
              <Coordinates
                type={type}
                name={AGS}
                coordinates={coordinates}
                projection={projection}
              />
            </g>
          );
        })}
      </svg>
      <LegendWrap>
        <LegendThreshold
          scale={colorScale}
          direction="row"
          labelMargin="3px 0 0 0"
          itemDirection="column"
          shapeWidth={"70px"}
          labelDelimiter={"-"}
          shapeMargin={"0"}
          labelLower={"<"}
          labelUpper={">"}
        />
      </LegendWrap>
      <SliderWrap>
        <Slider
          classes={useStyles()}
          color={"secondary"}
          value={year}
          onChange={(_, val) => setYear(val)}
          aria-labelledby="discrete-slider"
          step={1}
          marks={yearsAvailable.map((y) => ({
            label: `${y}`,
            value: y,
          }))}
          min={Math.min(...yearsAvailable)}
          max={Math.max(...yearsAvailable)}
        />
      </SliderWrap>
    </MapVizWrap>
  );
};

export default MapViz;
