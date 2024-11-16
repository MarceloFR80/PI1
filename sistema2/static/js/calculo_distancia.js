// Função para buscar coordenadas de um CEP usando a Geocoding API
async function buscarCoordenadasGoogle(cep) {
    const apiKey = 'AIzaSyC4qrmqXd3zG-Uj75fwpabt-qipWlBj1Uk'; // Substitua pela sua chave de API
    const url = `https://maps.googleapis.com/maps/api/geocode/json?address=${cep}&region=br&key=${apiKey}`;

    try {
        const response = await fetch(url);
        const data = await response.json();

        if (data.status !== "OK") {
            throw new Error("CEP não encontrado.");
        }

        // Retornar latitude e longitude
        return data.results[0].geometry.location; // Ex.: { lat: -23.55052, lng: -46.633308 }
    } catch (error) {
        console.error("Erro ao buscar coordenadas no Google Maps:", error.message);
        throw error;
    }
}

// Função para calcular a distância entre dois CEPs usando a Distance Matrix API
async function calcularDistancia(cepOrigem, cepDestino) {
    const apiKey = 'AIzaSyC4qrmqXd3zG-Uj75fwpabt-qipWlBj1Uk'; // Substitua pela sua chave API
    const url = `https://maps.googleapis.com/maps/api/distancematrix/json?origins=${cepOrigem}&destinations=${cepDestino}&region=br&key=${apiKey}`;
    
    try {
        console.log("URL da API:", url);
        const response = await fetch(url);
        
        // Verifica se a resposta foi bem-sucedida
        if (!response.ok) {
            throw new Error(`Erro na API: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        console.log("Dados retornados:", data);

        // Verifica se o status do resultado é OK
        const result = data.rows[0].elements[0];
        if (result.status === "OK") {
            const distancia = result.distance.text; // Distância formatada (ex: "518 km")
            const duracao = result.duration.text;  // Duração formatada (ex: "6 horas 7 minutos")
            return { distancia, duracao };
        } else {
            throw new Error(`Erro na resposta: ${result.status}`);
        }
    } catch (error) {
        console.error("Erro ao calcular distância:", error.message);
        throw error;
    }
}


