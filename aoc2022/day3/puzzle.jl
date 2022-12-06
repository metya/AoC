inputfile = joinpath(@__DIR__, "input.txt")

input = readlines(inputfile)

answer1 = (input .|> collect .|> 
x -> map(y -> islowercase(y) ? Int(y) - Int('a') + 1 : Int(y) - Int('A') + 27, x) |>
x -> (x[begin:Int(length(x)/2)], x[Int(length(x)/2)+1:end]) |> 
x -> intersect(x...)) |> sum |> sum

answer2 = ((input .|> collect .|> 
x -> map(y -> islowercase(y) ? Int(y) - Int('a') + 1 : Int(y) - Int('A') + 27, x)) |>
x -> reshape(x, (3, :)) |> eachcol |> collect .|>
x -> intersect(x...)) |> sum |> sum

print((answer1, answer2))