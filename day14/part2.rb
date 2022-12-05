all_lines = File.readlines("input.txt", chomp: true)           # Extrai linhas sem \n
polymer = all_lines[0].chars                                   # 1ª linha para Array de caracteres
rules = Hash[all_lines[2..].map { |rule| rule.split " -> " }]  # ["WC -> 🚾"] => {"WC" => 🚾}

elem_counter = Hash.new(0).merge polymer.tally
pair_counter = Hash.new(0).merge polymer.each_cons(2).tally

pp polymer
puts "-----------------"

40.times do
    new_pairs = {}
    pair_counter.each do |(left, right), count|
        inserted_elem = rules[left + right]
        # count, pair_counter[[left, right]] = pair_counter[[left, right]], 0
        count = pair_counter[[left, right]]
        pair_counter[[left, right]] = 0
        new_pairs[[left, inserted_elem]] = count
        new_pairs[[inserted_elem, right]] = count
        elem_counter[inserted_elem] += count
    end
    pair_counter.merge!(new_pairs) { |_key, old_value, new_value| old_value + new_value }
    p pair_counter
end

puts "-----------------"
pp elem_counter
puts "-----------------"
pp pair_counter
