using BenchmarkTools

inputfile = joinpath(@__DIR__, "input.txt")

input = read(inputfile, String)

solve1() = begin
    for r = 1:length(input)
        if length(unique(input[r:r+3])) == 4
            return r + 3
        end
    end
end

solve2() = begin
    for r = 1:length(input)
        if length(unique(input[r:r+13])) == 14
            return r + 13
        end
    end
end


print((solve1(), solve2()))

@btime solve1()
@brtime solve2()
