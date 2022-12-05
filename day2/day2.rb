horizontalPosition = depth = aim = 0

File.open("input.txt")
  .each_line
  .map(&:split).map { [_1, _2.to_i] }
  .each do
    |instruction, distance|
    case instruction
    when "down"
      aim += distance
    when "up"
      aim -= distance
    when "forward"
      horizontalPosition += distance
      depth += aim * distance
    end
  end

puts "horizontal position = #{horizontalPosition}"
puts "depth = #{depth}"
puts horizontalPosition * depth
