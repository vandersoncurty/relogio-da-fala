/**
 * Relógio da Fala — Interface Web Interativa
 * 
 * Desenha um relógio com 16 símbolos e dois ponteiros arrastáveis.
 * Utiliza Web Speech API para síntese de voz.
 */

// ============================================================
// CONFIGURAÇÕES
// ============================================================

const CONFIG = {
    raio: 220,
    raioSimbolo: 185,
    raioPonteiro1: 140,
    raioPonteiro2: 200,
    centroX: 300,
    centroY: 300,
    raioClique: 30,
    cores: {
        sujeito: '#3b82f6',
        verbo: '#22c55e',
        objeto: '#f97316',
        emoCAO: '#a855f7',
        fundo: '#1e293b',
        texto: '#f8fafc',
        ponteiro1: '#3b82f6',
        ponteiro2: '#ef4444'
    }
};

// ============================================================
// DADOS DA PLACA
// ============================================================

const SIMBOLOS = {
    1: { simbolo: 'EU', categoria: 'SUJEITO', x: 0, y: 0 },
    2: { simbolo: 'VOCÊ', categoria: 'SUJEITO', x: 0, y: 0 },
    3: { simbolo: 'SIM', categoria: 'CONFIRMACAO', x: 0, y: 0 },
    4: { simbolo: 'NÃO', categoria: 'CONFIRMACAO', x: 0, y: 0 },
    5: { simbolo: 'QUERO', categoria: 'VERBO', x: 0, y: 0 },
    6: { simbolo: 'PRECISO', categoria: 'VERBO', x: 0, y: 0 },
    7: { simbolo: 'COMER', categoria: 'VERBO', x: 0, y: 0 },
    8: { simbolo: 'BEBER', categoria: 'VERBO', x: 0, y: 0 },
    9: { simbolo: 'ÁGUA', categoria: 'OBJETO', x: 0, y: 0 },
    10: { simbolo: 'COMIDA', categoria: 'OBJETO', x: 0, y: 0 },
    11: { simbolo: 'BANHEIRO', categoria: 'OBJETO', x: 0, y: 0 },
    12: { simbolo: 'SAIR', categoria: 'OBJETO', x: 0, y: 0 },
    13: { simbolo: 'FELIZ', categoria: 'EMOCAO', x: 0, y: 0 },
    14: { simbolo: 'TRISTE', categoria: 'EMOCAO', x: 0, y: 0 },
    15: { simbolo: 'DOR', categoria: 'EMOCAO', x: 0, y: 0 },
    16: { simbolo: 'AJUDA', categoria: 'EMOCAO', x: 0, y: 0 }
};

