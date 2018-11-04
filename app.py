from bottle import route, run, request


@route('/')
def index():
    n = int(request.query.n)
    starting_x = float(request.query.starting_x)
    starting_y = float(request.query.starting_y)
    ending_x = float(request.query.ending_x)

    from solver import ODESolver

    solver = ODESolver(initial_x_1=starting_x, initial_y_1=starting_y, n=n, ending_x_2=ending_x)
    reference_x, reference_y = solver.calculate_reference()

    euler_x, euler_y = solver.calculate_euler()

    euler_err, euler_max = solver.calculate_euler_errors()

    improved_euler_x, improved_euler_y = solver.calculate_improved_euler()
    improved_euler_err, improved_euler_max = solver.calculate_improved_euler_errors()

    runge_kutta_x, runge_kutta_y = solver.calculate_runge_kutta()
    runge_kutta_err, runge_kutta_max = solver.calculate_runge_kutta_errors()

    from bottle import response
    from json import dumps
    rv = [
        {
            'title': 'Reference',
            'x': reference_x,
            'y': reference_y,
            'errors': [],
            'max_error': 123
        },
        {
            'title': 'Euler',
            'x': euler_x,
            'y': euler_y,
            'errors': euler_err,
            'max_error': euler_max
        },
        {
            'title': 'Improved Euler',
            'x': improved_euler_x,
            'y': improved_euler_y,
            'errors': improved_euler_err,
            'max_error': improved_euler_max
        },
        {
            'title': 'Runge-Kutta',
            'x': runge_kutta_x,
            'y': runge_kutta_y,
            'errors': runge_kutta_err,
            'max_error': runge_kutta_max
        },
    ]
    response.content_type = 'application/json'
    return dumps(rv)


run(host='localhost', port=8080, debug=True, reloader=True)
