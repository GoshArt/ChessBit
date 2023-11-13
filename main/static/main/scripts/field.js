let divSquare = '<div id="s$coord" class="square $color"></div>';
let divFigure = '<div id="f$coord" class="figure">$figure</div>';
let map;
let df;
let dsq;
let botColor = document.getElementById("botColor").value;
let color;
let turn = 'white';
fieldResolution();
$(function () {
    start()
    pressSquare();
});
$(window).resize(function () {
    fieldResolution();
});

function start() {
    map = document.getElementById("startMap").value.split('');
    addSquares();
    showFigures(map.join(""));
    if (color === "black") {
        $.post(
            "/field",
            {
                type: "firstMove"
            },
            changeMap,
        );
    }
    viewModalGaveUp();
    let resultModal = new bootstrap.Modal(document.getElementById('resultModal'))
    let admit_defeat_button = document.getElementById('admit-defeat-button');
    admit_defeat_button.addEventListener('click', () => {
        result_str.innerHTML = `К сожалению вы сдались и ваш король пал. \n Вы проиграли!\nПопробуйте заново и попытайтесь победить!`;
        resultModal.show();
        buttonSurrender();
    });
} //первичный запуск
function pressSquare() {
    dsq = document.querySelectorAll("div.square");
    dsq.forEach((event) => {
        event.addEventListener('click', () => {
            let coord = getCoordinates(event.id.slice(1))
            $.post(
                "/field",
                {
                    y: coord[1],
                    x: coord[0],
                    type: "pressSquare"
                },
                changeMap,
            );
        });
    });
} // обработка нажатие на ячейку
function viewMoveFigure(map) { //выводит на поле отображение ходов фигур
    for (let i = 0; i < 64; i++) {
        let sq = document.getElementById('s' + i)
        if (map[i + 64] === '2') {
            sq.style.backgroundColor = "#FFCF40";
            sq.style.border = '1px solid black';
        } else {
            sq.style.backgroundColor = "";
            sq.style.border = "";
        }
    }
} // отображение возможных ходов
function clearMoveMap() {
    for (let i = 64; i < 128; i++) {
        map[i] = '0'
    }
    viewMoveFigure(map)
} //очистка поля от ходов
function addSquares() {
    $('.board').html('');
    for (var coord = 0; coord < 64; coord++)
        $('.board').append(divSquare
            .replace('$coord', coord)
            .replace('$color',
                isBlackSquareAt(coord) ? 'sq_b' : 'sq_w'))
} //добавление ячеек поля
function showFigures(figures) {
    for (let coord = 0; coord < 64; coord++)
        showFigureAt(coord, figures.charAt(coord))
} //вывод фигур
function showFigureAt(coord, figure) {
    map[coord] = figure;
    $('#s' + coord).html(divFigure
        .replace('coord', coord)
        .replace('$figure', getChessSymbol(figure)))
} //вывод фигуры на координате
function getChessSymbol(figure) {
    switch (figure) {
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
} //вывод конкретного изображения
function isBlackSquareAt(coord) {
    return (coord % 8 + Math.floor(coord / 8)) % 2;
} //создание поля
function whichKingLoss(data) {
    const response = JSON.parse(data);
    let resultModal = new bootstrap.Modal(document.getElementById('resultModal'),)
    if (response.res === "Win") { //победа
        result_str.innerHTML = `Поздравляем, вы победили! Вражеский король повержен. Сыграйте снова и закрепите свой успех.`;
        resultModal.show()
    } else if (response.res === "Lose") {
        result_str.innerHTML = `К сожалению вы потерпели поражение и ваш король пал. Вы проиграли! Попробуйте заново и победите!`;
        resultModal.show()
    }
} //переделать для вывода информации
function changePawn(coord) {
    let selectFigureModal = new bootstrap.Modal(document.getElementById('selectFigureModal'))
    selectFigureModal.show();

    let select_bishop = document.getElementById('select_bishop');
    let select_rook = document.getElementById('select_rook');
    let select_queen = document.getElementById('select_queen');
    let select_knight = document.getElementById('select_knight');
    const selectKnightListener = function (event) {
        if (color === "white") {
            sendPawnChange("N")
        } else
            sendPawnChange("n")
        selectFigureModal.hide();
    };
    const selectBishopListener = function (event) {
        if (color === "white") {
            sendPawnChange("B")
        } else
            sendPawnChange("b")
        selectFigureModal.hide()
    };
    const selectRookListener = function (event) {
        if (color === "white") {
            sendPawnChange("R")
        } else
            sendPawnChange("r")
        selectFigureModal.hide()
    };
    const selectQueenListener = function (event) {
        if (color === "white") {
            sendPawnChange("Q")
        } else
            sendPawnChange("q")
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
} //Выбор фигуры для изменения
function buttonSurrender() {
    $.post(
        "/field",
        {
            type: "gaveUp"
        },
        viewModalGaveUp,
    );
} //Вызов функции сдачи
function changeMap(data) {
    const response = JSON.parse(data);
    map = response.map;
    console.log(response)
    console.log(response.turnType === "Selected")
    console.log(getVisualMap(map))
    if (response.turnType === "Selected" || response.turnType === "NoSelected") {
        viewMoveFigure(getVisualMap(map))
    } else if (response.turnType === "Correct" || response.turnType === "InСorrect") {1
        showFigures(getVisualMap(map))
        clearMoveMap();
    }
    if (response.turnType === "Correct"){
        turn = response.turnColor;
    }

} //Обработка запросов на изменение карты, должно работать
function getVisualMap(field) {
    if(color === "black"){
        return [...field.slice(0, 64).reverse(), ...field.slice(64, 128).reverse()]
    }else {
        return field
    }
} //визуально разворачивает карту если надо
function fieldResolution() {
    var width = $('.board').width();
    $('.board').height(width);
} //Изменяет разрешение поля
function getCoordinates(coord) {
    let x = coord % 8;
    let y = (coord - (coord % 8)) / 8;
    return [x, y]
} //возвращает координаты клетки поля
function sendPawnChange(figure) {
    $.post(
        "/field",
        {
            figure: figure,
            type: "changePawn"
        },
        changeMap,
    );
}
function pawnChangeRequest(data) {
    //тут должна быть функция
} //дописать
function viewModalGaveUp() {
}