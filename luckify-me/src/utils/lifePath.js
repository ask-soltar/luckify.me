/**
 * Life Path numerology calculations
 * Pythagorean method with master number preservation (11, 22, 33)
 */

/**
 * Reduce a number to single digit, preserving master numbers 11, 22, 33
 * @param {number} n
 * @returns {number} 1-9, 11, 22, or 33
 */
function reduceToSingleOrMaster(n) {
  while (n > 9 && n !== 11 && n !== 22 && n !== 33) {
    let sum = 0;
    while (n > 0) {
      sum += n % 10;
      n = Math.floor(n / 10);
    }
    n = sum;
  }
  return n;
}

/**
 * Calculate Life Path number
 * Pythagorean method: reduce month, day, year separately, then sum and reduce
 * @param {number} mo - Month (1-12)
 * @param {number} dy - Day (1-31)
 * @param {number} y - Year (e.g., 1989)
 * @returns {number} Life Path: 1-9, 11, 22, or 33
 */
export function calcLifePath(mo, dy, y) {
  // Month
  let mReduced = mo; // 1-12
  if (mo === 11) {
    mReduced = 11; // master
  } else if (mo === 12) {
    mReduced = 3; // 1+2
  } else {
    mReduced = mo; // 1-10, already fine (10 → 1+0 = 1)
  }
  if (mReduced === 10) mReduced = 1;

  // Day
  let dReduced = reduceToSingleOrMaster(dy);

  // Year
  let ySum = 0;
  let yTemp = y;
  while (yTemp > 0) {
    ySum += yTemp % 10;
    yTemp = Math.floor(yTemp / 10);
  }
  let yReduced = reduceToSingleOrMaster(ySum);

  // Final sum
  let total = mReduced + dReduced + yReduced;
  let lifePathNum = reduceToSingleOrMaster(total);

  return lifePathNum;
}

export { reduceToSingleOrMaster };
