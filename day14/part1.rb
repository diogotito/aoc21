File.open("input.txt") do |f|
    $template = f.readline.chomp
    f.readline
    $rules = Hash[f.each_line.map { |line| line.chomp.split " -> " }]
end

polymer = $template.chars

10.times do
    polymer = polymer.each_cons(2).flat_map { |left, right|
        [left, $rules[left + right]]
    } << polymer.last
    p polymer.length
end

least_common, most_common = polymer.group_by { |n| n }.values.minmax_by(&:size)
p [most_common, least_common].map { [_1.count, _1.first] }
puts most_common.length - least_common.length

# 1913: too low
# 3232: too high
# 3048: That's the right answer!