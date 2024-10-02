The challenge.py file looks for player dictionaries here.
This is the only way to set the minimaxer scorer parameters
for challenge.py.

A pdict file may contain the following parameters. The file 
must be a valid JSON string. Key/value pairs with default
values need not be included.

Comments are not allowed; include only text below.
{
      "algorithm": "minimaxer",
      "ai_active": false,
      "difficulty": 1,
      "ai_params": {
         "mcts_bias": [300, 200, 100, 100],
         "mcts_nodes": [100, 300, 500, 800],
         "mcts_pouts": [1, 1, 1, 1],
         "mm_depth": [1, 1, 3, 5]
      },
      "scorer": {
         "stores_m": 4,
         "access_m": 0,
         "seeds_m": 0,
         "empties_m": 0,
         "child_cnt_m": 0,
         "evens_m": 0,
         "repeat_turn": 0,
         "easy_rand": 0
}
