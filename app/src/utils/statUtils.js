export const mean = (arr) => {
  if (arr.length) {
    const sum = arr.reduce((st, cur) => st + cur);
    return sum / arr.length;
  }
  return null;
};

export const variance = (arr) => {
  if (arr.length) {
    const mu = mean(arr);
    const sum = arr.reduce((st, cur) => st + Math.pow(cur - mu, 2));
    return sum / arr.length;
  }
  return null;
};

export const std = (arr) => {
  if (arr.length) {
    return Math.pow(variance(arr), 0.5);
  }
  return null;
};

export const cov = (arrX, arrY) => {
  if (arrX.length && arrY.length && arrX.length === arrY.length) {
    const xMean = mean(arrX);
    const yMean = mean(arrY);
    const sum = arrX.reduce((st, curX, i) => {
      const curY = arrY[i];
      return st + (curX - xMean) * (curY - yMean);
    });
    return sum / arrX.length;
  }
  return null;
};

export const correlation = (arrX, arrY) => {
  if (arrX.length && arrY.length && arrX.length === arrY.length) {
    const covariance = cov(arrX, arrY);
    console.log(covariance);
    const stdX = std(arrX);
    const stdY = std(arrY);
    return covariance / (stdX * stdY);
  }
  return null;
};

export const round = (number, decimal = 2) =>
  Math.round(number * Math.pow(10, decimal)) / Math.pow(10, decimal);
