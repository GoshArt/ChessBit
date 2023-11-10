let divSquare = '<div id="s$coord" class="square $color"></div>';
let divFigure = '<div id="f$coord" class="figure">$figure</div>';
let map;
let df;
let dsq;
let botColor = document.getElementById("botColor").value;
let color;
let turn = 'white';


$(function () {
    start()
    pressSquare();
    if (color === "black") {
        reverseMap()
        $.post(
            "/field",
            {
                map: map.join(''),
            },
            onAjaxSuccess,
        );
    }
});
$( window ).resize(function() {
	res();
});

function updateFigures(){
    df = document.querySelectorAll("div.figure");
    df.forEach((event) => {
        event.addEventListener('click', () => {
            let coord = map.indexOf('3')-64
            if(coord < 0 && !thisEnemy(event.id.slice(2))){
                viewMoveFigure(event.id.slice(2));
            }
        });
    });
}
function start(){
    map = new Array(128)
    map = "rnbqkbnrpppppppp11111111111111111111111111111111PPPPPPPPRNBQKBNR0000000000000000000000000000000000000000000000000000000000000000".split('');
    // map = line.split('');
    console.log(map)
    if(botColor === "W"){
        color = "black"
        reverseMap()
        console.log("b")
    }else {
        color = "white"
        console.log("w")
    }

    addSquares();
    showFigures(map.join(""))
    updateFigures();
    buttonSurrender()
}
function pressSquare(){
    dsq = document.querySelectorAll("div.square");
    dsq.forEach((event) => {
        event.addEventListener('click', () => {
            let coord = map.indexOf('3')-64
            if(+map[+event.id.slice(1) + +64] === 2){
                map[event.id.slice(1)] = map[coord]
                map[coord] = 1;
                if(!whichKingLoss() && ((map[event.id.slice(1)] === 'P' && color === 'white') || (map[event.id.slice(1)] === 'p' && color === 'black')) &&  0 <= +event.id.slice(1) && +event.id.slice(1) <= 7){
                    changePawn(event.id.slice(1));
                }else {
                    showFigures(map.join(""));
                    updateFigures();
                }
                if(color==='black'){
                    reverseMap()
                }

                $.post(
                    "/field",
                    {
                        map: map.join(''),
                    },
                    onAjaxSuccess,
                );
            }
            if (+map[+event.id.slice(1) + +64] !== 3){
                clearMoveMap();
            }
        });
    });
}
function viewMoveFigure(coord){
    switch (map[coord]){
        case 'K':
            king(coord);
            break;
        case 'k':
            king(coord);
            break;
        case 'Q':
            verticalHorizontal(coord);
            diagonal(coord);
            break;
        case 'q':
            verticalHorizontal(coord);
            diagonal(coord);
            break;
        case 'R':
            verticalHorizontal(coord);
            break;
        case 'r':
            verticalHorizontal(coord);
            break;
        case 'B':
            diagonal(coord);
            break;
        case 'b':
            diagonal(coord);
            break;
        case 'N':
            knight(coord);
            break;
        case 'n':
            knight(coord);
            break;
        case 'P':
            pawn(coord);
            break;
        case 'p':
            pawn(coord);
            break;
        default :
             break
    }
    for(let i = 0; i < 64; i++) {
        let sq = document.getElementById('s'+i)
            if (map[i+64] === '2'){
                sq.style.backgroundColor = "#FFCF40";
                sq.style.border = '1px solid black';
            }else {
                sq.style.backgroundColor = "";
                sq.style.border = "";
            }
    }
}
function clearMoveMap(){
     for(let i = 64; i < 128; i++) {
            map[i] = '0'
    }
    viewMoveFigure()
}
function addSquares(){
    $('.board').html('');
    for (var coord = 0; coord < 64; coord++)
        $('.board').append(divSquare
            .replace('$coord', coord)
            .replace('$color',
            isBlackSquareAt(coord) ? 'sq_b' : 'sq_w'))
}
function showFigures(figures){
    for (let coord = 0; coord < 64; coord++)
        showFigureAt(coord,figures.charAt(coord))
}
function showFigureAt(coord, figure){
    map[coord] = figure;
    $('#s' + coord).html(divFigure
        .replace('coord', coord)
        .replace('$figure', getChessSymbol(figure)))
}
function getChessSymbol(figure){
    switch (figure){
        case 'K':
            return '<img src="/static/main/img/pieces/white/king.png" class="h-75 w-75 rounded mx-auto d-block" alt="♔" />'
        case 'Q':
            return '<img src="/static/main/img/pieces/white/queen.png" class="h-75 w-75 rounded mx-auto d-block" alt="♕" />'
        case 'R':
            return '<img src="/static/main/img/pieces/white/rook.png" class="h-75 w-75 rounded mx-auto d-block" alt="♖" />'
        case 'B':
            return '<img src="/static/main/img/pieces/white/bishop.png" class="h-75 w-75 rounded mx-auto d-block" alt="♗" />'
        case 'N':
            return '<img src="/static/main/img/pieces/white/knight.png" class="h-75 w-75 rounded mx-auto d-block" alt="♘" />'
        case 'P':
            return '<img src="/static/main/img/pieces/white/pawn.png" class="h-75 w-75 rounded mx-auto d-block" alt="♙" />'
        case 'k':
            return '<img src="/static/main/img/pieces/black/king.png" class="h-75 w-75 rounded mx-auto d-block" alt="♚" />'
        case 'q':
            return '<img src="/static/main/img/pieces/black/queen.png" class="h-75 w-75 rounded mx-auto d-block" alt="♛" />'
        case 'r':
            return '<img src="/static/main/img/pieces/black/rook.png" class="h-75 w-75 rounded mx-auto d-block" alt="♜" />'
        case 'b':
            return '<img src="/static/main/img/pieces/black/bishop.png" class="h-75 w-75 rounded mx-auto d-block"  alt="♝" />'
        case 'n':
            return '<img src="/static/main/img/pieces/black/knight.png" class="h-75 w-75 rounded mx-auto d-block" alt="♞" />'
        case 'p':
            return '<img src="/static/main/img/pieces/black/pawn.png" class="h-75 w-75 rounded mx-auto d-block" alt="♟" />'
        case '1':
            return ''
        default :
            return ''
    }
}
function isBlackSquareAt(coord){
    return(coord % 8 + Math.floor(coord/8)) % 2;
}
function verticalHorizontal(coord){
    map[64 + +coord] = "3"
    let i = coord

    while (availableSquare(i,8,1)){   //+8
        i = +i + 8
        if(thisEnemy(i)){
            break;
        }
    }
    i = coord
    while (availableSquare(i,-8,1)){   //-8
        i -=8
        if(thisEnemy(i)){
            break;
        }
    }
    i = coord
    while (availableSquare(i,1,0)){   //+1
        i = +i + 1
        if(thisEnemy(i)){
            break;
        }
    }
    i = coord
    while (availableSquare(i,-1,0)){   //-1
        i -=1
        if(thisEnemy(i)){
            break;
        }
    }
}
function diagonal(coord){
    map[64 + +coord] = '3'
    let i = coord
    while (availableSquare(i,9,1)){   //+9
        i = +i + 9
        if(thisEnemy(i)){
            break;
        }
    }
    i = coord
    while (availableSquare(i,-9,1)){   //-9
        i = +i - 9
        if(thisEnemy(i)){
            break;
        }
    }
    i = coord
    while (availableSquare(i,7,1)){   //+7
        i = +i + 7
        if(thisEnemy(i)){
            break;
        }
    }
    i = coord
    while (availableSquare(i,-7,1)){   //-7
        i = +i - 7
        if(thisEnemy(i)){
            break;
        }
    }

}
function knight(coord){
    map[64 + +coord] = '3'
    availableSquare(coord, 6, 1)
    availableSquare(coord, 10, 1)
    availableSquare(coord, 15, 2)
    availableSquare(coord, 17, 2)
    availableSquare(coord, -6, 1)
    availableSquare(coord, -10, 1)
    availableSquare(coord, -15, 2)
    availableSquare(coord, -17, 2)

}
function pawn(coord){
    map[64 + +coord] = '3'
    if(!(((map[coord] === 'P' && color === 'white') || (map[coord] === 'p' && color === 'black'))  &&  0 <= coord && coord <= 7)){
        if(!thisEnemy(coord-8)){
            availableSquare(coord,-8,1)
            if (48<= +coord && +coord <= 55 && !thisEnemy(coord-16)){
                availableSquare(coord-8,-8,1)
            }
        }
        if(thisEnemy(coord-7)){
            availableSquare(coord,-7,1)
        }
        if(thisEnemy(coord-9)){
            availableSquare(coord,-9,1)
        }
    }
}
function king(coord){
    map[64 + +coord] = '3'
    availableSquare(coord, 1, 0)
    availableSquare(coord, 7, 1)
    availableSquare(coord, 8, 1)
    availableSquare(coord, 9, 1)
    availableSquare(coord, -1, 0)
    availableSquare(coord, -7, 1)
    availableSquare(coord, -8, 1)
    availableSquare(coord, -9, 1)
}
function thisEnemy(coord){
    return (color === 'white' && map[coord] === map[coord].toLowerCase() && map[coord] !== '1') || (color === 'black' && map[coord] === map[coord].toUpperCase() && map[coord] !== '1');
}
function availableSquare(coord, add, line){
    if ((0 <= +coord + +add && +coord + +add <= 63 && Math.abs((((+coord + +add) - ((+coord+ +add) % 8)) / 8) - ((+coord - (+coord % +8)) / +8)) === line) && (thisEnemy(+coord + +add) || map[+coord + +add] === '1')){
        map[64 + +coord + +add] = '2'
        return true;
    }
    return false;
}
function whichKingLoss(){
    let resultModal = new bootstrap.Modal(document.getElementById('resultModal'), )
    if ((!map.includes('k') && color==="white") || (!map.includes('K') && color==="black")){ //победа
        result_str.innerHTML=`Поздравляем, вы победили! Вражеский король повержен. Сыграйте снова и закрепите свой успех.`;
        resultModal.show()
        return true
    } else if ((!map.includes('K') && color==="white") || (!map.includes('k') && color==="black")){
        result_str.innerHTML=`К сожалению вы потерпели поражение и ваш король пал. Вы проиграли! Попробуйте заново и победите!`;
        resultModal.show()
        return true
    }else {
        return false
    }
}
function changePawn(coord){
    let selectFigureModal = new bootstrap.Modal(document.getElementById('selectFigureModal'))
    selectFigureModal.show()
    let select_bishop = document.getElementById('select_bishop');
    let select_rook = document.getElementById('select_rook');
    let select_queen = document.getElementById('select_queen');
    let select_knight = document.getElementById('select_knight');
     const selectKnightListener = function (event) {
        if (color === "white"){
            map[coord] = "N"
        }else
            map[coord] = "n"
        showFigures(map.join(""));
        updateFigures();
        selectFigureModal.hide()
    };

     const selectBishopListener = function (event) {
        if (color === "white"){
            map[coord] = "B"
        }else
            map[coord] = "b"
        showFigures(map.join(""));
        updateFigures();
        selectFigureModal.hide()
    };
     const selectRookListener = function (event) {
        if (color === "white"){
            map[coord] = "R"
        }else
            map[coord] = "r"
        showFigures(map.join(""));
        updateFigures();
        selectFigureModal.hide()
    };
     const selectQueenListener = function (event) {
        if (color === "white"){
            map[coord] = "Q"
        }else
            map[coord] = "q"
        showFigures(map.join(""));
        updateFigures();
        selectFigureModal.hide()
    };

    select_knight.addEventListener('click', selectKnightListener);
    select_knight.removeEventListener('click', selectKnightListener);

    select_bishop.addEventListener('click', selectBishopListener);
    select_bishop.removeEventListener('click', selectBishopListener);

    select_rook.addEventListener('click', selectRookListener);
    select_rook.removeEventListener('click', selectRookListener);

    select_queen.addEventListener('click', selectQueenListener);
    select_rook.removeEventListener('click', selectQueenListener);

}
function buttonSurrender(){
    let resultModal = new bootstrap.Modal(document.getElementById('resultModal'), )
    let admit_defeat_button = document.getElementById('admit-defeat-button');
    admit_defeat_button.addEventListener('click', () => {
        result_str.innerHTML=`К сожалению вы сдались и ваш король пал. \n Вы проиграли!\nПопробуйте заново и попытайтесь победить!`;
        resultModal.show()
    });
}
function onAjaxSuccess(data) {
        map = data.split('');
        if(color==='black'){
            reverseMap();
        }
        whichKingLoss();
        showFigures(map.join(""));
        updateFigures();
        clearMoveMap();
}
function reverseMap(){
    map = [...map.slice(0,64).reverse(),  ...map.slice(64,128)]
}
function res(){
   var width = $('.board').width();
	 $('.board').height(width);
} res();

