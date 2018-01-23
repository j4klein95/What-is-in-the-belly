// create variables for selecting pie plot


function unpack(rows, index) {
  return rows.map(function(row) {
    return row[index];
  });
}

function plotPie(){
  Plotly.d3.json('/names', function(error, response) {
    for (i=0; i < response.length; i++){
      var selDataset = document.getElementById('selDataset');
      var data = response[i];
      var option = document.createElement('option');
      option.textContent = data;
      option.value = data;
      selDataset.append(option);
    }
  })
  Plotly.d3.json('')

};