const COMBINACOES = {
    'EU+QUERO': 'Eu quero',
    'EU+PRECISO': 'Eu preciso',
    'EU+COMER': 'Eu quero comer',
    'EU+BEBER': 'Eu quero beber',
    'VOCÊ+QUERO': 'Você quer',
    'VOCÊ+PRECISO': 'Você precisa',
    'EU+ÁGUA': 'Eu quero água',
    'EU+COMIDA': 'Eu quero comida',
    'EU+BANHEIRO': 'Eu preciso de banheiro',
    'EU+SAIR': 'Eu quero sair',
    'EU+FELIZ': 'Eu estou feliz',
    'EU+TRISTE': 'Eu estou triste',
    'EU+DOR': 'Eu estou com dor',
    'EU+AJUDA': 'Eu preciso de ajuda',
    'QUERO+ÁGUA': 'Quero água',
    'QUERO+COMIDA': 'Quero comida',
    'QUERO+BANHEIRO': 'Preciso ir ao banheiro',
    'QUERO+SAIR': 'Quero sair',
    'PRECISO+ÁGUA': 'Preciso de água',
    'PRECISO+COMIDA': 'Preciso de comida',
    'PRECISO+BANHEIRO': 'Preciso ir ao banheiro',
    'PRECISO+SAIR': 'Preciso sair',
    'COMER+ÁGUA': 'Comer e beber água',
    'COMER+COMIDA': 'Comer comida',
    'BEBER+ÁGUA': 'Beber água',
    'BEBER+COMIDA': 'Beber e comer',
    'TRISTE+COMER': 'Estou triste comendo',
    'TRISTE+BEBER': 'Estou triste bebendo',
    'TRISTE+ÁGUA': 'Não quero água',
    'TRISTE+COMIDA': 'Não quero comida',
    'TRISTE+BANHEIRO': 'Não quero ir ao banheiro',
    'TRISTE+SAIR': 'Não quero sair',
    'DOR+COMER': 'Estou com dor ao comer',
    'DOR+BEBER': 'Estou com dor ao beber',
    'DOR+ÁGUA': 'Estou com dor, preciso de água',
    'DOR+COMIDA': 'Estou com dor ao comer',
    'DOR+BANHEIRO': 'Estou com dor, preciso ir ao banheiro',
    'DOR+SAIR': 'Estou com dor, preciso sair',
    'FELIZ+COMER': 'Estou feliz comendo',
    'FELIZ+BEBER': 'Estou feliz bebendo',
    'FELIZ+ÁGUA': 'Estou feliz bebendo água',
    'FELIZ+COMIDA': 'Estou feliz comendo',
    'FELIZ+BANHEIRO': 'Estou feliz indo ao banheiro',
    'FELIZ+SAIR': 'Estou feliz saindo',
    'AJUDA+BANHEIRO': 'Preciso de ajuda para ir ao banheiro',
    'AJUDA+ÁGUA': 'Preciso de ajuda para pegar água',
    'AJUDA+COMIDA': 'Preciso de ajuda para comer',
    'AJUDA+SAIR': 'Preciso de ajuda para sair',
    'AJUDA+DOR': 'Preciso de ajuda, estou com dor',
    'AJUDA+TRISTE': 'Preciso de ajuda, estou triste',
    'DOR+AJUDA': 'Estou com dor, preciso de ajuda',
    'TRISTE+AJUDA': 'Estou triste, preciso de ajuda',
    'SIM+QUERO': 'Sim, eu quero',
    'SIM+PRECISO': 'Sim, eu preciso',
    'SIM+COMER': 'Sim, quero comer',
    'SIM+BEBER': 'Sim, quero beber',
    'NÃO+QUERO': 'Não, eu não quero',
    'NÃO+PRECISO': 'Não, eu não preciso',
    'NÃO+COMER': 'Não, não quero comer',
    'NÃO+BEBER': 'Não, não quero beber',
    'SIM+ÁGUA': 'Sim, quero água',
    'SIM+COMIDA': 'Sim, quero comida',
    'SIM+BANHEIRO': 'Sim, preciso ir ao banheiro',
    'SIM+SAIR': 'Sim, quero sair',
    'NÃO+ÁGUA': 'Não, não quero água',
    'NÃO+COMIDA': 'Não, não quero comida',
    'NÃO+BANHEIRO': 'Não, não preciso ir ao banheiro',
    'NÃO+SAIR': 'Não, não quero sair',
    'NÃO+FELIZ': 'Não estou feliz',
    'NÃO+TRISTE': 'Não estou triste',
    'NÃO+DOR': 'Não estou com dor',
    'NÃO+AJUDA': 'Não preciso de ajuda',
    'SIM+FELIZ': 'Sim, estou feliz',
    'SIM+TRISTE': 'Sim, estou triste',
    'SIM+DOR': 'Sim, estou com dor',
    'SIM+AJUDA': 'Sim, preciso de ajuda',
    'SIM+SIM': 'Sim',
    'NÃO+NÃO': 'Não',
    'VOCÊ+ÁGUA': 'Você quer água?',
    'VOCÊ+COMIDA': 'Você quer comida?',
    'VOCÊ+BANHEIRO': 'Você precisa ir ao banheiro?',
    'VOCÊ+SAIR': 'Você quer sair?',
    'VOCÊ+COMER': 'Você quer comer?',
    'VOCÊ+BEBER': 'Você quer beber?',
    'VOCÊ+FELIZ': 'Você está feliz?',
    'VOCÊ+TRISTE': 'Você está triste?',
    'VOCÊ+DOR': 'Você está com dor?',
    'VOCÊ+AJUDA': 'Você precisa de ajuda?',
    'FELIZ+TRISTE': 'Estou feliz e triste',
    'FELIZ+DOR': 'Estou feliz, mas com dor',
    'FELIZ+AJUDA': 'Estou feliz, preciso de ajuda',
    'TRISTE+DOR': 'Estou triste e com dor',
    'TRISTE+FELIZ': 'Estou triste e feliz',
    'DOR+TRISTE': 'Estou com dor e triste',
    'DOR+FELIZ': 'Estou com dor, mas feliz',
    'DOR+DOR': 'Estou com muita dor',
    'AJUDA+FELIZ': 'Preciso de ajuda, estou feliz',
    'AJUDA+TRISTE': 'Preciso de ajuda, estou triste',
    'AJUDA+DOR': 'Preciso de ajuda, estou com dor',
    'AJUDA+AJUDA': 'Preciso muito de ajuda',
    'AJUDA+QUERO': 'Preciso de ajuda, eu quero',
    'AJUDA+PRECISO': 'Preciso muito de ajuda',
    'AJUDA+COMER': 'Preciso de ajuda para comer',
    'AJUDA+BEBER': 'Preciso de ajuda para beber'
};

