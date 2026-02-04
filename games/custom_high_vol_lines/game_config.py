"""Game-specific configuration file, inherits from src/config/config.py"""

import os
from src.config.config import Config
from src.config.distributions import Distribution
from src.config.betmode import BetMode


class GameConfig(Config):

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self.game_id = "custom_high_vol_lines"
        self.provider_number = 0
        self.working_name = "Custom High Volatility 10 Lines"
        self.wincap = 500000.0
        self.win_type = "lines"
        self.rtp = 0.9600
        self.construct_paths()

        # Game Dimensions
        self.num_reels = 5
        self.num_rows = [3] * self.num_reels
        
        # Paytable: All values are integers >= 10.
        self.paytable = {
            (5, "W"): 5000,
            (4, "W"): 400,
            (3, "W"): 100,
            (5, "H1"): 800,
            (4, "H1"): 200,
            (3, "H1"): 50,
            (5, "H2"): 400,
            (4, "H2"): 100,
            (3, "H2"): 20,
            (5, "H3"): 200,
            (4, "H3"): 50,
            (3, "H3"): 10,
            (5, "H4"): 100,
            (4, "H4"): 30,
            (3, "H4"): 10,
            (5, "L1"): 40,
            (4, "L1"): 10,
            (3, "L1"): 10,
            (5, "L2"): 30,
            (4, "L2"): 10,
            (3, "L2"): 10,
            (5, "L3"): 20,
            (4, "L3"): 10,
            (3, "L3"): 10,
            (5, "L4"): 10,
            (4, "L4"): 10,
            (3, "L4"): 10,
            (5, "L5"): 10,
            (4, "L5"): 10,
            (3, "L5"): 10,
        }

        # 10 Lines
        self.paylines = {
            1: [1, 1, 1, 1, 1],
            2: [0, 0, 0, 0, 0],
            3: [2, 2, 2, 2, 2],
            4: [0, 1, 2, 1, 0],
            5: [2, 1, 0, 1, 2],
            6: [0, 0, 1, 2, 2],
            7: [2, 2, 1, 0, 0],
            8: [1, 0, 1, 2, 1],
            9: [1, 2, 1, 0, 1],
            10: [0, 1, 0, 1, 0],
        }

        self.include_padding = True
        self.special_symbols = {"wild": ["W"], "scatter": ["S"]}

        self.freespin_triggers = {
            self.basegame_type: {3: 10, 4: 15, 5: 20, 6: 20, 7: 20, 8: 20, 9: 20, 10: 20, 11: 20, 12: 20, 13: 20, 14: 20, 15: 20},
            self.freegame_type: {3: 5, 4: 10, 5: 15, 6: 15, 7: 15, 8: 15, 9: 15, 10: 15, 11: 15, 12: 15, 13: 15, 14: 15, 15: 15},
        }
        self.anticipation_triggers = {
            self.basegame_type: 2,
            self.freegame_type: 2,
        }
        
        reels = {"BR0": "BR0.csv", "FR0": "FR0.csv", "WCAP": "WCAP.csv"}
        self.reels = {}
        for r, f in reels.items():
            self.reels[r] = self.read_reels_csv(os.path.join(self.reels_path, f))

        self.padding_reels[self.basegame_type] = self.reels["BR0"]
        self.padding_reels[self.freegame_type] = self.reels["FR0"]
        self.padding_symbol_values = {"W": {}}

        freegame_condition = {
            "reel_weights": {
                self.basegame_type: {"BR0": 1},
                self.freegame_type: {"FR0": 1},
            },
            "scatter_triggers": {3: 50, 4: 20, 5: 5},
            "force_wincap": False,
            "force_freegame": True,
        }

        basegame_condition = {
            "reel_weights": {self.basegame_type: {"BR0": 1}},
            "force_wincap": False,
            "force_freegame": False,
        }

        wincap_condition = {
            "reel_weights": {
                self.basegame_type: {"BR0": 1, "WCAP": 20},
                self.freegame_type: {"FR0": 1, "WCAP": 20},
            },
            "scatter_triggers": {4: 1, 5: 2},
            "force_wincap": True,
            "force_freegame": True,
        }

        zerowin_condition = {
            "reel_weights": {self.basegame_type: {"BR0": 1}},
            "force_wincap": False,
            "force_freegame": False,
        }

        mode_maxwins = {"base": 500000, "bonus": 500000}
        
        self.bet_modes = [
            BetMode(
                name="base",
                cost=100.0,
                rtp=self.rtp,
                max_win=mode_maxwins["base"],
                auto_close_disabled=False,
                is_feature=True,
                is_buybonus=False,
                distributions=[
                    Distribution(
                        criteria="wincap",
                        quota=0.000002,
                        win_criteria=mode_maxwins["base"],
                        conditions=wincap_condition,
                    ),
                    Distribution(criteria="freegame", quota=0.10, conditions=freegame_condition),
                    Distribution(criteria="0", quota=0.40, win_criteria=0.0, conditions=zerowin_condition),
                    Distribution(criteria="basegame", quota=0.499998, conditions=basegame_condition),
                ],
            )
        ]
