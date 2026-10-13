const op = require('../src/operacoes');

describe('Erros: tipo e mensagem fazem parte do contrato existente', () => {
  test.each([
    ['divisao', [5, 0], 'Divisão por zero não é permitida.'],
    ['raizQuadrada', [-1], 'Não é possível calcular a raiz quadrada de um número negativo.'],
    ['fatorial', [-1], 'Fatorial não é definido para números negativos.'],
    ['maximoArray', [[]], 'Array vazio не possui valor máximo.'],
    ['minimoArray', [[]], 'Array vazio не possui valor mínimo.'],
    ['inverso', [0], 'Não é possível inverter o número zero.'],
    ['medianaArray', [[]], 'Array vazio не possui mediana.'],
  ])('%s rejeita %j com erro específico', (nome, args, mensagem) => {
    expect(() => op[nome](...args)).toThrow(new Error(mensagem));
  });
});

describe('Casos de fronteira e resultados exatos', () => {
  test.each([
    ['soma', [-3, 3], 0],
    ['subtracao', [-3, 2], -5],
    ['multiplicacao', [-3, 4], -12],
    ['divisao', [-9, 3], -3],
    ['potencia', [2, 0], 1],
    ['potencia', [2, -2], 0.25],
    ['raizQuadrada', [0], 0],
    ['restoDivisao', [-10, 3], -1],
    ['fatorial', [0], 1],
    ['fatorial', [1], 1],
    ['fatorial', [2], 2],
    ['fatorial', [5], 120],
    ['mediaArray', [[]], 0],
    ['mediaArray', [[-4, 0, 7]], 1],
    ['somaArray', [[]], 0],
    ['somaArray', [[-3, 0, 2]], -1],
    ['maximoArray', [[-9, -2, -4]], -2],
    ['minimoArray', [[-9, -2, -4]], -9],
    ['valorAbsoluto', [0], 0],
    ['valorAbsoluto', [3], 3],
    ['arredondar', [2.5], 3],
    ['arredondar', [-2.5], -2],
    ['isPar', [3], false],
    ['isPar', [0], true],
    ['isPar', [-2], true],
    ['isImpar', [2], false],
    ['isImpar', [0], false],
    ['isImpar', [-3], true],
    ['calcularPorcentagem', [0, 200], 0],
    ['inverterSinal', [-42], 42],
    ['inverterSinal', [0], -0],
    ['arredondarParaBaixo', [-2.1], -3],
    ['arredondarParaCima', [-2.9], -2],
    ['mdc', [12, 8], 4],
    ['mdc', [7, 0], 7],
    ['mdc', [0, 7], 7],
    ['mmc', [6, 8], 24],
    ['isPrimo', [-2], false],
    ['isPrimo', [0], false],
    ['isPrimo', [1], false],
    ['isPrimo', [2], true],
    ['isPrimo', [4], false],
    ['isPrimo', [9], false],
    ['fibonacci', [0], 0],
    ['fibonacci', [1], 1],
    ['fibonacci', [2], 1],
    ['fibonacci', [6], 8],
    ['produtoArray', [[]], 1],
    ['produtoArray', [[-2, 3]], -6],
    ['produtoArray', [[2, 0, 3]], 0],
    ['clamp', [-1, 0, 10], 0],
    ['clamp', [11, 0, 10], 10],
    ['clamp', [0, 0, 10], 0],
    ['clamp', [10, 0, 10], 10],
    // Object.is (usado por toBe) distingue os zeros IEEE 754.
    // Na igualdade dos limites, clamp retorna o próprio valor recebido.
    ['clamp', [-0, 0, 10], -0],
    ['clamp', [0, -10, -0], 0],
    ['isDivisivel', [10, 3], false],
    ['isDivisivel', [-10, 2], true],
    ['isDivisivel', [10, 0], false],
    ['celsiusParaFahrenheit', [100], 212],
    ['celsiusParaFahrenheit', [-40], -40],
    ['fahrenheitParaCelsius', [212], 100],
    ['fahrenheitParaCelsius', [-40], -40],
    ['inverso', [-4], -0.25],
    ['areaRetangulo', [0, 4], 0],
    ['perimetroRetangulo', [0, 4], 8],
    ['isMaiorQue', [5, 5], false],
    ['isMaiorQue', [3, 5], false],
    ['isMenorQue', [5, 5], false],
    ['isMenorQue', [5, 3], false],
    ['isEqual', [7, 8], false],
    ['isEqual', [7, '7'], false],
    ['medianaArray', [[30, 1, 20, 2]], 11],
    ['medianaArray', [[20, 3, 1]], 3],
    ['medianaArray', [[7]], 7],
    ['medianaArray', [[-5, 10]], 2.5],
    ['dobro', [-3], -6],
    ['triplo', [0], 0],
    ['metade', [3], 1.5],
  ])('%s(%j) = %s', (nome, args, esperado) => {
    expect(op[nome](...args)).toBe(esperado);
  });
});

describe('Resultados numéricos aproximados', () => {
  test.each([
    ['raizQuadrada', [2], Math.SQRT2],
    ['aumentarPorcentagem', [80, 25], 100],
    ['diminuirPorcentagem', [80, 25], 60],
    ['seno', [Math.PI / 2], 1],
    ['cosseno', [Math.PI], -1],
    ['tangente', [Math.PI / 4], 1],
    ['logaritmoNatural', [1], 0],
    ['logaritmoBase10', [1000], 3],
    ['hipotenusa', [5, 12], 13],
    ['grausParaRadianos', [90], Math.PI / 2],
    ['radianosParaGraus', [Math.PI / 2], 90],
    ['areaCirculo', [1], Math.PI],
  ])('%s(%j) aproxima %s', (nome, args, esperado) => {
    expect(op[nome](...args)).toBeCloseTo(esperado, 10);
  });
  test('mediana ordena uma cópia sem modificar a entrada', () => {
    const entrada = [30, 1, 20, 2];
    expect(op.medianaArray(entrada)).toBe(11);
    expect(entrada).toEqual([30, 1, 20, 2]);
  });
});
