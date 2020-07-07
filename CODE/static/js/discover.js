var selected_song_id_from_autocomplete;
hasLiked=false;
songSelected=false;
songAttributeSelected=false;
discoverClicked=false;
getMoreSimilarClicked=false;

$('.like_unlike_button').click(function(ev){
    var id = $(ev.currentTarget).attr('id');
    // alert(id);
    // var id_array = id.split("|");
    // alert(id_array[0], id_array[1]);
    if ($(ev.currentTarget).find('span').hasClass('glyphicon-thumbs-up')){
        $.get( "/like/" + id, function(data ) {
            console.log(data);
            $(ev.currentTarget).find('span').removeClass("glyphicon-thumbs-up").addClass("glyphicon-thumbs-down");
            get_recommendation_list(id);
        });
    }
    if ($(ev.currentTarget).find('span').hasClass('glyphicon-thumbs-down')){
        $.get( "/unlike/" + id, function(data ) {
            console.log(data);
            $(ev.currentTarget).find('span').removeClass("glyphicon-thumbs-down").addClass("glyphicon-thumbs-up");
            remove_recommendation_list();
        });
    }

});

function get_recommendation_list(song_id){
    // alert('fetching recomemndation_list'+song_id);
    $("#recommended_list_table").empty();
    $.get( "/recommend_song/" + song_id, function(data ) {
        // var json = JSON.parse(data);
        // alert(JSON.stringify(data));
        $("#recommended_list_table").append("<tr>");
        $.each(data,function(i,v){
            // console.log("key is " + i);
            // console.log("value is " + v);
            $("#recommended_list_table").append("<td>" + v+ "</td>");
        })
        $("#recommended_list_table").append("</tr>");
        
    });
}

function remove_recommendation_list(){
    $("#recommended_list_table").empty();
}

//select all checkboxes
$("#select_all").change(function(){  //"select all" change 
    $(".checkbox").prop('checked', $(this).prop("checked")); //change all ".checkbox" checked status
});

//".checkbox" change 
$('.checkbox').change(function(){
  	//uncheck "select all", if one of the listed checkbox item is unchecked
    if(false == $(this).prop("checked")){ //if this item is unchecked
        $("#select_all").prop('checked', false); //change "select all" checked status to false
    }
	//check "select all" if all checkbox items are checked
	if ($('.checkbox:checked').length == $('.checkbox').length ){
		$("#select_all").prop('checked', true);
    }
});


