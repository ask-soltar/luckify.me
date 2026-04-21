import {
  CENTER_DISPLAY_NAMES,
  CENTER_ORDER,
  HUMAN_DESIGN_CENTERS,
  HUMAN_DESIGN_CHANNELS,
  MOTOR_CENTERS,
} from '../constants/humanDesign.js';

function uniqueSortedNumbers(values) {
  return [...new Set(values)].sort((a, b) => a - b);
}

export function getActiveGates(activeGatesOrActivations = []) {
  if (!Array.isArray(activeGatesOrActivations)) return [];

  const gates = activeGatesOrActivations
    .map(item => (typeof item === 'object' && item !== null ? item.gate : item))
    .map(value => Number(value))
    .filter(value => Number.isInteger(value) && value >= 1 && value <= 64);

  return uniqueSortedNumbers(gates);
}

export function getDefinedChannels(activeGatesOrActivations = []) {
  const activeGateSet = new Set(getActiveGates(activeGatesOrActivations));

  return HUMAN_DESIGN_CHANNELS.filter(channel =>
    channel.gates.every(gate => activeGateSet.has(gate))
  );
}

export function getDefinedCenters(definedChannels = []) {
  const definedSet = new Set();

  for (const channel of definedChannels) {
    for (const center of channel.centers) definedSet.add(center);
  }

  return CENTER_ORDER.filter(center => definedSet.has(center));
}

function buildCenterGraph(definedChannels = []) {
  const graph = new Map();

  for (const center of CENTER_ORDER) graph.set(center, new Set());

  for (const channel of definedChannels) {
    const [left, right] = channel.centers;
    graph.get(left).add(right);
    graph.get(right).add(left);
  }

  return graph;
}

function areCentersConnected(graph, start, target) {
  if (start === target) return true;

  const queue = [start];
  const seen = new Set(queue);

  while (queue.length) {
    const current = queue.shift();
    for (const next of graph.get(current) || []) {
      if (next === target) return true;
      if (!seen.has(next)) {
        seen.add(next);
        queue.push(next);
      }
    }
  }

  return false;
}

function isMotorConnectedToThroat(definedChannels = []) {
  const graph = buildCenterGraph(definedChannels);

  return MOTOR_CENTERS.some(center =>
    areCentersConnected(graph, HUMAN_DESIGN_CENTERS.THROAT, center)
  );
}

export function getHumanDesignType({ definedChannels = [], definedCenters = [] } = {}) {
  const definedCenterSet = new Set(definedCenters);

  if (definedCenterSet.size === 0) return 'Reflector';

  const sacralDefined = definedCenterSet.has(HUMAN_DESIGN_CENTERS.SACRAL);
  const throatConnectedToMotor = isMotorConnectedToThroat(definedChannels);

  if (sacralDefined) {
    return throatConnectedToMotor ? 'Manifesting Generator' : 'Generator';
  }

  if (throatConnectedToMotor) return 'Manifestor';

  return 'Projector';
}

export function getAuthority({ type, definedCenters = [], definedChannels = [] } = {}) {
  const definedCenterSet = new Set(definedCenters);

  if (type === 'Reflector') {
    return {
      key: 'lunar',
      label: 'Lunar Authority',
      family: 'Outer Authority',
    };
  }

  // Emotional definition always overrides every lower authority.
  if (definedCenterSet.has(HUMAN_DESIGN_CENTERS.SOLAR_PLEXUS)) {
    return {
      key: 'emotional',
      label: 'Emotional Authority',
      family: 'Inner Authority',
    };
  }

  if (definedCenterSet.has(HUMAN_DESIGN_CENTERS.SACRAL)) {
    return {
      key: 'sacral',
      label: 'Sacral Authority',
      family: 'Inner Authority',
    };
  }

  if (definedCenterSet.has(HUMAN_DESIGN_CENTERS.SPLEEN)) {
    return {
      key: 'splenic',
      label: 'Splenic Authority',
      family: 'Inner Authority',
    };
  }

  if (definedCenterSet.has(HUMAN_DESIGN_CENTERS.EGO)) {
    // The vocal authorities are the rare non-emotional/non-sacral/non-splenic designs
    // that rely on hearing the truth of what they say.
    if (type === 'Manifestor') {
      return {
        key: 'ego-manifested',
        label: 'Ego Manifested Authority',
        family: 'Ego Authority',
      };
    }

    if (type === 'Projector' && definedCenterSet.has(HUMAN_DESIGN_CENTERS.G)) {
      return {
        key: 'ego-projected',
        label: 'Ego Projected Authority',
        family: 'Ego Authority',
      };
    }
  }

  if (type === 'Projector' && definedCenterSet.has(HUMAN_DESIGN_CENTERS.G)) {
    return {
      key: 'self-projected',
      label: 'Self-Projected Authority',
      family: 'Outer Authority',
    };
  }

  if (type === 'Projector') {
    return {
      key: 'mental-environmental',
      label: 'Mental / Environmental Authority',
      family: 'Outer Authority',
    };
  }

  return {
    key: 'none',
    label: 'No Authority',
    family: 'Unknown',
  };
}

export function deriveHumanDesign(activeGatesOrActivations = [], chartType = null) {
  const activeGates = getActiveGates(activeGatesOrActivations);
  const definedChannels = getDefinedChannels(activeGates);
  const definedCenters = getDefinedCenters(definedChannels);
  const type = chartType || getHumanDesignType({ definedChannels, definedCenters });
  const authority = getAuthority({ type, definedCenters, definedChannels });

  return {
    activeGates,
    definedChannels,
    definedCenters,
    definedCenterLabels: definedCenters.map(center => CENTER_DISPLAY_NAMES[center] || center),
    type,
    authority: authority.label,
    authorityKey: authority.key,
    authorityFamily: authority.family,
  };
}
