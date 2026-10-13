const fs = require('node:fs');
const crypto = require('node:crypto');
const { execFileSync } = require('node:child_process');
const original = 'c10621a4fe20f8332e783e06cad0e1b98449aad2';
const hash = value => crypto.createHash('sha256').update(value).digest('hex');
// Git autocrlf converte LF para CRLF no checkout Windows; compare o conteúdo lógico.
const canonical = value => value.toString('utf8').replace(/\r\n/g, '\n');
const sourceUnchanged = ['src/operacoes.js', 'test/operacoes.test.js'].every(file =>
  hash(canonical(execFileSync('git', ['show', `${original}:${file}`]))) === hash(canonical(fs.readFileSync(file))));
if (!sourceUnchanged) throw new Error('Fonte ou testes originais foram alterados.');
function metrics(stage) {
  const report = JSON.parse(fs.readFileSync(`evidence/${stage}/mutation/mutation.json`));
  const mutants = Object.values(report.files).flatMap(file => file.mutants);
  const states = {};
  for (const mutant of mutants) states[mutant.status] = (states[mutant.status] || 0) + 1;
  const valid = mutants.filter(m => !['CompileError', 'RuntimeError', 'Ignored'].includes(m.status)).length;
  const score = 100 * ((states.Killed || 0) + (states.Timeout || 0)) / valid;
  const jest = JSON.parse(fs.readFileSync(`evidence/${stage}/jest.json`));
  const coverage = JSON.parse(fs.readFileSync(`evidence/${stage}/coverage/coverage-summary.json`)).total;
  return { tests: jest.numTotalTests, passed: jest.numPassedTests, failed: jest.numFailedTests,
    states, total: mutants.length, score, coverage, mutants };
}
const initial = metrics('initial'), final = metrics('final');
if (initial.total !== final.total) throw new Error('Universos de mutantes divergentes.');
const signature = m => JSON.stringify([m.id, m.location, m.replacement, m.mutatorName]);
if (initial.mutants.map(signature).sort().join('\n') !== final.mutants.map(signature).sort().join('\n')) {
  throw new Error('Os mutantes iniciais e finais não são os mesmos.');
}
const critical = ['11', '183', '200'].map(id => ({ id,
  initial: initial.mutants.find(m => m.id === id).status,
  final: final.mutants.find(m => m.id === id).status }));
if (critical.some(m => m.initial !== 'Survived' || m.final !== 'Killed')) throw new Error('Evidência crítica inconsistente.');
for (const run of [initial, final]) delete run.mutants;
const summary = { original, sourceUnchanged, sourceSha256LF: hash(canonical(fs.readFileSync('src/operacoes.js'))),
  initial, final, critical, targetAbove98Met: final.score > 98,
  equivalentSurvivors: ['31', '32', '33', '35', '140'],
  environment: { node: process.version, platform: process.platform, arch: process.arch,
    jest: require('jest/package.json').version,
    stryker: JSON.parse(fs.readFileSync('node_modules/@stryker-mutator/core/package.json')).version } };
fs.writeFileSync('evidence/summary.json', JSON.stringify(summary, null, 2) + '\n');
console.log(JSON.stringify(summary, null, 2));
