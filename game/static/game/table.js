/** Additional functions **/

// Counter then redirect
/*
function decisionCounter(id, seconds, url) {
    var counter = seconds;
    var refreshIntervalId = setInterval(function(){
        counter--;
        document.getElementById(id).innerHTML = counter;
        if (counter == 0) {
            clearInterval(refreshIntervalId);
            window.location.href = url;
        }
    }, 1000);
    refreshIntervalId();
}
*/

/** WINNER Change player cards to css **/

function changePlayerCards(cards_id) {

    var player_cards_id = "player_cards_" + cards_id

    // 1. Get player cards
    var player_cards = document.getElementById(player_cards_id).innerHTML;

    if (player_cards.length < 10) {

        // 2. Change string to 2chars array
        player_arr = player_cards.match(/.{1,2}/g);
        var new_player = '';

        // 3. Put cards decorated by cards div's
        for (var i = 0; i < player_arr.length; i++) {
            if (player_arr[i][1] == '♥' || player_arr[i][1] == '♦') {
                new_player += ('<div class="card container-fluid m-1 text-danger">' + player_arr[i] + '</div>');
            } else {
                new_player += ('<div class="card container-fluid m-1">' + player_arr[i] + '</div>');
            }
        }
        document.getElementById(player_cards_id).innerHTML = new_player;
    }
}

/** REFRESH **/
window.onload = function() {

    // Change string to cards
    try {
        changePlayerCards(1);
        changePlayerCards(2);
        changePlayerCards(3);
        changePlayerCards(4);
    } catch (error) {
        console.log(error);
    }

    // Make fade effect
    /*
    document.getElementById("hideAll").style.opacity='0';
    setTimeout(function(){
        document.getElementById("hideAll").style.display = "none";
    }, 500);*/

    // Refresh site
    /*
    setTimeout(function(){
        window.location.reload(false);
    }, 2000);
    */

    // Decision counter
    //decisionCounter("decision_counter", 10, "/pass");
}


/** Change board cards to css **/

// 1. Get board cards
try {
    var board_cards = document.getElementById("board_cards").innerHTML;
} catch (error) {
    console.log(error);
    var board_cards = '';
}

if (board_cards.length > 0) {
    try {
        // 2. Change string to 2chars array
        board_arr = board_cards.match(/.{1,2}/g);
        var new_board = '';

        // 3. Put cards decorated by cards div's
        for (var i = 0; i < board_arr.length; i++) {
            if (board_arr[i][1] == '♥' || board_arr[i][1] == '♦') {
                new_board += ('<div class="card container-fluid m-1 text-danger">' + board_arr[i] + '</div>');
            } else {
                new_board += ('<div class="card container-fluid m-1">' + board_arr[i] + '</div>');
            }
        }
        document.getElementById("board_cards").innerHTML = new_board;
    } catch (error) {
        console.log(error);
    }
}



/** Range functionality **/

try {
    var check_call_buttons = document.getElementById("check_call_buttons").innerHTML;
    var raise_button = '<button type="submit" class="btn btn-lg btn-warning">raise</button>';
    var player_money = parseInt(document.getElementById("player_money").innerHTML);
    var pool = parseInt(document.getElementById("pool").innerHTML);

    // Input range functionality
    document.getElementById("formControlRange").oninput = function() {

        // Change text input and player money value if I drag range
        var new_value = parseInt(document.getElementById("formControlRange").value);
        document.getElementById("how_much").value = new_value;
        document.getElementById("player_money").innerHTML = (player_money - new_value);
        document.getElementById("pool").innerHTML = (pool + new_value);

        // Change button to 'Raise' if value in range > 0
        if (new_value > 0) {
            document.getElementById("raise_button").innerHTML = raise_button;
            document.getElementById("check_call_buttons").innerHTML = "";
        }

        // Change button to 'Check' if value in range == 0
        if (new_value == 0) {
            document.getElementById("raise_button").innerHTML = "";
            document.getElementById("check_call_buttons").innerHTML = check_call_buttons;
        }
    }
} catch (error) {
    console.log(error);
}