def tokenize(line)
    line.each_char.filter_map do |c|
        case c
        when '[', ']', ','
            c
        when '0'..'9'
            c.to_i
        end
    end
end

def add(sn1, sn2)
    ['[', *sn1, ',', *sn2, ']']
end

def explode(sn)
    depth = 0
    sn.each_cons(4).with_index do |(token, left, _comma, right), i|
        case token
        when '['
            depth += 1
            if depth > 4
                next unless Integer === left and Integer === right
                if (left_index = sn[0...i].rindex { Integer === _1 })
                    sn[left_index] += left
                end
                if (right_index = sn[i + 5..].find_index { Integer === _1 })
                    sn[i + 5 + right_index] += right
                end
                sn[i, 5] = [0]
                return true
            end
        when ']'
            depth -= 1
        end
    end
    false
end

def split(sn)
    if (index = sn.find_index { |token| Integer === token and token >= 10 })
        sn[index, 1] = ['[', sn[index] / 2, ",", (sn[index] / 2.0).ceil, ']']
        return true
    end
    false
end

def reduce(sn)
    1.times do
        explode(sn) and redo
        split(sn) and redo
    end
    sn
end

def magnitude(sn)
    return sn[0] if Integer === sn[0]

    depth = 0
    split_i = 1 + sn[1..].find_index { |token|
        (depth += { '[' => 1,
                    ']' => -1 }.fetch(token, default=0)).zero?
    }
    left = sn[1, split_i]
    right = sn[split_i + 2...-1]

    3 * magnitude(left) + 2 * magnitude(right)
end


# --- Part One ---

puts magnitude(File.foreach("input.txt")
                   .map(&method(:tokenize))
                   .reduce { |acc, input_line| reduce(add(acc, input_line)) })


# --- Part Two ---

puts File.readlines("input.txt")
         .map(&method(:tokenize))
         .repeated_permutation(2)
         .map { |a, b| magnitude(reduce(add(a, b))) }
         .max


# Answers:
# Part One: 4417
# Part Two: 4796
