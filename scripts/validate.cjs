// Executa as ferramentas reais; os relatórios históricos de evidence/ são imutáveis.
const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const stage = process.argv[2];
if (!['initial', 'final'].includes(stage)) throw new Error('Use initial ou final.');
const root = path.resolve(__dirname, '..');
process.chdir(root);
const output = path.join(root, 'reports', 'reproduced', stage);
fs.mkdirSync(output, { recursive: true });
function run(bin, args, log) {
  const result = spawnSync(process.execPath, [bin, ...args], {
    cwd: root, encoding: 'utf8', timeout: 600000, maxBuffer: 20 * 1024 * 1024,
    env: { ...process.env, FORCE_COLOR: '0' },
  });
  const text = (result.stdout || '') + (result.stderr || '');
  fs.writeFileSync(path.join(output, log), text);
  process.stdout.write(text);
  if (result.error || result.status !== 0) throw result.error || new Error(`Execução falhou: ${result.status}`);
}
run('node_modules/jest/bin/jest.js', [
  '--runInBand', '--coverage', '--coverageReporters=text',
  '--coverageReporters=json-summary', '--coverageReporters=html',
  `--coverageDirectory=${path.join(output, 'coverage')}`,
  '--json', `--outputFile=${path.join(output, 'jest.json')}`,
  ...(stage === 'initial' ? ['--testMatch=**/test/operacoes.test.js'] : []),
], 'jest.log');
const config = JSON.parse(fs.readFileSync('stryker.config.json'));
config.$schema = path.join(root, 'node_modules/@stryker-mutator/core/schema/stryker-schema.json');
config.htmlReporter.fileName = path.join(output, 'mutation/mutation.html');
config.jsonReporter.fileName = path.join(output, 'mutation/mutation.json');
if (stage === 'initial') {
  config.jest.config = { ...JSON.parse(fs.readFileSync('package.json')).jest,
    testMatch: ['**/test/operacoes.test.js'] };
}
const configFile = path.join(output, 'stryker.config.json');
fs.writeFileSync(configFile, JSON.stringify(config, null, 2));
run('node_modules/@stryker-mutator/core/bin/stryker.js', ['run', configFile], 'stryker.log');
console.log(`Relatórios reproduzidos: ${output}`);
