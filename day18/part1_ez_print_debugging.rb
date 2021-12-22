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
    # puts "<0>"
    depth = 0
    sn.each_cons(4).with_index do |(token, left, _comma, right), i|
        case token
        when '['
            depth += 1
            if depth > 4
                unless Integer === left and Integer === right
                    # puts "<0> skipping...    #{[token, left, _comma, right].join}"
                    next
                end
                if (left_index = sn[0...i].rindex { Integer === _1 })
                    # puts "<0> Exploding left <--"
                    sn[left_index] += left
                end
                if (right_index = sn[i + 5..].index { Integer === _1 })
                    # puts "<0> Exploding right -->"
                    sn[i + 5 + right_index] += right
                end
                # puts "<0> Collapsing #{sn[i, 5].join} at #{i}..#{i + 5} into [0]"
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
    # puts "(|)"
    if (index = sn.index { |token| Integer === token and token >= 10 })
        # puts "(|) Before splitting: #{sn.join}"
        # puts "(|) Splitting #{sn[index, 1].join} into #{['[', sn[index] / 2, ",", (sn[index] / 2.0).ceil, ']'].join}"
        sn[index, 1] = ['[', sn[index] / 2, ",", (sn[index] / 2.0).ceil, ']']
        # puts "(|)  After splitting: #{sn.join}"
        return true
    end
    false
end

def reduce(sn)
    1.times do
        # puts "~~~"
        explode(sn) and redo
        split(sn) and redo
    end
    sn
end

def magnitude(sn)
    42
end

r=File.foreach("input.txt").map(&method(:tokenize)).reduce do |acc, input_line|
    # puts "\n=== Input line: #{input_line.join} ==="
    # puts "-- Current acc: #{acc.join} --"
    res = reduce(add(acc, input_line))
    # puts "> res: #{res.join}"
    res
end

p r.join
p magnitude(r)