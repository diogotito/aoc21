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
            when '0'..'9'
                curr_tree.send :"#{state}=", RegularNumber.new(c.to_i, parent=curr_tree)
            when '['
                curr_tree = Pair.new(curr_tree)
                curr_tree.parent.send :"#{state}=", curr_tree unless state == :begin
                state = :left
            when ','
                state = :right
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

    def climb_left
        raise "Can't climb from root" if root?
        curr_node = @parent
        curr_node = curr_node.parent until curr_node.right_child?
        curr_node.parent
    end

    def rightmost
        curr_node = self
        curr_node = curr_node.right while curr_node.is_a? Pair
        curr_node
    end

    def climb_right
        raise "Can't climb from root" if root?
        curr_node = @parent
        curr_node = curr_node.parent until curr_node.left_child?
        curr_node
    end

    def leftmost
        curr_node = self
        curr_node = curr_node.left while curr_node.is_a? Pair
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

    def initialize(value, parent=nil)
        super(parent)
        @value = value
    end

    def to_s
        "(#@value)"
    end
end

class Pair < SnailfishNumber
    attr_accessor :left, :right

    def initialize(parent=nil, left=nil, right=nil)
        super(parent)
        @left = left
        @right = right
    end

    def to_s
        "<#{@left || ?_}, #{@right || ?_}>"
    end

    def +(other)
        p = Pair.new(nil, self, other)
        @parent = other.parent = p
        p.reduce!
    end

    def each_left_right_rec(depth=0, &block)
        return to_enum(:each_left_right_rec) unless block_given?
        yield self, depth
        @left.each_left_right_rec(depth + 1, &block) if @left.is_a? Pair
        @right.each_left_right_rec(depth + 1, &block) if @right.is_a? Pair
    end

    def reduce!
        each_left_right_rec do |pair, depth|
            pair.explode! if depth >= 4
        end
        self
    end

    def explode!
        begin
            l = climb_left.left.righmost
            l.change_to! l.value + @left.value
        rescue Exception => e
            # Nothing on the left to change
        end

        begin
            r = climb_right.right.leftmost
            r.change_to! r.value + @right.value
        rescue Exception => e
            # Nothing on the right to change
        end

        change_to! 0
    end
end

# Example
sn = SnailfishNumber.parse "[[[[[9,8],1],2],3],4]"
puts sn
sn.reduce!
puts sn