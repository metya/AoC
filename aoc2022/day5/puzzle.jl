using BenchmarkTools
using DataStructures

inputfile = joinpath(@__DIR__, "input.txt")

stack, instructions = split(read(inputfile, String), "\n\n") .|> x -> split(x, "\n")

parse_input() = begin
    queues = DefaultDict(Deque{Char})
    stackes = DefaultDict(Stack{Char})

    for row in stack
        for (i, j) in zip(2:4:length(row), 1:length(2:4:length(row)))
            if row[i] == ' '
                nothing
            elseif row[i] == '1'
                break
            else
                push!(queues[j], row[i])
            end
        end
    end

    for (index, queue) in queues
        while !isempty(queue)
            push!(stackes[index], pop!(queue))
        end
    end

    instr =
        (instructions .|> split .|> x -> Base.tryparse.(Int, x)) .|>
        x -> x[findall(y -> !isnothing(y), x)]
    stackes, instr
end

solve1(stackes, instrs) = begin
    stackes = deepcopy(stackes)
    instrs = deepcopy(instrs)
    for (n, from, to) in instrs
        for i = 1:n
            push!(stackes[to], pop!(stackes[from]))
        end
    end
    join([first(stackes[i]) for i = 1:length(stackes)])
end

solve2(stackes, instrs) = begin
    stackes = deepcopy(stackes)
    instrs = deepcopy(instrs)
    queue = Deque{Char}()
    for (n, from, to) in instrs
        [push!(queue, pop!(stackes[from])) for i = 1:n]
        [push!(stackes[to], pop!(queue)) for i = 1:n]
    end
    join([first(stackes[i]) for i = 1:length(stackes)])
end

stackes, instrs = parse_input()
print((solve1(stackes, instrs), solve2(stackes, instrs)))

@btime(solve1(stackes, instrs))
@btime(solve2(stackes, instrs))