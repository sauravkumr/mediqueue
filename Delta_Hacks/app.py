from flask import Flask, render_template, request, session, redirect

from db_methods import methods, config
app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdkjhlsdfg'
execute = methods(config)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=["GET","POST"])
def login():
    form = request.form.to_dict()
    if 'first' in form and 'last' in form and 'birthday' in form and 'provider' in form:
        session['first'] = first = form['first']
        session['last'] = last = form['last']
        session['birthday'] = birthday = form['birthday']
        session['provider'] = provider = form['provider']
        session['spot'] = spot = execute.new_spot()
        print(form)
        execute.new_entry(first, last, birthday, provider, spot)
        return redirect('/queues')

    return render_template('login.html')

@app.route('/queues')
def queues():
    first = session['first']
    last = session['last']
    session['spot'] =  execute.get_spot(first, last)
    
    infront = execute.total_infront(first, last)
    if session['spot'] != None:
        return render_template('queues.html', name = first, spot = session['spot'][0], total_infront = infront)
    return render_template('queues.html', name = first, spot = 1, total_infront = infront)

@app.route('/leave')
def leave():
    if 'first' in session:
        first = session['first']
        last = session['last']
        spot = session['spot']
        execute.leave(first, last, spot)
        for i in list(session.keys()):
            session.pop(i,None)

    return redirect('/login')

if __name__ == '__main__':
    app.run(debug = True)

#host on heroku
#refresh wont update, queries
