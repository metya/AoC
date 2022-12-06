using BenchmarkTools

inputfile = joinpath(@__DIR__, "input.txt")

input =
    readlines(inputfile) .|>
    x -> split(x, ',') .|> x -> replace(x, '-' => ':') .|> x -> Meta.parse.(x) .|> eval

answer1 =
    (input .|> x -> (issubset(x...), issubset(reverse(x)...)) |> x -> x[1] || x[2]) |> sum

answer2 = (input .|> x -> intersect(x...) |> length) |> x -> findall(!iszero, x) |> length

print((answer1, answer2))
