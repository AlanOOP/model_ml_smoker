
const form = document.getElementById('predictionForm');
const result = document.querySelector('#result');



const handleSubmit = async (e) => {
    e.preventDefault();

    const GATA4 = document.getElementById('GATA4').value;
    const Gene1689 = document.getElementById('Gene1689').value;

    if (!GATA4 || !Gene1689) {
        return alert('Todos los campos son requeridos');
    }

    const data = { GATA4, Gene1689 };


    try {
        await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
            .then((res) => res.json())
            .then((data) => {

                // create element p to show the result
                const p = document.createElement('p');
                // p.textContent = `Predicción: ${data.prediction}`;

                if (data.prediction === 1) {
                    p.className = 'text-red-500 font-bold text-2xl mt-4 text-center bg-red-100 p-4 shadow-md  border-l-4 border-red-400';
                    p.textContent = `Predicción: ${data.prediction} - El paciente tiene un riesgo alto de padecer Cáncer`;

                } else {
                    p.className = 'text-green-500 font-bold text-2xl mt-4 text-center bg-green-100 p-4 shadow-md  border-l-4 border-green-500';
                    p.textContent = `Predicción: ${data.prediction} - El paciente tiene un riesgo bajo de padecer Cáncer`;
                }

                //borrar el resultado anterior
                result.innerHTML = '';
                // mostrar el resultado
                result.appendChild(p);

            });

    } catch (error) {
        console.error('Error:', error);
    }
}

form.addEventListener('submit', handleSubmit);

