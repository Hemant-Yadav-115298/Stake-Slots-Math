from game_executables import GameExecutables
from src.calculations.statistics import get_random_outcome


class GameStateOverride(GameExecutables):
    """
    This class is is used to override or extend universal state.py functions.
    """

    def reset_book(self):
        super().reset_book()

    def assign_special_sym_function(self):
        # We don't have any special symbol functions (like multipliers) for now
        self.special_symbol_functions = {}

    # You can add custom wild behaviors here if needed, but for now it's standard.
    def check_repeat(self):
        super().check_repeat()
        if self.repeat is False:
            # Check if we need to repeat based on distribution criteria (e.g. wincap, zero win)
            win_criteria = self.get_current_betmode_distributions().get_win_criteria()
            if win_criteria is not None and self.final_win != win_criteria:
                self.repeat = True
                return
            if win_criteria is None and self.final_win == 0:
                self.repeat = True
                return
