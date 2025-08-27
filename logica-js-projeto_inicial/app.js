alert('Welcome the secret number game');
// let é tipo o var do python
let secret_number = parseInt(Math.random()*10+1);
// prompt é tipo um input 
let number_user ;
let trys = 1; 




// if funciona semelhante 
// no python usamos a fstring print(f'') aqui usamos a craze (` e $)
// elif seria else if 

// if sem o while:

// if (secret_number == number_user) {
//     alert(`Nice!!, you accept the scret number (${secret_number})`);
// }
// else if (secret_number < number_user ) {
//     alert('O seu numero é maior que o numero secreto')
// }
// else if (secret_number > number_user ) {
//     alert('O seu numero é menor que o numero secreto')
// }

while(secret_number != number_user){
    number_user = prompt('Say me a number beetween 1-30');

    let trys_write =  trys > 1 ? 'tentativas' : 'tentativa';

    if (secret_number == number_user) {
    alert(`Nice!!, you accept the scret number (${secret_number}) em (${trys}) ${trys_write}`);
    }
    else if (secret_number < number_user ) {
        alert(`O seu numero é maior que o numero secreto em (${trys}) tentativas`);
    }
    else if (secret_number > number_user ) {
        alert(`O seu numero é menor que o numero secreto em (${trys}) tentativas`);
    };

    trys++
 
}