// ============================================================
// ESTADO GLOBAL
// ============================================================

let canvas, ctx;
let ponteiro1 = 1;
let ponteiro2 = 5;
let arrastando = null;
let anguloPonteiro1 = 0;
let anguloPonteiro2 = 0;
let mensagem = '';
let valida = false;
let modoPictograma = false;
let pictogramas = {};
let imagensPictogramas = {};

// ============================================================
// INICIALIZAÇÃO
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
    canvas = document.getElementById('clockCanvas');
    ctx = canvas.getContext('2d');
    
    // Configurar canvas responsivo
    configurarCanvas();
    
    // Calcular posições dos símbolos
    calcularPosicoes();
    
    // Pré-carregar vozes (importante para alguns navegadores)
    if ('speechSynthesis' in window) {
        // Carregar vozes imediatamente
        speechSynthesis.getVoices();
        
        // Alguns navegadores precisam deste evento
        speechSynthesis.onvoiceschanged = () => {
            console.log('Vozes carregadas:', speechSynthesis.getVoices().length);
        };
    }
    
    // Event listeners
    canvas.addEventListener('mousedown', onMouseDown);
    canvas.addEventListener('mousemove', onMouseMove);
    canvas.addEventListener('mouseup', onMouseUp);
    canvas.addEventListener('mouseleave', onMouseUp);
    
    // Touch events
    canvas.addEventListener('touchstart', onTouchStart, { passive: false });
    canvas.addEventListener('touchmove', onTouchMove, { passive: false });
    canvas.addEventListener('touchend', onTouchEnd);
    
    // Teclado
    document.addEventListener('keydown', onKeyDown);
    
    // Botão de voz
    document.getElementById('voiceBtn').addEventListener('click', falar);
    
    // Botão de toggle pictograma
    document.getElementById('togglePictograma').addEventListener('click', alternarModoPictograma);
    
    // Carregar frases rápidas
    carregarFrasesRapidas();
    
    // Carregar pictogramas
    carregarPictogramas();
    
    // Redimensionar com janela
    window.addEventListener('resize', () => {
        configurarCanvas();
        calcularPosicoes();
        desenhar();
    });
    
    // Desenhar
    desenhar();
});

function configurarCanvas() {
    const container = canvas.parentElement;
    const estilo = getComputedStyle(container);
    const paddingLeft = parseFloat(estilo.paddingLeft);
    const paddingRight = parseFloat(estilo.paddingRight);
    const contentWidth = container.clientWidth - paddingLeft - paddingRight;
    const tamanho = Math.min(contentWidth, 700);

    canvas.style.width = tamanho + 'px';
    canvas.style.height = tamanho + 'px';

    const dpr = window.devicePixelRatio || 1;
    canvas.width = tamanho * dpr;
    canvas.height = tamanho * dpr;
    ctx.scale(dpr, dpr);

    const metade = tamanho / 2;

    CONFIG.centroX = metade;
    CONFIG.centroY = metade;
    CONFIG.raio = metade * 0.82;
    CONFIG.raioSimbolo = metade * 0.70;
    CONFIG.raioPonteiro1 = metade * 0.55;
    CONFIG.raioPonteiro2 = metade * 0.78;
    CONFIG.raioClique = metade * 0.11;
}

