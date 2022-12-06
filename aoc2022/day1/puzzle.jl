
inputfile = joinpath(@__DIR__, "input.txt")
input =
    read(inputfile, String) |>
    x -> split(x, "\n\n") .|> x -> split(x) .|> x -> parse(Int, x)

answer1 = input .|> sum |> maximum

answer2 = input .|> sum |> sort |> reverse |> x -> x[1:3] |> sum


println(answer1)
println(answer2)