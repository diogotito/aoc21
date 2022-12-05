def fuel_cost(distance); (1 + distance) * distance / 2 end

crabs = File.read('input.txt').split(',').map(&:to_i)

puts (crabs.min..crabs.max).map { |x|
	crabs.sum { |crab_x| fuel_cost (x - crab_x).abs }
}.min