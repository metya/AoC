using BenchmarkTools
using MLStyle

inputfile = joinpath(@__DIR__, "input.txt")

input = split.(readlines(inputfile))

h = Dict("i" => 1, "j" => 1)
t = Dict("i" => 1, "j" => 1)
maxH = 1
maxV = 1
minH = 1
minV = 1

grid = zeros(Int, 350, 350)

function mark(D, i, j, steps)
    c = 1
    if D == "R"
        while c >= steps
            

for line in input
    direction = line[1]
    steps = parse(Int, line[2])
    println(h)
    @match direction begin
            "R" => (h["j"] += steps)
            "L" => (h["j"] -= steps)
            "D" => (h["i"] += steps)
            "U" => (h["i"] -= steps)
    end
    maxH = maximum([h["j"], maxH])
    maxV = maximum([h["i"], maxV])
    minH = minimum([h["j"], minH])
    minV = minimum([h["i"], minV])
end

i, j = (23, 296)
for line in input
    @match direction begin
        "R" => (h["j"] += steps)
        "L" => (h["j"] -= steps)
        "D" => (h["i"] += steps)
        "U" => (h["i"] -= steps)
    end
end

