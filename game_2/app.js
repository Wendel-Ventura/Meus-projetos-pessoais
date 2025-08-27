let listaNumeroSorteados = []
let numeroLimite = 3
let secret_number = gerarNumeroAleatorio()
let tentativas = 1


exibirMensagemIniciar()

function exibirMensagemIniciar () {
    exibirTextoNaTela('h1','Jogo do número secreto')
    exibirTextoNaTela('p','Escolha um número entre 1 e 10') 
}

function exibirTextoNaTela(tag, texto){
    let campo = document.querySelector(tag);
    campo.innerHTML = texto;
    responsiveVoice.speak(texto, 'Brazilian Portuguese Female', {rate:1.2} );
}

function verificarChute() {
    let chute = document.querySelector('input').value
    let tentativas_escrita = tentativas > 1 ? 'tentativas' : 'tentativa'
    if (chute == secret_number) {
        exibirTextoNaTela('h1','Acertouuuu! ');
        exibirTextoNaTela('p',`Você descobriu o numero secreto! Em apenas ${tentativas} ${tentativas_escrita}`);
        document.getElementById('reiniciar').removeAttribute('disabled');
    }else if (chute > secret_number) {
        exibirTextoNaTela('h1','Quase! ');
        exibirTextoNaTela('p',`O numero secreto é menor que seu chute`);
    }else {
        exibirTextoNaTela('h1','Quase! ');
        exibirTextoNaTela('p',`O numero secreto é maior que seu chute`);
    }

    tentativas ++;
    limparCampo()
};

function gerarNumeroAleatorio () {
    let numeroEscolhido = parseInt(Math.random()* numeroLimite + 1);
    let quantidadeDeElementosNalista = listaNumeroSorteados.length;

    if (quantidadeDeElementosNalista == numeroLimite
    ) {
        listaNumeroSorteados = [];
        }

    if (listaNumeroSorteados.includes(numeroEscolhido)){
        return gerarNumeroAleatorio()
    }else {
        listaNumeroSorteados.push(numeroEscolhido)
        return numeroEscolhido
    }
}

function limparCampo (){
    chute = document.querySelector('input');
    chute.value = ''
}

function reiniciarjogo (){
    secret_number = gerarNumeroAleatorio()
    limparCampo()
    tentativas = 1
    exibirMensagemIniciar()
    document.getElementById('reiniciar').setAttribute('disabled',true)
}


