def print_tokens_table(tokens_table):
    print("========= Tokens Table =========")
    t = PrettyTable(['TOKEN', 'VALUE', 'LINE', 'COLUMN'])
    for entrie in tokens_table:
        t.add_row([entrie['token'], entrie['value'],
                  entrie['line'], entrie['column']])
    print(t)
    print()
    print()


def print_token_list(token_list):
    print("========= Token List =========")
    for tok in token_list:
        print(tok)
    print()
    print()


def print_symbols_table(symbols_table):
  print("========= Symbols Table =========")
  t = PrettyTable(['NAME', 'TYPE', 'DECLARED', 'REFERENCED'])
  for key in symbols_table:
    symbol = symbols_table[key]
    t.add_row([symbol['name'], symbol['type'],
				symbol['declared_line'], symbol['referenced_lines']])
  print(t)
  print()
  print()