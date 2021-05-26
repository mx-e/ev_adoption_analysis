import React, { useEffect, useMemo, useState } from "react";
import { requestData } from "../requests";
import { CircularProgress } from "@material-ui/core";
import MapViz from "../components/map-viz";
import styled from "styled-components";

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

const CenteredLayout = styled.div`
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
`;

const DataProperties = Object.freeze({
  BEV_TOTAL: "battery_electric",
  PETROL_TOTAL: "petrol",
  DIESEL_TOTAL: "diesel",
});

const dispatchError = (err) => {
  console.log(err);
};

const initialOpts = {};

export const MapView = () => {
  const [optsState, setOptsState] = useState(initialOpts);
  const [data, setData] = useState({});
  const [selectedProperty, setSelectedProperty] = useState(
    DataProperties.BEV_TOTAL
  );
  useEffect(() => requestData(setData, dispatchError), [setData]);
  console.log(data);
  const handleChange = (event) => {
    setSelectedProperty(event.target.value);
  };
  const isDataLoaded = Object.keys(data).length > 0;
  return isDataLoaded ? (
    <MapViewWrap>
      <Col>
        <div
          style={{ display: "flex", justifyContent: "center" }}
          className="bp3-select bp3-minimal"
        >
          <select value={selectedProperty} onChange={handleChange}>
            {Object.values(DataProperties).map((property) => (
              <option value={property}>{property}</option>
            ))}
          </select>
        </div>
        <MapViz geoJson={data} dataProperty={selectedProperty} />
      </Col>
    </MapViewWrap>
  ) : (
    <CenteredLayout>
      <CircularProgress color="secondary" />
    </CenteredLayout>
  );
};

export default MapView;
