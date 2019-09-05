var board,
  game = new Chess();

var makeRandomMove = function() {
  var possibleMoves = game.moves();

  // exit if the game is over
  if (game.game_over() === true ||
    game.in_draw() === true ||
    possibleMoves.length === 0) return;

  var randomIndex = Math.floor(Math.random() * possibleMoves.length);
  game.move(possibleMoves[randomIndex]);
  board.position(game.fen());

  window.setTimeout(makeRandomMove, 500);
};

var playPetrovMove = function(i, petrovList) {
  var possibleMoves = game.moves();

  // exit if the game is over
  if (game.game_over() === true ||
    game.in_draw() === true ||
    possibleMoves.length === 0) return;

  game.move(petrovList[i])

  board.position(game.fen());

  window.setTimeout(function() {
    playPetrovMove(i+=1, petrovList)
  }, 500);
};


board = ChessBoard('board', 'start');

window.setTimeout(function() {
  playPetrovMove(0, immortalArray)
}, 500);

immortalArray = ['e4', 'e5', 'f4', 'exf4', 'Bc4', 'Qh4+', 'Kf1', 'b5', 'Bxb5', 'Nf6', 'Nf3', 'Qh6', 'd3', 'Nh5', 'Nh4',
                 'Qg5', 'Nf5', 'c6', 'g4', 'Nf6', 'Rg1', 'cxb5', 'h4', 'Qg6', 'h5', 'Qg5', 'Qf3', 'Ng8', 'Bxf4', 'Qf6',
                 'Nc3', 'Bc5', 'Nd5', 'Qxb2', 'Bd6', 'Bxg1', 'e5', 'Qxa1', 'Ke2', 'Na6', 'Nxg7', 'Kd8', 'Qf6', 'Nxf6', 'Be7']

petrovArray = ['e4', 'e5', 'Nf3', 'Nf6']

// latest, best version of this idea would be to randomly pick a game to display 
// e.x. "You're white" - plays immortal game
// or "You're black" - plays a deep line of the Petrov defense
// or "You're white" - plays a game I actually played as white
//
// a harder version would be to play a game of "me (what I program)" vs. random moves
