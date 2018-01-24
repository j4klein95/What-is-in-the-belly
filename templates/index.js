// create variables for selecting pie plot


function unpack(rows, index) {
  return rows.map(function(row) {
    return row[index];
  });
}

function optionPie(){
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
};

function get_pie_data(sampleID) {
  Plotly.d3.json('/samples/'+ sampleID, function(error, response) {
    if (error) return console.warn(error);
    var sample_values_array = [];
    var otu_id_array = [];
    for (i=0; i<10; i++) {
      sample_values_array.push(response.otu_ids[i]);
      sample_values_array.push(response.sample_values[i]);
    }
  })
};

function build_pie_chart()
