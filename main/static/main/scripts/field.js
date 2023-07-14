var divSquare = '<div id="s$coord" class="square $color"></div>';
var divFigure = '<div id="f$coord" class="figure">$figure</div>';
var map;

$(function (){
    start()
});

function start(){
    map = new Array(64)
    addSquares();
    showFigures("rnbqkbnrpppppppp11111111111111111111111111111111PPPPPPPPRNBQKBNR ")
}

function setDraggable(){
    $('.figure').draggable();
}
function setDroppable(){
    $('.square').droppable({
        drop: function (event, ui) {
            var frCoord = ui.draggable.attr('id').substring(1);
            var toCoord = this.id.substring(1);
            moveFigure(frCoord, toCoord);
        }
    });
}
function moveFigure(frCoord, toCoord){
    console.log('move from ' + frCoord + ' to ' + toCoord)
    figure = map[frCoord];
    showFigureAt(frCoord, "1")
    showFigureAt(toCoord, figure)
}
function addSquares(){
    $('.board').html('');
    for (var coord = 0; coord < 64; coord++)
        $('.board').append(divSquare
            .replace('$coord', coord)
            .replace('$color',
            isBlackSquareAt(coord) ? 'sq_b' : 'sq_w'))
    setDroppable();
}
function showFigures(figures){
    for (var coord = 0; coord < 64; coord++)
        showFigureAt(coord,figures.charAt(coord))
}
function showFigureAt(coord,figure){
    map[coord] = figure;
    $('#s' + coord).html(divFigure
        .replace('coord', coord)
        .replace('$figure', getChessSymbol(figure)))
    setDraggable()
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