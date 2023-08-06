data_type = 2
data_list = ['annual', 'biennial', 'perennial']
data_list2 = ['🥕', '🍅', '🍅', '🥕', '🍆', '🍅', '🍅', '🍅', '🥕', '🍅']
data_list_dict = [
        {'icon': '🍓', 'name': 'Strawberry', 'duration': 'perennial'},
        {'icon': '🥕', 'name': 'Carrot', 'duration': 'biennial'},
        {'icon': '🍆', 'name': 'Eggplant', 'duration': 'perennial'},
        {'icon': '🍅', 'name': 'Tomato', 'duration': 'annual'},
        {'icon': '🥔', 'name': 'Potato', 'duration': 'unknown'},
    ]
data_list_dict2 = [
          {
              'icon': '🍓', 'name': 'Strawberry', 'duration': 2
          },
          {
              'icon': '🥕', 'name': 'Carrot', 'duration': 1
          },
          {
              'icon': '🍆', 'name': 'Eggplant', 'duration': 2
          },
          {
              'icon': '🍅', 'name': 'Tomato', 'duration': 0
          },
          {
              'icon': '🥔', 'name': 'Potato', 'duration': -1
          },
      ]
data_list_dict3 = [
          {'name': 'Strawberry', 'season': 1585699200}, # April, 2020
          {'name': 'Carrot', 'season': 1590969600},     # June, 2020
          {'name': 'Artichoke', 'season': 1583020800},  # March, 2020
          {'name': 'Tomato', 'season': 1588291200},     # May, 2020
          {'name': 'Potato', 'season': 1598918400},     # September, 2020
      ]
data_list_str = ['🍓Strawberry 🥕Carrot 🍆Eggplant', '🍅Tomato 🥔Potato']
data_list_str2 = ['🍓Strawberry,🥕Carrot,🍆Eggplant', '🍅Tomato,🥔Potato', '🍓Strawberry,🥕Carrot,🍆Eggplant']
data_list_str3 = ['   🍓Strawberry   \n', '   🥕Carrot   \n', '   🍆Eggplant   \n', '   🍅Tomato   \n', '   #🥔Potato   \n']
data_list_str4 = [
          '🍓, Strawberry, perennial',
          '🥕, Carrot, biennial ignoring trailing words',
          '🍆, Eggplant, perennial',
          '🍅, Tomato, annual',
          '🥔, Potato, perennial',
          '# 🍌, invalid, format',
          'invalid, 🍉, format',
      ]
data_list_str5 = [
          '# 🍓, Strawberry, perennial',
          '# 🥕, Carrot, biennial ignoring trailing words',
          '# 🍆, Eggplant, perennial - 🍌, Banana, perennial',
          '# 🍅, Tomato, annual - 🍉, Watermelon, annual',
          '# 🥔, Potato, perennial',
      ]
data_list_list = [['🍓Strawberry', '🥕Carrot', '🍆Eggplant'], ['🍅Tomato', '🥔Potato']]
data_list_tuple = [('🍓', 'Strawberry'), ('🥕', 'Carrot'), ('🍆', 'Eggplant'), ('🍅', 'Tomato'),
                   ('🥔', 'Potato'), (None, 'Invalid')]
data_list_tuple2 = [(0, 'annual'), (1, 'biennial'), (2, 'perennial')]
data_list_tuple3 = [
      ('Apple', '🍎'),
      ('Apple', '🍏'),
      ('Eggplant', '🍆'),
      ('Tomato', '🍅'),
  ]
data_list_tuple4 = [
      ('Apple', 'perennial'),
      ('Carrot', 'biennial'),
      ('Tomato', 'perennial'),
      ('Tomato', 'annual'),
  ]
data_list_set = [
          {'🍓', '🥕', '🍌', '🍅', '🌶️'},
          {'🍇', '🥕', '🥝', '🍅', '🥔'},
          {'🍉', '🥕', '🍆', '🍅', '🍍'},
          {'🥑', '🥕', '🌽', '🍅', '🥥'},
      ]


