# Ruby's Integer class conveniently provides us methods for the add, mul, div
# and mod instructions (+, *, / and %, respectively)
#   - Yes, these are valid method names in Ruby and the operators are
#     syntatic sugar to call them and pass the right operand by argument!
# Only the eql instruction is missing a method. Let's fix that!
class Integer
    # Here I've opened the Integer class to define a method to be called by eql
    # on any Integer value
    def equals_1_0(other)
        self == other ? 1 : 0
    end
end

class ALU
    # @instance_variables are private in Ruby
    # attr_reader generates "getter" methods automatically
    # () are optional when calling methods, so using these will look like
    #     puts alu.w + alu.x + alu.y + alu.z
    # Looks like public member access in other langs!
    attr_reader :w, :x, :y, :z

    # The constructor function, called by ALU.new() after the object is allocated
    def initialize(input)
        @w = @x = @y = @z = 0
        @input = input
    end

    # Associate every instruction name with an Integer method name
    ops = {
        add: :+,
        mul: :*,
        div: :/,
        mod: :%,
        eql: :equals_1_0
    }

    # Metaprogramming:
    # For each key in `ops`, define a method that performs the corresponding Integer
    # method on a given variable and operand and stores the result back in the variable
    ops.each do |binop_name, integer_method|
        define_method :"perform_#{binop_name}" do |var, operand|
            # Fetch 1st operand and 2nd operand (if it's a variable name)
            var_value = instance_variable_get(:"@#{var}")
            operand_value = instance_variable_get(:"@#{operand}") rescue operand

            # Call `integer_method` on var (which should be an Integer instance
            # by now), passing `operand` as an argument.
            result = var_value.send(integer_method, operand_value)
            instance_variable_set(:"@#{var}", result)

            # It's called `send` because when you call a method in
            # "more pure" OO language like Ruby and Smalltalk, you're supposed
            # to imagine it as sending a message to an object.
            # Defining a method, then, is like teaching a class of objects how
            # to respond to a new kind of message.
            # When an object doesn't know how to respond to a particular message,
            # Ruby calls a special method named "method_missing", which can be
            # overriden to do whatever the hell we want (dynamically define new
            # methods like above, or make objects respond to arbitrary bare words
            # if you're implementing a weird DSL of sorts). By default it just
            # raises a NoMethodException to behave like most other dynamic langs.
        end
    end

    # Now we can call perform_add, perform_mul, perform_div, perform_mod
    # and perform_eql on ALU objects!
    # There's only the odd one out, perform_inp, to implement. Let's do it now!

    def perform_inp(var, _operand=nil)
        instance_variable_set(:"@#{var}", @input.shift)
    end

    # To finish this madness, let's use send() just one more time to dynamically
    # dispatch instructions to a "perform_<instruction_name>" call

    def execute_program(program)
        # Program is an array of arrays of size 3
        program.each do |instruction_name, var, operand|
            send(:"perform_#{instruction_name}", var, operand)
        end
        @z == 0  # Last expression in a method is returned
    end

    # A human readable representation of the ALU state
    def to_s
        "<ALU  w=#@w, x=#@x, y=#@y, z=#@z  |#{@input.join}>"
    end
end


program = File.readlines("input.txt", chomp: true).map do |line|
    (instruction_name, var, operand) = line.split

    instruction_name = instruction_name.to_sym
    var = var.to_sym
    operand = Integer(operand) rescue operand&.to_sym  # &. doesn't convert nil

    [instruction_name, var, operand].filter &:itself  # nils exclude themselves
end


BRUTEFORCE = 100
puts "Will attempt #{BRUTEFORCE} times"

BRUTEFORCE.times do |i|
    puts
    puts " Attempt #{i + 1} ".center(79, ":")
    alu = ALU.new(14.times.collect { rand 1..9 })
    puts alu
    valid = alu.execute_program(program)
    puts valid ? "Valid".ljust(79, "!") : "Not valid..."
    puts alu
    break if valid
end