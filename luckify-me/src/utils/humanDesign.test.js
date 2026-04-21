import test from 'node:test';
import assert from 'node:assert/strict';

import { deriveHumanDesign } from './humanDesign.js';

function activationSet(gates) {
  return gates.map(gate => ({ gate }));
}

test('Reflector resolves to Lunar Authority with no defined channels', () => {
  const result = deriveHumanDesign(activationSet([1, 2]));

  assert.equal(result.type, 'Reflector');
  assert.equal(result.authority, 'Lunar Authority');
  assert.deepEqual(result.definedCenters, []);
  assert.deepEqual(result.definedChannels, []);
});

test('Solar Plexus definition overrides lower authorities', () => {
  const result = deriveHumanDesign(activationSet([59, 6, 57, 20, 34]));

  assert.equal(result.authority, 'Emotional Authority');
  assert.equal(result.type, 'Manifesting Generator');
  assert.deepEqual(
    result.definedChannels.map(channel => channel.key).sort(),
    ['20-34', '20-57', '34-57', '59-6']
  );
});

test('Sacral definition resolves to Sacral Authority when Solar Plexus is undefined', () => {
  const result = deriveHumanDesign(activationSet([34, 20]));

  assert.equal(result.type, 'Manifesting Generator');
  assert.equal(result.authority, 'Sacral Authority');
});

test('Splenic projector resolves to Splenic Authority', () => {
  const result = deriveHumanDesign(activationSet([16, 48]));

  assert.equal(result.type, 'Projector');
  assert.equal(result.authority, 'Splenic Authority');
});

test('Ego manifestor resolves to Ego Manifested Authority', () => {
  const result = deriveHumanDesign(activationSet([21, 45]));

  assert.equal(result.type, 'Manifestor');
  assert.equal(result.authority, 'Ego Manifested Authority');
});

test('Self-projected projector resolves to Self-Projected Authority', () => {
  const result = deriveHumanDesign(activationSet([31, 7]));

  assert.equal(result.type, 'Projector');
  assert.equal(result.authority, 'Self-Projected Authority');
});

test('Mental projector resolves to Mental / Environmental Authority', () => {
  const result = deriveHumanDesign(activationSet([17, 62]));

  assert.equal(result.type, 'Projector');
  assert.equal(result.authority, 'Mental / Environmental Authority');
});