// ============================================================
// CÁLCULO DE POSIÇÕES
// ============================================================

function calcularPosicoes() {
    for (let i = 1; i <= 16; i++) {
        const angulo = ((i - 1) * (360 / 16) - 90) * Math.PI / 180;
        SIMBOLOS[i].x = CONFIG.centroX + CONFIG.raioSimbolo * Math.cos(angulo);
        SIMBOLOS[i].y = CONFIG.centroY + CONFIG.raioSimbolo * Math.sin(angulo);
    }
}

function posicaoParaAngulo(pos) {
    return ((pos - 1) * (360 / 16) - 90) * Math.PI / 180;
}

function anguloParaPosicao(angulo) {
    let graus = (angulo * 180 / Math.PI + 90 + 360) % 360;
    let pos = Math.round(graus / (360 / 16)) % 16;
    if (pos === 0) pos = 16;
    return pos;
}

// ============================================================
// DESENHO
// ============================================================

function desenhar() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    desenharFundo();
    desenharQuadrantes();
    desenharSimbolos();
    desenharPonteiro(anguloPonteiro1, CONFIG.raioPonteiro1, CONFIG.cores.ponteiro1, 'P1');
    desenharPonteiro(anguloPonteiro2, CONFIG.raioPonteiro2, CONFIG.cores.ponteiro2, 'P2');
    desenharCentro();
}

