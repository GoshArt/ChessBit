let divSquare = '<div id="s$coord" class="square $color"></div>';
let divFigure = '<div id="f$coord" class="figure">$figure</div>';
let map;
let df;
let dsq;
let color = 'white';

$(function (){
    start()

    dsq.forEach((event) => {
        event.addEventListener('click', () => {
            let coord = -1
            for(let i = 1; i < 64; i++) {
                if('3' === map[+i+64]){
                    coord = i
                }
            }
            if(+map[+event.id.slice(1) + +64] === 2){
                map[event.id.slice(1)] = map[coord]
                map[coord] = 1;
                clearMoveMap();
                showFigures(map.join(""));
                updateFigures();

            } else if(+map[+event.id.slice(1) + +64] === 0){
                clearMoveMap();
            }
        });
    });
});
function updateFigures(){
    df = document.querySelectorAll("div.figure");
    df.forEach((event) => {
        event.addEventListener('click', () => {
            let coord = -1
            for(let i = 1; i < 64; i++) {
                if('3' === map[+i+64]){
                    coord = i
                }
            }
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
    addSquares();
    showFigures(map.join(""))
    dsq = document.querySelectorAll("div.square");
    updateFigures();
}


function moveFigure(frCoord, toCoord){
    console.log('move from ' + frCoord + ' to ' + toCoord)
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
            return '♔'
        case 'Q':
            return '♕'
        case 'R':
            return '♖'
        case 'B':
            return '♗'
        case 'N':
            return '♘'
        case 'P':
            return '♙'
        case 'k':
            return '♚'
        case 'q':
            return '♛'
        case 'r':
            return '♜'
        case 'b':
            return '♝'
        case 'n':
            return '♞'
        case 'p':
            return '♟'
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
    availableSquare(coord,-8,1)
    if (48<= +coord && +coord <= 55){
        console.log("A")
        availableSquare(coord-8,-8,1)
    }
    if(thisEnemy(coord-7)){
        availableSquare(coord,-7,1)
    }
    if(thisEnemy(coord-9)){
        availableSquare(coord,-9,1)
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