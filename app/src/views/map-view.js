import React, { useState } from "react";
import { makeStyles, Slider } from "@material-ui/core";
import MapViz from "../components/map-viz";
import styled from "styled-components";
import { scaleLinear } from "@visx/scale";
import { Circle } from "@visx/shape";
import { Axis, Orientation } from "@visx/axis";
import { ColorSchemes, Colors } from "../utils/colorUtils";
import { correlation, round } from "../utils/statUtils";

const MapViewWrap = styled.div`
  flex-grow: 1;
  display: flex;
  flex-direction: row;
  justify-content: center;
  width: 100%;
`;

const Col = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
`;

const SubHeader = styled.h4`
  font-family: "Quicksand", "sans-serif";
  text-align: center;
  margin-bottom: 10px;
  font-size: 0.6em;
`;

const SliderWrap = styled.div`
  width: 80%;
  margin-left: auto;
  margin-right: auto;
  font-family: "Quicksand", "sans-serif";
`;

const getYearsFromMeasure = (geoJson, measure) =>
  Object.keys(geoJson.features[0].data[measure]);

const useStyles = makeStyles({
  markLabel: {
    color: "white",
  },
});

const minAndMax = (arr) => [Math.min(...arr), Math.max(...arr)];

const ScatterViz = ({ data, xDataSource, yDataSource, metaData, year }) => {
  const xData = data.map((feature) => feature.data[xDataSource.key]);
  const yData = data.map((feature) => feature.data[yDataSource.key][year]);

  console.log(data);
  console.log(xData, yData);
  const [minX, maxX] = minAndMax(xData);
  const [minY, maxY] = minAndMax(yData);
  const padding = 40;
  const xScale = scaleLinear({
    domain: [minX, maxX],
    range: [padding, 480 - padding],
  });
  const yScale = scaleLinear({
    domain: [0, 1],
    range: [400 - padding, padding],
  });

  const correlationCoeff = correlation(xData, yData);

  return (
    <div>
      <svg width={480} height={400}>
        {data.map((point, i) => (
          <Circle
            key={`point-${point[0]}-${i}`}
            className="dot"
            cx={xScale(xData[i])}
            cy={yScale(yData[i])}
            r={2}
            fill={Colors[xDataSource.colorScheme]}
            opacity={0.7}
          />
        ))}
        <Axis
          orientation={Orientation.bottom}
          scale={xScale}
          top={400 - padding}
          stroke={"whitesmoke"}
          tickLabelProps={() => ({
            style: {
              fill: "whitesmoke",
              fontSize: 8,
              transform: "translate(2px, -10px)",
            },
          })}
          tickLength={10}
          tickStroke={"whitesmoke"}
          label={"% of votes"}
          labelOffset={5}
          labelProps={{
            fill: "whitesmoke",
            fontSize: 10,
          }}
        />
        <Axis
          scale={yScale}
          orientation={Orientation.left}
          left={padding}
          stroke={"whitesmoke"}
          tickLabelProps={() => ({
            style: {
              fill: "whitesmoke",
              fontSize: 8,
              transform: "translate(-17px, 2.5px)",
            },
          })}
          tickLength={4}
          tickStroke={"whitesmoke"}
          label={"% of total vehicles"}
          labelOffset={25}
          labelProps={{
            fill: "whitesmoke",
            fontSize: 10,
          }}
        />
      </svg>
      <div style={{ padding: 10, display: "flex", justifyContent: "center" }}>
        <span>Correlation Coefficient: {round(correlationCoeff)}</span>
      </div>
    </div>
  );
};

export const MapView = ({ data }) => {
  const [selectedVehicleStock, setSelectedVehicleStock] =
    useState("battery_electric");
  const [selectedParty, setSelectedParty] = useState("greens");

  const yearsAvailable = getYearsFromMeasure(data, selectedVehicleStock);
  const [year, setYear] = useState(yearsAvailable.slice(-1)[0]);

  const classes = useStyles();
  console.log(data);
  const handleStockSelection = (event) => {
    setSelectedVehicleStock(event.target.value);
  };
  const handlePartySelection = (event) => {
    setSelectedParty(event.target.value);
  };
  const metaData = data?.meta;
  console.log(metaData);
  return (
    <MapViewWrap>
      <Col>
        <SubHeader>select a vehicle stock</SubHeader>
        <div
          style={{ display: "flex", justifyContent: "center" }}
          className="bp3-select bp3-minimal"
        >
          <select value={selectedVehicleStock} onChange={handleStockSelection}>
            {metaData
              .filter((dataSource) => dataSource.dataTopic === "vehicles")
              .map((dataSource) => (
                <option key={dataSource.key} value={dataSource.key}>
                  {dataSource.name}
                </option>
              ))}
          </select>
        </div>
        <MapViz
          geoJson={data}
          selectedDataSource={metaData.find(
            (dataSource) => dataSource.key === selectedVehicleStock
          )}
          metaData={metaData}
          year={year}
        />
        <SubHeader>select a political party</SubHeader>
        <div
          style={{ display: "flex", justifyContent: "center" }}
          className="bp3-select bp3-minimal"
        >
          <select value={selectedParty} onChange={handlePartySelection}>
            {metaData
              .filter((dataSource) => dataSource.dataTopic === "votes")
              .map((dataSource) => (
                <option key={dataSource.key} value={dataSource.key}>
                  {dataSource.name}
                </option>
              ))}
          </select>
        </div>
        <ScatterViz
          data={data.features.map((feature) => ({
            properties: feature.properties,
            data: feature.data,
          }))}
          metaData={metaData}
          xDataSource={metaData.find(
            (dataSource) => dataSource.key === selectedParty
          )}
          yDataSource={metaData.find(
            (dataSource) => dataSource.key === selectedVehicleStock
          )}
          year={year}
        />

        <SubHeader>see how the values changed over time</SubHeader>
        <SliderWrap>
          <Slider
            classes={classes}
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
      </Col>
    </MapViewWrap>
  );
};

export default MapView;
