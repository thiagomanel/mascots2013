import sys

if __name__ == "__main__":
    machines = {"abelhinha":
                    "../../data/input/2011_10_21-abelhinha.clean.cut.order.expected"}

    machine = sys.argv[1].strip()
    print machines[machine]

