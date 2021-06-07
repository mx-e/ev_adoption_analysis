const sqlite3 = require("sqlite3").verbose();
const fs = require("fs");

const db = new sqlite3.Database("../ev_adoption.sqlite");

let appData = {};

const convertToPercent = (number, decimal) =>
  Math.round(number * 100 * Math.pow(10, decimal)) / Math.pow(10, decimal);

const add_county_data = (err, { name, statistical_id }) => {
  geoDataMatch = appData.features.find(
    (feature) => parseInt(feature.properties.RS) === statistical_id
  );
};

const get_total_stock = (vehicleData) => {
  const { petrol, diesel, gas, hybrid_total, battery_electric, other } =
    vehicleData;
  return petrol + diesel + gas + hybrid_total + battery_electric + other;
};

const add_stocks_to_county = (err, row) => {
  const { year, county_id, ...vehicleData } = row;
  totalStock = get_total_stock(vehicleData);
  geoDataMatch = appData.features.find(
    (feature) => parseInt(feature.properties.RS) === county_id
  );
  if (geoDataMatch.data) {
    Object.keys(vehicleData).forEach((property) => {
      geoDataMatch.data[property][year] = convertToPercent(
        vehicleData[property] / totalStock,
        6
      );
    });
  } else {
    geoDataMatch.data = Object.fromEntries(
      Object.keys(vehicleData).map((property) => [
        property,
        Object.fromEntries([
          [year, convertToPercent(vehicleData[property] / totalStock, 6)],
        ]),
      ])
    );
  }
};

const add_votes_to_county = (err, row) => {
  const { county_id, total_votes, ...votesData } = row;
  geoDataMatch = appData.features.find(
    (feature) => parseInt(feature.properties.RS) === county_id
  );
  if (geoDataMatch.data) {
    Object.keys(votesData).forEach((property) => {
      geoDataMatch.data[property] = convertToPercent(
        votesData[property] / total_votes,
        6
      );
    });
  } else {
    geoDataMatch.data = Object.fromEntries(
      Object.keys(votesData).map((property) => [
        property,
        convertToPercent(votesData[property] / total_votes, 6),
      ])
    );
  }
};

const write_data = () => {
  appData.features = appData.features.filter((feature) => feature.data);
  console.log("FINISHED BUILDING JS OBJECT, WRITING...");
  serializedData = JSON.stringify(appData);
  fs.writeFile("./frontend_data.json", serializedData, function (err) {
    if (err) return console.log(err);
  });
  console.log("FINISHED WRITING JSON!");
};

const add_meta = () => {
  appData.meta = [
    ...appData.meta,
    {
      name: "battery electric vehicle (BEV) share",
      key: "battery_electric",
      thresholds: [0.0625, 0.125, 0.25, 0.5, 1, 2, 4],
      colorScheme: "yellow",
      hasMultipleYears: true,
      dataTopic: "vehicles",
    },
  ];
  appData.meta = [
    ...appData.meta,
    {
      name: "plug-in hybrid share",
      key: "hybrid_plug_in",
      thresholds: [0.0625, 0.125, 0.25, 0.5, 1, 2, 4],
      colorScheme: "pink",
      hasMultipleYears: true,
      dataTopic: "vehicles",
    },
  ];
  appData.meta = [
    ...appData.meta,
    {
      name: "cdu/csu vote share",
      key: "cdu_csu",
      thresholds: [5, 10, 15, 20, 25, 30, 35, 40],
      colorScheme: "black",
      hasMultipleYears: false,
      dataTopic: "votes",
    },
  ];
  appData.meta = [
    ...appData.meta,
    {
      name: "spd vote share",
      key: "spd",
      thresholds: [5, 10, 15, 20, 25, 30, 35, 40],
      colorScheme: "red",
      hasMultipleYears: false,
      dataTopic: "votes",
    },
  ];
  appData.meta = [
    ...appData.meta,
    {
      name: "greens vote share",
      key: "greens",
      thresholds: [5, 10, 15, 20, 25, 30, 35, 40],
      colorScheme: "green",
      hasMultipleYears: false,
      dataTopic: "votes",
    },
  ];
  appData.meta = [
    ...appData.meta,
    {
      name: "fdp vote share",
      key: "fdp",
      thresholds: [5, 10, 15, 20, 25, 30, 35, 40],
      colorScheme: "yellow",
      hasMultipleYears: false,
      dataTopic: "votes",
    },
  ];
  appData.meta = [
    ...appData.meta,
    {
      name: "left vote share",
      key: "the_left",
      thresholds: [5, 10, 15, 20, 25, 30, 35, 40],
      colorScheme: "pink",
      hasMultipleYears: false,
      dataTopic: "votes",
    },
  ];
  appData.meta = [
    ...appData.meta,
    {
      name: "afd vote share",
      key: "afd",
      thresholds: [5, 10, 15, 20, 25, 30, 35, 40],
      colorScheme: "blue",
      hasMultipleYears: false,
      dataTopic: "votes",
    },
  ];
  appData.meta = [
    ...appData.meta,
    {
      name: "other parties vote share",
      key: "other_parties",
      thresholds: [5, 10, 15, 20, 25, 30, 35, 40],
      colorScheme: "grey",
      hasMultipleYears: false,
      dataTopic: "votes",
    },
  ];
};

const add_votes = () =>
  db.each(
    `SELECT county_id, total_votes, cdu_csu, spd, greens, fdp, the_left, afd, other_parties from votes`,
    add_votes_to_county,
    write_data
  );

const add_vehicle_stocks = () =>
  db.each(
    `SELECT county_id, year, petrol, diesel, gas, hybrid_total, hybrid_plug_in, battery_electric, other
  FROM vehicle_stock`,
    add_stocks_to_county,
    add_votes
  );

const incorporate_counties = () =>
  db.each(
    "SELECT name, type, statistical_id FROM counties",
    add_county_data,
    add_vehicle_stocks
  );

fs.readFile("../geo/germany_counties.json", (err, data) => {
  if (err) {
    throw err;
  }
  appData = JSON.parse(data);
  appData.meta = [];
  add_meta();
  incorporate_counties();
});
