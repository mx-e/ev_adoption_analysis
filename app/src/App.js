import MapView from "./views/map-view";
import styled from "styled-components";
import React from "react";

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
`;
const App = () => (
  <AppWrap>
    <Header>Electric Vehicle Adoption in Germany</Header>
    <MapView />
  </AppWrap>
);

export default App;
