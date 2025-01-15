@app.route("/delete/<int:sno>", methods=['GET', 'POST'])
def delete(sno):
    allTask=Task.query.filter_by(sno=sno).first()
    db.session.delete(Task)
    db.session.commit()
    return redirect("/")
