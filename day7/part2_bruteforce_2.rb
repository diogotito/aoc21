crabs = File.read('input.txt').split(',').map(&:to_i)

pp Range.new(*crabs.minmax)
  .map { |x| crabs.map { |c| (x - c).abs } }
  .map { |cs| cs.map {|c| (1 + c) * c / 2} }
  .map(&:sum)
  .min