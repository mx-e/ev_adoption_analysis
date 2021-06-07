import MapView from "./views/map-view";
import styled from "styled-components";
import React, { useEffect, useState } from "react";
import { requestData } from "./requests";
import { CircularProgress } from "@material-ui/core";

const AppWrap = styled.div`
  background-color: #282c34;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: calc(10px + 2vmin);
  color: white;
`;

const Header = styled.h1`
  font-family: "Quicksand", "sans-serif";
  text-align: center;
  margin-bottom: 10px;
  font-size: 1.6em;
`;

const CenteredLayout = styled.div`
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
`;

const dispatchError = (err) => {
  console.log(err);
};

const App = () => {
  const [data, setData] = useState({});
  useEffect(() => requestData(setData, dispatchError), [setData]);

  const isDataLoaded = Object.keys(data).length > 0;

  return (
    <AppWrap>
      <Header>
        Is political alignment predictive of electric vehicle purchase decisions
        ?
      </Header>
      {isDataLoaded ? (
        <MapView data={data} />
      ) : (
        <CenteredLayout>
          <CircularProgress color="secondary" />
        </CenteredLayout>
      )}
    </AppWrap>
  );
};

export default App;
