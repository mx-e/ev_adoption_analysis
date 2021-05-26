import axios from 'axios'

export const requestData = (dispatch, errorDispatch) => {
  axios
    .get("./frontend_data.json")
    .then((result) => {
      dispatch(result.data);
    })
    .catch((error) => {
      errorDispatch(error);
    });
};

