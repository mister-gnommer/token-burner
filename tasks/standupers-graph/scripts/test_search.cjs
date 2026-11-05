const assert = require('node:assert/strict');
const {readFileSync} = require('node:fs');
const {join} = require('node:path');
const {runInNewContext} = require('node:vm');
const {test} = require('node:test');

const template = readFileSync(join(__dirname, 'interactive_template.html'), 'utf8');
const normalize = template.match(/const normalize = .*;/)[0];
const matching = template.slice(template.indexOf('const surname ='), template.indexOf('function closeSearch()'));
const names = ['Anna Żak', 'Zenon Bąk', 'Adam Bąk', 'Lorem (Ipsum Ćma)', 'Łukasz Ipsum'];
function search(query) {
  return Array.from(runInNewContext(`${normalize}
    DATA.nodes.forEach(n => n.search = normalize(n.name));
    ${matching}
    searchMatches().map(n => n.name);`, {
    DATA: {nodes: names.map(name => ({name}))},
    d3: {select: () => ({property: () => query})},
  }));
}

test('results sort by Polish surname, with first names breaking ties and parentheses ignored', () => {
  assert.deepEqual(search(''), ['Adam Bąk', 'Zenon Bąk', 'Lorem (Ipsum Ćma)', 'Łukasz Ipsum', 'Anna Żak']);
});
test('partial names match without accents, including ł, and absent names return no results', () => {
  assert.deepEqual(search('  BAK '), ['Adam Bąk', 'Zenon Bąk']);
  assert.deepEqual(search('luk'), ['Łukasz Ipsum']);
  assert.deepEqual(search('cma'), ['Lorem (Ipsum Ćma)']);
  assert.deepEqual(search('missing'), []);
});
