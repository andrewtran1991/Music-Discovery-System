//Create svg
var svg = d3.select("body")
        .append("svg")
        // .attr("width",1500)
        // .attr("height",1000)
        .attr("x",0)
        .attr("y",0);

var year = 'Any';
var danceability=0; 
var liveness=0;
var energy=0;
var tempo=0;
var valence=0;
table_columns=['song_name', 'sample','artist_name', 'tempo', 'loudness', 'mode', 'speechiness', 'liveness', 'valence', 'danceability', 'energy', 'acousticness', 'instrumentalness', 'artist_popularity', 'album_popularity', 'sp_album_release_date_year']
table_columns_1=['song_name', 'artist_name', 'tempo', 'valence']

var year_data=[]
year_data.push("Any")
for(var i=1950; i <=2020; i++){
    year_data.push(i)
}

var options = d3.select("#year").selectAll("option")
		.data(year_data)
	    .enter().append("option")
        .text(d => d)

var select = d3.select("#year")
            .on("change", function() {
                year = this.value;
                // update(this.value);
                // d3.select('#value').text(this.value);
                update_all_criteria(year, tempo,energy,valence, liveness,danceability);
            })
        
var slider = d3.sliderHorizontal()
                .min(0)
                .max(200)
                .step(20)
                .width(300)
                .displayValue(false)
                .on('onchange', val => {
                    d3.select('#value').text(val);
                    tempo=val;
                    // update_tempo(year, val);
                    update_all_criteria(year, tempo,energy,valence, liveness,danceability);
                });
    
      d3.select('#slider')
            .append('svg')
            // .attr('width', 500)
            // .attr('height', 100)
            .append('g')
            .attr('transform', 'translate(30,30)')
            .call(slider);

var slider1 = d3.sliderHorizontal()
            .min(0)
            .max(1)
            .step(0.1)
            .width(300)
            .displayValue(false)
            .on('onchange', val => {
                d3.select('#value').text(val);
                energy=val;
                // update_energy(year, val);
                update_all_criteria(year, tempo,energy,valence, liveness,danceability);
            });

  d3.select('#slider1')
        .append('svg')
        // .attr('width', 500)
        // .attr('height', 100)
        .append('g')
        .attr('transform', 'translate(30,30)')
        .call(slider1);

var slider2 = d3.sliderHorizontal()
        .min(0)
        .max(1)
        .step(0.1)
        .width(300)
        .displayValue(false)
        .on('onchange', val => {
            d3.select('#value').text(val);
            valence=val;
            // update_valence(year, val);
            update_all_criteria(year, tempo,energy,valence, liveness,danceability);
        });

d3.select('#slider2')
    .append('svg')
    // .attr('width', 500)
    // .attr('height', 100)
    .append('g')
    .attr('transform', 'translate(30,30)')
    .call(slider2);

var slider3 = d3.sliderHorizontal()
    .min(0)
    .max(1)
    .step(0.1)
    .width(300)
    .displayValue(false)
    .on('onchange', val => {
        d3.select('#value').text(val);
        liveness=val;
        // update_liveness(year, val);
        update_all_criteria(year, tempo,energy,valence, liveness,danceability);
    });
    
d3.select('#slider3')
        .append('svg')
        // .attr('width', 500)
        // .attr('height', 100)
        .append('g')
        .attr('transform', 'translate(30,30)')
        .call(slider3);

var slider4 = d3.sliderHorizontal()
        .min(0)
        .max(1)
        .step(0.1)
        .width(300)
        .displayValue(false)
        .on('onchange', val => {
            d3.select('#value').text(val);
            danceability=val;
            // update_danceability(year, val);
            update_all_criteria(year, tempo,energy,valence, liveness,danceability);
        });

d3.select('#slider4')
    .append('svg')
    // .attr('width', 500)
    // .attr('height', 100)
    .append('g')
    .attr('transform', 'translate(30,30)')
    .call(slider4);


update(year);

function update(year){
    d3.select('#value').text(year);

    d3.json('/get_songs_by_year/'+year). then(function(data){

    var table_plot = makeTable(table_columns)
        .datum(data)
        .sortBy('song_name', true)
    
    $("#table_div").replaceWith('<div id="table_div"> </div>');
    d3.select('#table_div').call(table_plot);

    })
    .catch(function(error){
        console.log(error)
    });    
}//end of update function


function update_tempo(year, tempo){
    d3.select('#value').text(year);
    d3.json('/get_songs_by_year_tempo/'+year+'/'+tempo). then(function(data){
    
    var table_plot = makeTable(table_columns)
        .datum(data)
        .sortBy('song_name', true)
    
    $("#table_div").replaceWith('<div id="table_div"> </div>');
    d3.select('#table_div').call(table_plot);

    })
    .catch(function(error){
        console.log(error)
    });    
}//end of update_tempo function

function update_energy(year, energy){
    d3.select('#value').text(year);
    d3.json('/get_songs_by_year_energy/'+year+'/'+energy). then(function(data){
    
    var table_plot = makeTable(table_columns)
        .datum(data)
        .sortBy('song_name', true)
    
    $("#table_div").replaceWith('<div id="table_div"> </div>');
    d3.select('#table_div').call(table_plot);

    })
    .catch(function(error){
        console.log(error)
    });    
}//end of update_energy function

function update_valence(year, valence){
    d3.select('#value').text(year);
    d3.json('/get_songs_by_year_valence/'+year+'/'+valence). then(function(data){
    
    var table_plot = makeTable(table_columns)
        .datum(data)
        .sortBy('song_name', true)
    
    $("#table_div").replaceWith('<div id="table_div"> </div>');
    d3.select('#table_div').call(table_plot);

    })
    .catch(function(error){
        console.log(error)
    });    
}//end of update_valence function


function update_liveness(year, liveness){
    d3.select('#value').text(year);
    d3.json('/get_songs_by_year_liveness/'+year+'/'+liveness). then(function(data){
    
    var table_plot = makeTable(table_columns)
        .datum(data)
        .sortBy('song_name', true)
    
    $("#table_div").replaceWith('<div id="table_div"> </div>');
    d3.select('#table_div').call(table_plot);

    })
    .catch(function(error){
        console.log(error)
    });    
}//end of update_liveness function


function update_danceability(year, danceability){
    d3.select('#value').text(year);
    d3.json('/get_songs_by_year_danceability/'+year+'/'+danceability). then(function(data){
    
    var table_plot = makeTable(table_columns)
        .datum(data)
        .sortBy('song_name', true)
    
    $("#table_div").replaceWith('<div id="table_div"> </div>');
    d3.select('#table_div').call(table_plot);

    })
    .catch(function(error){
        console.log(error)
    });    
}//end of update_danceability function


function update_all_criteria(year, tempo, energy, valence, liveness, danceability){
    d3.select('#value').text(year);
    d3.json('/get_songs_by_all_criteria/'+year+'/'+tempo+'/'+energy+'/'+valence+'/'+liveness+'/'+danceability). then(function(data){
    
    var table_plot = makeTable(table_columns)
        .datum(data)
        .sortBy('song_name', true)
    
    $("#table_div").replaceWith('<div id="table_div"> </div>');
    d3.select('#table_div').call(table_plot);

    })
    .catch(function(error){
        console.log(error)
    });    
}//end of update_danceability function




