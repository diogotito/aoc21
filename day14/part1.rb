all_lines = File.readlines("input.txt", chomp: true)           # Extrai linhas sem \n
polymer = all_lines[0].chars                                   # 1ª linha para Array de caracteres
rules = Hash[all_lines[2..].map { |rule| rule.split " -> " }]  # ["WC -> 🚾", ...] => {"WC" => 🚾, ...}

10.times do
    polymer = polymer.each_cons(2).flat_map do  # WCL => WC CL
        [_1, rules[_1 + _2]]                    #     => W🚾 C🆑
    end << polymer[-1]                          #     => W🚾C🆑L
end

# Subtrai o nº de ocorrências do elemento que aparece menos vezes ao nº do que aparece mais
polymer.tally     # Faz tipo collections.Counter() do Python. Retorna uma Hash {"E" => 123}
       .values    # Uma array só com os nº de ocorrências
       .minmax.tap { |min, max| puts max - min }