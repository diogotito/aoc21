puts File.foreach('input.txt')
  .flat_map { _1.split(' | ')[1].split }
  .count { [2, 3, 4, 7].include? _1.length }