using MLStyle
using BenchmarkTools

inputfile = joinpath(@__DIR__, "input.txt")

input =
    readlines(inputfile) .|>
    x ->
        replace(x, "A" => 1, "B" => 2, "C" => 3, "X" => 1, "Y" => 2, "Z" => 3) |>
        split |>
        x -> parse.(Int, x) |> x -> tuple(x...)

first(round) = @match round begin
    (1, 2) || (2, 3) || (3, 1) => round[2] + 6
    (2, 1) || (3, 2) || (1, 3) => round[2]
    _ => round[2] + 3
end

second(round) = @match round begin
    (x, 1) => x == 1 ? (1, 3) : x == 2 ? (2, 1) : (3, 2)
    (x, 2) => (x, x)
    (x, 3) => x == 1 ? (1, 2) : x == 2 ? (2, 3) : (3, 1)
end

solve(input) = begin
    input .|> first |> sum, input .|> second .|> first |> sum
end

print(solve(input))

@btime solve(input)

