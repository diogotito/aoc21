class DiracDice
    attr_reader :current_face, :rolls

    def initialize(initial_value=1)
        @current_face = initial_value
        @rolls = 0
    end

    def roll
        result = @current_face
        @current_face = 1 + @current_face % 100
        @rolls += 1
        result
    end
end


class Player
    attr_accessor :position, :score

    def initialize(position=1, score=0)
        @position = position
        @score = score
    end

    def advance!(n)
        @position = (n + @position - 1) % 10 + 1
        @score += @position
    end

    def win?
        @score >= 1000
    end
end

(p1, p2) = File.read("input.txt").scan(/\d+$/).map { |sp| Player.new(sp.to_i) }
die = DiracDice.new
p p1, p2, die

def practice_game(p1, p2, die)
    loop do
        (r1, r2, r3) = [die.roll, die.roll, die.roll]
        p1.advance!(r1 + r2 + r3)
        puts "Player 1 rolls #{r1}+#{r2}+#{r3} and moves to space #{p1.position} for a total score of #{p1.score}."
        return p2 if p1.win?

        (r1, r2, r3) = [die.roll, die.roll, die.roll]
        p2.advance!(r1 + r2 + r3)
        puts "Player 2 rolls #{r1}+#{r2}+#{r3} and moves to space #{p2.position} for a total score of #{p2.score}."
        return p1 if p2.win?
    end
end

loser = practice_game(p1, p2, die)

p p1, p2, die
puts die.rolls * loser.score
