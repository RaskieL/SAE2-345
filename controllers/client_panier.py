#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article', None)
    quantite = request.form.get('quantite')
    # ---------
    print(id_article)
    if id_article is not None and id_article != "":
        sql = '''SELECT * FROM declinaison WHERE declinaison.id_gant = %s;'''
        mycursor.execute(sql,(id_article))
        declinaisons = mycursor.fetchall()
        
        #print(len(declinaisons))

        if len(declinaisons) == 1:
            id_declinaison = declinaisons[0]['id_declinaison']
            prix = declinaisons[0]['prix_declinaison']
            sql = '''SELECT gant.nom_gant FROM gant JOIN declinaison ON declinaison.id_gant = gant.id_gant WHERE declinaison.id_declinaison = %s;'''
            mycursor.execute(sql, (id_declinaison));
            nom = mycursor.fetchone()
            stock = declinaisons[0]['stock']
        elif len(declinaisons) == 0:
            abort("PROBLEME NOMBRE DE DECLINAISON !!!")
        else:
            # En gros là faut renvoyer sur la page où on choisira la déclinaison à ajouter dans le panier lorsqu'il y en a plusieures
            sql = ''''''
    else:
        id_declinaison = request.form.get('id_declinaison',None)
# ajout dans le panier d'une déclinaison d'un article (si 1 declinaison : immédiat sinon => vu pour faire un choix
    # sql = '''    '''
    # mycursor.execute(sql, (id_article))
    # declinaisons = mycursor.fetchall()
    # if len(declinaisons) == 1:
    #     id_declinaison_article = declinaisons[0]['id_declinaison_article']
    # elif len(declinaisons) == 0:
    #     abort("pb nb de declinaison")
    # else:
    #     sql = '''   '''
    #     mycursor.execute(sql, (id_article))
    #     article = mycursor.fetchone()
    #     return render_template('client/boutique/declinaison_article.html'
    #                                , declinaisons=declinaisons
    #                                , quantite=quantite
    #                                , article=article)

# ajout dans le panier d'un article
# A completer et corriger
    sql = '''SELECT COUNT(*) AS count FROM ligne_panier WHERE id_declinaison = %s AND id_utilisateur = %s'''
    mycursor.execute(sql, (id_declinaison,id_client))
    linealreadyexists = mycursor.fetchone()
    print(str(linealreadyexists['count']))
    if linealreadyexists['count'] == 0:
        sql = '''INSERT INTO ligne_panier VALUES (%s, %s, %s, %s, %s, %s);'''
        panier_tuple = (id_declinaison, id_client, quantite, prix, nom['nom_gant'], str(int(stock)-int(quantite)))
        print("id decli: " + str(id_declinaison) + " id client: " + str(id_client) + " quantite: "+ str(quantite) + " prix: " + str(prix) + " nom: " + nom['nom_gant'])
        mycursor.execute(sql, panier_tuple)
        get_db().commit()
    else:
        sql = '''SELECT stock FROM ligne_panier WHERE id_declinaison = %s AND id_utilisateur = %s;'''
        mycursor.execute(sql, (id_declinaison, id_client))
        current_stock = mycursor.fetchone()
        if current_stock['stock'] > 0:
            sql = '''UPDATE ligne_panier SET quantite = quantite+1, stock=stock-1 WHERE id_declinaison = %s AND id_utilisateur = %s;'''
            mycursor.execute(sql, (id_declinaison, id_client))
            get_db().commit()

    return redirect('/client/article/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_declinaison = request.form.get('id_declinaison','')
    quantite = 1

    # ---------
    # partie 2 : on supprime une déclinaison de l'article
    # id_declinaison_article = request.form.get('id_declinaison_article', None)

    sql = '''SELECT * FROM ligne_panier WHERE id_declinaison = %s AND id_utilisateur = %s'''
    mycursor.execute(sql, (id_declinaison, id_client))
    article_panier= mycursor.fetchone()
    print(article_panier)

    if not(article_panier is None) and article_panier['quantite'] > 1:
        sql = '''UPDATE ligne_panier SET quantite = quantite-1, stock=stock+1 WHERE id_declinaison = %s AND id_utilisateur = %s;'''
        mycursor.execute(sql, (id_declinaison, id_client))
    else:
        sql = '''DELETE FROM ligne_panier WHERE id_declinaison =%s AND id_utilisateur = %s;'''
        mycursor.execute(sql, (id_declinaison, id_client))

    # mise à jour du stock de l'article disponible
    get_db().commit()
    return redirect('/client/article/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = '''DELETE FROM ligne_panier WHERE id_utilisateur = %s'''
    mycursor.execute(sql,client_id)
    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_declinaison = request.form.get('id_declinaison')

    sql = '''DELETE FROM ligne_panier WHERE id_declinaison =%s AND id_utilisateur = %s;'''
    mycursor.execute(sql,(id_declinaison,id_client))
    #sql2=''' mise à jour du stock de l'article : stock = stock + qté de la ligne pour l'article'''

    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    # test des variables puis
    # mise en session des variables
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    # suppression  des variables en session
    print("suppr filtre")
    return redirect('/client/article/show')
