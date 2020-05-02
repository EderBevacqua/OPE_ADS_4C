from flask import Blueprint, jsonify, request, render_template, redirect,url_for, session, abort, flash, redirect
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.debug import DebuggedApplication
from services.solicitarEmprestimo_service import \
    listarEmp as service_listarEmp, \
    listarEqui as service_listarEqui, \
    equipDisponivel as service_equipDisponivel, \
    addEquipamento as service_addEquipamento, \
    removeEquip as service_removeEquip, \
    localizar as service_localiza, \
    criar as service_criar, \
    remover as service_remover, \
    atualizar as service_atualiza

solicitarEmprestimo_app = Blueprint('solicitarEmprestimo_app', __name__, template_folder='templates/solicitarEmprestimo')

@solicitarEmprestimo_app.route('/emprestimos/adicionarEquipamento/<int:id_emprestimo>', methods=['POST'])
def adicionarEquipamento(id_emprestimo):
    if request.method == 'POST' and request.form.getlist('addEquip') !=[]:
        for idEquip in request.form.getlist('addEquip'):
            addEquip = service_addEquipamento(id_emprestimo,idEquip)
        if addEquip == True:
            flash('Equipamento adicionado no empréstimo')
            return redirect('/emprestimos')
        else:
            flash('Algo de errado aconteceu')
            return redirect('/emprestimos')
    flash('Nenhum equipamento adicionado')
    return redirect("/emprestimos")

@solicitarEmprestimo_app.route('/emprestimos/removerEquipamento/<int:id_emprestimo>/<int:id_equipamento>', methods=['POST','GET'])
def removerEquipamento(id_emprestimo,id_equipamento):
    rm=service_removeEquip(id_emprestimo, id_equipamento)
    if rm != None:
        flash('Equipamento removido do empréstimo')
        return redirect('/emprestimos')


@solicitarEmprestimo_app.route('/emprestimos', methods=['POST','GET'])
@login_required
def emprestimos():
    if current_user.isAdmin == 1:
        return render_template("solicitarEmprestimo/emprestimos.html", emprestimos=service_listarEmp(), equipamentos=service_equipDisponivel())
    else:
        emprestimos=[]
        for e in service_listarEmp():
            if e[0].id_usuario == current_user.id_usuario:
                emprestimos.append(e)
        return render_template("solicitarEmprestimo/emprestimos.html", emprestimos=emprestimos)

@solicitarEmprestimo_app.route('/solicitarEmprestimo', methods=['POST','GET'])
@login_required
def solicitarEmprestimo():
    return render_template("solicitarEmprestimo/solicitarEmprestimo.html")

@solicitarEmprestimo_app.route('/solicitarEmprestimo/cadastrar', methods=['POST','GET'])
@login_required
def cadastrar():
    try:
        if request.method == 'POST':
            nova_solicitacao = {'id':'', 'id_emprestimo':'', 'id_equipamento':'', 'id_usuario':'', 'dtSolicitacao':'', 'dtEmprestimo':request.form['dtEmprestimo'], 'dtDevolucao':request.form['dtDevolucao'], 'status':'', 'nome':request.form.get('nome'), 'numeroMatricula':request.form.get('numeroMatricula'), 'departamento':'', 'email':'', 'telefone':'', 'numeroEquipamento':request.form['numeroEquipamento'], 'marca':'','modelo':'', 'situacao':''}
            solicitacao = service_criar(nova_solicitacao)
        if solicitacao == None:
            return render_template("solicitarEmprestimo/solicitarEmprestimo.html", mensagem = "solictacao não pode ser cadastrado! \n")
        else:
            flash('Solicitação de empréstimo registrada')
            return redirect('/emprestimos')
        return render_template("solicitarEmprestimo/solicitarEmprestimo.html")
    except ValueError as e:
        return e

