import test from 'node:test';
import assert from 'node:assert/strict';

import {
  deriveHumanDesign,
  getAuthority,
  getDefinedCenters,
  getDefinedChannels,
  getHumanDesignType,
} from '../src/utils/humanDesign.js';
import { calcAllActivations } from '../src/utils/geneKeys.js';

test('Reflector charts with no definition use Lunar Authority', () => {
  const result = deriveHumanDesign([]);

  assert.equal(result.type, 'Reflector');
  assert.deepEqual(result.definedCenters, []);
  assert.equal(result.authority, 'Lunar Authority');
});

test('Solar Plexus definition overrides Sacral and produces Emotional Authority', () => {
  const result = deriveHumanDesign([59, 6]);

  assert.equal(result.type, 'Generator');
  assert.ok(result.definedCenters.includes('Sacral'));
  assert.ok(result.definedCenters.includes('Solar Plexus'));
  assert.equal(result.authority, 'Emotional Authority');
});

test('Sacral-defined non-emotional generators use Sacral Authority', () => {
  const result = deriveHumanDesign([5, 15]);

  assert.equal(result.type, 'Generator');
  assert.ok(result.definedCenters.includes('Sacral'));
  assert.ok(!result.definedCenters.includes('Solar Plexus'));
  assert.equal(result.authority, 'Sacral Authority');
});

test('Projectors with Spleen definition and no higher authority use Splenic Authority', () => {
  const result = deriveHumanDesign([57, 10]);

  assert.equal(result.type, 'Projector');
  assert.ok(result.definedCenters.includes('Spleen'));
  assert.ok(!result.definedCenters.includes('Sacral'));
  assert.ok(!result.definedCenters.includes('Solar Plexus'));
  assert.equal(result.authority, 'Splenic Authority');
});

test('Valid Ego manifestor charts use Ego Manifested Authority', () => {
  const result = deriveHumanDesign([21, 45]);

  assert.equal(result.type, 'Manifestor');
  assert.ok(result.definedCenters.includes('Ego'));
  assert.equal(result.authority, 'Ego Manifested Authority');
  assert.equal(result.authorityFamily, 'Ego Authority');
});

test('Valid self-projected projectors use Self-Projected Authority', () => {
  const result = deriveHumanDesign([1, 8]);

  assert.equal(result.type, 'Projector');
  assert.ok(result.definedCenters.includes('G'));
  assert.equal(result.authority, 'Self-Projected Authority');
});

test('Projectors with no inner authority use Mental / Environmental Authority', () => {
  const result = deriveHumanDesign([43, 23]);

  assert.equal(result.type, 'Projector');
  assert.equal(result.authority, 'Mental / Environmental Authority');
});

test('Emotional definition still wins when Solar Plexus, Sacral, and Spleen are all defined', () => {
  const result = deriveHumanDesign([59, 6, 57, 10]);

  assert.ok(result.definedCenters.includes('Solar Plexus'));
  assert.ok(result.definedCenters.includes('Sacral'));
  assert.ok(result.definedCenters.includes('Spleen'));
  assert.equal(result.authority, 'Emotional Authority');
});

test('Defined channels can be derived from existing activation objects', () => {
  const activations = [
    { chart: 'conscious', planet: 'Sun', gate: 39, line: 1 },
    { chart: 'design', planet: 'Earth', gate: 55, line: 6 },
    { chart: 'conscious', planet: 'Moon', gate: 39, line: 2 },
  ];

  const channels = getDefinedChannels(activations);
  const centers = getDefinedCenters(channels);
  const type = getHumanDesignType({ definedChannels: channels, definedCenters: centers });
  const authority = getAuthority({ type, definedChannels: channels, definedCenters: centers });

  assert.deepEqual(channels.map(channel => channel.key), ['39-55']);
  assert.deepEqual(centers, ['Solar Plexus', 'Root']);
  assert.equal(type, 'Projector');
  assert.equal(authority.label, 'Emotional Authority');
});

test('Activation calculation includes both lunar nodes for Human Design definition', () => {
  const activations = calcAllActivations({
    year: 1990,
    month: 6,
    day: 15,
    birthTime: '12:00',
    tzOffset: 0,
  });

  const planets = activations.map(item => `${item.chart}:${item.planet}`);

  assert.equal(activations.length, 26);
  assert.ok(planets.includes('conscious:N.Node'));
  assert.ok(planets.includes('conscious:S.Node'));
  assert.ok(planets.includes('design:N.Node'));
  assert.ok(planets.includes('design:S.Node'));
});
