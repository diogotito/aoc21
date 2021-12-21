# TODO mudar isto para um módulo a ser mixed-in em RegularNumber e Pair
class SnailfishNumber
    attr_accessor :parent

    def initialize(parent = nil)
        @parent = parent
    end

    def self.parse(line)
        state = :begin
        curr_tree = nil
        line.each_char do |c|
            case c
            when '['
                curr_tree = Pair.new(curr_tree)
                curr_tree.parent.send :"#{state}=", curr_tree unless state == :begin
                state = :left
            when ','
                state = :right
            when '0'..'9'
                branch = curr_tree.send(state)  # access the .left or .right branch
                if branch.nil?
                    curr_tree.send(:"#{state}=", RegularNumber.new(c.to_i, parent=curr_tree))
                else
                    branch.value = branch.value * 10 + c.to_i
                end
            when ']'
                return curr_tree if curr_tree.root?
                curr_tree = curr_tree.parent
            end
        end
    end

    def root?
        @parent.nil?
    end

    def depth
        (root?) ? 0
                : 1 + parent.depth
    end

    def left_child?
        not root? and @parent.left == self
    end

    def right_child?
        not root? and @parent.right == self
    end

    def root
        curr_node = self
        curr_node = curr_node.parent until curr_node.root?
        curr_node
    end

    def climb_left
        raise "Can't climb from root" if root?
        curr_node = self
        curr_node = curr_node.parent until curr_node.nil? or curr_node.right_child?
        curr_node &. parent
    end

    def climb_right
        raise "Can't climb from root" if root?
        curr_node = self
        curr_node = curr_node.parent until curr_node.nil? or curr_node.left_child?
        curr_node &. parent
    end

    def leftmost
        curr_node = self
        curr_node = curr_node.left while curr_node.is_a? Pair
        curr_node
    end

    def rightmost
        curr_node = self
        curr_node = curr_node.right while curr_node.is_a? Pair
        curr_node
    end

    def change_to!(value=nil)
        raise "Can't change root node" if root?
        return change_to!(yield @value) if block_given? and is_a? RegularNumber
        value = case value
            in Integer
                RegularNumber.new(value, parent=@parent)
            in [Integer => l, Integer => r]
                p = Pair.new(@parent)
                p.left = RegularNumber.new(l, parent=p)
                p.right = RegularNumber.new(r, parent=p)
                p
            end
        @parent.left = value if left_child?
        @parent.right = value if right_child?
        value
    end
end

class RegularNumber < SnailfishNumber
    attr_accessor :value
    alias_method :magnitude, :value

    def initialize(value, parent=nil)
        super(parent)
        @value = value
    end

    def split!
        change_to! [@value / 2, (@value / 2.0).ceil]
    end

    def inspect
        "(#@value)"
    end

    def to_s
        "#@value"
    end
end

class Pair < SnailfishNumber
    attr_accessor :left, :right

    def initialize(parent=nil, left=nil, right=nil)
        super(parent)
        @left = left
        @right = right
    end

    def inspect
        "<#{@left.inspect || ?_}, #{@right.inspect || ?_}>"
    end

    def to_s
        "[#@left,#@right]"
    end

    def magnitude
        3 * @left.magnitude + 2 * @right.magnitude
    end

    def +(other)
        p = Pair.new(nil, self, other)
        @parent = other.parent = p
        p.reduce!
    end

    def each_leaf(&block)
        return enum_for(__method__) unless block_given?
        [@left, @right].each do |branch|
            case branch
            when Pair
                branch.each_leaf(&block)
            when RegularNumber
                yield branch
            end
        end
    end

    def each_left_right_rec(depth=0, &block)
        return enum_for(__method__) unless block_given?
        yield self, depth
        @left.each_left_right_rec(depth + 1, &block) if @left.is_a? Pair
        @right.each_left_right_rec(depth + 1, &block) if @right.is_a? Pair
    end

    def reduce!(once=false)
        1.times do
            try_explode_once! and redo
            try_split_once! and redo
        end
        self
    end

    def try_explode_once!
        (pair, _depth) = each_left_right_rec.find { |_pair, depth| depth >= 4 }
        pair.explode! unless pair.nil?
    end

    def try_split_once!
        each_leaf.find { |leaf| (leaf.value) >= 10 }&.split!
    end

    def explode!
        climb_left  &. left  &. rightmost &. change_to! { |old_v| old_v + @left.value }
        climb_right &. right &. leftmost  &. change_to! { |old_v| old_v + @right.value }
        change_to! 0
    end
end

class Array
    def to_sn
        SnailfishNumber.parse to_s
    end
end

class String
    def to_sn
        SnailfishNumber.parse self
    end
end


require 'test/unit'