$(function() {
    $("#autocomplete").autocomplete({
        source:function(request, response) {
            $.getJSON("/autocomplete",{
                q: request.term, // in flask, "q" will be the argument to look for using request.args
            }, function(data) {
                // response(data.json_list); // matching_results from jsonify
                response($.map(data.json_list, function(item, key ) {
                    return {
                        label: item.song_name,
                        value: item.song_id
                    }
                }));
            });
        },
        minLength: 2,
        select: function(event, ui) {
            event.preventDefault();
            $('#autocomplete').val(ui.item.label);
            console.log(ui.item.value); // not in your question, but might help later
            console.log(ui.item.label);
            selected_song_id_from_autocomplete = ui.item.value;
            songSelected=true;
            discoverClicked=false;
            getMoreSimilarClicked=false;
        }
    });
});

    function view_cluster(){
        var songAttributechecked=[]
        $("input:checkbox[name='check[]']:checked").each(function(){
            songAttributechecked.push($(this).val());
            songAttributeSelected=true;
        });
        if (songAttributechecked.length !=3){
            alert("Please select 3 features to view the clusters");
            return;
        }
        if (!discoverClicked || !getMoreSimilarClicked){
            alert("Please discover and like songs to see clusters");
            return;
        }
        window.location.href="/plot_cluster"
    }

   function get_similar_songs(){
        if (!hasLiked){
            alert("Please like a song below to proceed");
            return;
        }
        var songAttributechecked=[]
        $("input:checkbox[name='check[]']:checked").each(function(){
            songAttributechecked.push($(this).val());
            songAttributeSelected=true;
        });
        if (songAttributechecked.length >3){
            alert("Please select 3 or less song features to start with");
            return;
        }
        // alert(songAttributechecked);
        // alert(selected_song_id_from_autocomplete);
        json_song_attributes = JSON.stringify(songAttributechecked);
        $("#like_unlike_table").empty();
        tr=$('<tr/>');
        tr.append("<th>Song Name</th>");
        tr.append("<th>Artist Name</th>");
        tr.append("<th>Sample</th>");
        tr.append("<th>Album Name</th>");
        tr.append("<th>Like/Unlike</th>");
        $('#like_unlike_table').append(tr);

    $.get( "/get_similar_songs/"+ selected_song_id_from_autocomplete+"/"+json_song_attributes, function(data ) {
        // alert(data);

        var tr;
        getMoreSimilarClicked=true;
        for(var i=0; i<data.length;i++){
            tr=$('<tr/>');
            // tr.append("<td>"+data[i].row_counter+"</td>");
            tr.append("<td>"+data[i].song_name+"</td>");
            tr.append("<td>"+data[i].artist_name+"</td>");
            tr.append("<td><iframe src='https://open.spotify.com/embed/track/" + data[i].song_id +"' width='300' height='80' frameborder='0' allowtransparency='true' allow='encrypted-media'></iframe><br><a href='spotify:track:"+data[i].song_id+"'>Full Song on Spotify</a></td>");
            tr.append("<td>"+data[i].album_name+"</td>");
            // tr.append("<td>"+data[i].track_href+"</td>");
            // tr.append('<td><button type="button" class="btn btn-default like_unlike_button" <span class="glyphicon glyphicon-thumbs-up" aria-hidden="true"></span></button></td>');
            tr.append('<td><button type="button" id="' + data[i].song_id + 'l" class="btn btn-default like_button"><span class="glyphicon glyphicon-thumbs-up" aria-hidden="true"></span></button><button type="button" id="' + data[i].song_id + 'd" class="btn btn-default unlike_button"><span class="glyphicon glyphicon-thumbs-down" aria-hidden="true"></span></button><label id="' + data[i].song_id + 'text" ></label></td>');
            $('#like_unlike_table').append(tr);
            
        }
        hasLiked=false;
    });

   }



    function discover_songs(){
        var songAttributechecked=[]
        $("input:checkbox[name='check[]']:checked").each(function(){
            songAttributechecked.push($(this).val());
            songAttributeSelected=true;
        });
        if (!songAttributeSelected || !songSelected){
            alert("Please select a song and choose features to continue");
            return;
        }
        // alert(songAttributechecked.length)
        if (songAttributechecked.length >3){
            alert("Please select 3 or less song features to start with");
            return;
        }
        // alert(songAttributechecked);
        // alert(selected_song_id_from_autocomplete);
        json_song_attributes = JSON.stringify(songAttributechecked);
        // alert(json_song_attributes);
        $("#like_unlike_table").empty();
        tr=$('<tr/>');
        tr.append("<th>Song Name</th>");
        tr.append("<th>Artist Name</th>");
        tr.append("<th>Sample</th>");
        tr.append("<th>Album Name</th>");
        tr.append("<th>Like/Unlike</th>");
        $('#like_unlike_table').append(tr);


        $.get( "/discover_songs/" + selected_song_id_from_autocomplete+"/"+json_song_attributes, function(data ) {
            // alert(data);
            console.log(data);
            discoverClicked = true;
            var tr;
            for(var i=0; i<data.length;i++){
                tr=$('<tr/>');
                // tr.append("<td>"+data[i].row_counter+"</td>");
                tr.append("<td>"+data[i].song_name+"</td>");
                tr.append("<td>"+data[i].artist_name+"</td>");
                tr.append("<td><iframe src='https://open.spotify.com/embed/track/" + data[i].song_id +"' width='300' height='80' frameborder='0' allowtransparency='true' allow='encrypted-media'></iframe><br><a href='spotify:track:"+data[i].song_id+"'>Full Song on Spotify</a></td>");
                tr.append("<td>"+data[i].album_name+"</td>");
                // tr.append("<td>"+data[i].track_href+"</td>");
                // tr.append('<td><button type="button" class="btn btn-default like_unlike_button" <span class="glyphicon glyphicon-thumbs-up" aria-hidden="true"></span></button></td>');
                tr.append('<td><button type="button" id="' + data[i].song_id + 'l" class="btn btn-default like_button"><span class="glyphicon glyphicon-thumbs-up" aria-hidden="true"></span></button><button type="button" id="' + data[i].song_id + 'd" class="btn btn-default unlike_button"><span class="glyphicon glyphicon-thumbs-down" aria-hidden="true"></span></button><label id="' + data[i].song_id + 'text" ></label></td>');
                $('#like_unlike_table').append(tr);
                
            }
        });
    }

    $(document).on("click",".like_unlike_button", function(ev){

        var id = $(ev.currentTarget).attr('id');
        // alert(id);
        // var id_array = id.split("|");
        // alert(id_array[0], id_array[1]);
        
        if ($(ev.currentTarget).find('span').hasClass('glyphicon-thumbs-up')){
            $.get( "/like/" + id, function(data ) {
                console.log(data);
                $('#'+id).find('span').removeClass("glyphicon-thumbs-up").addClass("glyphicon-thumbs-down");
                hasLiked = true;
                // get_recommendation_list(id);
            });
        }
        if ($(ev.currentTarget).find('span').hasClass('glyphicon-thumbs-down')){
            $.get( "/unlike/" + id, function(data ) {
                console.log(data);
                $("#"+id).find('span').removeClass("glyphicon-thumbs-down").addClass("glyphicon-thumbs-up");
                // remove_recommendation_list();
            });
        }
    });
    $(document).on("click",".like_button", function(ev){
    
        var id1 = $(ev.currentTarget).attr('id');
        id = id1.substr(0,id1.length-1);
        // alert(id);
        // var id_array = id.split("|");
        // alert(id_array[0], id_array[1]);
        
        if ($(ev.currentTarget).find('span').hasClass('glyphicon-thumbs-up')){
            $.get( "/like/" + id, function(data ) {
                console.log(data);
                //$('#'+id + "l").find('span').removeClass("glyphicon-thumbs-up");
                //$('#'+id + "d").find('span').removeClass("glyphicon-thumbs-down");
                document.getElementById(id+"d").disabled = true;
                document.getElementById(id+"l").disabled = true;
                document.getElementById(id+"text").innerHTML = "Liked";
                hasLiked = true;
                // get_recommendation_list(id);
            });
        }
    });
    $(document).on("click",".unlike_button", function(ev){
    
        var id = $(ev.currentTarget).attr('id');
        id = id.substr(0,id.length-1);
        // alert(id);
        // var id_array = id.split("|");
        // alert(id_array[0], id_array[1]);        
        if ($(ev.currentTarget).find('span').hasClass('glyphicon-thumbs-down')){
            $.get( "/unlike/" + id, function(data ) {
                console.log(data);
                //$('#'+id + "l").find('span').removeClass("glyphicon-thumbs-up");
                //$('#'+id + "d").find('span').removeClass("glyphicon-thumbs-down");
                document.getElementById(id+"d").disabled = true;
                document.getElementById(id+"l").disabled = true;
                document.getElementById(id+"text").innerHTML = "Unliked";
                hasLiked = true;
            });
        }
    });


