using BenchmarkTools
using DataStructures
using AbstractTrees

inputfile = joinpath(@__DIR__, "example.txt")

input = readlines(inputfile)

struct Elemen
    name::String
    size::Int64
    loeqwe
end

struct TreeNode
    name::String
    size::In
    children::Vector{Int}
end

function read_files_size(input, Directory, line_number)
    println("we are in the $folder")
    println(input[line_number])
    dir = Dict()
    dir[folder] = Dict()
    dir["size"] = 0
    # dir["size"] = 0
    while line_number <= length(input) && !startswith(input[line_number], "\$ cd")
        println(input[line_number])
        if startswith(input[line_number], "\$ ls")
            line_number += 1
        elseif startswith(input[line_number], "dir")
            # dir[folder][input[line_number][5:end]] = Dict()
            # dir[folder][input[line_number][5:end]]["size"] = 0
            line_number += 1
        else
            dir["size"] += parse(Int, split(input[line_number])[1])
            line_number += 1
        end
    end
    if startswith(input[line_number], "\$ cd")
        println(input[line_number])
        if input[line_number][6:end] == ".."
            return dir
        else
            dir[folder] = read_files_size(input, input[line_number][6:end], line_number + 1)
        end
    end
    return dir
end

# fs = read_files_size(input, "/", 2)



# -------------

stack_based_solution() = begin
    stack = []; sizes = []
    for line in input
        if line == "\$ cd .."
            size = pop!(stack)
            append!(sizes, size)
            stack[end] += size
        elseif startswith(line, "\$ cd")
            append!(stack, 0)
        elseif isnumeric(line[1])
            stack[end] += parse(Int, split(line)[1])
        end
    end
    s = vcat(sizes, stack)
    f = s |> x->filter(y -> y < 100_000, x) |> sum
    s = s |> x->filter(y -> y >= maximum(x) - 40_000_000, x) |> minimum
    f, s
end

# @btime stack_based_solution()