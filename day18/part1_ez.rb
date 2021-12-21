require 'json'

File.foreach("input.txt") do |line|
    ary = JSON.load line
    p ary
end