import {
  schemeGreys,
  schemePuBu,
  schemeRdPu,
  schemeReds,
  schemeYlGn,
  schemeYlOrBr,
} from "d3-scale-chromatic";

export const ColorSchemes = Object.freeze({
  yellow: schemeYlOrBr,
  pink: schemeRdPu,
  black: schemeGreys,
  red: schemeReds,
  green: schemeYlGn,
  blue: schemePuBu,
  grey: schemeGreys,
});

export const Colors = Object.freeze({
  yellow: "#FFED00",
  pink: "#BE3075",
  black: "#000000",
  red: "#EB001F",
  green: "#64A12D",
  blue: "#009EE0",
  grey: "grey",
});
