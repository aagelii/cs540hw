import pokemon_stats as ps

pokemons = ps.load_data("Pokemon.csv")
pokemons_x_y = []
for row in pokemons:
    pokemons_x_y.append(ps.calculate_x_y(row))
HAC = ps.hac(pokemons_x_y)
print(HAC)
# dataset = ps.random_x_y(20)
# ps.imshow_hac(pokemons_x_y)
