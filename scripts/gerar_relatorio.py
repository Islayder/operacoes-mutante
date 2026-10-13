"""Gera quatro páginas a partir dos JSONs e das capturas reais preservadas."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
try:
    import reportlab
except ImportError:
    sys.path.insert(0, str(ROOT / '.tools/python'))
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

FONT, BOLD = 'Helvetica', 'Helvetica-Bold'
fonts = Path('C:/Windows/Fonts')
if (fonts / 'segoeui.ttf').exists():
    pdfmetrics.registerFont(TTFont('Segoe', str(fonts / 'segoeui.ttf')))
    pdfmetrics.registerFont(TTFont('Segoe-Bold', str(fonts / 'segoeuib.ttf')))
    pdfmetrics.registerFontFamily('Segoe', normal='Segoe', bold='Segoe-Bold', italic='Segoe', boldItalic='Segoe-Bold')
    FONT, BOLD = 'Segoe', 'Segoe-Bold'

summary = json.loads((ROOT / 'evidence/summary.json').read_text(encoding='utf-8'))
initial, final = summary['initial'], summary['final']
revision = subprocess.check_output(['git', 'log', '-1', '--format=%H', '--', 'test/operacoes.adicionais.test.js'], cwd=ROOT, text=True).strip()
OUTPUT = ROOT / 'docs/Relatorio_Teste_Mutacao.pdf'
OUTPUT.parent.mkdir(exist_ok=True)
W, H = A4
M, CW = 42, W - 84
NAVY, GREEN, GRAY = colors.HexColor('#19394A'), colors.HexColor('#167A6D'), colors.HexColor('#52636D')
c = canvas.Canvas(str(OUTPUT), pagesize=A4, pageCompression=1)
c.setTitle('Análise de Eficácia de Testes com Teste de Mutação')
c.setAuthor('Islayder Jackson Ribeiro de Oliveira')
c.setSubject('Testes de Software — matrícula 859552 — resultados reais de Jest e StrykerJS')

def pct(v):
    return f'{v:.2f}'.replace('.', ',') + '%'

def para(text, y, size=10, leading=14, color=NAVY, width=CW, x=M, bold=False):
    style = ParagraphStyle('body', fontName=BOLD if bold else FONT, fontSize=size, leading=leading, textColor=color)
    p = Paragraph(text, style)
    _, height = p.wrap(width, H)
    if y - height < 43:
        raise ValueError(f'Conteúdo excede a página: {text[:80]}')
    p.drawOn(c, x, y-height)
    return y-height

def heading(text, y):
    return para(text, y, size=13, leading=18, color=GREEN, bold=True)-8

def page(number, label):
    c.setFillColor(GREEN)
    c.rect(0, H-9, W, 9, fill=1, stroke=0)
    c.setFont(BOLD, 8)
    c.setFillColor(GRAY)
    c.drawString(M, H-30, 'TESTES DE SOFTWARE  /  TESTE DE MUTAÇÃO')
    c.setFont(FONT, 8)
    c.drawRightString(W-M, H-30, label)
    c.setStrokeColor(colors.HexColor('#D8E2E5'))
    c.line(M, 35, W-M, 35)
    c.setFont(FONT, 7.6)
    c.drawString(M, 22, 'Islayder Jackson Ribeiro de Oliveira  |  859552')
    c.drawRightString(W-M, 22, f'{number} / 4')

def table(data, y, widths, row_height=21):
    t = Table(data, colWidths=widths, rowHeights=row_height)
    t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), FONT), ('FONTSIZE', (0,0), (-1,-1), 9.2),
        ('FONTNAME', (0,0), (-1,0), BOLD), ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#EEF5F5'), colors.white]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 9),
        ('LINEBELOW', (0,-1), (-1,-1), 0.6, colors.HexColor('#CBDADD')),
    ]))
    _, height = t.wrap(CW, H)
    t.drawOn(c, M, y-height)
    return y-height-10

def screenshot(name, y, crop, width=450):
    """Recorta apenas a exibição no PDF; o JPG original permanece intacto."""
    reader = ImageReader(str(ROOT / 'evidence/screenshots' / name))
    iw, ih = reader.getSize()
    left, top, right, bottom = crop
    scale = width / (right-left)
    height = (bottom-top)*scale
    x = M + (CW-width)/2
    y -= height
    if y < 45:
        raise ValueError('Imagem excede a página')
    c.saveState()
    p = c.beginPath()
    p.rect(x, y, width, height)
    c.clipPath(p, stroke=0, fill=0)
    c.drawImage(reader, x-left*scale, y-(ih-bottom)*scale, width=iw*scale, height=ih*scale)
    c.restoreState()
    return y-7

# 1 — capa
page(1, 'Relatório acadêmico')
y = para('Análise de Eficácia<br/>de Testes com<br/>Teste de Mutação', 681, size=27, leading=35, bold=True)
c.setFillColor(GREEN)
c.rect(M, y-28, 90, 4, fill=1, stroke=0)
y = para('Disciplina: <b>Testes de Software</b>', y-62, size=13, leading=19)
y = para('<b>Islayder Jackson Ribeiro de Oliveira</b><br/>Matrícula: 859552', y-28, size=13, leading=21)
y = para('13 de outubro de 2026', y-24, size=11, leading=16, color=GRAY)
y = heading('Projeto e rastreabilidade', y-60)
y = para('Biblioteca JavaScript com 50 operações matemáticas.<br/>Fork: <link href="https://github.com/Islayder/operacoes-mutante" color="#167A6D">github.com/Islayder/operacoes-mutante</link><br/>Revisão dos testes: '+revision[:12], y, size=10.3, leading=16)
y = para('<b>Resultado verificado:</b> '+pct(initial['score'])+' para '+pct(final['score'])+'.<br/>149 testes aprovados; código original preservado.', y-24, size=11, leading=17)
para('<b>Limitação declarada:</b> a meta estrita superior a 98% permanece pendente. Cinco mutantes equivalentes no domínio matemático previsto foram mantidos no resultado oficial.', y-24, size=10, leading=15, color=GRAY)
c.showPage()

# 2 — análise inicial e primeiro mutante
page(2, 'Linha de base e asserções')
y = heading('1. Análise inicial e método', 785)
y = para('A biblioteca de 50 funções foi recuperada do commit '+summary['original'][:12]+'. Os 50 testes originais passaram antes das melhorias. A instrumentação contabiliza 53 funções porque inclui callbacks. A implementação e a suíte original foram preservadas.', y)
y = para('Ambiente: Node 24.19.0, npm 11.17.0, Jest 29.7.0 e StrykerJS/Jest runner 10.0.0, Windows x64. Foram usados os operadores padrão em todo src/operacoes.js, cobertura por teste e duas instâncias. Dependências fixadas no lockfile.', y-8)
data = [['Métrica', 'Inicial', 'Final'], ['Testes aprovados', '50 / 50', '149 / 149']]
for key, label in [('statements','Instruções'),('branches','Ramos'),('functions','Funções'),('lines','Linhas')]:
    data.append([label, pct(initial['coverage'][key]['pct']), pct(final['coverage'][key]['pct'])])
data.append(['Mutation Score oficial', pct(initial['score']), pct(final['score'])])
y = table(data, y-12, [CW-184,92,92], 21)
y = para('A cobertura de linhas de 98,64% coexistia com 56 mutantes não detectados. Executar uma linha não garante exercitar seus dois ramos nem distinguir um resultado correto de outro incorreto. A cobertura inicial de ramos, 58,82%, já indicava lacunas.', y-2)
y = heading('2. Mutante 11 — mensagem de erro em divisao', y-17)
y = para('<b>Arquivo:</b> src/operacoes.js:8. O StringLiteral substituiu a mensagem por uma string vazia. O teste original usava apenas <b>toThrow()</b>: qualquer exceção satisfazia a asserção. O novo teste exige <b>toThrow(new Error("Divisão por zero não é permitida."))</b>, verificando a mensagem existente.', y, size=9.8, leading=13.5)
y = screenshot('03-divisao-inicial.jpg', y-12, (16,375,776,805), width=435)
para('Figura 1. Captura real do HTML inicial: mensagem apagada e estado Survived. Na execução final, o ID 11 foi Killed.', y, size=8.4, leading=11, color=GRAY)
c.showPage()

# 3 — outros dois mutantes, com capturas reais
page(3, 'Fronteiras e diversidade de entradas')
y = heading('3. Mutante 183 — igualdade em isMaiorQue', 785)
y = para('<b>src/operacoes.js:104.</b> O EqualityOperator trocou <b>a &gt; b</b> por <b>a &gt;= b</b>. O único caso original, (10, 5), retorna true em ambas as versões. A fronteira de igualdade estava ausente. A asserção <b>expect(isMaiorQue(5, 5)).toBe(false)</b> distingue os comportamentos e matou o mutante.', y, size=10, leading=14)
y = screenshot('01-isMaiorQue-inicial.jpg', y-10, (16,375,776,805), width=435)
y = para('Figura 2. Alteração de &gt; para &gt;= no relatório inicial; ID 183: Survived → Killed.', y, size=8.4, leading=11, color=GRAY)
y = heading('4. Mutante 200 — ordenação em medianaArray', y-20)
y = para('<b>src/operacoes.js:109.</b> O MethodExpression removeu <b>.sort((a, b) =&gt; a - b)</b>, mantendo apenas a cópia do array. A entrada original [1, 2, 3, 4, 5] já estava ordenada. Os novos casos <b>[20, 3, 1] → 3</b> e <b>[30, 1, 20, 2] → 11</b> exigem ordenação numérica; o segundo também cobre a mediana de tamanho par.', y, size=10, leading=14)
y = screenshot('02-mediana-inicial.jpg', y-10, (16,360,776,805), width=420)
para('Figura 3. Ordenação removida no HTML original; ID 200: Survived → Killed. Os JPGs completos também acompanham a entrega.', y, size=8.4, leading=11, color=GRAY)
c.showPage()

# 4 — solução, resultados, equivalentes e conclusão
page(4, 'Resultados e limites da evidência')
y = heading('5. Soluções implementadas e validação', 785)
y = para('Foram adicionados 99 testes em test/operacoes.adicionais.test.js: zero, negativos, erros com mensagens, arrays vazios, primos e compostos, conversões não nulas, igualdade, mediana par/ímpar e entradas desordenadas. Resultados exatos usam toBe; aproximações usam toBeCloseTo com dez casas. A mediana também é verificada quanto à preservação da entrada.', y)
y = para('Os limites de clamp incluem os zeros IEEE 754: <b>clamp(-0, 0, 10)</b> preserva -0 e <b>clamp(0, -10, -0)</b> preserva +0. toBe distingue esses valores e detecta as trocas de &lt; e &gt; por comparações inclusivas.', y-7)
data = [['Estado dos 213 mutantes', 'Inicial', 'Final']]
for key,label in [('Killed','Mortos por falha de teste'),('Timeout','Timeouts (também detectados)'),('Survived','Sobreviventes'),('NoCoverage','Sem cobertura')]:
    data.append([label,str(initial['states'].get(key,0)),str(final['states'].get(key,0))])
data.append(['Ignorados / erros', '0 / 0', '0 / 0'])
y = table(data,y-12,[CW-184,92,92],20)
y = para('<b>Score = (Killed + Timeout) / total válido.</b> Inicial: 157/213 = 73,71%; final: 208/213 = 97,65%, melhora de <b>23,94 pontos percentuais</b>. Duas execuções de cada etapa reproduziram as mesmas contagens. As três mutações analisadas foram mortas; a cobertura final atingiu 100% nas quatro métricas.',y, size=9.8,leading=13.5)
y = heading('6. Cinco equivalentes e a meta não atingida', y-16)
y = para('<b>IDs 31, 32, 33 e 35 — fatorial, linha 19.</b> Desabilitar todo ou parte de <b>n === 0 || n === 1</b>, ou trocar || por &amp;&amp;, preserva o resultado. Para 0 e 1, o acumulador começa em 1 e o laço iniciado em 2 não executa; para outros números, o retorno antecipado já não ocorre.', y, size=9.6,leading=13)
y = para('<b>ID 140 — produtoArray, linha 84.</b> Retirar o retorno antecipado de array vazio leva a <b>[].reduce(..., 1)</b>, que também retorna 1. A equivalência vale para arrays numéricos comuns com reduce nativo; não se generaliza a métodos sobrescritos ou Proxies.', y-6, size=9.6,leading=13)
y = para('Mantidos esses cinco no universo original, o teto é <b>208/213 = 97,65%</b>; superar 98% exigiria 209 detecções. Nenhum mutante foi ignorado, nenhum operador excluído e nenhuma fonte alterada para elevar o score. A meta permanece pendente de decisão do professor sobre equivalentes ou revisão do projeto/meta.', y-6, size=9.6,leading=13)
y = heading('7. Conclusão', y-16)
y = para('Cobertura mede execução; mutação avalia a capacidade de detectar alterações. A melhoria demonstrou o valor de fronteiras, entradas variadas e asserções específicas. Os equivalentes também mostram que uma pontuação deve ser interpretada com o domínio e as evidências, sem transformar um alvo numérico em incentivo à manipulação.', y, size=9.6,leading=13)
y = para('<b>Reprodução:</b> npm ci; npm run validate:initial; npm run validate:final. JSONs, HTMLs, logs, capturas, hashes e análise detalhada: pasta evidence/ do fork. Commit dos testes: '+revision[:12]+'.', y-12,size=8.5,leading=11.5,color=GRAY)
para('<b>Referências:</b> enunciado do professor; <link href="https://stryker-mutator.io/docs/stryker-js/getting-started/" color="#167A6D">documentação oficial StrykerJS</link>; <link href="https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/" color="#167A6D">estados e métricas dos mutantes</link>.', y-7,size=8.2,leading=11,color=GRAY)
c.save()
print(OUTPUT)
