from flask import Flask, render_template, request
import math

app = Flask(__name__)

def find_change_gears(Z, available_gears, max_sols, index_ratio, max_iter=1000000, decimal=9):
    solutions = []
    k = 1

    while len(solutions) < max_sols and k <= max_iter:
        C = 18 * k
        D = Z * k

        if C not in available_gears or D not in available_gears:
            k += 1
            continue

        ratio = round(C / D, decimal)
        if ratio == index_ratio:
            solutions.append((C, D))

        k += 1

    return solutions if len(solutions) >= max_sols else None

def find_gears_helix(beta_radians, M, n, available_gears, tolerance=1e-6):
    H = (6 * math.sin(beta_radians)) / (M * n)

    solutions = []
    for A in available_gears:
        for B in available_gears:
            for C in available_gears:
                for D in available_gears:
                    calc_h = (A / B) * (C / D)

                    if abs(calc_h - H) <= tolerance:
                        solutions.append((A, B, C, D))

                        if len(solutions) >= 2:
                            beta1 = math.degrees(math.asin((M * n * solutions[0][0] / solutions[0][1] * solutions[0][2] / solutions[0][3]) / 6))
                            beta2 = math.degrees(math.asin((M * n * solutions[1][0] / solutions[1][1] * solutions[1][2] / solutions[1][3]) / 6))

                            if abs(beta1 - beta_radians) <= abs(beta2 - beta_radians):
                                return solutions[0]
                            else:
                                return solutions[1]

    return solutions

@app.route('/', methods=['GET', 'POST'])
def index():
    result_helix = None
    result_gears = None
    beta = Z = index_ratio = None
    

    if request.method == 'POST':
        beta = float(request.form['beta'])
        beta_radians = math.radians(beta)
        Z = int(request.form['Z'])
        max_sols = int(request.form['max_sols'])
        M = 10
        n = 1

        available_gears = [18, 20, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 53, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 103, 104, 109, 113, 125, 127, 131, 137, 139]

        # Helix gear calculation
        result_helix = find_gears_helix(beta_radians, M, n, available_gears)

        # Change gear calculation
        C = 18
        decimal = 9
        index_ratio = round(C / Z, decimal)
        result_gears = find_change_gears(Z, available_gears, max_sols, index_ratio)

    return render_template('index.html', beta=beta, Z=Z, index_ratio=index_ratio, result_helix=result_helix,result_gears=result_gears)

if __name__ == '__main__':
    app.run(debug=True)
