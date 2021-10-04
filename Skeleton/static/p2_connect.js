function autoUpdate() {
    myVar = setInterval(getNewBoard, 500);
}

function getNewBoard(){
    const Http =  new XMLHttpRequest();
    var url = "http://127.0.0.1:5000/autoUpdate"
    Http.open("GET",url)
    Http.send()
    Http.onload = function(){
        if(Http.readyState == Http.DONE){
            if(Http.status == 200){
                data = JSON.parse(Http.response)
                
                if(data['move'] != ""){
                    displayBoard(data['move'])
                    if(data['winner'].length > 0){
                        document.getElementById('winner').innerHTML = "Winner is: " + data['winner']
                    }

                }

            }
        }
    }
}

function displayBoard(board){
    for(var row = 0; row < board.length; row++){
        for(var col = 0; col < board[0].length; col++){
            if(board[row][col] == 'red'){
                document.getElementsByClassName('col'+ (col+1))[row].style.backgroundColor = 'red'
            }else if(board[row][col] == 'yellow'){
                document.getElementsByClassName('col'+ (col+1))[row].style.backgroundColor = 'yellow'
            }
        }
    }
}

function move(event){
    const Http =  new XMLHttpRequest();
    const url = 'http://127.0.0.1:5000/move2'
    Http.open('POST', url)
    Http.setRequestHeader("Content-Type", "application/json");
    let classNames = event.target.getAttribute('class')
    data = JSON.stringify({'column': classNames.split(' ')[1]})
    Http.responseType = 'text'
    
    Http.send(data)

    Http.onload = function(){
        if(Http.readyState == Http.DONE){
            if(Http.status == 200){
                data = JSON.parse(Http.response)
                if(data['invalid'] == true){

                    //displayBoard(data['move'])
                    if(data['winner'].length > 0){
                        document.getElementById('winner').innerHTML =  "Winner is: " + data['winner']
                    }

                    else{
                        document.getElementById('error').innerHTML = "Error: " + data['reason']
                    }
                    
                }else{
                    document.getElementById('error').innerHTML = ""
                    displayBoard(data['move'])

                    if(data['winner'].length > 0){
                        document.getElementById('winner').innerHTML = "Winner is: " + data['winner']
                    }
                    
                }
                
            }
        }
    }
}

autoUpdate()