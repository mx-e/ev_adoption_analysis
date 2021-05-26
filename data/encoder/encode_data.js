const sqlite3 = require("sqlite3").verbose();
const fs = require("fs");

const db = new sqlite3.Database("../ev_adoption.sqlite");

let appData = {};

const add_county_data = (err, { name, statistical_id }) => {
  geoDataMatch = appData.features.find(
    (feature) => parseInt(feature.properties.RS) === statistical_id
  );
};

const add_stocks_to_county = (err, row) => {
  const { year, county_id, ...vehicleData } = row;
  geoDataMatch = appData.features.find(
    (feature) => parseInt(feature.properties.RS) === county_id
  );
  if (geoDataMatch.data) {
    Object.keys(vehicleData).forEach((property) => {
      geoDataMatch.data[property][year] = vehicleData[property];
    });
  } else {
    geoDataMatch.data = Object.fromEntries(
      Object.keys(vehicleData).map((property) => [
        property,
        Object.fromEntries([[year, vehicleData[property]]]),
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

const add_vehicle_stocks = () =>
  db.each(
    `SELECT county_id, year, petrol, diesel, gas, hybrid_total, hybrid_plug_in, battery_electric, other
  FROM vehicle_stock`,
    add_stocks_to_county,
    write_data
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
  incorporate_counties();
});
