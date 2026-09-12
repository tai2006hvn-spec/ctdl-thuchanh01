# Load an unmodified standalone solution once, then call its main() repeatedly.
# Only valid cases run here: invalid cases require isolated processes for exit(1).
source, directory, count_text = ARGS
count = parse(Int, count_text)
for i in 0:(count - 1)
    open(joinpath(directory, "$i.in"), "r") do input
        open(joinpath(directory, "$i.out"), "w") do output
            redirect_stdin(input) do
                redirect_stdout(output) do
                    if i == 0
                        include(source)
                    else
                        Base.invokelatest(main)
                    end
                end
            end
        end
    end
    write(joinpath(directory, "$i.done"), "passed process boundary\n")
end
