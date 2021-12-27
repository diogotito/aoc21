import Control.Monad (forM_)
import Debug.Trace (trace)
-- {-# LANGUAGE TupleSections #-}

-- w, x, y, z = 0
-- 0 in z --> Valid

type ALUState = (Int, Int, Int, Int, [Int])

data VariableName = W | X | Y | Z deriving (Eq, Read, Show)
type RightOperand = Either VariableName Int

initialState :: ALUState
initialState = (0, 0, 0, 0, [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 1, 2, 3, 4])


-- Helpers

setVariable :: VariableName -> Int -> ALUState -> ALUState
setVariable W value (_, x, y, z, inp) = (value, x, y, z, inp)
setVariable X value (w, _, y, z, inp) = (w, value, y, z, inp)
setVariable Y value (w, x, _, z, inp) = (w, x, value, z, inp)
setVariable Z value (w, x, y, _, inp) = (w, x, y, value, inp)

getVariable :: VariableName -> ALUState -> Int
getVariable W (value, _, _, _, _) = value
getVariable X (_, value, _, _, _) = value
getVariable Y (_, _, value, _, _) = value
getVariable Z (_, _, _, value, _) = value

evalRightOperand :: RightOperand -> ALUState -> Int
evalRightOperand (Left var) state = getVariable var state
evalRightOperand (Right val) _ = val

-- Instructions

inpInstruction :: VariableName -> ALUState -> ALUState
inpInstruction var (w, x, y, z, i:inputs) = setVariable var i (w, x, y, z, inputs)
inpInstruction _ (_, _, _, _, []) = undefined

addInstruction :: VariableName -> RightOperand -> ALUState -> ALUState
addInstruction var rhs state = setVariable var (getVariable var state + evalRightOperand rhs state) state

mulInstruction :: VariableName -> RightOperand -> ALUState -> ALUState
mulInstruction var rhs state = setVariable var (getVariable var state * evalRightOperand rhs state) state

divInstruction :: VariableName -> RightOperand -> ALUState -> ALUState
divInstruction var rhs state = setVariable var (getVariable var state `div` evalRightOperand rhs state) state

modInstruction :: VariableName -> RightOperand -> ALUState -> ALUState
modInstruction var rhs state = setVariable var (getVariable var state `mod` evalRightOperand rhs state) state

eqlInstruction :: VariableName -> RightOperand -> ALUState -> ALUState
eqlInstruction var rhs state = setVariable var (if getVariable var state == evalRightOperand rhs state then 1 else 0) state


-- IO

varName :: Char -> VariableName
varName 'w' = W
varName 'x' = X
varName 'y' = Y
varName 'z' = Z
varName _ = undefined

rightOperand :: String -> RightOperand
rightOperand "w" = Left W
rightOperand "x" = Left X
rightOperand "y" = Left Y
rightOperand "z" = Left Z
rightOperand num = Right (read num :: Int)

evalInstruction :: [String] -> ALUState -> ALUState
evalInstruction ["inp", [variable]] = inpInstruction $ varName variable
evalInstruction ["add", [variable], rhs] = addInstruction (varName variable) (rightOperand rhs)
evalInstruction ["mul", [variable], rhs] = mulInstruction (varName variable) (rightOperand rhs)
evalInstruction ["div", [variable], rhs] = divInstruction (varName variable) (rightOperand rhs)
evalInstruction ["mod", [variable], rhs] = modInstruction (varName variable) (rightOperand rhs)
evalInstruction ["eql", [variable], rhs] = eqlInstruction (varName variable) (rightOperand rhs)
evalInstruction wat = trace ("what is " ++ unwords wat) id


main = do
    program <- map words . lines <$> readFile "input.txt"
    let transformation = foldr ((.) . evalInstruction) id program
    let finalState = transformation initialState

    putStrLn "Initial state: "
    print initialState
    putStrLn ""
    putStrLn "Final State:"
    print finalState