// $(function() {
//     $.ajax({
//         url: "/autocomplete",
//         }).done(function (data) {
          
//             //data = JSON.stringify(data);
//             //alert(data);
//             console.log(data);
//             // $('#autocomplete').autocomplete({
//             //     source: data.json_list,
//             //     minLength: 2
//             // });
//             //$('#autocomplete').autocomplete(data);
//             autocomplete(document.getElementById("autocomplete"), data);
//         });
//     });

function autocomplete(inp, arr) {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function(e) {
      var a, b, i, val = this.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;
      /*create a DIV element that will contain the items (values):*/
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      /*append the DIV element as a child of the autocomplete container:*/
      this.parentNode.appendChild(a);
      /*for each item in the array...*/
      for (i = 0; i < arr.length; i++) {
        /*check if the item starts with the same letters as the text field value:*/
        if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
          /*create a DIV element for each matching element:*/
          b = document.createElement("DIV");
          /*make the matching letters bold:*/
          b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
          b.innerHTML += arr[i].substr(val.length);
          /*insert a input field that will hold the current array item's value:*/
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          /*execute a function when someone clicks on the item value (DIV element):*/
              b.addEventListener("click", function(e) {
              /*insert the value for the autocomplete text field:*/
              inp.value = this.getElementsByTagName("input")[0].value;
              /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
              closeAllLists();
          });
          a.appendChild(b);
        }
      }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
      x[i].parentNode.removeChild(x[i]);
    }
  }
}
/*execute a function when someone clicks in the document:*/
document.addEventListener("click", function (e) {
    closeAllLists(e.target);
});
}