function desenharFundo() {
    const extra = CONFIG.raio * 0.09;
    ctx.beginPath();
    ctx.arc(CONFIG.centroX, CONFIG.centroY, CONFIG.raio + extra, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(30, 41, 59, 0.5)';
    ctx.fill();

    ctx.beginPath();
    ctx.arc(CONFIG.centroX, CONFIG.centroY, CONFIG.raio, 0, Math.PI * 2);
    ctx.fillStyle = CONFIG.cores.fundo;
    ctx.fill();
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
    ctx.lineWidth = CONFIG.raio * 0.009;
    ctx.stroke();
}

function desenharQuadrantes() {
    const cores = [
        { cor: 'rgba(59, 130, 246, 0.1)', inicio: 0, fim: 4 },
        { cor: 'rgba(34, 197, 94, 0.1)', inicio: 4, fim: 8 },
        { cor: 'rgba(249, 115, 22, 0.1)', inicio: 8, fim: 12 },
        { cor: 'rgba(168, 85, 247, 0.1)', inicio: 12, fim: 16 }
    ];
    
    cores.forEach(({ cor, inicio, fim }) => {
        const anguloInicio = ((inicio - 1) * (360 / 16) - 90) * Math.PI / 180;
        const anguloFim = ((fim - 1) * (360 / 16) - 90) * Math.PI / 180;
        
        ctx.beginPath();
        ctx.moveTo(CONFIG.centroX, CONFIG.centroY);
        ctx.arc(CONFIG.centroX, CONFIG.centroY, CONFIG.raio, anguloInicio, anguloFim);
        ctx.closePath();
        ctx.fillStyle = cor;
        ctx.fill();
    });
}

function desenharSimbolos() {
    const raioSimbSel = CONFIG.raio * 0.13;
    const raioSimbNao = CONFIG.raio * 0.11;
    const espessuraSel = CONFIG.raio * 0.014;
    const espessuraNao = CONFIG.raio * 0.009;
    const fontSizeSel = CONFIG.raio * 0.052;
    const fontSizeNao = CONFIG.raio * 0.047;

    for (let i = 1; i <= 16; i++) {
        const { x, y, simbolo, categoria } = SIMBOLOS[i];

        let cor;
        switch (categoria) {
            case 'SUJEITO':
            case 'CONFIRMACAO':
                cor = CONFIG.cores.sujeito;
                break;
            case 'VERBO':
                cor = CONFIG.cores.verbo;
                break;
            case 'OBJETO':
                cor = CONFIG.cores.objeto;
                break;
            case 'EMOCAO':
                cor = CONFIG.cores.emoCAO;
                break;
            default:
                cor = CONFIG.cores.texto;
        }

        const selecionado = (i === ponteiro1 || i === ponteiro2);
        const raio = selecionado ? raioSimbSel : raioSimbNao;

        ctx.beginPath();
        ctx.arc(x, y, raio, 0, Math.PI * 2);
        ctx.fillStyle = selecionado ? cor : 'rgba(30, 41, 59, 0.9)';
        ctx.fill();
        ctx.strokeStyle = cor;
        ctx.lineWidth = selecionado ? espessuraSel : espessuraNao;
        ctx.stroke();

        if (modoPictograma && imagensPictogramas[simbolo]) {
            const img = imagensPictogramas[simbolo];
            const imgSize = raio * 1.4;
            ctx.save();
            ctx.beginPath();
            ctx.arc(x, y, raio - CONFIG.raio * 0.009, 0, Math.PI * 2);
            ctx.clip();
            ctx.drawImage(img, x - imgSize/2, y - imgSize/2, imgSize, imgSize);
            ctx.restore();
        } else {
            ctx.fillStyle = selecionado ? '#0f172a' : '#f8fafc';
            const fs = selecionado ? fontSizeSel : fontSizeNao;
            ctx.font = `bold ${fs}px Inter, sans-serif`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            if (simbolo.length > 5) {
                ctx.font = `bold ${fs * 0.85}px Inter, sans-serif`;
            }
            ctx.fillText(simbolo, x, y);
        }
    }
}

function desenharPonteiro(angulo, raio, cor, label) {
    const x = CONFIG.centroX + raio * Math.cos(angulo);
    const y = CONFIG.centroY + raio * Math.sin(angulo);

    ctx.beginPath();
    ctx.moveTo(CONFIG.centroX, CONFIG.centroY);
    ctx.lineTo(x, y);
    ctx.strokeStyle = cor;
    ctx.lineWidth = CONFIG.raio * 0.014;
    ctx.lineCap = 'round';
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(x, y, CONFIG.raio * 0.037, 0, Math.PI * 2);
    ctx.fillStyle = '#0f172a';
    ctx.fill();
    ctx.strokeStyle = cor;
    ctx.lineWidth = CONFIG.raio * 0.018;
    ctx.stroke();

    ctx.fillStyle = '#f8fafc';
    ctx.font = `bold ${CONFIG.raio * 0.047}px Inter, sans-serif`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(label, x, y);
}

function desenharCentro() {
    ctx.beginPath();
    ctx.arc(CONFIG.centroX, CONFIG.centroY, CONFIG.raio * 0.07, 0, Math.PI * 2);
    ctx.fillStyle = '#1e293b';
    ctx.fill();
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
    ctx.lineWidth = CONFIG.raio * 0.009;
    ctx.stroke();
}

// ============================================================
// INTERAÇÃO
// ============================================================

function onMouseDown(e) {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    clique(x, y);
}

function onMouseMove(e) {
    if (arrastando === null) return;
    
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    arrastar(x, y);
}

function onMouseUp() {
    arrastando = null;
}

function onTouchStart(e) {
    e.preventDefault();
    const touch = e.touches[0];
    const rect = canvas.getBoundingClientRect();
    const x = touch.clientX - rect.left;
    const y = touch.clientY - rect.top;
    
    clique(x, y);
}

function onTouchMove(e) {
    e.preventDefault();
    if (arrastando === null) return;
    
    const touch = e.touches[0];
    const rect = canvas.getBoundingClientRect();
    const x = touch.clientX - rect.left;
    const y = touch.clientY - rect.top;
    
    arrastar(x, y);
}

function onTouchEnd() {
    arrastando = null;
}

function clique(x, y) {
    // Verificar se clicou em um símbolo
    for (let i = 1; i <= 16; i++) {
        const { x: sx, y: sy } = SIMBOLOS[i];
        const dist = Math.sqrt((x - sx) ** 2 + (y - sy) ** 2);
        
        if (dist < CONFIG.raioClique) {
            if (arrastando === null) {
                // Alternar entre ponteiros
                if (ponteiro1 === i) {
                    arrastando = 1;
                } else if (ponteiro2 === i) {
                    arrastando = 2;
                } else {
                    // Atribuir ao ponteiro mais próximo
                    const anguloClique = Math.atan2(y - CONFIG.centroY, x - CONFIG.centroX);
                    const diff1 = Math.abs(anguloClique - anguloPonteiro1);
                    const diff2 = Math.abs(anguloClique - anguloPonteiro2);
                    
                    if (diff1 < diff2) {
                        ponteiro1 = i;
                        anguloPonteiro1 = posicaoParaAngulo(i);
                        arrastando = 1;
                    } else {
                        ponteiro2 = i;
                        anguloPonteiro2 = posicaoParaAngulo(i);
                        arrastando = 2;
                    }
                }
                
                atualizarMensagem();
                desenhar();
                return;
            }
        }
    }
}

function arrastar(x, y) {
    const angulo = Math.atan2(y - CONFIG.centroY, x - CONFIG.centroX);
    const pos = anguloParaPosicao(angulo);
    
    if (arrastando === 1) {
        ponteiro1 = pos;
        anguloPonteiro1 = posicaoParaAngulo(pos);
    } else if (arrastando === 2) {
        ponteiro2 = pos;
        anguloPonteiro2 = posicaoParaAngulo(pos);
    }
    
    atualizarMensagem();
    desenhar();
}

function onKeyDown(e) {
    // Espaço para falar — mas não interceptar quando o foco está em um
    // botão, para preservar a ativação nativa (evita ação dupla)
    if (e.code === 'Space') {
        if (e.target instanceof Element && e.target.closest('button')) return;
        e.preventDefault();
        falar();
    }

    // Setas para controlar ponteiros (evita rolagem da página em paralelo)
    if (e.code.startsWith('Arrow')) {
        e.preventDefault();
    }
    if (e.code === 'ArrowLeft') {
        ponteiro1 = ((ponteiro1 - 2 + 16) % 16) + 1;
        anguloPonteiro1 = posicaoParaAngulo(ponteiro1);
        atualizarMensagem();
        desenhar();
    }
    if (e.code === 'ArrowRight') {
        ponteiro1 = (ponteiro1 % 16) + 1;
        anguloPonteiro1 = posicaoParaAngulo(ponteiro1);
        atualizarMensagem();
        desenhar();
    }
    if (e.code === 'ArrowUp') {
        ponteiro2 = ((ponteiro2 - 2 + 16) % 16) + 1;
        anguloPonteiro2 = posicaoParaAngulo(ponteiro2);
        atualizarMensagem();
        desenhar();
    }
    if (e.code === 'ArrowDown') {
        ponteiro2 = (ponteiro2 % 16) + 1;
        anguloPonteiro2 = posicaoParaAngulo(ponteiro2);
        atualizarMensagem();
        desenhar();
    }
}

// ============================================================
// MENSAGEM
// ============================================================

function atualizarMensagem() {
    const simbolo1 = SIMBOLOS[ponteiro1].simbolo;
    const simbolo2 = SIMBOLOS[ponteiro2].simbolo;
    
    const chave1 = `${simbolo1}+${simbolo2}`;
    const chave2 = `${simbolo2}+${simbolo1}`;
    
    if (COMBINACOES[chave1]) {
        mensagem = COMBINACOES[chave1];
        valida = true;
    } else if (COMBINACOES[chave2]) {
        mensagem = COMBINACOES[chave2];
        valida = true;
    } else {
        mensagem = `${simbolo1} + ${simbolo2}`;
        valida = false;
    }
    
    // Atualizar interface
    const messageCard = document.getElementById('messageCard');
    const messageText = document.getElementById('messageText');
    const messageStatus = document.getElementById('messageStatus');
    const voiceBtn = document.getElementById('voiceBtn');
    
    messageText.textContent = mensagem;
    
    messageCard.classList.remove('valid', 'invalid');
    
    if (valida) {
        messageCard.classList.add('valid');
        messageStatus.querySelector('.status-text').textContent = 'Válida';
        voiceBtn.disabled = false;
    } else {
        messageCard.classList.add('invalid');
        messageStatus.querySelector('.status-text').textContent = 'Inválida';
        voiceBtn.disabled = true;
    }
}

// ============================================================
// VOZ
// ============================================================

function falar() {
    if (!mensagem || !valida) return;
    
    const voiceBtn = document.getElementById('voiceBtn');
    voiceBtn.classList.add('speaking');
    
    // Tentar Web Speech API primeiro
    if ('speechSynthesis' in window) {
        // Cancelar qualquer fala anterior
        speechSynthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(mensagem);
        utterance.lang = 'pt-BR';
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;
        
        // Tentar selecionar voz em português
        const voices = speechSynthesis.getVoices();
        const ptBrVoice = voices.find(v => v.lang === 'pt-BR' || v.lang.startsWith('pt'));
        if (ptBrVoice) {
            utterance.voice = ptBrVoice;
        }
        
        utterance.onstart = () => {
            console.log('Iniciando fala:', mensagem);
        };
        
        utterance.onend = () => {
            console.log('Fala concluída');
            voiceBtn.classList.remove('speaking');
        };
        
        utterance.onerror = (event) => {
            console.error('Erro na fala:', event.error);
            // Fallback para API do Flask
            falarComFlask();
        };
        
        speechSynthesis.speak(utterance);
    } else {
        // Fallback para API do Flask
        falarComFlask();
    }
}

function falarComFlask() {
    const voiceBtn = document.getElementById('voiceBtn');
    
    fetch(`/api/falar?texto=${encodeURIComponent(mensagem)}`)
        .then(response => {
            if (!response.ok) throw new Error('Erro ao gerar áudio');
            return response.blob();
        })
        .then(blob => {
            const url = URL.createObjectURL(blob);
            const audio = new Audio(url);
            audio.onended = () => {
                voiceBtn.classList.remove('speaking');
                URL.revokeObjectURL(url);
            };
            audio.onerror = () => {
                voiceBtn.classList.remove('speaking');
                URL.revokeObjectURL(url);
            };
            audio.play();
        })
        .catch(error => {
            console.error('Erro ao falar:', error);
            voiceBtn.classList.remove('speaking');
        });
}

// ============================================================
// FRASES RÁPIDAS
// ============================================================

function carregarFrasesRapidas() {
    const container = document.getElementById('phraseChips');
    const frasesComuns = [
        { texto: 'Eu quero água', p1: 1, p2: 9 },
        { texto: 'Eu preciso de ajuda', p1: 1, p2: 16 },
        { texto: 'Estou com dor', p1: 15, p2: 15 },
        { texto: 'Eu quero sair', p1: 1, p2: 12 },
        { texto: 'Sim', p1: 3, p2: 3 },
        { texto: 'Não', p1: 4, p2: 4 }
    ];
    
    frasesComuns.forEach(frase => {
        const chip = document.createElement('button');
        chip.type = 'button';
        chip.className = 'phrase-chip';
        chip.textContent = frase.texto;
        chip.addEventListener('click', () => {
            ponteiro1 = frase.p1;
            ponteiro2 = frase.p2;
            anguloPonteiro1 = posicaoParaAngulo(frase.p1);
            anguloPonteiro2 = posicaoParaAngulo(frase.p2);
            atualizarMensagem();
            desenhar();
        });
        container.appendChild(chip);
    });
}

// ============================================================
// PICTOGRAMAS (ARASAAC)
// ============================================================

function carregarPictogramas() {
    fetch('/api/pictogramas')
        .then(response => response.json())
        .then(data => {
            pictogramas = data;
            console.log('Pictogramas carregados:', Object.keys(pictogramas).length);
            // Pré-carregar imagens
            Object.entries(pictogramas).forEach(([simbolo, info]) => {
                if (info.url) {
                    const img = new Image();
                    img.crossOrigin = 'anonymous';
                    img.src = info.url;
                    img.onload = () => {
                        imagensPictogramas[simbolo] = img;
                        if (modoPictograma) desenhar();
                    };
                }
            });
        })
        .catch(error => {
            console.error('Erro ao carregar pictogramas:', error);
        });
}

function alternarModoPictograma() {
    modoPictograma = !modoPictograma;
    const btn = document.getElementById('togglePictograma');
    btn.classList.toggle('active', modoPictograma);
    btn.setAttribute('aria-pressed', String(modoPictograma));
    btn.innerHTML = modoPictograma
        ? '<span aria-hidden="true">📝</span> Texto'
        : '<span aria-hidden="true">🖼️</span> Pictogramas';
    desenhar();
}
