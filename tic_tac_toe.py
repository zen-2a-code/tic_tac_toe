class Player:
    """
    Simple player class for use in games like programs. 

    Arguments:

        draws: (int) Total draws between players
        name: (str) The name of the player

    Methods:

        set_player_char: Sets the character that will be used from the
            player
        get_user_input: Get the row and column where the character to be
            placed in a field instance. The result will always be list
            from two `int`
        print_players_results: prints the result of the players
        add_win: Adds win to the winner, and lose to the loser.
    """
    draws = 0

    def __init__(self, name: str) -> None:
        self.name = name
        self._char = ""
        self._wins = 0
        self._loses = 0

    def set_player_char(self, the_other_player=None):
        """
        Set the player char

        Allowed chars are single length strings (char) and must not be
        already used by the other player.
        If the_other_player argument is not specified the selected char
        must only oblige by len == 1 rule.
        :param the_other_player: (Optional) It is to be used to check for
            already chosen char. Recommended use for the second player
        """
        char = ""
        while len(char) != 1:
            char = input("Please enter your character (must be only one): ")
            if the_other_player:
                print("This character has already been selected by the other player")
                if char == the_other_player._char:
                    char = ""
        self._char = char

    @staticmethod
    def get_user_input(player) -> list:
        """Get the needed user_input for placement on the field

        To input to be successful does many checks for a valid input, also
        call itself if wrong input is entered until valid input is given.
        """
        user_input = input("{0.name} please enter row and column separated "
                           "with space: ".format(player))
        if len(user_input) > 3:
            print("The input is too long, please try again!")
            return Player.get_user_input(player)
        else:
            try:
                row, column = user_input.split(" ")
            except ValueError:
                print("Please use separator for the values")
                return Player.get_user_input(player)
            try:
                row, column = int(row), int(column)
                if row > 3 or column > 3:
                    print("Please enter numbers between 1 and 3 (inclusive)")
                    return Player.get_user_input(player)
            except ValueError:
                print("Please enter numbers.")
                return Player.get_user_input(player)

            return [row, column]

    @staticmethod
    def print_players_results(player_1, player_2):
        """Takes two Player objects and prints info about their stats"""
        print("\t{0.name:<8} Wins: {0._wins}, Loses: {0._loses}".format(player_1))
        print("\t{0.name:<8} Wins: {0._wins}, Loses: {0._loses} ".format(player_2))
        print("\tDraws: {0}".format(Player.draws))

    @staticmethod
    def add_win(winner, loser):
        """Adds win to the winner and lose to the loser

        in addition, of that calls print_player_result function
        """
        print("{0.name} WINS!".format(winner))
        winner._wins += 1
        loser._loses += 1
        Player.print_players_results(winner, loser)


class Field:
    """
    Creates a few instance

    This class in responsible for creating a play field for a game of
    tic-tac-toe, all task for displaying the field
    are delegated to the class.

    Methods:
         create_field(): - creates the play field, the first time must be
            called manually.
        check_win(): - Checks for occurrence of win
        check_draw() - Check for a draw.
        add_move() - adds the turn of the player on the play field.
        new_game() - clears the field and prints new playing field

    """

    def __init__(self):
        self._field = [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]

    def create_field(self):
        for row in self._field:
            for entry in row:
                if entry == "-":
                    print("[ ]", end="")
                else:
                    print(f"[{entry}]", end="")
            print()

    def check_draw(self) -> bool:
        for row in self._field:
            for entry in row:
                if entry == "-":
                    return False
        else:
            return True

    def check_win(self, player) -> bool:
        """Check for reached combination in any possible combination

        if the combination is confirmed returns True
        and stops executing ,otherwise continues to the next
        possible type of combination.

        :return: bool True if there is combination achieved , False if
            there is not.
        """
        if self._check_rows(player):
            return True
        elif self._check_column(player):
            return True
        elif self._check_left_diagonal(player):
            return True
        elif self._check_right_diagonal(player):
            return True
        else:
            return False

    def _check_rows(self, player) -> bool:
        for row in self._field:
            for entry in row:
                if entry != player._char:
                    break
            else:
                return True  # if the whole row contains player.char
        return False

    def _check_column(self, player) -> bool:

        for column in range(3):
            for row in range(3):
                entry = self._field[row][column]
                if entry != player._char:
                    break
            else:
                return True

        return False

    def _check_left_diagonal(self, player):
        return self._check_diagonal(player)

    def _check_right_diagonal(self, player):
        return self._check_diagonal(player, left=False)

    def _check_diagonal(self, player, left=True) -> bool:
        """Check for combinations for the diagonals

        if the check_diagonal is called by _check_left_diagonal uses
        normal range from 0 to 3 (exclusive), otherwise uses reverse
        range from 2 to 0 (inclusive)
        """
        if left:
            arange = range(3)
        else:
            arange = range(2, -1, -1)

        j = 0
        for index in arange:
            entry = self._field[index][j]
            if entry != player._char:
                return False
            j += 1
        else:
            return True

    def add_move(self, row: int, column: int, player):
        """
        Add move of the player to the field

        If that entry in the field is already occupied prints message
            and calls itself again .
        """
        row -= 1
        column -= 1

        if self._field[row][column] != "-":
            print("The field is not empty. Please try again!")
            row, column = player.get_user_input(player)
            self.add_move(row, column, player)
        else:
            self._field[row][column] = player._char
            self._add_space()
            self.create_field()

    def new_game(self):
        """Bring the field to the new game state and prints it."""
        self._field = [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]
        self._add_space()
        self.create_field()

    @staticmethod
    def _add_space():
        for i in range(2):
            print("=" * 15)


def another_game() -> bool:
    """
    :return: User choice if he wants another round - True/False
    """
    stop_game = input("Do you want to play one more round? n = `no`"
                      " press any other key to continue ").casefold()
    if stop_game == "n":
        return False
    else:
        return True


def game_turn(row: int, column: int, player: Player, play_field: Field,
              other_player: Player) -> bool:
    """
    The main function responsible for the game of tic-tac-toe

    :param row: The row for placement of figure
    :param column: The column to place a figure
    :param player: Instance of Player object that char will be used to
        be placed on the field.
    :param play_field: Instance of Field object that is responsible for
        playing field and the data in it.
    :param other_player: Instance of the Player object that is needed
        to preform a checks.
    :return: bool:  True if the main loop has to continue,
        False if the game ends
    """
    play_field.add_move(row, column, player)
    if play_field.check_win(player):
        Player.add_win(player, other_player)
        new_game = another_game()
        if new_game:
            play_field.new_game()
            return True
        else:
            return False

    elif play_field.check_draw():
        Player.draws += 1
        Player.print_players_results(player, other_player)
        new_game = another_game()
        if new_game:
            play_field.new_game()
            return True
        else:
            return False
    else:
        return True


if __name__ == "__main__":

    player1 = Player(input("Player 1 please enter your name: "))
    player1.set_player_char()

    player2 = Player(input("Player 2 please enter your name: "))
    player2.set_player_char(player1)

    field = Field()
    field.create_field()
    play_game = True

    while play_game:
        player1_turn = player1.get_user_input(player1)
        player1_row, player1_column = player1_turn
        play_game = game_turn(player1_row, player1_column,
                              player1, field, player2)

        if not play_game:
            continue

        player2_turn = player2.get_user_input(player2)
        player2_row, player2_column = player2_turn
        play_game = game_turn(player2_row, player2_column,
                              player2, field, player1)