class MyTest < Test::Unit::TestCase
    def assert_explosion(from, to, msg)
        assert_equal(to.to_s.gsub(' ', ""), from.to_sn.try_explode_once!&.root&.to_s, msg)
    end

    def assert_split(from, to, msg)
        assert_equal(to.to_s.gsub(' ', ""), from.to_sn.try_split_once!&.root&.to_s, msg)
    end

    def assert_reduce(from, to, msg)
        assert_equal(to.to_s.gsub(' ', ""), from.to_sn.reduce!.to_s, msg)
    end

    def assert_addition(n1, n2, to, msg)
        assert_equal(to.to_s.gsub(' ', ""), (n1.to_sn + n2.to_sn).to_s, msg) 
    end

    def assert_magnitude(sn, mag, msg)
        assert_equal(mag, sn.to_sn.magnitude, msg)
    end

    def test_single_explode
        assert_explosion([[[[[9,8],1],2],3],4],
            [[[[0,9],2],3],4],
            "1-1: the 9 has no regular number to its left, so it is not added to any regular number")
        assert_explosion([7,[6,[5,[4,[3,2]]]]],
            [7,[6,[5,[7,0]]]],
            "1-2: the 2 has no regular number to its right, and so it is not added to any regular number")
        assert_explosion([[6,[5,[4,[3,2]]]],1],
            [[6,[5,[7,0]]],3],
            "1-3")
        assert_explosion([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]],
            [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]],
            "1-4: the pair [3,2] is unaffected because the pair [7,3] is further to the left; [3,2] would explode on the next action")
        assert_explosion([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]],
            [[3,[2,[8,0]]],[9,[5,[7,0]]]],
            "1-5")

        assert_explosion([[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]],
            [[[[0,7],4],[7,[[8,4],9]]],[1,1]],
            "2-1")
        assert_explosion([[[[0,7],4],[7,[[8,4],9]]],[1,1]],
            [[[[0,7],4],[15,[0,13]]],[1,1]],"2-2")
        assert_explosion([[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]],
            [[[[0,7],4],[[7,8],[6,0]]],[8,1]],"2-3")
    end

    def test_single_split
        assert_split([[[[0,7],4],[15,[0,13]]],[1,1]],
            [[[[0,7],4],[[7,8],[0,13]]],[1,1]],
            "3-1")
        assert_split([[[[0,7],4],[[7,8],[0,13]]],[1,1]],
            [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]],
            "3-2")
    end

    def test_reduce
        assert_reduce([[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]],
            [[[[0,7],4],[[7,8],[6,0]]],[8,1]],
            "4-1: First reduction example")
    end

    def test_addition
        assert_addition([[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],
            [7,[[[3,7],[4,3]],[[6,3],[8,8]]]],
            [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]],
            '5-1: Steps from the "slightly larger example"')
        assert_addition([[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]],
            [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]],
            [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]],
            "5-2")
        assert_addition([[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]],
            [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]],
            [[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]],
            "5-3")
        assert_addition([[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]],
            [7,[5,[[3,8],[1,4]]]],
            [[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]],
            "5-4")
        assert_addition([[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]],
            [[2,[2,2]],[8,[8,1]]],
            [[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]],
            "5-5")
        assert_addition([[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]],
            [2,9],
            [[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]],
            "5-6")
        assert_addition([[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]],
            [1,[[[9,3],9],[[9,0],[0,7]]]],
            [[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]],
            "5-7")
        assert_addition([[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]],
            [[[5,[7,4]],7],1],
            [[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]],
            "5-8")
        assert_addition([[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]],
            [[[[4,2],2],6],[8,7]],
            [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]],
            "5-9")
    end

    def test_magnitude
        assert_magnitude([9,1], 29, "6-1: First example")
        assert_magnitude([1,9], 21, "6-2: Second example")
        assert_magnitude([[9,1],[1,9]], 129, "6-3: Recursive example")

        assert_magnitude([[1,2],[[3,4],5]], 143, "7-1: A few more magnitude examples")
        assert_magnitude([[[[0,7],4],[[7,8],[6,0]]],[8,1]], 1384, "7-2")
        assert_magnitude([[[[1,1],[2,2]],[3,3]],[4,4]], 445, "7-3")
        assert_magnitude([[[[3,0],[5,3]],[4,4]],[5,5]], 791, "7-4")
        assert_magnitude([[[[5,0],[7,4]],[5,5]],[6,6]], 1137, "7-5")
        assert_magnitude([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]], 3488, "7-6")
    end
end

puts "Answer for Part One:"

puts File.foreach("input.txt", chomp: true)
         .map(&:to_sn)
         .reduce(:+)
         .magnitude

puts "*  " * 30
puts

puts "Answer for Part Two:"

puts File.readlines("input.txt", chomp: true)
         .repeated_permutation(2)
         .map { |a, b| (a.to_sn + b.to_sn).magnitude }
         .max

puts "** " * 30
puts
