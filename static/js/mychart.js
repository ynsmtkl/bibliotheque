const ctxBar = document.getElementById('myChartBar');
const ctxLine = document.getElementById('myChartLine');
const ctxDoughnut = document.getElementById('myChartDoughnut');
const ctxPie = document.getElementById('myChartPie');

const myDataJoursElement = document.getElementById('myDataJours');
const myDataMoisElement = document.getElementById('myDataMois');
const myDataCategoriesElement = document.getElementById('myDataCategories');
const myDataCategoriesCountElement = document.getElementById('myDataCategoriesCount');

const dataJours = JSON.parse(myDataJoursElement.textContent);
const dataMois = JSON.parse(myDataMoisElement.textContent);
const dataCategories = JSON.parse(myDataCategoriesElement.textContent);
const dataCategoriesCount = JSON.parse(myDataCategoriesCountElement.textContent);


const keysJours = Object.keys(dataJours);
const valuesJours = Object.values(dataJours);

const keysMois = Object.keys(dataMois);
const valuesMois = Object.values(dataMois);

// Extract array of noms
var noms = dataCategories.map(function(item) {
    return item.nom;
});

// Extract array of livre_counts
var livreCounts = dataCategories.map(function(item) {
    return item.livre_count;
});

// Extract array of noms
var nomsCategoriesDemande = dataCategoriesCount.map(function(item) {
    return item.nom;
});

// Extract array of livre_counts
var livreDemandeCounts = dataCategoriesCount.map(function(item) {
    return item.livre_demand_count;
});


new Chart(ctxBar, {
    type: 'bar',
    data: {
        labels: keysJours,
        datasets: [{
            label: '# d\'emprunts',
            data: valuesJours,
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        },
        //maintainAspectRatio: false,
    }
});

new Chart(ctxLine, {
    type: 'line',
    data: {
        labels: keysMois,
        datasets: [{
            label: '# d\'emprunts',
            data: valuesMois,
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        },
        height: 100,
    }
});

new Chart(ctxDoughnut, {
    type: 'doughnut',
    data: {
        labels: noms,
        datasets: [{
            label: '# de livres',
            data: livreCounts,
            borderWidth: 1,
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        },
        maintainAspectRatio: false,
    }
});

new Chart(ctxPie, {
    type: 'pie',
    data: {
        labels: nomsCategoriesDemande,
        datasets: [{
            label: '# de demandes',
            data: livreDemandeCounts,
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        },
        maintainAspectRatio: false,
    }
});