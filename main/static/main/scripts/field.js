let divSquare = '<div id="s$coord" class="square $color"></div>';
let divFigure = '<div id="f$coord" class="figure">$figure</div>';
let map;
let df;
let dsq;

$(function (){
    start()

    dsq.forEach((event) => {
        event.addEventListener('click', () => {
            console.log(event)
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
            console.log(event)
            let coord = -1
            for(let i = 1; i < 64; i++) {
                if('3' === map[+i+64]){
                    coord = i
                }
            }
            if(coord < 0){
                viewMoveFigure(event.id.slice(2));
            }
        });
    });
}
function start(){
    map = new Array(128)
    map = "rnbqkbnrpppppppp111111111111n1111111111111111111PPPPPPPPRNBQKBNR0000000000000000000000000000000000000000000000000000000000000000".split('');
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
        // case 'K' || 'k':
        //     return '♔'
        case 'Q':
            vertical(coord);
            horizontal(coord);
            diagonal(coord);
            break;
        case 'q':
            vertical(coord);
            horizontal(coord);
            diagonal(coord);
            break;
        case 'R':
            vertical(coord);
            horizontal(coord);
            break;
        case 'r':
            vertical(coord);
            horizontal(coord);
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
        // case 'P' || 'p':
        //     return '♙'
        // case '1':
        //     return ''
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

function vertical(coord){
    let r = coord % 8
    for (let i = 0; i < 8; i++) {
        map[64+r+i*8] = "2"
    }
    map[64 + +coord] = "3"
}
function horizontal(coord){
    let r = (coord - (coord % 8)) / 8
    for (let i = 0; i < 8; i++) {
        map[64+r*8+i] = "2"
    }
    map[64 + +coord] = "3"
}
function diagonal(coord){
    map[64 + +coord] = '3'
    let i = +coord + 9
    while (i <= 63 && Math.abs(((i - (i % 8)) / 8) - (((i-9) - ((i-9) % 8)) / 8)) === 1){   //+9
        map[64 + +i] = '2'
        i += 9
    }
    i = coord-9
    while (0 <= i && Math.abs(((i - (i % 8)) / 8) - (((i+9) - ((i+9) % 8)) / 8)) === 1){   //-9
        map[64 + +i] = '2'
        i -= 9
    }
    i = +coord + 7
    while (i <= 63 && Math.abs(((i - (i % 8)) / 8) - (((i-7) - ((i-7) % 8)) / 8)) === 1){   //+7
        map[64 + +i] = '2'
        i += 7
    }
    i = coord - 7
    while (0 <= i && Math.abs(((i - (i % 8)) / 8) - (((i+7) - ((i+7) % 8)) / 8)) === 1){   //-7
        map[64 + +i] = '2'
        i -= 7
    }

}
function knight(coord){
    map[64 + +coord] = '3'
    let i = +coord + 6
    if (i <= 63 && Math.abs(((i - (i % 8)) / 8) - (((i-6) - ((i-6) % 8)) / 8)) === 1){   //+6
        map[64 + +i] = '2'
    }
    i = +coord+10
    if (i <= 63 && Math.abs(((i - (i % 8)) / 8) - (((i-10) - ((i-10) % 8)) / 8)) === 1){   //+10
        map[64 + +i] = '2'
    }
    i = +coord+15
    if (i <= 63 && Math.abs(((i - (i % 8)) / 8) - (((i-15) - ((i-15) % 8)) / 8)) === 2){   //+15
        map[64 + +i] = '2'
    }
    i = +coord+17
    if (i <= 63 && Math.abs(((i - (i % 8)) / 8) - (((i-17) - ((i-17) % 8)) / 8)) === 2){   //+17
        map[64 + +i] = '2'
    }
    i = coord - 6
    if (0 <= i && Math.abs(((i - (i % 8)) / 8) - (((i+6) - ((i+6) % 8)) / 8)) === 1){   //-6
        map[64 + +i] = '2'
    }
    i = coord - 10
    if (0 <= i && Math.abs(((i - (i % 8)) / 8) - (((i+10) - ((i+10) % 8)) / 8)) === 1){   //-10
        map[64 + +i] = '2'
    }
    i = coord - 15
    if (0 <= i && Math.abs(((i - (i % 8)) / 8) - (((i+15) - ((i+15) % 8)) / 8)) === 2){   //-16
        map[64 + +i] = '2'
    }
    i = coord - 17
    if (0 <= i && Math.abs(((i - (i % 8)) / 8) - (((i+17) - ((i+17) % 8)) / 8)) === 2){   //-17
        map[64 + +i] = '2'
    }

}
