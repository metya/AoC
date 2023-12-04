using BenchmarkTools

inputfile = joinpath(@__DIR__, "input.txt")

input = readlines(inputfile)

grid = input .|> collect .|> x -> parse.(Int, x)

mgrid = permutedims(reduce(hcat, grid))

solve1(mgrid) = begin
    fish = zeros(Int, size(mgrid))
    fish[begin, :] .= 1
    fish[end, :] .= 1
    fish[:, begin] .= 1
    fish[:, end] .= 1

    for i = 2:size(mgrid)[1]-1
        for j = 2:size(mgrid)[1]-1
            center = mgrid[i, j]
            if all(center .> mgrid[begin:i-1, j]) ||
               all(center .> mgrid[i+1:end, j]) ||
               all(center .> mgrid[i, begin:j-1]) ||
               all(center .> mgrid[i, j+1:end])
                fish[i, j] = 1
            end
        end
    end
    count(==(1), fish)
end

solve2(mgrid) = begin
    fish = zeros(Int, size(mgrid))
    for i = 2:size(mgrid)[1]-1
        for j = 2:size(mgrid)[1]-1
            sl = i + 1
            score_down = 1
            center = mgrid[i, j]
            while center > mgrid[sl, j] && sl <= size(mgrid)[1] - 1
                sl += 1
                score_down += 1
            end
            score_up = 1
            sl = i - 1
            while center > mgrid[sl, j] && sl >= 2
                sl -= 1
                score_up += 1
            end
            score_right = 1
            sl = j + 1
            while center > mgrid[i, sl] && sl <= size(mgrid)[1] - 1
                score_right += 1
                sl += 1
            end
            score_left = 1
            sl = j - 1
            while center > mgrid[i, sl] && sl >= 2
                score_left += 1
                sl -= 1
            end
            score = score_down * score_left * score_right * score_up
            fish[i, j] = score
        end
    end
    maximum(fish)
end

print((solve1(mgrid), solve2(mgrid)))